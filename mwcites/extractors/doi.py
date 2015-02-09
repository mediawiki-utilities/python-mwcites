import re
from collections import defaultdict

import mwparserfromhell as mwp
from more_itertools import peekable

from ..identifier import Identifier

DOI_RE = re.compile(r'\b(10\.\d+/[^\s\|\]\}\?\,]+)')

def extract_regex(text):
    for match in DOI_RE.finditer(text):
        id = re.sub(TAGS_RE, "", match.group(1)).rstrip(".")
        yield Identifier("doi", id)

DOI_START_RE = re.compile(r'10\.[0-9]{4,}/')

HTML_TAGS = ['ref', 'span', 'div', 'table', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
             'b', 'u', 'i', 's', 'ins', 'del', 'code', 'tt', 'blockquote',
             'pre']

TAGS_RE = re.compile(r'<(/\s*)?(' + '|'.join(HTML_TAGS) + ')(\s[^>\n\r]+)?>', re.I)


def extract_mwp(text):
    no_tags = mwp.parse(text).strip_code()
    for match in DOI_RE.finditer(no_tags):
        id = re.sub(TAGS_RE, "", match.group(1)).rstrip(".")
        yield Identifier("doi", id)

LEXICON = [
    (DOI_START_RE.pattern, 'doi_start'),
    (r'\(',                'open_paren'),
    (r'\)',                'close_paren'),
    (r'\[',                'open_bracket'),
    (r'\]',                'close_bracket'),
    (r'<!--',              'comment_start'),
    (r'-->',               'comment_end'),
    (TAGS_RE.pattern,      'tag'),
    (r'<',                 'open_angle'),
    (r'>',                 'close_angle'),
    (r'\{',                'open_curly'),
    (r'\}',                'close_curly'),
    (r'\|',                'pipe'),
    (r'[,\.;!]',           'punct'),
    (r'[\?#]',             'url_end'),
    (r'[\n\r]+',           'break'),
    (r'\s+',               'whitespace'),
    (r'\w+',               'word'),
    (r'.',                 'etc')
]

def extract_island(text):
    tokens = tokenize_finditer(text, LEXICON)
    tokens = peekable(tokens)
    
    while tokens.peek(None) is not None:
        
        if tokens.peek()[0] == 'doi_start':
            yield ('doi', read_doi(tokens))
        
        next(tokens)


def tokenize_finditer(text, lexicon=LEXICON):
    pattern = '|'.join("(?P<{0}>{1})".format(name, pattern)
                       for pattern, name in lexicon)
    
    group_regex = re.compile(pattern, re.I|re.U|re.M)
    
    for match in group_regex.finditer(text):
        yield match.lastgroup, match.group(0)


"""
def tokenize_scanner(text, lexicon=LEXICON):
    scanner = re.Scanner(lexicon)
    tokens, remainder = scanner.scan(text)
    return tokens
"""

#from mwcites.extractors.doi import tokenize_scan
#list(tokenize_scan("foo bar baz.{}"))

def read_doi(tokens):
    assert tokens.peek()[0] == 'doi_start'
    
    depth = defaultdict(lambda: 0)
    
    doi_buffer = [next(tokens)[1]]
    
    while tokens.peek(None) is not None:
        name, match = tokens.peek()
        
        if name in ('url_end', 'break', 'whitespace', 'tag', 'pipe',
                    'comment_start', 'comment_end'):
            break
        elif name == 'open_bracket':
            depth['bracket'] += 1
            doi_buffer.append(next(tokens)[1])
        elif name == 'open_curly':
            depth['curly'] += 1
            doi_buffer.append(next(tokens)[1])
        elif name == 'close_bracket':
            if depth['bracket'] > 0:
                depth['bracket'] -= 1
                doi_buffer.append(next(tokens)[1])
            else:
                break
        elif name == 'close_curly':
            if depth['curly'] > 0:
                depth['curly'] -= 1
                doi_buffer.append(next(tokens)[1])
            else:
                break
        else:
            doi_buffer.append(next(tokens)[1])
        
    
    # Do not return a doi with punctuation at the end
    return re.sub(r'[\.,!]+$', '', ''.join(doi_buffer))



def tokenize_search(text, start, lexicon=LEXICON):
    pattern = '|'.join("(?P<{0}>{1})".format(name, pattern)
                       for pattern, name in lexicon)
    
    group_regex = re.compile(pattern, re.I|re.U)
    
    match = group_regex.search(text, start)
    while match is not None:
        yield match.lastgroup, match.group(0)
        match = group_regex.search(text, match.span()[1])

def extract_search(text, lexicon=LEXICON):
    
    last_end = 0
    for match in DOI_START_RE.finditer(text):
        if match.span()[0] > last_end:
            tokens = tokenize_search(text, match.span()[0], lexicon=lexicon)
            tokens = peekable(tokens)
            doi = read_doi(tokens)
            last_end = match.span()[0] + len(doi)
            yield Identifier('doi', doi)
        else:
            last_end = max(match.span()[1], last_end)

extract = extract_search # Setting the default to the best method
