import re
from ..identifier import Identifier

ISBN_RE = re.compile('isbn\s?=?\s?([0-9\-Xx]+)', re.I)

def extract(text):
    for match in ISBN_RE.finditer(text):
        yield Identifier('isbn', match.group(1).replace('-', ''))
