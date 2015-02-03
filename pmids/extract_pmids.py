"""
Extracts PubMed IDs from articles

Usage:
    extract_pmids -h | --help
    extract_pmids <dump_path>...

Options:
    -h --help        Shows this documentation
"""

import re

import docopt
from mw import xml_dump

PMID_RE = re.compile(r"\b(pmid|pmc) *= *(pmc)?([0-9]+)\b", re.I)

# See: https://en.wikipedia.org/w/index.php?
#      title=Wikipedia%3AVillage_pump_%28technical%29&
#      diff=630990203&oldid=630985731
PMURL_RE = re.compile(r"//www\.ncbi\.nlm\.nih\.gov" +
                      r"/pubmed/([0-9]+)", re.I)
PMCURL_RE = re.compile(r"//www\.ncbi\.nlm\.nih\.gov" +
                       r"/pmc/articles/PMC([0-9]+)", re.I)



def main():
    args = docopt.docopt(__doc__)
    
    def process_dump(dump, path):
        
        for page in dump:
            if page.namespace != 0: continue
            
            id_appearance = {}
            ids = set()
            for revision in page:
                ids = set()
                
                for match in PMID_RE.finditer(revision.text or ""):
                    ids.add((match.group(1).lower(), int(match.group(3))))
                
                for match in PMURL_RE.finditer(revision.text or ""):
                    ids.add(("pmid", int(match.group(1))))
                
                for match in PMCURL_RE.finditer(revision.text or ""):
                    ids.add(("pmc", int(match.group(1))))
                
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
