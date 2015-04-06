import pprint

from nose.tools import eq_

from .. import arxiv
from ...identifier import Identifier

INPUT_TEXT = """
This is a doi randomly placed in the text 10.0000/m1
Here's a typo that might be construed as a doi 10.60 people were there.
{{cite|...|arxiv=0706.0001v1|pmid=10559875}}
<ref>Halfaker, A., Geiger, R. S., Morgan, J. T., & Riedl, J. (2012).
The rise and decline of an open collaboration system: How Wikipedia’s
reaction to popularity is causing its decline.
American Behavioral Scientist,
0002764212469365 arxiv:0706.0002v1</ref>.  Hats pants and banana
[http://arxiv.org/0706.0003]
[http://arxiv.org/abs/0706.0004v1]
[https://arxiv.org/abs/0706.0005v1]
[https://arxiv.org/abs/math.GT/0309001]
[https://arxiv.org/abs/-math.gs/0309002]
{{cite|...|arxiv=foobar.hats/0101003|issue=1656}}
http://www.google.com/sky/#latitude=3.362&longitude=160.1238441&zoom=
10.2387/234310.2347/39423
<!--
    10.2387/234310.2347/39423-->
"""
EXPECTED = [
    Identifier('arxiv', "0706.0001"),
    Identifier('arxiv', "0706.0002"),
    Identifier('arxiv', "0706.0003"),
    Identifier('arxiv', "0706.0004"),
    Identifier('arxiv', "0706.0005"),
    Identifier('arxiv', "math.gt/0309001"),
    Identifier('arxiv', "math.gs/0309002"),
    Identifier('arxiv', "foobar.hats/0101003")
]

def test_extract():
    ids = list(arxiv.extract(INPUT_TEXT))
    pprint.pprint(ids)
    pprint.pprint(EXPECTED)
    eq_(ids, EXPECTED)
