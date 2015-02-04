import re

import mwparserfromhell as mwp

DOI_RE = re.compile(r'\b(10\.\d+/[^\s\|\]\}]+)', re.I)

TAGS_RE = re.compile(r'</?\s*(ref|span|div|table|h[1-6]|b|ins|del)\b[^>\n\r]*>', re.I)

def extract(text):
    for match in DOI_RE.finditer(text):
        id = re.sub(TAGS_RE, "", match.group(1))
        yield ("doi", id)


def extract_mwp(text):
    no_tags = mwp.parse(text).strip_code()
    for match in DOI_RE.finditer(no_tags):
        yield ("doi", id)
