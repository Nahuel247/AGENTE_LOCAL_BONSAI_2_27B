############################################################
# BONSAI 2: UN ASISTENTE DISPONIBLE EN LA CONSOLA PYTHON
############################################################
# Cargar este archivo en la consola de PyCharm una vez por sesión.
# Después puedes alternar agente("pregunta") y tus cálculos de Python.

##############################
# IMPORTAMOS LAS LIBRERÍAS
##############################

import atexit
import json
import socket
import subprocess
import time
import urllib.error
import urllib.request
import sys
from pathlib import Path

# Al ejecutar un archivo, permitimos encontrar rutas.py también desde otra carpeta.
if '__file__' in globals():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
from rutas import PATH_PROYECTO, PATH_MODELOS, PATH_RUNTIME

# No perder la referencia a un modelo ya cargado si ejecutas otra vez el archivo.
if 'proceso_bonsai' in globals() and proceso_bonsai.poll() is None:
    raise RuntimeError('Bonsai ya está cargado. Usa agente(...) o cerrar_modelo() antes de reiniciar.')

##############################
# DEFINIMOS LAS FUNCIONES
##############################

def recibir_respuesta(solicitud, mostrar):
    """Enviar la consulta y devolver texto, métricas y motivo de finalización."""
    # Guardamos los fragmentos para reconstruir la respuesta al terminar.
    fragmentos = []
    metricas = {}
    motivo_fin = None
    terminado = False
    aviso_pensando = False
    try:
        with urllib.request.urlopen(solicitud, timeout=300) as respuesta_http:
            # El servidor envía eventos de texto; imprimimos cada fragmento al llegar.
            for linea in respuesta_http:
                linea = linea.decode('utf-8').strip()
                if not linea.startswith('data:'):
                    continue
                contenido = linea[5:].strip()
                # [DONE] confirma que el servidor terminó de enviar la respuesta.
                if contenido == '[DONE]':
                    terminado = True
                    break
                evento = json.loads(contenido)
                if evento.get('error'):
                    raise RuntimeError(f"El servidor devolvió un error: {evento['error']}")
                metricas.update(evento.get('timings') or {})
                if not evento.get('choices'):
                    continue
                opcion = evento['choices'][0]
                delta = opcion.get('delta', {})
                # Avisamos que está razonando sin imprimir el razonamiento interno.
                if mostrar and delta.get('reasoning_content') and not aviso_pensando:
                    print('[Pensando...]', flush=True)
                    aviso_pensando = True
                texto = delta.get('content') or ''
                if texto:
                    fragmentos.append(texto)
                    if mostrar:
                        print(texto, end='', flush=True)
                if opcion.get('finish_reason'):
                    motivo_fin = opcion['finish_reason']
    except urllib.error.HTTPError as error:
        detalle = error.read().decode('utf-8', errors='replace')
        raise RuntimeError(f'{detalle}\nSi agotaste el contexto, usa limpiar_historial().') from error

    if mostrar:
        print()
    # No aceptamos una conexión cortada como si fuera una respuesta completa.
    if not terminado or motivo_fin is None:
        raise RuntimeError('La transmisión se interrumpió. La respuesta parcial no se agregó al historial.')
    return ''.join(fragmentos), metricas, motivo_fin


def mostrar_metricas(metricas, duracion):
    """Mostrar el tiempo total de consulta y la velocidad informada por el servidor."""
    print(f'\nTiempo de respuesta: {duracion:.2f} segundos')
    velocidad = metricas.get('predicted_per_second')
    if velocidad is not None:
        print(f'Generación: {velocidad:.2f} tokens/s')


def agente(pregunta=None, mostrar=True):
    """Consultar al modelo; mostrar=False devuelve el texto en vez de imprimirlo."""
    # Comprobamos que el modelo siga cargado y pedimos texto si no se proporcionó.
    if proceso_bonsai.poll() is not None:
        raise RuntimeError('El modelo está cerrado. Vuelve a ejecutar el archivo 005.')
    if pregunta is None:
        pregunta = input('Tú: ')
    if not isinstance(pregunta, str) or not pregunta.strip():
        raise ValueError('Escribe una pregunta de texto no vacía.')

    # Enviamos la conversación previa junto con la pregunta y los parámetros actuales.
    mensajes = historial + [{'role': 'user', 'content': pregunta}]
    consulta = {
        'messages': mensajes,
        'max_tokens': max_tokens,
        'temperature': temperatura,
        'stream': True,
        'cache_prompt': True,
        'chat_template_kwargs': {'enable_thinking': thinking},
    }
    solicitud = urllib.request.Request(
        url + '/v1/chat/completions', data=json.dumps(consulta).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
    )

    # Recibimos e imprimimos los fragmentos conforme llegan, sin recargar el modelo.
    inicio = time.perf_counter()
    respuesta, metricas, motivo_fin = recibir_respuesta(solicitud, mostrar)
    duracion = time.perf_counter() - inicio

    # Actualizamos el historial solo si la transmisión terminó correctamente.
    historial[:] = mensajes + [{'role': 'assistant', 'content': respuesta}]
    if motivo_fin == 'length':
        print('Respuesta cortada por longitud: revisa max_tokens y el contexto disponible.')
    if mostrar:
        mostrar_metricas(metricas, duracion)
    else:
        return respuesta


