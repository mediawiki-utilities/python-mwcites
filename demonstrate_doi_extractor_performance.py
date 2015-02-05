import time

from mw import api

from mwcites.extractors import doi

session = api.Session("https://en.wikipedia.org/w/api.php",
                      user_agent="Demo doi extractor")

revisions = session.revisions.query(titles={"Psychotherapy"},
                                    properties={'content'})
lots = next(revisions)['*']
print("Text with lots of DOIs has {0} characters".format(len(lots)))

revisions = session.revisions.query(titles={"Waffle"},
                                    properties={'content'})
few = next(revisions)['*']
print("Text with few DOIs has {0} characters".format(len(few)))


start = time.time()
for i in range(50):
    ids = set(doi.extract(lots))
    ids = set(doi.extract(few))
print("Regex strategy: {0}".format(time.time() - start))

start = time.time()
for i in range(50):
    ids = set(doi.extract_mwp(lots))
    ids = set(doi.extract_mwp(few))
print("MWP strategy: {0}".format(time.time() - start))


start = time.time()
for i in range(50):
    ids = set(doi.extract_island(lots))
    ids = set(doi.extract_island(few))
print("Island parser strategy: {0}".format(time.time() - start))

start = time.time()
for i in range(50):
    ids = set(doi.extract_search(lots))
    ids = set(doi.extract_search(few))
print("Search parser strategy: {0}".format(time.time() - start))
