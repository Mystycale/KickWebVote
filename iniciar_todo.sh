#!/bin/bash

echo "============================================================"
echo "           KICK VOTE ENGINE - AUTO-CONFIGURACION (LINUX)"
echo "============================================================"
echo ""

# 1. Comprobar si existe el entorno virtual
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

# Iniciar servidor en segundo plano
echo "[+] Iniciando Servidor Python..."
source venv/bin/activate
python3 run.py &

# Iniciar Ngrok (requiere que el usuario lo tenga instalado en el PATH)
echo "[+] Iniciando Tunel Ngrok..."
ngrok http 8000
