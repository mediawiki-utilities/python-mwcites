"""
Extracts academic citations from articles from the history of Wikipedia articles
by processing a pages-meta-history XML dump and matching regular expressions
to revision content.

Currently supported identifies include:
 * PubMed
 * DOI

Usage:
    extract_cites -h | --help
    extract_cites <dump_path>...

Options:
    -h --help        Shows this documentation
"""
from itertools import chain

import docopt
from mw import xml_dump

from .extractors import doi, pubmed


def main():
    args = docopt.docopt(__doc__)
    
    def process_dump(dump, path):
        
        for page in dump:
            if page.namespace != 0: continue
            
            id_appearance = {}
            ids = set()
            for revision in page:
                
                ids = set(doi.extract(revision.text)) + \
                      set(pubmed.extract(revision.text))
                
                for id in ids:
                    if id not in id_appearance:
                       id_appearance[id] = (revision.id, revision.timestamp)
                
            for id in ids: #For the ids in the last version of the page
                appearance_id, appearance_timestamp = id_appearance[id]
                yield (page.id, page.title, appearance_id, appearance_timestamp, id[0], id[1])
                
            
        
    
    print("page_id\tpage_title\trev_id\ttimestamp\ttype\tid")
    
    id_metas = xml_dump.map(args['<dump_path>'], process_dump)
    for page_id, title, rev_id, timestamp, type, id in id_metas:
        
        print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}"\
              .format(page_id,
                      title.replace("\t", "\\t").replace("\n", "\\n"),
                      rev_id,
                      timestamp.long_format(),
                      type, id))
