"""Track browser tabs so closing the last one releases the local model."""
import json
import re
import secrets
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, parse_qs


class ChatLifecycle:
    def __init__(self, ui_dir, origin, context=8192, settings_path=None):
        self.tabs = {}
        self.last_seen = time.monotonic()
        self.connected = False
        self.lock = threading.Lock()
        self.stopping = threading.Event()
        token = secrets.token_urlsafe(32)
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                # Una conexión abierta por pestaña permite detectar el cierre aun sin pagehide.
                query = parse_qs(urlsplit(self.path).query)
                tab = query.get('id', [''])[0]
                if (urlsplit(self.path).path != '/events' or self.headers.get('Origin') != origin
                        or query.get('token') != [token] or not 0 < len(tab) <= 64):
                    self.send_error(400)
                    return
                connection = secrets.token_hex(8)
                with owner.lock:
                    owner.connected = True
                    owner.last_seen = time.monotonic()
                    owner.tabs[tab] = (owner.last_seen, connection)
                try:
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/event-stream')
                    self.send_header('Cache-Control', 'no-store')
                    self.send_header('Access-Control-Allow-Origin', origin)
                    self.end_headers()
                    while not owner.stopping.is_set():
                        with owner.lock:
                            if owner.tabs.get(tab, (None, None))[1] != connection:
                                break
                        self.wfile.write(b'data: alive\n\n')
                        self.wfile.flush()
                        with owner.lock:
                            if owner.tabs.get(tab, (None, None))[1] == connection:
                                owner.tabs[tab] = (time.monotonic(), connection)
                        owner.stopping.wait(1)
                except OSError:
                    pass  # El navegador cerró la conexión.
                finally:
                    with owner.lock:
                        if owner.tabs.get(tab, (None, None))[1] == connection:
                            owner.tabs.pop(tab, None)
                            owner.last_seen = time.monotonic()

            def do_POST(self):
                try:
                    length = int(self.headers.get('Content-Length', '0'))
                    if self.headers.get('Origin') != origin or not 0 < length <= 1024:
                        raise ValueError('Invalid request')
                    data = json.loads(self.rfile.read(length))
                    if data.get('token') != token or not isinstance(data.get('id'), str) or len(data['id']) > 64:
                        raise ValueError('Invalid token or tab')
                    if data.get('event') == 'context':
                        with owner.lock:
                            if 'context' in data:
                                value = data['context']
                                if type(value) is not int or not 2048 <= value <= 262144 or settings_path is None:
                                    raise ValueError('Invalid context')
                                settings_path.parent.mkdir(parents=True, exist_ok=True)
                                temporary = settings_path.with_suffix('.tmp')
                                temporary.write_text(json.dumps({'context': value}), encoding='utf-8')
                                temporary.replace(settings_path)
                            saved = json.loads(settings_path.read_text(encoding='utf-8'))['context'] if settings_path and settings_path.exists() else context
                        payload = json.dumps({'active': context, 'saved': saved}).encode()
                        self.send_response(200)
                        self.send_header('Access-Control-Allow-Origin', origin)
                        self.send_header('Content-Type', 'application/json')
                        self.send_header('Content-Length', str(len(payload)))
                        self.end_headers()
                        self.wfile.write(payload)
                        return
                    if data.get('event') not in ('alive', 'close'):
                        raise ValueError('Invalid event')
                    with owner.lock:
                        owner.connected = True
                        owner.last_seen = time.monotonic()
                        if data['event'] == 'close':
                            owner.tabs.pop(data['id'], None)
                        else:
                            owner.tabs[data['id']] = (owner.last_seen, None)
                    self.send_response(204)
                    self.send_header('Access-Control-Allow-Origin', origin)
                    self.end_headers()
                except (ValueError, TypeError, AttributeError):
                    self.send_error(400)
                except OSError:
                    self.send_error(500, 'No se pudo guardar el contexto')

            def log_message(self, *_):
                pass

        self.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        config = dict(url=f'http://127.0.0.1:{self.server.server_port}/', token=token)
        script = '''(() => {
          const config = CONFIG;
          window.bonsaiSession = config;
          let stream, id;
          const start = () => {
            if (stream) return;
            id = crypto.randomUUID();
            stream = new EventSource(config.url+'events?'+new URLSearchParams({token:config.token,id}));
          };
          start();
          addEventListener('pagehide',()=>{
            if (stream) stream.close();
            stream = null;
            navigator.sendBeacon(config.url, JSON.stringify({token:config.token,id,event:'close'}));
          });
          addEventListener('pageshow',start);
        })();'''.replace('CONFIG', json.dumps(config))
        (ui_dir / 'chat-session.js').write_text(script, encoding='utf-8')
        index = ui_dir / 'index.html'
        html = index.read_text(encoding='utf-8-sig')
        html = re.sub(r'<script src="/chat-session\.js[^\"]*"></script>', '', html)
        html = html.replace('<head>', f'<head><script src="/chat-session.js?v={secrets.token_hex(8)}"></script>', 1)
        index.write_text(html, encoding='utf-8')

    def should_stop(self, now=None):
        now = time.monotonic() if now is None else now
        with self.lock:
            self.tabs = {key:seen for key,seen in self.tabs.items() if now-seen[0] < 180}
            # Reloads get 8 seconds; a browser crash eventually expires its heartbeat.
            return self.connected and not self.tabs and now-self.last_seen >= 8

    def close(self):
        self.stopping.set()
        self.server.shutdown()
        self.server.server_close()
