import re
from ..identifier import Identifier

# Also correctly parses malformed inputs such as below:
# isbn=2 906700-09-6 (notice the space instead of a hyphen) or
# isbn=2 10 004179 7 (notice spaces instead of hyphens)
ISBN_RE = re.compile('isbn\s?=?\s?([\d]+([\d\s\-]+)[\dXx])', re.I)


def extract(text):
    for match in ISBN_RE.finditer(text):
        yield Identifier(
            'isbn',
            match.group(1).replace('-', '').replace(' ', '').strip()
        )
