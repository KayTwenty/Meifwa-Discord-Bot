import re

url_rx = re.compile(r'https?://(?:www\.)?.+')
track_title_rx = re.compile(r"\([^()]*\)")