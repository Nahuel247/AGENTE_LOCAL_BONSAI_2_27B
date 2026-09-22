"""Launch the bundled llama.cpp web chat with Bonsai 2, locally and without DSpark."""
import argparse
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
import webbrowser
from datetime import datetime, timezone
# Encontrar los módulos del proyecto al ejecutar app/chat_web.py directamente.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from rutas import cargar_config
from app.chat_lifecycle import ChatLifecycle

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=ROOT / 'configuracion' / 'modelo.json')
    parser.add_argument('--port', type=int, default=8088)
    parser.add_argument('--context', type=int, default=8192)
    parser.add_argument('--max-tokens', type=int, default=2048)
    parser.add_argument('--effort', choices=['medium', 'xhigh'], default='medium')
    parser.add_argument('--no-thinking', action='store_true')
    parser.add_argument('--no-browser', action='store_true')
    parser.add_argument('--reuse-existing', action='store_true', help='Abre la instancia del mismo modelo si ya está lista.')
    parser.add_argument('--keep-alive', action='store_true', help='Mantener el modelo cargado aunque se cierre el navegador.')
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        parser.error('El puerto debe estar entre 1024 y 65535.')
    if args.context < 2048 or not 0 < args.max_tokens < args.context:
        parser.error('Usa contexto >= 2048 y 0 < max-tokens < contexto.')
    config = cargar_config(args.config)
    model = Path(config['model']).resolve(strict=True)
    binary = Path(config['server']).resolve(strict=True)
    # Fail before loading another model when this address is already occupied.
    with socket.socket() as probe:
        if os.name == 'nt':
            probe.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        try:
            probe.bind(('127.0.0.1', args.port))
        except OSError:
            if args.reuse_existing:
                try:
                    base = f'http://127.0.0.1:{args.port}'
                    with urllib.request.urlopen(base + '/v1/models', timeout=3) as response:
                        models = json.load(response).get('data', [])
                    with urllib.request.urlopen(base + '/health', timeout=3) as response:
                        ready = json.load(response).get('status') == 'ok'
                    if ready and any(item.get('id') == model.stem for item in models):
                        if not args.no_browser:
                            webbrowser.open(base + '/index.html?ui=thinking1')
                        print('Abriendo la instancia de Bonsai que ya estaba iniciada.')
                        return 0
                except (OSError, ValueError):
                    pass
            parser.error(f'El puerto {args.port} está ocupado. Cierra la instancia anterior o usa --port.')
    folder = ROOT / 'datos' / 'registros' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
    folder.mkdir(parents=True, exist_ok=False)
    ui = dict(showThoughtInProgress=False, excludeReasoningFromContext=True,
              showMessageStats=True, renderUserContentAsMarkdown=True,
              titleGenerationUseLLM=False, titleGenerationUseFirstLine=True,
              pasteLongTextToFileLen=0, jsSandboxEnabled=False,
              max_tokens=args.max_tokens, temperature=0.7, top_p=0.9,
              customJson=json.dumps({'cache_prompt': True}))
    ui_path = folder / 'ui_config.json'
    ui_path.write_text(json.dumps(ui, indent=2), encoding='utf-8')
    command = [str(binary), '-m', str(model), '--alias', model.stem,
               '--host', '127.0.0.1', '--port', str(args.port),
               '-c', str(args.context), '-b', '256', '-ub', '256',
               '-ngl', '99', '-t', '8', '-tb', '8', '-np', '1', '-fa', 'on',
               '--jinja', '--cache-ram', '0', '--cache-prompt', '--no-context-shift',
               '--reasoning', 'off' if args.no_thinking else 'on',
               '--reasoning-effort', args.effort, '--reasoning-format', 'deepseek',
               '-n', str(args.max_tokens), '--temp', '0.7', '--top-p', '0.9',
               '--webui', '--ui-config-file', str(ui_path), '--no-agent',
               '--cors-origins', f'http://127.0.0.1:{args.port}']
    (folder / 'command.json').write_text(json.dumps(command, indent=2), encoding='utf-8')
    if (ROOT / 'web_ui' / 'index.html').is_file():
        command += ['--path', str(ROOT / 'web_ui')]
        (folder / 'command.json').write_text(json.dumps(command, indent=2), encoding='utf-8')
    url = f'http://127.0.0.1:{args.port}'
    print(f'Modelo: {model.name}\nCargando con CUDA, sin DSpark...\nRegistros: {folder}', flush=True)
    process = None
    lifecycle = None
    try:
        if not args.keep_alive and (ROOT / 'web_ui' / 'index.html').is_file():
            lifecycle = ChatLifecycle(ROOT / 'web_ui', url)
        with (folder / 'server.log').open('w', encoding='utf-8') as log:
            process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT,
                                       creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            deadline = time.monotonic() + 180
            while True:
                if process.poll() is not None:
                    raise RuntimeError(f'El runtime terminó con código {process.returncode}. Revisa {folder / "server.log"}')
                try:
                    with urllib.request.urlopen(url + '/health', timeout=2) as response:
                        if json.load(response).get('status') == 'ok':
                            break
                except (OSError, urllib.error.URLError):
                    pass
                if time.monotonic() >= deadline:
                    raise TimeoutError('El modelo no estuvo listo en 180 segundos. Revisa server.log.')
                time.sleep(0.25)
            print(f'Chat listo: {url}\nThinking: {not args.no_thinking}; esfuerzo: {args.effort}; caché activada.', flush=True)
            print('Ctrl+C detiene el servidor. Al cerrar la última pestaña, se libera la GPU tras 8 segundos.' if lifecycle else 'Ctrl+C detiene el servidor y libera la GPU.', flush=True)
            if not args.no_browser:
                webbrowser.open(url + '/index.html?ui=thinking1' if (ROOT / 'web_ui' / 'index.html').is_file() else url)
            while process.poll() is None:
                if lifecycle and lifecycle.should_stop():
                    print('Se cerró la última pestaña. Liberando VRAM...', flush=True)
                    return 0
                time.sleep(0.5)
            return process.returncode
    except KeyboardInterrupt:
        print('\nCerrando el chat...', flush=True)
        return 0
    finally:
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=10)
        if lifecycle:
            lifecycle.close()
        print('Servidor detenido.', flush=True)


if __name__ == '__main__':
    raise SystemExit(main())
