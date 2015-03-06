from collections import namedtuple

from mw import Timestamp
from nose.tools import eq_

from ..extract import extract_cite_history
from ...identifier import Identifier


def test_extract_cite_history():
    FakeRevision = namedtuple("Revision", ['id', 'timestamp', 'text'])

    FakeExtractor = namedtuple("Extractor", ['extract'])

    class FakePage:
        def __init__(self, id, title):
            self.id = id
            self.title = title
        def __iter__(self):
            return iter([
                FakeRevision(1, Timestamp(1), "id1 id2"),
                FakeRevision(2, Timestamp(2), "id1 id3"),
                FakeRevision(3, Timestamp(3), "id1 id2 id3"),
                FakeRevision(4, Timestamp(4), "id1 id2 id4"),
                FakeRevision(5, Timestamp(5), "id1 id2 id4"),
            ])

    fake_page = FakePage(1, "Title")

    def extract(text):
        return (Identifier('fake', id) for id in text.split(" "))
    extractor = FakeExtractor(extract)

    expected = [(1, "Title", 1, Timestamp(1), "fake", "id1"),
                (1, "Title", 1, Timestamp(1), "fake", "id2"),
                (1, "Title", 4, Timestamp(4), "fake", "id4")]

    citations = list(extract_cite_history(fake_page, [extractor]))
    eq_(len(citations), len(expected))
    for cite in extract_cite_history(fake_page, [extractor]):
        assert cite in expected
