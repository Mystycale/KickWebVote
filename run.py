import asyncio
import sys
import uvicorn

if __name__ == "__main__":
    print("\n" + "="*60)
    print(">>> INICIANDO KICK VOTE ENGINE (MODO ESTABLE WINDOWS) <<<")
    print("="*60)
    
    if sys.platform == 'win32':
        print(">>> Configurando WindowsProactorEventLoopPolicy...")
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # Desactivamos reload para garantizar que el proceso hijo no herede un bucle incorrecto
    print(">>> Iniciando servidor en http://127.0.0.1:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
