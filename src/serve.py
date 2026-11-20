"""Minimal static server that reads files whole (D: drive rejects os.fstat on open handles)."""
import json
import mimetypes
import os
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from contact_delivery import CONTACT_PATH, MAX_BODY, ContactRateLimit, receive_contact

ROOT = os.path.abspath(sys.argv[1])
PORT = int(sys.argv[2])
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

    def do_POST(self):
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


ThreadingHTTPServer(('127.0.0.1', PORT), H).serve_forever()
