#!/bin/bash

echo "============================================================"
echo "           KICK VOTE ENGINE - AUTO-CONFIGURACION (LINUX)"
echo "============================================================"
echo ""

# Función para limpiar procesos al salir
cleanup() {
    echo ""
    echo "[!] Cerrando procesos..."
    kill $PYTHON_PID 2>/dev/null
    exit
}

# Ejecutar cleanup si se pulsa Ctrl+C o si el script termina
trap cleanup SIGINT SIGTERM

# 1. Liberar el puerto 8000 por si acaso quedó algo de antes (Muy importante en Linux)
fuser -k 8000/tcp 2>/dev/null

# 2. Comprobar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "[!] Entorno virtual no detectado. Iniciando instalacion..."
    echo "[+] Creando entorno virtual (venv)..."
    python3 -m venv venv
    
    echo "[+] Instalando librerias necesarias..."
    ./venv/bin/python3 -m pip install --upgrade pip
    ./venv/bin/pip install -r requirements.txt
    
    echo "[+] Instalando motores de navegador..."
    ./venv/bin/playwright install chromium
    
    echo ""
    echo "[OK] Instalacion completada con exito."
    echo ""
fi

echo "[!] Asegurate de tener Ngrok instalado en tu sistema Linux."
read -p "Presiona Enter para iniciar el servidor..."

# 3. Iniciar servidor en segundo plano
echo "[+] Iniciando Servidor Python..."
source venv/bin/activate
python3 run.py &
PYTHON_PID=$! # <--- Guardamos el ID del proceso para poder matarlo luego

# 4. Iniciar Ngrok
echo "[+] Iniciando Tunel Ngrok..."
ngrok http 8000

# Si llegamos aquí (Ngrok se cierra), limpiamos todo
cleanup
