import secrets
import base64

def gen_token(bytes=32):
    """Generate a cryptographically secure random token.
    """
    return secrets.token_hex(bytes)

def pretty_date(date):
    """Display a datetime object in an easy to read string.

    Registered as a Jinja2 global in UI.
    """
    return date.strftime('%d/%m/%Y %H:%M:%S')

def b64encode(string):
    """Base64 encode a string, returning a string.
    """
    return base64.b64encode(string.encode()).decode()
