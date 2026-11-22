"""Owner login for the "Beheer" environment (kiosk mode). Shared by api/beheer.py (Vercel) and src/serve.py (local).

One owner account, configured only through environment variables:
  AIRTECHNIC_BEHEER_EMAIL          login e-mail address
  AIRTECHNIC_BEHEER_PASSWORD_HASH  pbkdf2_sha256$<iterations>$<salt b64>$<hash b64>  (make one: python tools/beheer_password.py)
  AIRTECHNIC_BEHEER_SECRET         at least 32 random characters; signs the session cookie

The session is a signed, expiring token in an HttpOnly cookie. Without configuration every login fails with
'not_configured' (never a silent success). Requests are JSON: {"action": "login"|"logout"|"status", ...}.
"""
import base64
import hashlib
import hmac
import json
import os
import threading
import time

COOKIE = 'at_beheer'
MAX_BODY = 2048
SESSION_SHORT = 12 * 3600          # one fair day
SESSION_LONG = 30 * 24 * 3600      # "remember this device" (kiosk PC at the stand)


def _b64(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')


def _unb64(text):
    return base64.urlsafe_b64decode(text + '=' * (-len(text) % 4))


def hash_password(password, iterations=600_000, salt=None):
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations)
    return f'pbkdf2_sha256${iterations}${_b64(salt)}${_b64(digest)}'


def verify_password(password, stored):
    try:
        algo, iterations, salt, digest = stored.split('$')
        if algo != 'pbkdf2_sha256':
            return False
        test = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), _unb64(salt), int(iterations))
        return hmac.compare_digest(test, _unb64(digest))
    except (ValueError, TypeError):
        return False


def _config():
    email = os.environ.get('AIRTECHNIC_BEHEER_EMAIL', '').strip().lower()
    stored = os.environ.get('AIRTECHNIC_BEHEER_PASSWORD_HASH', '').strip()
    secret = os.environ.get('AIRTECHNIC_BEHEER_SECRET', '')
    if not email or not stored or len(secret) < 32:
        return None
    return email, stored, secret.encode('utf-8')


def make_token(email, ttl, secret, now=None):
    payload = _b64(json.dumps({'e': email, 'x': int((now or time.time()) + ttl)}, separators=(',', ':')).encode())
    sig = _b64(hmac.new(secret, payload.encode('ascii'), hashlib.sha256).digest())
    return f'{payload}.{sig}'


def read_token(token, secret, now=None):
    try:
        payload, sig = token.split('.')
        good = _b64(hmac.new(secret, payload.encode('ascii'), hashlib.sha256).digest())
        if not hmac.compare_digest(sig, good):
            return None
        data = json.loads(_unb64(payload))
        if data['x'] < (now or time.time()):
            return None
        return data
    except (ValueError, KeyError, TypeError):
        return None


def cookie_value(header):
    for part in (header or '').split(';'):
        name, _, value = part.strip().partition('=')
        if name == COOKIE:
            return value
    return ''


def set_cookie(token, ttl, secure=True):
    flags = '; Secure' if secure else ''
    return f'{COOKIE}={token}; Max-Age={ttl}; Path=/; HttpOnly; SameSite=Strict{flags}'


def clear_cookie(secure=True):
    flags = '; Secure' if secure else ''
    return f'{COOKIE}=; Max-Age=0; Path=/; HttpOnly; SameSite=Strict{flags}'


class LoginRateLimit:
    """Per-instance brake: 5 failed attempts per address per 15 minutes."""

    def __init__(self, limit=5, window=900):
        self.limit, self.window, self.lock, self.fails = limit, window, threading.Lock(), {}

    def blocked(self, address):
        now = time.time()
        with self.lock:
            hits = [t for t in self.fails.get(address, []) if now - t < self.window]
            self.fails[address] = hits
            return len(hits) >= self.limit

    def fail(self, address):
        with self.lock:
            self.fails.setdefault(address, []).append(time.time())

    def reset(self, address):
        with self.lock:
            self.fails.pop(address, None)


def handle(raw, cookie_header, address, limit, secure=True):
    """Returns (status, body dict, Set-Cookie header or None)."""
    try:
        data = json.loads(raw.decode('utf-8')) if raw else {}
        if not isinstance(data, dict):
            raise ValueError
    except (ValueError, UnicodeDecodeError):
        return 400, {'ok': False, 'code': 'invalid'}, None
    action = data.get('action', 'status')
    cfg = _config()
    if action == 'logout':
        return 200, {'ok': True, 'code': 'logged_out'}, clear_cookie(secure)
    if cfg is None:
        return 503, {'ok': False, 'code': 'not_configured'}, None
    email, stored, secret = cfg
    if action == 'status':
        session = read_token(cookie_value(cookie_header), secret)
        if not session:
            return 401, {'ok': False, 'code': 'no_session'}, None
        return 200, {'ok': True, 'code': 'session', 'email': session['e'], 'expires': session['x']}, None
    if action != 'login':
        return 400, {'ok': False, 'code': 'invalid'}, None
    if limit.blocked(address):
        return 429, {'ok': False, 'code': 'too_many'}, None
    given = str(data.get('email', ''))[:200].strip().lower()
    password = str(data.get('password', ''))[:200]
    good_mail = hmac.compare_digest(given.encode(), email.encode())
    good_pass = verify_password(password, stored)          # always computed: no timing hint about the e-mail
    if not (good_mail and good_pass):
        limit.fail(address)
        return 401, {'ok': False, 'code': 'wrong'}, None
    limit.reset(address)
    ttl = SESSION_LONG if data.get('remember') else SESSION_SHORT
    token = make_token(email, ttl, secret)
    return 200, {'ok': True, 'code': 'session', 'email': email, 'expires': int(time.time() + ttl)}, set_cookie(token, ttl, secure)
