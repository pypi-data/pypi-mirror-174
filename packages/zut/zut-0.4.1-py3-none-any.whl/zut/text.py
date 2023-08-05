from __future__ import annotations
import re, unicodedata

def slugen(value, separator='-') -> str:
    """ 
    Generate a slug.
    Simplier and more determinist than django.utils.text.slugify().
    """
    if value is None:
        return ""
    
    # Remove accents and other diacritic/non-ascii characters
    value = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode("ascii")

    # Lowercase the string
    value = value.lower()

    # Replace everything that is not a letter or digit by hyphens
    value = re.sub(r"[^a-z0-9]", "-", value)

    # Trim leading, trailing, and consecutive hyphens
    return re.sub(r"-+", separator, value).strip(separator)
