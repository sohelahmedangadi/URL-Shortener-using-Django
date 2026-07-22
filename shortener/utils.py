import random
import re
import string

SHORT_CODE_ALPHABET = string.ascii_letters + string.digits
SHORT_CODE_LENGTH = 7

# Reserved words that can't be used as custom aliases because they collide
# with other URL routes in this project.
RESERVED_CODES = {
    "admin", "login", "logout", "signup", "register", "dashboard",
    "static", "accounts", "shorten", "api", "stats",
}

ALIAS_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")


def generate_short_code(length=SHORT_CODE_LENGTH):
    """Generate a random unique short code, avoiding collisions in the DB."""
    from .models import ShortURL

    while True:
        code = "".join(random.choices(SHORT_CODE_ALPHABET, k=length))
        if not ShortURL.objects.filter(short_code=code).exists():
            return code


def validate_custom_alias(alias):
    """Return an error message string if the alias is invalid, else None."""
    from .models import ShortURL

    if not alias:
        return None
    if len(alias) < 3 or len(alias) > 20:
        return "Custom alias must be between 3 and 20 characters."
    if not ALIAS_PATTERN.match(alias):
        return "Custom alias can only contain letters, numbers, hyphens, and underscores."
    if alias.lower() in RESERVED_CODES:
        return "That alias is reserved. Please choose another."
    if ShortURL.objects.filter(short_code__iexact=alias).exists():
        return "That alias is already taken."
    return None
