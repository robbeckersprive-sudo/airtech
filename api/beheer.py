"""Same-origin Vercel endpoint for the owner login (Beheer / kiosk mode). Logic: src/beheer_auth.py."""
import json
from http.server import BaseHTTPRequestHandler
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from beheer_auth import MAX_BODY, LoginRateLimit, handle


class handler(BaseHTTPRequestHandler):
    # Best-effort per-instance limit; add a Vercel Firewall rule for POST /api/beheer for a shared one.
    limit = LoginRateLimit()

    def respond(self, status, body, cookie=None):
        data = json.dumps(body).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        if cookie:
            self.send_header('Set-Cookie', cookie)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self.respond(405, {'ok': False, 'code': 'method_not_allowed'})

    def do_POST(self):
        origin = self.headers.get('Origin')
        host = self.headers.get('Host')
        if origin and origin != f'https://{host}':
            return self.respond(403, {'ok': False, 'code': 'forbidden'})
        if self.headers.get_content_type() != 'application/json':
            return self.respond(415, {'ok': False, 'code': 'invalid'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
        except ValueError:
            return self.respond(400, {'ok': False, 'code': 'invalid'})
        if not 0 <= length <= MAX_BODY:
            return self.respond(413, {'ok': False, 'code': 'invalid'})
        raw = self.rfile.read(length) if length else b''
        address = self.headers.get('x-vercel-forwarded-for') or self.client_address[0]
        status, body, cookie = handle(raw, self.headers.get('Cookie'), address, self.limit)
        self.respond(status, body, cookie)

    def log_message(self, *_args):
        pass
