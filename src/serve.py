"""Minimal static server that reads files whole (D: drive rejects os.fstat on open handles)."""
import json
import mimetypes
import os
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from contact_delivery import CONTACT_PATH, MAX_BODY, ContactRateLimit, receive_contact
from beheer_auth import MAX_BODY as BEHEER_MAX, LoginRateLimit, handle as beheer_handle

ROOT = os.path.abspath(sys.argv[1])
PORT = int(sys.argv[2])
# Local test login for Beheer (kiosk mode): KEY=value lines from the gitignored .env.beheer, never in production.
if os.path.isfile(os.path.join(ROOT, '.env.beheer')):
    for _line in open(os.path.join(ROOT, '.env.beheer'), encoding='utf-8'):
        _k, _sep, _val = _line.strip().partition('=')
        if _sep and not _k.startswith('#'):
            os.environ.setdefault(_k, _val)
mimetypes.add_type('image/avif', '.avif')
mimetypes.add_type('image/webp', '.webp')
mimetypes.add_type('font/woff2', '.woff2')
mimetypes.add_type('text/javascript', '.js')


class H(BaseHTTPRequestHandler):
    contact_limit = ContactRateLimit()

    def send_contact_status(self, status, code):
        body = json.dumps({'ok': status == 200, 'code': code}).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    beheer_limit = LoginRateLimit()

    def do_beheer(self):
        """Local twin of api/beheer.py (owner login for kiosk mode). Cookie without Secure: plain http on localhost."""
        origin = self.headers.get('Origin')
        if origin and origin not in (f'https://{self.headers.get("Host")}', f'http://{self.headers.get("Host")}'):
            status, body, cookie = 403, {'ok': False, 'code': 'forbidden'}, None
        else:
            length = int(self.headers.get('Content-Length', '0') or 0)
            raw = self.rfile.read(min(length, BEHEER_MAX)) if length else b''
            status, body, cookie = beheer_handle(raw, self.headers.get('Cookie'), self.client_address[0], self.beheer_limit, secure=False)
        data = json.dumps(body).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        if cookie:
            self.send_header('Set-Cookie', cookie)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if urllib.parse.urlsplit(self.path).path == '/api/beheer':
            return self.do_beheer()
        if urllib.parse.urlsplit(self.path).path != '/' + CONTACT_PATH:
            return self.send_contact_status(404, 'not_found')
        origin = self.headers.get('Origin')
        expected_host = self.headers.get('Host')
        if origin and origin not in (f'https://{expected_host}', f'http://{expected_host}'):
            return self.send_contact_status(403, 'forbidden')
        if self.headers.get_content_type() != 'application/json':
            return self.send_contact_status(415, 'invalid')
        try:
            length = int(self.headers.get('Content-Length', '0'))
        except ValueError:
            return self.send_contact_status(400, 'invalid')
        if not 0 < length <= MAX_BODY:
            return self.send_contact_status(413, 'invalid')
        self.connection.settimeout(10)
        try:
            raw = self.rfile.read(length)
        except TimeoutError:
            return self.send_contact_status(408, 'invalid')
        status, code = receive_contact(raw, self.client_address[0], self.contact_limit)
        self.send_contact_status(status, code)

    def do_GET(self):
        path = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path).lstrip('/') or 'index.html'
        full = os.path.normpath(os.path.join(ROOT, path))
        if not full.startswith(ROOT + os.sep) or not os.path.isfile(full):
            self.send_response(404); self.end_headers(); return
        with open(full, 'rb') as f:
            data = f.read()
        self.send_response(200)
        self.send_header('Content-Type', mimetypes.guess_type(full)[0] or 'application/octet-stream')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        sys.stdout.write('%s\n' % (fmt % args)); sys.stdout.flush()


ThreadingHTTPServer.request_queue_size = 64   # the kiosk loads many images at once; the default 5 refuses connections
ThreadingHTTPServer(('127.0.0.1', PORT), H).serve_forever()
