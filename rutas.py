"""Leer las rutas privadas del PC; este módulo no carga el modelo."""
import json
from pathlib import Path

archivo = Path(__file__).resolve().parent / 'rutas_locales.txt'
if not archivo.is_file():
    raise FileNotFoundError('Copia rutas_ejemplo.txt como rutas_locales.txt y completa sus rutas absolutas.')
nombres = ('PATH_PROYECTO', 'PATH_AMBIENTES', 'PATH_MODELOS', 'PATH_PYTHON')
rutas = {}
for numero, linea in enumerate(archivo.read_text(encoding='utf-8-sig').splitlines(), 1):
    linea = linea.strip()
    if not linea or linea.startswith('#'):
        continue
    nombre, separador, valor = linea.partition('=')
    nombre, valor = nombre.strip(), valor.strip()
    if not separador or nombre not in nombres or nombre in rutas:
        raise ValueError(f'Línea {numero} de rutas_locales.txt: usa NOMBRE = ruta, sin nombres repetidos ni desconocidos.')
    rutas[nombre] = valor
for nombre in nombres:
    if not Path(rutas.get(nombre, '')).is_absolute():
        raise ValueError(f'Completa {nombre} con una ruta absoluta, sin comillas, en rutas_locales.txt.')

PATH_PROYECTO = Path(rutas['PATH_PROYECTO'])
PATH_AMBIENTES = Path(rutas['PATH_AMBIENTES'])
PATH_MODELOS = Path(rutas['PATH_MODELOS'])
# Compartimos esta versión del runtime entre los proyectos que usan el modelo.
PATH_RUNTIME = PATH_MODELOS / 'Ternary-Bonsai-2-27B/runtime/prism-b10709-9a9394a'
rutas['PATH_RUNTIME'] = str(PATH_RUNTIME)
PATH_PYTHON = Path(rutas['PATH_PYTHON'])
if not PATH_PYTHON.resolve().is_relative_to(PATH_AMBIENTES.resolve()):
    raise ValueError('PATH_PYTHON debe estar dentro de PATH_AMBIENTES.')


def cargar_config(archivo_config):
    """Resolver los marcadores PATH de una configuración de modelo."""
    config = json.loads(Path(archivo_config).read_text(encoding='utf-8-sig'))
    for nombre in ('model', 'server', 'drafter'):
        if nombre in config:
            config[nombre] = config[nombre].format_map(rutas)
    return config
