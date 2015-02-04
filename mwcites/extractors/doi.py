import re

import mwparserfromhell as mwp
from more_itertools import peekable

DOI_RE = re.compile(r'\b(10\.\d+/[^\s\|\]\}\?\,]+)', re.I)

TAGS_RE = re.compile(r'</?\s*(ref|span|div|table|h[1-6]|b|ins|del)\b[^>\n\r]*>', re.I)


def extract(text):
    for match in DOI_RE.finditer(text):
        id = re.sub(TAGS_RE, "", match.group(1)).rstrip(".")
        yield ("doi", id)


def extract_mwp(text):
    no_tags = mwp.parse(text).strip_code()
    for match in DOI_RE.finditer(no_tags):
        yield ("doi", id)


SYMBOLS = (
    ('doi_start',     re.compile(r'([0-9]{2})\.[0-9]{4,}(\.[0-9]+)*/?')),
    ('(',             re.compile(r'\(')),
    (')',             re.compile(r'\)')),
    ('[',             re.compile(r'\[')),
    (']',             re.compile(r'\]')),
    ('>',             re.compile(r'>')),
    ('<',             re.compile(r'<')),
    ('{',             re.compile(r'{')),
    ('}',             re.compile(r'}')),
    ('punct',         re.compile(r'[,\.;]')),
    ('url_end',       re.compile(r'[\?#]')),
    ('break',         re.compile(r'[\n\r]+')),
    ('whitespace',    re.compile(r'\s+')),
    ('word',          re.compile(r'\w+')),
    ('etc',           re.compile(r'.'))
)

def extract_island(text):
    tokens = tokenize(text, SYMBOLS)
    tokens = peekable(tokens)
    
    while tokens.peek(None) is not None:
        
        if tokens.peek()[0] == 'doi_start':
            yield read_doi(tokens)

def tokenize(text, symbols):
    _, regexes = zip(*symbols)
    patterns = (r.pattern for r in regexes)
    group_regex = re.compile('|'.join("({0})".format(pattern) for pattern in patterns), re.I|re.U)
    for match in group_regex.finditer(text):
        for name, regex in symbols:
            if regex.match(match.group(0)):
                yield name, match.group(0)
                break


def read_doi(tokens):
    assert tokens.peek()[0] = 'doi_start'
    
    depth = defaultdict(lambda: 0)
    
    doi = next(tokens)[1]
    
    while tokens.peek(None) is not None:
        pass #TODO!
