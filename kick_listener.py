import asyncio
import json
import sys
from typing import Optional, Tuple

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from playwright.async_api import async_playwright


async def kick_ws_listener(
    streamer: str,
    out_queue: asyncio.Queue,
    headless: bool = True,
    stop_event: Optional[asyncio.Event] = None,
):
    """
    Connects to kick.com/{streamer} via Playwright, intercepts the
    WebSocket chat frames and puts (created_at, username, content)
    tuples into out_queue.
    """
    async with async_playwright() as p:
        try:
            print(f"[Listener] Intentando lanzar Google Chrome local (headless={headless})...", flush=True)
            browser = await p.chromium.launch(
                channel="chrome",
                headless=headless,
                args=["--disable-blink-features=AutomationControlled"]
            )
            print("[Listener] Google Chrome lanzado con éxito.", flush=True)
        except Exception as e_chrome:
            print(f"[Listener] Chrome no disponible ({e_chrome}). Intentando con Microsoft Edge...", flush=True)
            try:
                browser = await p.chromium.launch(
                    channel="msedge",
                    headless=headless,
                    args=["--disable-blink-features=AutomationControlled"]
                )
                print("[Listener] Microsoft Edge lanzado con éxito.", flush=True)
            except Exception as e_edge:
                print(f"\n[ERROR CRÍTICO] No se pudo lanzar ni Chrome ni Edge: {e_edge}", flush=True)
                print("Asegúrate de tener Google Chrome o Microsoft Edge instalados.\n", flush=True)
                return

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        print("[Listener] Contexto de navegación creado.", flush=True)
        page = await context.new_page()

        def extract_from_parsed(parsed) -> Optional[Tuple[str, str, str]]:
            if not isinstance(parsed, dict):
                return None
            ev = parsed.get("event") or parsed.get("type")
            if isinstance(ev, str) and "ChatMessageEvent" in ev:
                raw = parsed.get("data")
                inner = None
                if isinstance(raw, str):
                    try:
                        inner = json.loads(raw)
                    except Exception:
                        inner = None
                elif isinstance(raw, dict):
                    inner = raw
                if isinstance(inner, dict):
                    created = inner.get("created_at") or ""
                    content = inner.get("content") or ""
                    sender = inner.get("sender") or {}
                    username = None
                    if isinstance(sender, dict):
                        username = sender.get("username") or sender.get("name")
                    if username and content is not None:
                        # print(f"[Listener] Extracted: {username}: {content}") # Too noisy if kept enabled
                        return created, username, str(content)
            return None

        def try_parse_frame(payload):
            text = None
            if isinstance(payload, (bytes, bytearray)):
                try:
                    text = payload.decode("utf-8")
                except Exception:
                    return None
            elif isinstance(payload, str):
                text = payload
            else:
                return None
            try:
                parsed = json.loads(text)
            except Exception:
                return None
            return extract_from_parsed(parsed)

        async def handle_frame_raw(raw):
            payload = raw.payload if hasattr(raw, "payload") else raw
            parsed = try_parse_frame(payload)
            if not parsed:
                return
            created, username, content = parsed
            print(f"[Listener] Chat message from {username}: {content}", flush=True)
            await out_queue.put((created or "", username, content))

        def on_ws(ws):
            ws.on(
                "framereceived",
                lambda frame: asyncio.create_task(handle_frame_raw(frame)),
            )
            ws.on(
                "framesent",
                lambda frame: asyncio.create_task(handle_frame_raw(frame)),
            )

        page.on("websocket", on_ws)
        print(f"[Listener] Navigating to https://kick.com/{streamer}...", flush=True)
        await page.goto(
            f"https://kick.com/{streamer}",
            wait_until="domcontentloaded",
            timeout=60_000,
        )
        print("[Listener] Page loaded. Listening for messages...", flush=True)
        try:
            while True:
                if stop_event and stop_event.is_set():
                    break
                await asyncio.sleep(1)
        finally:
            await browser.close()