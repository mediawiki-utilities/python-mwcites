import pprint

from nose.tools import eq_

from .. import doi
from ...identifier import Identifier

INPUT_TEXT = """
This is a doi randomly placed in the text 10.0000/m1
Here's a typo that might be construed as a doi 10.60 people were there.
{{cite|...|doi=10.0000/m2|pmid=10559875}}
<ref>Halfaker, A., Geiger, R. S., Morgan, J. T., & Riedl, J. (2012).
The rise and decline of an open collaboration system: How Wikipedia’s
reaction to popularity is causing its decline.
American Behavioral Scientist,
0002764212469365 doi: 10.1177/0002764212469365</ref>.  Hats pants and banana
[http://dx.doi.org/10.1170/foo<bar>(herp)derp]
[http://dx.doi.org/10.1170/foo<bar>(herp)derp[waffles]]
"""
EXPECTED = [
    Identifier('doi', "10.0000/m1"),
    Identifier('doi', "10.0000/m2"),
    Identifier('doi', "10.1177/0002764212469365"),
    Identifier('doi', "10.1170/foo<bar>(herp)derp"),
    Identifier('doi', "10.1170/foo<bar>(herp)derp[waffles]")
]

"""
def test_extract_regex():
    ids = list(doi.extract_regex(INPUT_TEXT))
    pprint.pprint(ids)
    pprint.pprint(EXPECTED)
    eq_(ids, EXPECTED)

def test_extract_mwp():
    ids = list(doi.extract_mwp(INPUT_TEXT))
    pprint.pprint(ids)
    pprint.pprint(EXPECTED)
    eq_(ids, EXPECTED)
"""

def test_extract():
    ids = list(doi.extract(INPUT_TEXT))
    pprint.pprint(ids)
    pprint.pprint(EXPECTED)
    eq_(ids, EXPECTED)

def test_extract_island():
    ids = list(doi.extract_island(INPUT_TEXT))
    pprint.pprint(ids)
    pprint.pprint(EXPECTED)
    eq_(ids, EXPECTED)
    
def test_extract_search():
    ids = list(doi.extract_search(INPUT_TEXT))
    pprint.pprint(ids)
    pprint.pprint(EXPECTED)
    eq_(ids, EXPECTED)
