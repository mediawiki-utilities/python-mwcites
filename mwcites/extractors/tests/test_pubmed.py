from nose.tools import eq_

from .. import pubmed
from ...identifier import Identifier

def test_extract():

    text = """
    This is some text with a template cite. {{cite|...|...|pmid=1}}.
    This is some text with a template cite. {{cite|...|...|pmid = 2|...}}.
    This is some text with a template cite. {{cite|...|...|pmc = 3|...}}.
    This is some text with a template cite. {{cite|...|...|pmc = pmc4|...}}.
    This is some text with a link [http://www.ncbi.nlm.nih.gov/pubmed/5 ID]
    Another link [https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6 ID]
    """
    ids = list(pubmed.extract(text))
    expected = [
        Identifier('pmid', "1"),
        Identifier('pmid', "2"),
        Identifier('pmc', "3"),
        Identifier('pmc', "4"),
        Identifier('pmid', "5"),
        Identifier('pmc', "6")
    ]
    print(ids)
    print(expected)
    eq_(ids, expected)
