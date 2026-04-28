@echo off
title Lanzador de Kick Vote Engine
echo ============================================================
echo           KICK VOTE ENGINE - INICIO AUTOMATICO
echo ============================================================
echo.
echo [!] IMPORTANTE: Recuerda encender tu VPN antes de continuar
echo     para proteger tu direccion IP en Ngrok.
echo.
pause

echo.
echo [+] Iniciando Servidor Python...
start "Servidor Kick Vote" cmd /k "python run.py"

echo [+] Iniciando Tunel Ngrok...
echo [i] Si es la primera vez, puede que tarde unos segundos en descargar.
start "Tunel Ngrok" cmd /k "npx.cmd ngrok http 8000"

echo.
echo ============================================================
echo  ¡Todo listo! Revisa las nuevas ventanas para ver los links.
echo ============================================================
echo.
pause
