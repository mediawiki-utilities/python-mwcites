import re

TEMPLATE_RE = re.compile(r"\b(pmid|pmc)\s*=\s*(pmc)?([0-9]+)\b", re.I)

PMURL_RE = re.compile(r"//www\.ncbi\.nlm\.nih\.gov" +
                      r"/pubmed/([0-9]+)\b", re.I)
PMCURL_RE = re.compile(r"//www\.ncbi\.nlm\.nih\.gov" +
                       r"/pmc/articles/PMC([0-9]+)\b", re.I)

def extract(text):
    text = str(text or "")
    
    for match in TEMPLATE_RE.finditer(text):
        yield (match.group(1).lower(), match.group(3))
            
    for match in PMURL_RE.finditer(text):
        yield ("pmid", match.group(1))
    
    for match in PMCURL_RE.finditer(text):
        yield ("pmc", match.group(1))
