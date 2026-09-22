# Ejecución directa: copia todo en la consola Python o ejecuta el archivo.

##############################
# IMPORTAMOS LAS LIBRERÍAS
##############################

import subprocess
import sys
from pathlib import Path

# Al ejecutar un archivo, permitimos encontrar rutas.py también desde otra carpeta.
if '__file__' in globals():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
from rutas import PATH_PROYECTO, PATH_PYTHON

##############################
# DEFINIMOS LAS RUTAS Y LOS PARÁMETROS
##############################

proyecto = PATH_PROYECTO
python = PATH_PYTHON
lanzador = proyecto / 'app/chat_web.py'

contexto = 8192       # Entrada, historial y generación comparten este espacio.
max_tokens = 4096     # Máximo de salida, incluyendo el razonamiento.
thinking = True
esfuerzo = 'medium'   # Opciones del lanzador: medium o xhigh.
puerto = 8088         # Mantenerlo permite recuperar los chats del mismo navegador.

##############################
# COMPROBAMOS LOS ARCHIVOS Y LA GPU
##############################

if not python.is_file() or not lanzador.is_file():
    raise FileNotFoundError('No se encontró el entorno de Bonsai o el lanzador web.')

gpu = subprocess.run(
    ['nvidia-smi', '--query-gpu=memory.used', '--format=csv,noheader,nounits'],
    capture_output=True, text=True, check=True, timeout=15,
)
if int(gpu.stdout.splitlines()[0]) > 2300:
    raise RuntimeError(
        'La GPU está ocupada. Si usabas el 004, ejecuta cerrar_modelo() en su consola. '
        'Si la web ya está abierta, úsala sin iniciar otra copia.'
    )

##############################
# INICIAMOS EL MODELO Y ABRIMOS LA WEB
##############################

# Reutilizamos la web existente: conserva tablas, historial y controles en español.
comando = [
    str(python), '-X', 'utf8', str(lanzador),
    '--context', str(contexto), '--max-tokens', str(max_tokens),
    '--effort', esfuerzo, '--port', str(puerto),
]
if not thinking:
    comando.append('--no-thinking')

# El lanzador abre el navegador cuando el modelo termina de cargar.
# Los ajustes guardados en el navegador pueden prevalecer sobre estos parámetros.
# Cerrar la última pestaña del chat activa la liberación de GPU del lanzador.
print('Iniciando la web de Bonsai. El navegador se abrirá cuando esté lista.', flush=True)
resultado = subprocess.run(comando, cwd=str(proyecto))
resultado.check_returncode()
print('El chat web terminó.')
