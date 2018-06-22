import re
from ..identifier import Identifier

ISSN_RE = re.compile('issn\s?=?\s?([0-9]{4}\-[0-9]{3}([0-9]|X))', re.I)

def extract(text):
    for match in ISSN_RE.finditer(text):
        yield Identifier(
            'issn',
            match.group(1).replace('-', '').replace(' ', '').strip()
        )
