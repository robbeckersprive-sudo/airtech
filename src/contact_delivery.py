from email.errors import HeaderParseError
from email.headerregistry import Address
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
import json
import os
import re
import smtplib
import ssl
from threading import Lock
from time import monotonic


RECIPIENT = 'info@airtechnicsolutions.com'
CONTACT_PATH = 'api/contact'
MAX_BODY = 32768
FIELD_LIMITS = {'naam': 120, 'email': 254, 'bedrijf': 160, 'telefoon': 60, 'vraagstuk': 4000}
REQUIRED_FIELDS = {'naam', 'email', 'vraagstuk'}

CONTACT_TOPICS = {
    'algemeen': ('Algemene vraag', 'Vertel ons waar u hulp bij zoekt. Een korte toelichting is genoeg.'),
    'installatieontwerp': ('Ontwerp van een installatie', 'Welk proces wilt u inrichten of verbeteren? Noem het materiaal en de gewenste capaciteit als u die al weet.'),
    'druk-of-vacuumtransport': ('Druk- of vacuümtransport', 'Welk product wilt u transporteren? Vermeld indien bekend de capaciteit en transportafstand.'),
    'cyclonen': ('Cyclonen en afscheiders', 'Beschrijf wat u uit de luchtstroom wilt afscheiden. Vermeld indien bekend het luchtdebiet en de gewenste afscheiding.'),
    'multicycloon': ('Multicycloon', 'Noem het te scheiden materiaal, het luchtdebiet en de beschikbare inbouwruimte, voor zover bekend.'),
    'cycloon-maatwerk': ('Cycloon op maat', 'Beschrijf uw installatie en wat maatwerk nodig maakt, bijvoorbeeld de inbouwruimte, aansluitingen of materiaalkeuze.'),
    'transportafscheider': ('Transportafscheider', 'Vertel ons welk materiaal u transporteert en hoe het na de afscheider moet worden opgevangen of afgevoerd.'),
    'cycloonafscheider': ('Advies cycloonafscheider', 'Noem het te scheiden materiaal, het luchtdebiet en het resultaat dat u wilt bereiken, voor zover bekend.'),
    'cycloon-documentatie': ('Documentatie cycloon', 'Welke informatie zoekt u? Denk aan inbouwmaten, aansluitingen, materialen of procescondities.'),
}


# Keep selectable category enquiries aligned with the catalogue content.
from category_data import CATEGORIES
for _slug, _category in CATEGORIES.items():
    CONTACT_TOPICS[_slug] = (_category['name'], _category['request'])
    for _option in _category['items']:
        CONTACT_TOPICS[_slug + '-' + _option['variant']] = (
            _category['name'] + ' · ' + _option['name'], _category['request'])


from product_routes import PRODUCT_ROUTES
from solution_data import SOLUTIONS
for _solution in SOLUTIONS.values():
    CONTACT_TOPICS[_solution['topic']] = (_solution['name'], _solution['request'])

for _category_slug, _routes in PRODUCT_ROUTES.items():
    for _variant, _product_slug in _routes.items():
        _base = CONTACT_TOPICS.get(_category_slug + '-' + _variant,
                                  (_product_slug.replace('-', ' ').capitalize(), 'Beschrijf uw product, proces en gewenste uitvoering.'))
        CONTACT_TOPICS.setdefault(_product_slug, _base)
        CONTACT_TOPICS[_product_slug + '-documentatie'] = (
            'Documentatie · ' + _base[0], 'Welke informatie zoekt u over deze uitvoering? Denk aan maten, aansluitingen, materialen of procescondities.')


def validate(payload):
    if not isinstance(payload, dict):
        raise ValueError('invalid')
    topic = payload.get('onderwerp')
    if not isinstance(topic, str) or topic not in CONTACT_TOPICS:
        raise ValueError('invalid_topic')
    data = {}
    for key, limit in FIELD_LIMITS.items():
        value = payload.get(key, '')
        if not isinstance(value, str):
            raise ValueError(key)
        value = value.strip()
        if len(value) > limit or (key in REQUIRED_FIELDS and not value):
            raise ValueError(key)
        if key != 'vraagstuk' and any(ch in value for ch in '\r\n'):
            raise ValueError(key)
        if any(ord(ch) < 32 and ch not in '\r\n\t' for ch in value):
            raise ValueError(key)
        data[key] = value
    if not data['email'].isascii() or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', data['email']):
        raise ValueError('email')
    try:
        Address(addr_spec=data['email'])
    except (ValueError, HeaderParseError):
        raise ValueError('email') from None
    return topic, data


class ContactRateLimit:
    def __init__(self):
        self.attempts = []
        self.lock = Lock()

    def allow(self, address):
        now = monotonic()
        with self.lock:
            self.attempts[:] = [item for item in self.attempts if now - item[0] < 600]
            if len(self.attempts) >= 50 or sum(ip == address for _, ip in self.attempts) >= 6:
                return False
            self.attempts.append((now, address))
            return True


def send_contact(topic, data):
    host = os.environ['AIRTECHNIC_SMTP_HOST']
    username = os.environ['AIRTECHNIC_SMTP_USERNAME']
    password = os.environ['AIRTECHNIC_SMTP_PASSWORD']
    sender = os.environ.get('AIRTECHNIC_SMTP_FROM', username)
    security = os.environ.get('AIRTECHNIC_SMTP_SECURITY', 'smtps')
    port = int(os.environ.get('AIRTECHNIC_SMTP_PORT', '465' if security == 'smtps' else '587'))
    if not all((host, username, password, sender)) or security not in {'smtps', 'starttls'}:
        raise ValueError('invalid SMTP configuration')

    subject = CONTACT_TOPICS[topic][0]
    message = EmailMessage()
    message['From'] = Address(display_name='Airtechnic Solutions website', addr_spec=sender)
    message['To'] = RECIPIENT
    message['Date'] = formatdate(usegmt=True)
    message['Message-ID'] = make_msgid(domain=sender.rsplit('@', 1)[-1])
    message['Reply-To'] = Address(addr_spec=data['email'])
    message['Subject'] = f'Websiteaanvraag: {subject}'
    body = [f'Onderwerp: {subject}', f'Naam: {data["naam"]}', f'E-mailadres: {data["email"]}']
    for key, label in (('bedrijf', 'Bedrijf'), ('telefoon', 'Telefoon')):
        if data[key]:
            body.append(f'{label}: {data[key]}')
    message.set_content('\n'.join((*body, '', data['vraagstuk'])), cte='quoted-printable')

    tls = ssl.create_default_context()
    client = (
        smtplib.SMTP_SSL(host, port, timeout=10, context=tls)
        if security == 'smtps' else smtplib.SMTP(host, port, timeout=10)
    )
    try:
        if security == 'starttls':
            client.starttls(context=tls)
        client.login(username, password)
        refused = client.send_message(message, from_addr=sender, to_addrs=[RECIPIENT])
        if refused:
            raise smtplib.SMTPRecipientsRefused(refused)
    finally:
        client.close()


def receive_contact(raw, address, rate_limit):
    try:
        payload = json.loads(raw)
        topic, data = validate(payload)
    except (ValueError, UnicodeError, RecursionError):
        return 400, 'invalid'
    if payload.get('website'):
        return 400, 'invalid'
    if not rate_limit.allow(address):
        return 429, 'rate_limited'
    try:
        send_contact(topic, data)
    except (KeyError, OSError, ValueError, smtplib.SMTPException):
        # Keep personal data, credentials and SMTP responses out of HTTP responses and logs.
        return 503, 'unavailable'
    return 200, 'sent'
