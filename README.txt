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
- Navegador Google Chrome o Microsoft Edge instalado (opcional, 
  el programa descargará su propia versión de Chromium).

------------------------------------------------------------
2. INSTALACIÓN
------------------------------------------------------------

Antes de ejecutarlo por primera vez, abre una terminal en la 
carpeta del proyecto y ejecuta:

1. Instalar librerías necesarias:
   pip install -r requirements.txt

2. Instalar el motor del navegador (Playwright):
   playwright install chromium

------------------------------------------------------------
3. CÓMO EJECUTAR EL PROGRAMA
------------------------------------------------------------

Para garantizar la estabilidad en Windows y evitar errores de 
red, utiliza el lanzador especializado:

   python run.py

Una vez ejecutado:
1. Abre tu navegador en: http://127.0.0.1:8000
2. Introduce el nombre de tu canal de Kick.
3. Se abrirá automáticamente una ventana de navegador (Chromium) 
   que se conectará a tu chat. NO CIERRES esta ventana, ya que 
   es la que "lee" los votos.

------------------------------------------------------------
4. FUNCIONAMIENTO DE LAS VOTACIONES
------------------------------------------------------------

- Crear encuestas: Desde la web, ve a "Create New Poll", 
  pon una pregunta y las opciones.
- Votar: Los espectadores solo tienen que escribir el NÚMERO 
  de la opción en el chat (ejemplo: "1" o "2").
- Resultados: Verás las barras de progreso actualizarse en 
  tiempo real en la web.
- Historial: Todas las votaciones se guardan en el archivo 
  'history.json' y pueden consultarse en la sección "History".

------------------------------------------------------------
5. SOLUCIÓN DE PROBLEMAS (FAQ)
------------------------------------------------------------

* El navegador no se abre:
  Asegúrate de haber ejecutado 'playwright install chromium'.

* Los votos no se cuentan:
  - Verifica que la ventana de Chromium esté en el canal correcto.
  - Asegúrate de que la encuesta esté "LIVE" (Activa).
  - Revisa la consola para ver si hay errores de conexión.

* Error "NotImplementedError":
  Este error ocurre si intentas usar 'uvicorn' directamente en 
  Windows. Usa siempre 'python run.py' para evitarlo.

------------------------------------------------------------
Desarrollado para streamers de Kick.
¡Disfruta de tu Kick Vote Engine!
============================================================
