import re
from ..identifier import Identifier

# Also correctly parses malformed inputs such as below:
# isbn=2 906700-09-6 (malformed input — notice the space)
ISBN_RE = re.compile('isbn\s?=?\s?(([0-9]+\s)?([0-9\-Xx]+))', re.I)

def extract(text):
    for match in ISBN_RE.finditer(text):
        yield Identifier(
            'isbn',
            match.group(1).replace('-', '').replace(' ', '')
        )
