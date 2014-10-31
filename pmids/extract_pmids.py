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

PMID_RE = re.compile(r"\b(pmid|pmc) *= *([0-9]+)\b", re.I)

# See: https://en.wikipedia.org/w/index.php?
#      title=Wikipedia%3AVillage_pump_%28technical%29&
#      diff=630990203&oldid=630985731
PMURL_RE = re.compile(r"http://www\.ncbi\.nlm\.nih\.gov" +
                      r"/pubmed/([0-9]+)", re.I)
PMCURL_RE = re.compile(r"http://www\.ncbi\.nlm\.nih\.gov" +
                       r"/pmc/articles/PMC([0-9]+)", re.I)

def main():
    args = docopt.docopt(__doc__)
    
    def process_dump(dump, path):
        
        for page in dump:
            
            for revision in page:
                ids = set()
                
                for match in PMID_RE.finditer(revision.text or ""):
                    ids.add((match.group(1), int(match.group(2))))
                
                for match in PMURL_RE.finditer(revision.text or ""):
                    ids.add(("pmid", int(match.group(1))))
                
                for match in PMCURL_RE.finditer(revision.text or ""):
                    ids.add(("pmc", int(match.group(1))))
                
                for type, id in ids:
                    yield (page.id, page.namespace, page.title, revision.id,
                           type, id)
                
            
        
    
    print("page_id\tpage_namespace\tpage_title\trev_id\ttype\tid")
    
    id_metas = xml_dump.map(args['<dump_path>'], process_dump)
    for page_id, namespace, title, rev_id, type, id in id_metas:
        
        print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}"\
              .format(page_id, namespace,
                      title.replace("\t", "\\t").replace("\n", "\\n"),
                      rev_id, type, id))
