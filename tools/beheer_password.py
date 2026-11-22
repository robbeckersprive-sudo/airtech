"""Make the values for the Beheer login (paste them into Vercel → Settings → Environment Variables).

Usage:  python tools/beheer_password.py
Asks for the password without echoing it and prints AIRTECHNIC_BEHEER_PASSWORD_HASH and a fresh
AIRTECHNIC_BEHEER_SECRET. The password itself is never stored.
"""
import getpass
import os
import secrets
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
from beheer_auth import hash_password  # noqa: E402

first = getpass.getpass('Nieuw wachtwoord (min. 12 tekens): ')
if len(first) < 12 or first != getpass.getpass('Herhaal: '):
    sys.exit('Wachtwoorden verschillen of zijn korter dan 12 tekens.')
print('AIRTECHNIC_BEHEER_PASSWORD_HASH=' + hash_password(first))
print('AIRTECHNIC_BEHEER_SECRET=' + secrets.token_urlsafe(48))
