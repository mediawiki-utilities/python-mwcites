import time

from mw import api

from mwcites.extractors import doi

session = api.Session("https://en.wikipedia.org/w/api.php",
                      user_agent="Demo doi extractor")

text = next(session.revisions.query(titles={"Psychotherapy"},
                                    properties={'content'}))['*']
print(len(text))

start = time.time()
for i in range(1000):
    ids = set(doi.extract(text))
print("Regex strategy: {0}".format(time.time() - start))

start = time.time()
for i in range(1000):
    ids = set(doi.extract_mwp(text))
print("MWP strategy: {0}".format(time.time() - start))
