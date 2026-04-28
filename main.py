import sys
import asyncio

# --- PARCHE OBLIGATORIO PARA WINDOWS + PLAYWRIGHT ---
if sys.platform == 'win32':
    # Esto DEBE ir antes de cualquier otra importación de asyncio o fastapi
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

print(">>> DEBUG: CARGANDO MAIN.PY...", file=sys.stderr, flush=True)

import re
import uuid
import os
from typing import List, Optional

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from contextlib import asynccontextmanager
import storage
from kick_listener import kick_ws_listener
from models import Votation

# ---------------------------------------------------------------------------
# Lifespan manager (Modern replacement for startup/shutdown events)
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_running_loop()
    print("\n" + "!"*60, flush=True)
    print("!!! KICK VOTE ENGINE: STARTING UP !!!", flush=True)
    print(f"!!! LOOP TYPE: {type(loop).__name__} !!!", flush=True)
    print("!"*60 + "\n", flush=True)
    
    # Inicia el procesador de votos
    asyncio.create_task(votation_consumer())
    
    # Si hay un canal por defecto, abre el navegador automáticamente
    if DEFAULT_CHANNEL:
        print(f"[Main] Auto-start streamer: {DEFAULT_CHANNEL}", flush=True)
        asyncio.create_task(start_kick_session(DEFAULT_CHANNEL))
    
    yield
    
    print("\n" + "!"*60, flush=True)
    print("!!! KICK VOTE ENGINE: SHUTTING DOWN !!!", flush=True)
    print("!"*60 + "\n", flush=True)
    if listener_stop_event:
        listener_stop_event.set()

app = FastAPI(title="Kick Vote Web", lifespan=lifespan)

# ---------------------------------------------------------------------------
# Global state
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Global state & Config
# ---------------------------------------------------------------------------
DEFAULT_CHANNEL = ""  # Déjalo vacío para elegirlo en la web, o pon un nombre para auto-inicio
current_channel: Optional[str] = None
current_votation: Optional[Votation] = None
kick_message_queue: asyncio.Queue = asyncio.Queue()
ws_clients: List[WebSocket] = []
listener_task: Optional[asyncio.Task] = None
listener_stop_event: Optional[asyncio.Event] = None


# ---------------------------------------------------------------------------
# WebSocket helpers
# ---------------------------------------------------------------------------
async def broadcast(data: dict):
    dead = []
    for ws in ws_clients:
        try:
            await ws.send_json(data)
        except Exception:
            dead.append(ws)
    for d in dead:
        if d in ws_clients:
            ws_clients.remove(d)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    ws_clients.append(websocket)
    # Push current state to new client
    if current_votation:
        payload = current_votation.to_ws_payload()
        payload["recent_voters"] = current_votation.recent_voters(5)
        if not current_votation.active:
            payload["type"] = "poll_ended"
            payload["voters_by_option"] = {
                str(k): v
                for k, v in current_votation.voters_by_option().items()
            }
        await websocket.send_json(payload)
    if current_channel:
        await websocket.send_json(
            {"type": "session_info", "channel": current_channel}
        )
    try:
        while True:
            try:
                await asyncio.wait_for(websocket.receive_text(), timeout=25)
            except asyncio.TimeoutError:
                await websocket.send_json({"type": "ping"})
    except WebSocketDisconnect:
        pass
    finally:
        if websocket in ws_clients:
            ws_clients.remove(websocket)


# ---------------------------------------------------------------------------
# Background consumer – processes Kick chat messages
# ---------------------------------------------------------------------------
async def votation_consumer():
    global current_votation
    while True:
        try:
            created, kick_user, content = await kick_message_queue.get()
            if current_votation and current_votation.active:
                # Clean HTML tags if present (e.g. <p>1</p>)
                clean_content = re.sub(r'<[^>]*>', '', str(content)).strip()
                print(f"[Consumer] Got message from {kick_user}: {clean_content}")
                
                m = re.match(r"^(\d+)$", clean_content)
                if m:
                    option_idx = int(m.group(1))
                    accepted = current_votation.try_vote(kick_user, option_idx)
                    if accepted:
                        print(f"[Consumer] Vote accepted for {kick_user}: {option_idx}")
                        payload = current_votation.to_ws_payload()
                        payload["recent_voters"] = current_votation.recent_voters(5)
                        await broadcast(payload)
                    else:
                        print(f"[Consumer] Vote REJECTED for {kick_user}: {option_idx} (Invalid option or already voted)")
        except Exception as e:
            print("Consumer error:", e)
        await asyncio.sleep(0)


