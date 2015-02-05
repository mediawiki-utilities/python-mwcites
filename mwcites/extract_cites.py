"""
Extracts academic citations from articles from the history of Wikipedia articles
by processing a pages-meta-history XML dump and matching regular expressions
to revision content.

Currently supported identifies include:

 * PubMed
 * DOI
 
Outputs a TSV file with the following fields:

 * page_id: The identifier of the Wikipedia article (int), e.g. 1325125
 * page_title: The title of the Wikipedia article (utf-8), e.g. Club cell
 * rev_id: The Wikipedia revision where the citation was first added (int),
           e.g. 282470030
 * timestamp: The timestamp of the revision where the citation was first added.
              (ISO 8601 datetime), e.g. 2009-04-08T01:52:20Z
 * type: The type of identifier, e.g. pmid
 * id: The id of the cited scholarly article (utf-8),
       e.g 10.1183/09031936.00213411

Usage:
    extract_cites -h | --help
    extract_cites <dump_file>...

Options:
    -h --help        Shows this documentation
"""
from itertools import chain

import docopt
from mw import xml_dump

from .extractors import doi, pubmed

HEADERS = ("page_id", "page_title", "rev_id", "timestamp", "type", "id")

def main():
    args = docopt.docopt(__doc__)
    
    run(args['<dump_file>'])

def run(paths, extractors=[doi, pubmed]):
    
    def process_dump(dump, path):
        
        for page in dump:
            if page.namespace != 0: continue
            else:
                for cite in process_page(page, extractors):
                    yield cite
        
    
    print("\t".join(HEADERS))
    
    cites = xml_dump.map(paths, process_dump)
    
    for page_id, title, rev_id, timestamp, type, id in cites:
        
        print("\t".join(encode(v) for v in (page_id,
                                            title,
                                            rev_id,
                                            timestamp.long_format(),
                                            type,
                                            id)))

def encode(val):
    if val == "None":
        return "NULL"
    else:
        if isinstance(val, bytes):
            val = str(val, 'utf-8')
        
        return str(val).replace("\t", "\\t").replace("\n", "\\n")

def process_page(page, extractors):
    appearances = {} # For tracking the first appearance of an ID
    ids = set() # For holding onto the ids in the last revision.
    for revision in page:
        ids = set(extract_ids(revision.text, extractors))
        
        # For each ID, check to see if we have seen it before
        for id in ids:
            if id not in appearances:
               appearances[id] = (revision.id, revision.timestamp)
        
    for id in ids: #For the ids in the last version of the page
        rev_id, timestamp = appearances[id]
        yield (page.id, page.title, rev_id, timestamp, id.type, id.id)

def extract_ids(text, extractors):
    for extractor in extractors:
        for id in extractor.extract(text):
            yield id