def limpiar_historial():
    """Empezar otra conversación sin descargar el modelo de la GPU."""
    historial[:] = [{'role': 'system', 'content': instruccion}]
    print('Historial borrado. Puedes seguir usando agente(...).')


def cerrar_modelo(proceso=None):
    """Liberar la memoria del modelo y mantener abierta la consola Python."""
    if proceso is None:
        proceso = proceso_bonsai
    if proceso.poll() is None:
        proceso.terminate()
        try:
            proceso.wait(timeout=15)
        except subprocess.TimeoutExpired:
            proceso.kill()
            proceso.wait(timeout=10)
        print('Modelo cerrado.')

##############################
# DEFINIMOS LAS RUTAS Y LOS PARÁMETROS
##############################

proyecto = PATH_PROYECTO
modelo = PATH_MODELOS / 'Ternary-Bonsai-2-27B/Ternary-Bonsai-2-27B-PTQ1_0.gguf'
ejecutable = PATH_RUNTIME / 'llama-server.exe'
archivo_log = proyecto / 'privado/consultas_terminal/bonsai_chat.log'
archivo_log.parent.mkdir(parents=True, exist_ok=True)

contexto = 4096       # Historial + entrada + respuesta.
max_tokens = 1536     # Máximo por respuesta; incluye el razonamiento.
temperatura = 0.3
thinking = True
gpu_layers = 99
threads = 8
batch = 128
puerto = 8090
url = f'http://127.0.0.1:{puerto}'

instruccion = (
    'Eres un asistente local. Responde en español y ayuda a resolver las tareas '
    'del usuario. Si falta información, pregúntala. No afirmes haber navegado, '
    'abierto archivos ni ejecutado herramientas cuando no lo hayas hecho.'
)
historial = [{'role': 'system', 'content': instruccion}]

##############################
# COMPROBAMOS LOS ARCHIVOS Y LA GPU
##############################

if not modelo.is_file() or not ejecutable.is_file():
    raise FileNotFoundError('Falta el modelo o el runtime. Ejecuta primero el paso 002.')
with socket.socket() as conexion:
    conexion.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
    conexion.bind(('127.0.0.1', puerto))  # Si está ocupado, no cargamos otro modelo.

gpu = subprocess.run(
    ['nvidia-smi', '--query-gpu=memory.used', '--format=csv,noheader,nounits'],
    capture_output=True, text=True, check=True, timeout=15,
)
if int(gpu.stdout.splitlines()[0]) > 2300:
    raise RuntimeError('Cierra otros chats o juegos para dejar espacio en la GPU.')

##############################
# CARGAMOS EL MODELO UNA SOLA VEZ
##############################

comando = [
    str(ejecutable), '-m', str(modelo), '--host', '127.0.0.1', '--port', str(puerto),
    '-c', str(contexto), '-ngl', str(gpu_layers), '-t', str(threads), '-tb', str(threads),
    '-b', str(batch), '-ub', str(batch), '-np', '1', '-fa', 'on', '--jinja',
    '--cache-ram', '0', '--cache-prompt', '--no-context-shift', '--no-agent',
    '--reasoning', 'on' if thinking else 'off',
]
print('Cargando Bonsai...')
with archivo_log.open('w', encoding='utf-8') as log:
    proceso_bonsai = subprocess.Popen(
        comando, stdout=log, stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )
# Cerrar también al salir normalmente de Python; no cierra procesos ajenos.
atexit.register(cerrar_modelo, proceso_bonsai)

inicio = time.perf_counter()
try:
    while True:
        if proceso_bonsai.poll() is not None:
            raise RuntimeError(f'El servidor terminó. Revisa {archivo_log}')
        try:
            with urllib.request.urlopen(url + '/health', timeout=3) as respuesta_http:
                if json.load(respuesta_http)['status'] == 'ok':
                    break
        except OSError:
            pass
        if time.perf_counter() - inicio > 180:
            raise TimeoutError(f'El modelo no cargó a tiempo. Revisa {archivo_log}')
        time.sleep(0.25)
except BaseException:
    cerrar_modelo()
    raise

##############################
# VOLVEMOS A LA CONSOLA PYTHON
##############################

print('Listo. Puedes seguir usando Python y consultar agente("tu pregunta").')
print('limpiar_historial() empieza otra conversación; cerrar_modelo() libera la GPU.')

# Ejemplos para ejecutar después, cuando tú quieras:
# agente("Recuerda que el presupuesto es 500")
# total = 500 * 1.19
# agente(f"El total calculado en Python es {total}. Explícalo brevemente.")
# respuesta = agente("Resume nuestra conversación", mostrar=False)
# cerrar_modelo()
