============================================================
           KICK VOTE ENGINE - GUÍA DE USUARIO
============================================================

Este programa permite crear votaciones en tiempo real para tu 
chat de Kick.com, utilizando un navegador automatizado para 
leer los mensajes y una interfaz web para gestionar las 
encuestas y ver los resultados.

------------------------------------------------------------
1. REQUISITOS PREVIOS
------------------------------------------------------------

- Python 3.10 o superior instalado.
- Google Chrome o Microsoft Edge instalado (El programa usará 
  preferiblemente tu navegador Chrome local).
- Node.js instalado (Opcional, para compartir el servidor).

------------------------------------------------------------
2. INSTALACIÓN
------------------------------------------------------------

Antes de ejecutarlo por primera vez, abre una terminal en la 
carpeta del proyecto y ejecuta:

1. Instalar librerías necesarias:
   pip install -r requirements.txt

2. Preparar el motor del navegador:
   playwright install

------------------------------------------------------------
3. CÓMO EJECUTAR EL PROGRAMA
------------------------------------------------------------

Para garantizar la estabilidad en Windows y evitar errores, 
utiliza siempre el lanzador especializado:

   python run.py

Una vez ejecutado:
1. Abre tu navegador en: http://127.0.0.1:8000
2. Introduce el nombre de tu canal de Kick.
3. Se abrirá automáticamente una ventana de tu navegador local 
   (Chrome o Edge) conectada al chat. NO CIERRES esta ventana, 
   ya que es la que "lee" los votos.

------------------------------------------------------------
4. FUNCIONAMIENTO DE LAS VOTACIONES
------------------------------------------------------------

- Crear encuestas: Desde la web, ve a "Create New Poll".
- Votar: Los espectadores escriben el NÚMERO de la opción 
  en el chat (ejemplo: "1"). Las barras de progreso se 
  actualizan en tiempo real.
- Historial: Se guarda en 'history.json' y se puede ver 
  en la sección "History" de la web.

------------------------------------------------------------
5. COMPARTIR Y PRIVACIDAD (IMPORTANTE)
------------------------------------------------------------

Si quieres que otras personas controlen la votación o vean los 
resultados desde fuera de tu casa, puedes usar Ngrok:

1. PROTEGE TU IP: Antes de nada, enciende una VPN (como 
   ProtonVPN o Cloudflare WARP) para que Ngrok no muestre 
   tu ubicación real.
2. Abre una nueva terminal y ejecuta:
   npx.cmd ngrok http 8000
3. Pasa el enlace de Ngrok a tus amigos.

------------------------------------------------------------
6. SOLUCIÓN DE PROBLEMAS (FAQ)
------------------------------------------------------------

* El navegador no se abre:
  Asegúrate de tener Google Chrome o Microsoft Edge instalado 
  en tu PC. Si el error persiste, revisa los logs de la consola.

* Las barras no se actualizan en tiempo real:
  Refresca la página web con F5 o Ctrl+F5 para asegurarte de 
  tener la última versión del código cargada.

* Error "NotImplementedError":
  Ocurre si usas 'uvicorn' directamente. Usa siempre 
  'python run.py'.

------------------------------------------------------------
Desarrollado para streamers de Kick.
¡Disfruta de tu Kick Vote Engine!
============================================================