# (El bloque lifespan arriba ya maneja el inicio)


async def start_kick_session(channel: str):
    global current_channel, listener_task, listener_stop_event, kick_message_queue
    print(f"[Main] Iniciando sesión para: {channel}", flush=True)

    channel = channel.strip().lower()
    
    # Detener listener anterior si existe
    if listener_stop_event:
        listener_stop_event.set()
    if listener_task and not listener_task.done():
        listener_task.cancel()
        try:
            await listener_task
        except:
            pass

    # Limpiar cola
    while not kick_message_queue.empty():
        try: kick_message_queue.get_nowait()
        except asyncio.QueueEmpty: break
    
    current_channel = channel
    listener_stop_event = asyncio.Event()
    
    # Iniciar el navegador (headless=False para que se vea)
    listener_task = asyncio.create_task(
        kick_ws_listener(channel, kick_message_queue, headless=False, stop_event=listener_stop_event)
    )

    def on_listener_done(t):
        try:
            t.result()
        except Exception as e:
            print(f"[Main] Listener task failed: {e}")
    listener_task.add_done_callback(on_listener_done)
    
    await broadcast({"type": "session_info", "channel": channel})


# ---------------------------------------------------------------------------
# Pydantic request models
# ---------------------------------------------------------------------------
class SessionRequest(BaseModel):
    channel: str


class PollCreateRequest(BaseModel):
    question: str
    options: List[str]
    max_votes_per_user: int = 1


# ---------------------------------------------------------------------------
# REST endpoints
# ---------------------------------------------------------------------------
@app.post("/api/session")
async def create_session(req: SessionRequest):
    print(f"\n[API] Recibida solicitud de conexión para: {req.channel}", flush=True)
    if not req.channel:
        raise HTTPException(400, "Channel name required")
    
    await start_kick_session(req.channel)
    return {"status": "ok", "channel": current_channel}


@app.get("/api/session")
async def get_session():
    return {"channel": current_channel, "active": current_channel is not None}


@app.post("/api/poll")
async def create_poll(req: PollCreateRequest):
    global current_votation

    if not current_channel:
        raise HTTPException(400, "No Kick channel connected. Set channel first.")
    if current_votation and current_votation.active:
        raise HTTPException(400, "A poll is already active. End it first.")
    if len(req.options) < 2:
        raise HTTPException(400, "At least 2 options required")
    options = [o.strip() for o in req.options if o.strip()]
    if len(options) < 2:
        raise HTTPException(400, "At least 2 non-empty options required")
    if req.max_votes_per_user < 1:
        raise HTTPException(400, "max_votes_per_user must be >= 1")

    poll_id = str(uuid.uuid4())[:8].upper()
    current_votation = Votation(
        poll_id=poll_id,
        question=req.question or "Votación",
        options=options,
        max_votes_per_user=req.max_votes_per_user,
        channel=current_channel,
    )

    payload = current_votation.to_ws_payload()
    payload["type"] = "poll_started"
    payload["recent_voters"] = []
    await broadcast(payload)
    return {"status": "ok", "poll_id": poll_id}


@app.delete("/api/poll")
async def end_poll():
    global current_votation

    if not current_votation or not current_votation.active:
        raise HTTPException(400, "No active poll to end")

    current_votation.finalize()
    history_data = current_votation.to_history_dict()
    storage.save_poll(history_data)

    payload = current_votation.to_ws_payload()
    payload["type"] = "poll_ended"
    payload["voters_by_option"] = {
        str(k): v for k, v in current_votation.voters_by_option().items()
    }
    await broadcast(payload)
    return {"status": "ok", "result": history_data}


@app.get("/api/poll")
async def get_current_poll():
    if not current_votation:
        return {"active": False}
    data = current_votation.to_ws_payload()
    data["voters_by_option"] = {
        str(k): v for k, v in current_votation.voters_by_option().items()
    }
    data["recent_voters"] = current_votation.recent_voters(5)
    return data


@app.get("/api/history")
async def get_history():
    return storage.load_history()


@app.get("/api/history/{poll_id}")
async def get_history_item(poll_id: str):
    poll = storage.get_poll(poll_id)
    if not poll:
        raise HTTPException(404, "Poll not found")
    return poll


# ---------------------------------------------------------------------------
# Serve SPA
# ---------------------------------------------------------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    return FileResponse("static/index.html")
