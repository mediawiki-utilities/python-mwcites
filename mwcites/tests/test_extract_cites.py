from collections import namedtuple

from mw import Timestamp
from nose.tools import eq_

from ..extract_cites import process_page


def process_page():
    FakeRevision = namedtuple("Revision", ['id', 'timestamp', 'text'])
    
    FakeExtractor = namedtuple("Extractor", ['extract'])
    
    fake_page = [
        FakeRevision(1, Timestamp(1), "id1 id2"),
        FakeRevision(2, Timestamp(2), "id1 id3"),
        FakeRevision(3, Timestamp(3), "id1 id2 id3"),
        FakeRevision(4, Timestamp(4), "id1 id2 id4"),
        FakeRevision(5, Timestamp(5), "id1 id2 id4"),
    ]
    fake_page.id = 1
    fake_page.title = "Title"
    
    extractor = FakeExtractor(lambda t: ('fake', id) for id in t.split(" "))
    
    cites = list(process_page(fake_page, [extractor]))
    
    eq_(cites,
        [(1, "Title", 1, Timestamp(1), "fake", "id1"),
         (1, "Title", 1, Timestamp(1), "fake", "id2"),
         (1, "Title", 4, Timestamp(4), "fake", "id4")])
