from nose.tools import eq_

from .. import pubmed


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
        ('pmid', "1"),
        ('pmid', "2"),
        ('pmc', "3"),
        ('pmc', "4"),
        ('pmid', "5"),
        ('pmc', "6")
    ]
    print(ids)
    print(expected)
    eq_(ids, expected)
