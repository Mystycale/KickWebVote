============================================================
           KICK VOTE ENGINE - GUÍA DE USUARIO
============================================================

Este programa permite crear votaciones en tiempo real para tu 
chat de Kick.com, utilizando tu propio navegador para leer 
los mensajes y una interfaz web para gestionar todo.

------------------------------------------------------------
1. REQUISITOS PREVIOS
------------------------------------------------------------

- Python 3.10 o superior instalado.
- Google Chrome o Microsoft Edge instalado.
- Node.js (Opcional, para compartir el servidor).

------------------------------------------------------------
2. INSTALACIÓN Y EJECUCIÓN (ONE-CLICK)
------------------------------------------------------------

No necesitas instalar nada manualmente. El programa lo hará 
por ti la primera vez que lo abras:

En WINDOWS:
1. Haz doble clic en el archivo: iniciar_todo.bat
2. Espera a que termine la instalación automática.

En LINUX:
1. Dale permisos al archivo: chmod +x iniciar_todo.sh
2. Ejecútalo: ./iniciar_todo.sh

------------------------------------------------------------
3. CÓMO USAR EL PROGRAMA
------------------------------------------------------------

Una vez iniciado el servidor:
1. Entra en tu navegador a: http://127.0.0.1:8000
2. Introduce el nombre de tu canal de Kick.
3. Se abrirá una ventana de Chrome/Edge conectada al chat. 
   ¡No la cierres! Es la que captura los votos.

------------------------------------------------------------
4. COMPARTIR Y PRIVACIDAD (IMPORTANTE)
------------------------------------------------------------

Para que otras personas controlen la votación por internet:

1. PROTEGE TU IP: Enciende una VPN (como ProtonVPN o 
   Cloudflare WARP) ANTES de abrir el programa.
2. El archivo 'iniciar_todo' abrirá automáticamente una 
   ventana de Ngrok con un enlace público.
3. Pasa ese enlace (.ngrok-free.app) a tus amigos.

------------------------------------------------------------
5. SOLUCIÓN DE PROBLEMAS (FAQ)
------------------------------------------------------------

* ¿Por qué se abre una ventana de Chrome sola?
  Es normal, es el "lector" de votos. Debe estar abierta.

* Las barras no se mueven:
  Refresca la web con F5. Asegúrate de que la encuesta 
  esté en estado "LIVE".

* Error al iniciar (Windows):
  Asegúrate de que 'python' esté en el PATH de tu sistema.

------------------------------------------------------------
Desarrollado para streamers de Kick.
¡Disfruta de tu Kick Vote Engine!
============================================================
