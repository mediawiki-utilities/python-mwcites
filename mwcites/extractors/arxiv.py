import re

from ..identifier import Identifier

# From http://arxiv.org/help/arxiv_identifier
old_id = r"-?(?P<old_id>([a-z]+(.[a-z]+)/)?[0-9]{4}[0-9]+)"
new_id = r"(?P<new_id>[0-9]{4}.[0-9]+)(v[0-9]+)?"

prefixes=["arxiv\s*=\s*", "//arxiv\.org/(abs/)?", "arxiv:\s?"]

ARXIV_RE = re.compile(r"({0})".format("|".join(prefixes)) +
                      r"({0}|{1})".format(old_id, new_id), re.I|re.U)

def extract(text):
    for match in ARXIV_RE.finditer(text):
        id = match.group('new_id') or match.group("old_id")
        yield Identifier("arxiv", id.lower())
