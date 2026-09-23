############################################################
# BONSAI 2: DESCARGAMOS EL MODELO Y SU RUNTIME
############################################################
# Los pesos se guardan fuera del proyecto, en MODELOS_DESCARGADOS.

##############################
# IMPORTAMOS LAS LIBRERÍAS
##############################

import hashlib
import shutil
import stat
import urllib.request
import zipfile
import sys
from pathlib import Path

# Al ejecutar un archivo, permitimos encontrar rutas.py también desde otra carpeta.
if '__file__' in globals():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
from rutas import PATH_PROYECTO, PATH_MODELOS, PATH_RUNTIME

##############################
# DEFINIMOS LAS RUTAS Y LOS ARCHIVOS
##############################

proyecto = PATH_PROYECTO
carpeta_modelos = PATH_MODELOS
carpeta_runtime = PATH_RUNTIME

modelo = {
    'destino': carpeta_modelos / 'Ternary-Bonsai-2-27B/Ternary-Bonsai-2-27B-PTQ1_0.gguf',
    'url': 'https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/resolve/6ed5e12bf84b7a63069882c91dd9e9218647d17b/Ternary-Bonsai-2-27B-PTQ1_0.gguf',
    'bytes': 5946648928,
    'sha256': '53107f530aa52eb00912263ab1ee29bd199261c87cd7b4ad4ca1318c1fe33ee3',
}

runtime = {
    'destino': carpeta_runtime / 'llama-prism-b10709-9a9394a-bin-win-cuda-12.4-x64.zip',
    'url': 'https://github.com/PrismML-Eng/llama.cpp/releases/download/prism-b10709-9a9394a/llama-prism-b10709-9a9394a-bin-win-cuda-12.4-x64.zip',
    'bytes': 253442371,
    'sha256': 'f565c8428c1f108311f65ed97f02425188b3aa3c745c2bc597521bbd24bcbbc9',
}

bibliotecas_cuda = {
    'destino': carpeta_runtime / 'cudart-llama-bin-win-cuda-12.4-x64.zip',
    'url': 'https://github.com/ggml-org/llama.cpp/releases/download/b10964/cudart-llama-bin-win-cuda-12.4-x64.zip',
    'bytes': 391443627,
    'sha256': '8c79a9b226de4b3cacfd1f83d24f962d0773be79f1e7b75c6af4ded7e32ae1d6',
}

archivos = [modelo, runtime, bibliotecas_cuda]

##############################
# DEFINIMOS LAS FUNCIONES NECESARIAS
##############################

def verificar_archivo(ruta, tamano, huella):
    """Comprobar que el archivo coincide con el publicado; no modificarlo."""
    with ruta.open('rb') as archivo:
        huella_obtenida = hashlib.file_digest(archivo, 'sha256').hexdigest()
    if ruta.stat().st_size != tamano or huella_obtenida != huella:
        raise ValueError(f'Tamaño o SHA256 incorrecto. Se conserva para revisión: {ruta}')


def extraer_runtime(archivos_zip, destino):
    """Extraer los binarios faltantes sin sobrescribir archivos distintos."""
    contenido = {}
    for ruta_zip in archivos_zip:
        with zipfile.ZipFile(ruta_zip) as archivo_zip:
            for elemento in archivo_zip.infolist():
                ruta = (destino / elemento.filename).resolve()
                if not ruta.is_relative_to(destino.resolve()) or stat.S_ISLNK(elemento.external_attr >> 16):
                    raise ValueError('El ZIP contiene una ruta insegura.')
                if not elemento.is_dir():
                    contenido[ruta] = (ruta_zip, elemento)

    # CUDA va al final de la lista: sus DLL prevalecen ante nombres repetidos.
    espacio_necesario = sum(
        elemento.file_size for ruta, (_, elemento) in contenido.items()
        if not ruta.exists()
    )
    if shutil.disk_usage(destino).free < espacio_necesario + 2 * 1024**3:
        raise RuntimeError('No hay espacio para extraer el runtime.')

    for ruta, (ruta_zip, elemento) in contenido.items():
        with zipfile.ZipFile(ruta_zip) as archivo_zip:
            with archivo_zip.open(elemento) as archivo:
                huella = hashlib.file_digest(archivo, 'sha256').hexdigest()
            if ruta.exists():
                verificar_archivo(ruta, elemento.file_size, huella)
                continue
            ruta.parent.mkdir(parents=True, exist_ok=True)
            temporal = ruta.with_name(ruta.name + '.instalando')
            with archivo_zip.open(elemento) as origen, temporal.open('xb') as salida:
                shutil.copyfileobj(origen, salida)
            verificar_archivo(temporal, elemento.file_size, huella)
            temporal.rename(ruta)

##############################
# REVISAMOS LAS UBICACIONES Y EL ESPACIO
##############################

if not carpeta_modelos.is_dir():
    raise FileNotFoundError(f'Revisa la ubicación del directorio de modelos: {carpeta_modelos}')
if not modelo['destino'].resolve().is_relative_to(carpeta_modelos.resolve()):
    raise ValueError('Los pesos deben permanecer en MODELOS_DESCARGADOS.')
carpeta_runtime.mkdir(parents=True, exist_ok=True)

bytes_faltantes = sum(a['bytes'] for a in archivos if not a['destino'].exists())
for carpeta in (carpeta_modelos, carpeta_runtime):
    if shutil.disk_usage(carpeta).free < bytes_faltantes + 2 * 1024**3:
        raise RuntimeError(f'No hay espacio suficiente en {carpeta}')

##############################
# DESCARGAMOS LOS ARCHIVOS QUE FALTEN
##############################

for archivo in archivos:
    destino = archivo['destino']
    if destino.exists():
        verificar_archivo(destino, archivo['bytes'], archivo['sha256'])
        print('Verificado, sin descargar:', destino.name)
        continue

    destino.parent.mkdir(parents=True, exist_ok=True)
    parcial = destino.with_suffix(destino.suffix + '.part')
    if not parcial.exists():
        print('Descargando:', destino.name, flush=True)
        # El parcial del modelo se guarda junto a los pesos, nunca en el proyecto.
        with urllib.request.urlopen(archivo['url'], timeout=120) as origen:
            with parcial.open('xb') as salida:
                shutil.copyfileobj(origen, salida)
    # Si una descarga anterior quedó incompleta, se conserva y se informa el error.
    verificar_archivo(parcial, archivo['bytes'], archivo['sha256'])
    parcial.rename(destino)

##############################
# EXTRAEMOS EL RUNTIME CUDA
##############################

archivos_zip = [runtime['destino'], bibliotecas_cuda['destino']]
extraer_runtime(archivos_zip, carpeta_runtime)
print('\nModelo:', modelo['destino'])
print('Runtime:', carpeta_runtime)
print('Listo. Puedes ejecutar 003 - Primer llamado.py.')
