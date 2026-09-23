############################################################
# BONSAI 2: CREAMOS EL ACCESO DIRECTO DEL ESCRITORIO
############################################################

##############################
# IMPORTAMOS LAS LIBRERÍAS
##############################

import base64
import os
import subprocess
import sys
from pathlib import Path

if '__file__' in globals():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
from rutas import PATH_PROYECTO, PATH_PYTHON

##############################
# DEFINIMOS LAS RUTAS
##############################

lanzador = PATH_PROYECTO / '004 - Chat web.py'
icono = PATH_PROYECTO / 'app/web_ui/nc-logo.ico'

if not all(archivo.is_file() for archivo in (PATH_PYTHON, lanzador, icono)):
    raise FileNotFoundError('Revisa el intérprete, el archivo 004 y el icono NC.')

##############################
# CREAMOS O ACTUALIZAMOS EL ACCESO DIRECTO
##############################

# Windows localiza el escritorio real, incluso si está dentro de OneDrive.
# Las rutas viajan como datos, sin incorporarlas al código de PowerShell.
entorno = os.environ.copy()
entorno.update({
    'BONSAI_PYTHON': str(PATH_PYTHON),
    'BONSAI_PROYECTO': str(PATH_PROYECTO),
    'BONSAI_ICONO': str(icono),
    'BONSAI_ARGUMENTOS': subprocess.list2cmdline(['-X', 'utf8', str(lanzador)]),
})
instrucciones = """
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$shell = New-Object -ComObject WScript.Shell
$escritorio = $shell.SpecialFolders.Item('Desktop')
$rutaAcceso = Join-Path $escritorio 'Bonsai 2 - Chat local.lnk'
$acceso = $shell.CreateShortcut($rutaAcceso)
$acceso.TargetPath = $env:BONSAI_PYTHON
$acceso.Arguments = $env:BONSAI_ARGUMENTOS
$acceso.WorkingDirectory = $env:BONSAI_PROYECTO
$acceso.IconLocation = $env:BONSAI_ICONO + ',0'
$acceso.Description = 'Bonsai 2 · Adaptado por Nahuel Canelo'
$acceso.WindowStyle = 7
$acceso.Save()
Write-Output $rutaAcceso
"""
codigo = base64.b64encode(instrucciones.encode('utf-16-le')).decode('ascii')
resultado = subprocess.run(
    ['powershell.exe', '-NoProfile', '-NonInteractive', '-EncodedCommand', codigo],
    env=entorno, capture_output=True, text=True, encoding='utf-8', errors='replace',
    timeout=30, creationflags=subprocess.CREATE_NO_WINDOW,
)
if resultado.returncode:
    raise RuntimeError(resultado.stderr.strip())

print('Acceso directo creado:', resultado.stdout.strip())
print('Haz doble clic para iniciar Python y abrir la web. La consola queda minimizada.')
print('Cierra las pestañas del chat para que el lanzador libere la memoria del modelo.')
