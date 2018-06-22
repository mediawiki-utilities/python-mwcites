import pprint
from nose.tools import eq_

from .. import issn
from ...identifier import Identifier

INPUT_TEXT = """
 {{cite book|work=Billboard|title=Sinatra FBI Files Opened|first=Bill|last=Holland|url=https://books.google.com/books?id=KQoEAAAAMBAJ&dq=Bill+Holland+1998+Billboard+page+10&q=walter+winchell#v=snippet&q=walter%20winchell&f=false|date=December 19, 1998|page=10|issn=0006-2510}}
    """


EXPECTED = [
    Identifier('issn', '00062510'),
]

def test_extract():
    ids = list(issn.extract(INPUT_TEXT))
    pprint.pprint(ids)
    pprint.pprint(EXPECTED)
    eq_(ids, EXPECTED)
