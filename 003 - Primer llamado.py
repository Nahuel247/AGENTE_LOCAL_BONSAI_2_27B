############################################################
# BONSAI 2: REALIZAMOS UNA CONSULTA AL MODELO
############################################################
# Ejecutar después de preparar el entorno y descargar el modelo.

##############################
# IMPORTAMOS LAS LIBRERÍAS
##############################

import json
import subprocess
import time
import sys
from pathlib import Path

# Al ejecutar un archivo, permitimos encontrar rutas.py también desde otra carpeta.
if '__file__' in globals():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
from rutas import PATH_PROYECTO, PATH_MODELOS

##############################
# DEFINIMOS LAS FUNCIONES
##############################

def mostrar_metricas(registro):
    """Mostrar tokens, velocidad y aviso de corte a partir del registro del runtime."""
    # El runtime informa la velocidad de generación sin incluir la carga del modelo.
    # Leemos el mensaje final del registro, no estimamos tokens a partir de palabras.
    mensaje_final = None
    for linea in registro.splitlines():
        marca = 'http: streamed chunk: data: '
        if marca not in linea:
            continue
        contenido = linea.split(marca, 1)[1]
        if not contenido.startswith('{'):
            continue
        mensaje = json.loads(contenido)
        if mensaje.get('choices') and mensaje['choices'][0].get('finish_reason'):
            mensaje_final = mensaje

    if mensaje_final is not None:
        metricas = mensaje_final.get('timings', {})
        tokens_generados = metricas.get('predicted_n')
        tokens_por_segundo = metricas.get('predicted_per_second')
        if tokens_generados is not None:
            print(f'\nTokens generados: {tokens_generados}')
        if tokens_por_segundo is not None:
            print(f'Velocidad de generación: {tokens_por_segundo:.2f} tokens/s')
        else:
            print('El runtime no informó la velocidad de generación.')
        if mensaje_final['choices'][0]['finish_reason'] == 'length':
            print('Respuesta cortada por longitud: revisa max_tokens y el espacio de contexto disponible.')
    else:
        print('\nNo se encontraron las métricas finales en el registro del runtime.')

##############################
# DEFINIMOS LAS RUTAS
##############################

proyecto = PATH_PROYECTO
modelo = PATH_MODELOS / 'Ternary-Bonsai-2-27B/Ternary-Bonsai-2-27B-PTQ1_0.gguf'
ejecutable = proyecto / 'runtime/prism-b10709-9a9394a/llama-cli.exe'
archivo_respuesta = proyecto / 'privado/consultas_terminal/bonsai_ultima_respuesta.txt'
archivo_log = proyecto / 'privado/consultas_terminal/bonsai_ultima_consulta.log'
archivo_log.parent.mkdir(parents=True, exist_ok=True)



##############################
# COMPROBAMOS LOS ARCHIVOS Y LA GPU
##############################

if not modelo.is_file() or not ejecutable.is_file():
    raise FileNotFoundError('Falta el modelo o el runtime. Ejecuta primero el archivo 002.')

gpu = subprocess.run(
    ['nvidia-smi', '--query-gpu=memory.used', '--format=csv,noheader,nounits'],
    capture_output=True, text=True, check=True, timeout=15,
)
if int(gpu.stdout.splitlines()[0]) > 2300:
    raise RuntimeError('La GPU está ocupada. Cierra otros chats o juegos antes de cargar el modelo.')


##############################
# CONFIGURAMOS EL MODELO
##############################

contexto = 2048      # Capacidad total para la entrada y la generación.
max_tokens = 1536    # Máximo de tokens generados, incluido el razonamiento.
temperatura = 0.0    # Menor variación entre respuestas.
thinking = True    # False o True para activar el razonamiento.
gpu_layers = 99
threads = 8
batch = 128

##############################
# DEFINIMOS LA PREGUNTA
##############################

pregunta = 'Explica en tres frases qué es un modelo de lenguaje.'

##############################
# CARGAMOS EL MODELO Y CONSULTAMOS
##############################

# Este GGUF usa el runtime de PrismML. Python lo ejecuta para una sola consulta.
# Al terminar, llama-cli se cierra y libera la memoria que ocupó el modelo.
comando = [
    str(ejecutable), '-m', str(modelo), '-p', pregunta,
    '-c', str(contexto), '-n', str(max_tokens), '--temp', str(temperatura),
    '-ngl', str(gpu_layers), '-t', str(threads), '-tb', str(threads),
    '-b', str(batch), '-ub', str(batch), '-fa', 'on',
    '--single-turn', '--simple-io', '--no-display-prompt', '--color', 'off',
    '--reasoning', 'on' if thinking else 'off', '--verbose',
    '--output', str(archivo_respuesta),
]

inicio = time.perf_counter()
resultado = subprocess.run(
    comando, capture_output=True, text=True, encoding='utf-8', errors='replace',
    timeout=300, creationflags=subprocess.CREATE_NO_WINDOW,
)
duracion = time.perf_counter() - inicio

##############################
# MOSTRAMOS LA RESPUESTA Y EL TIEMPO
##############################

# Conservar los mensajes técnicos separados de la respuesta, para revisar errores.
archivo_log.write_text(resultado.stderr, encoding='utf-8')
resultado.check_returncode()
respuesta = archivo_respuesta.read_text(encoding='utf-8')
print(respuesta.strip())

mostrar_metricas(resultado.stderr)
print(f'\nTiempo total (carga + respuesta): {duracion:.2f} segundos')
print('Modelo cerrado.')
