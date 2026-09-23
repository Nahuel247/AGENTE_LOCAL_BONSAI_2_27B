"""Leer las rutas privadas del PC; este módulo no carga el modelo."""
import json
from pathlib import Path

archivo = Path(__file__).resolve().parent / 'rutas_locales.json'
if not archivo.is_file():
    raise FileNotFoundError('Copia rutas_ejemplo.json como rutas_locales.json y completa sus rutas absolutas.')
rutas = json.loads(archivo.read_text(encoding='utf-8-sig'))
for nombre in ('PATH_PROYECTO', 'PATH_AMBIENTES', 'PATH_MODELOS', 'PATH_PYTHON'):
    if not isinstance(rutas.get(nombre), str) or not Path(rutas[nombre]).is_absolute():
        raise ValueError(f'Completa {nombre} con una ruta absoluta en rutas_locales.json.')

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
