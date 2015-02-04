from nose.tools import eq_

from .. import doi


def test_extract():
    
    text = """
    This is a doi randomly placed in the text 10.0000/m1
    Here's a typo that might be construed as a doi 10.60 people were there.
    {{cite|...|doi=10.0000/m2|pmid=10559875}}
    <ref>Halfaker, A., Geiger, R. S., Morgan, J. T., & Riedl, J. (2012).
    The rise and decline of an open collaboration system: How Wikipedia’s
    reaction to popularity is causing its decline.
    American Behavioral Scientist,
    0002764212469365 doi: 10.1177/0002764212469365</ref>
    """
    ids = list(doi.extract(text))
    expected = [
        ('doi', "10.0000/m1"),
        ('doi', "10.0000/m2"),
        ('doi', "10.1177/0002764212469365")
    ]
    print(ids)
    print(expected)
    eq_(ids, expected)
