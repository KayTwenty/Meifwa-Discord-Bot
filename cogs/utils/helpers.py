from math import floor, log10
import re
import aiohttp
import base64
from urllib.parse import urlencode

invite_re = re.compile("discord(?:app\.com|\.gg)[\/invite\/]?(?:(?!.*[Ii10OolL]).[a-zA-Z0-9]{5,6}|[a-zA-Z0-9\-]{2,32})")

def clean_text(text: str):
    return invite_re.sub("[INVITE]", text.replace("@", "@\u200B"))



