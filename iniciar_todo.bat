@echo off
setlocal
title Lanzador Automático - Kick Vote Engine

echo ============================================================
echo           KICK VOTE ENGINE - AUTO-CONFIGURACION
echo ============================================================
echo.

:: Si ya existe la carpeta venv, saltamos la instalacion
if exist "venv\Scripts\python.exe" goto START_APP

:SETUP
echo [!] Entorno virtual no detectado o incompleto.
echo [+] Iniciando instalacion automatica...
echo.

echo [+] Creando entorno virtual (venv)...
python -m venv venv
if errorlevel 1 goto ERROR_PYTHON

echo [+] Instalando librerias necesarias (esto puede tardar)...
venv\Scripts\python -m pip install --upgrade pip >nul
venv\Scripts\pip install -r requirements.txt
if errorlevel 1 goto ERROR_INSTALL

echo [+] Instalando motores de navegador (Playwright)...
venv\Scripts\playwright install chromium
if errorlevel 1 goto ERROR_INSTALL

echo.
echo [OK] Instalacion completada con exito.
echo.
pause

:START_APP
echo ============================================================
echo           KICK VOTE ENGINE - INICIANDO SESION
echo ============================================================
echo.
echo [!] IMPORTANTE: Recuerda encender tu VPN antes de continuar.
echo.
pause

echo [+] Lanzando Servidor Python...
start "Servidor Kick Vote" cmd /k "venv\Scripts\python run.py"

echo [+] Lanzando Tunel Ngrok...
start "Tunel Ngrok" cmd /k "npx.cmd ngrok http 8000"

echo.
echo [OK] Todo en marcha. Revisa las nuevas ventanas.
exit /b

:ERROR_PYTHON
echo.
echo [ERROR] No se pudo ejecutar 'python'. 
echo Asegurate de que Python esta instalado y añadido al PATH.
pause
exit /b

:ERROR_INSTALL
echo.
echo [ERROR] Hubo un problema durante la instalacion de librerias.
echo Revisa tu conexion a internet e intenta de nuevo.
pause
exit /b
