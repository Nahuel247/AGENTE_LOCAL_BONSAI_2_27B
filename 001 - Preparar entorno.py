############################################################
# BONSAI 2: PREPARAMOS EL ENTORNO DE PYTHON
############################################################
# Ejecutar con Python 3.12. Este paso no descarga ni carga el modelo.

##############################
# IMPORTAMOS LAS LIBRERÍAS
##############################

import subprocess
import sys
import venv
from pathlib import Path

# Al ejecutar un archivo, permitimos encontrar rutas.py también desde otra carpeta.
if '__file__' in globals():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
from rutas import PATH_AMBIENTES

##############################
# DEFINIMOS LAS RUTAS
##############################

carpeta_ambientes = PATH_AMBIENTES
nuevo_entorno = carpeta_ambientes / 'bonsai_27b'

########################################
# REVISAMOS LOS ENTORNOS QUE YA EXISTEN
########################################

# Los tres scripts usan librerías incluidas en Python 3.12.
interpretes = list(carpeta_ambientes.glob('*/Scripts/python.exe'))
interpretes += list(carpeta_ambientes.glob('*/.venv/Scripts/python.exe'))
interpretes = sorted(interpretes)

# Preferimos el entorno de Bonsai si ya existe.
python_bonsai = nuevo_entorno / 'Scripts/python.exe'
if python_bonsai in interpretes:
    interpretes.remove(python_bonsai)
    interpretes.insert(0, python_bonsai)

python_entorno = None
for interprete in interpretes:
    try:
        resultado = subprocess.run(
            [str(interprete), '--version'], capture_output=True,
            text=True, check=True, timeout=15,
        )
    except (OSError, subprocess.SubprocessError) as error:
        print('No se pudo revisar:', interprete, error)
        continue

    version = resultado.stdout.strip()
    print(interprete, '|', version)
    if version.startswith('Python 3.12.') and python_entorno is None:
        python_entorno = interprete

########################################
# CREAMOS UN ENTORNO SOLO SI HACE FALTA
########################################

if python_entorno is None:
    if sys.version_info[:2] != (3, 12):
        raise RuntimeError('Ejecuta este archivo con Python 3.12 para crear el entorno.')
    if nuevo_entorno.exists():
        raise RuntimeError('El destino existe pero no sirve. Cambia nuevo_entorno; no se modificará el existente.')
    if not nuevo_entorno.resolve().is_relative_to(carpeta_ambientes.resolve()):
        raise ValueError('El entorno debe quedar dentro de AMBIENTES_PYTHON.')
    venv.EnvBuilder(with_pip=True).create(nuevo_entorno)
    python_entorno = nuevo_entorno / 'Scripts/python.exe'

##############################
# MOSTRAMOS EL RESULTADO
##############################

print('\nSelecciona este intérprete en PyCharm:')
print(python_entorno)
print('\nNo es necesario instalar paquetes adicionales para los pasos 002 y 003.')
print('Siguiente paso: 002 - Descargar modelo y runtime.py')
