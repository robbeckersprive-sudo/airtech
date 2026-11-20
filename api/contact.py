"""Same-origin Vercel endpoint for the existing contact form."""
import json
from http.server import BaseHTTPRequestHandler
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from contact_delivery import MAX_BODY, ContactRateLimit, receive_contact


class handler(BaseHTTPRequestHandler):
    # Best-effort per-instance limit; configure shared throttling in Vercel WAF.
    contact_limit = ContactRateLimit()

    def respond(self, status, code):
        body = json.dumps({'ok': status == 200, 'code': code}).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self.respond(405, 'method_not_allowed')

    def do_POST(self):
        origin = self.headers.get('Origin')
        host = self.headers.get('Host')
        if origin and origin != f'https://{host}':
            return self.respond(403, 'forbidden')
        if self.headers.get_content_type() != 'application/json':
            return self.respond(415, 'invalid')
        try:
            length = int(self.headers.get('Content-Length', '0'))
        except ValueError:
            return self.respond(400, 'invalid')
        if not 0 < length <= MAX_BODY:
            return self.respond(413, 'invalid')
        raw = self.rfile.read(length)
        if len(raw) != length:
            return self.respond(400, 'invalid')
        address = self.headers.get('x-vercel-forwarded-for') or self.client_address[0]
        status, code = receive_contact(raw, address, self.contact_limit)
        self.respond(status, code)

    def log_message(self, *_args):
        pass
