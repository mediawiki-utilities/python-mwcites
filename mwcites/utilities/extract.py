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
    extract -h | --help
    extract <dump_file>... [--extractor=<classpath>...]

Options:
    -h --help                Shows this documentation
    <dump_file>              The path to a set of dump files to process.  If no
                             files are specified, <stdin> will be read.
    --extractor=<classpath>  The class path to set of extractors to apply
                             [default: <all>]
"""
import sys
from itertools import chain

import docopt
from mw import xml_dump

from ..extractors import doi, pubmed

ALL_EXTRACTORS = [doi, pubmed]

HEADERS = ("page_id", "page_title", "rev_id", "timestamp", "type", "id")

def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)
    dump_files = args['<dump_file>']
    
    if args['--extractor'] == ['<all>']:
        extractors = ALL_EXTRACTORS
    else:
        extractors = [import_from_path(path) for path in args['--extractor']]
    
    run(dump_files, extractors)

def run(dump_files, extractors):
    
    print("\t".join(HEADERS))
    
    cites = extract(dump_files, extractors=extractors)
    for page_id, title, rev_id, timestamp, type, id in cites:
        
        print("\t".join(tsv_encode(v) for v in (page_id,
                                                title,
                                                rev_id,
                                                timestamp.long_format(),
                                                type,
                                                id)))

def extract(dump_files, extractors=ALL_EXTRACTORS):
    """
    Extracts cites from a set of `dump_files`.
    
    :Parameters:
        dump_files : str | `file`
            A set of files MediaWiki XML dump files
            (expects: pages-meta-history)
        extractors : `list`(`extractor`)
            A list of extractors to apply to the text
    
    :Returns:
        `iterable` -- a generator of extracted cites
    
    """
    # Dump processor function
    def process_dump(dump, path):
        for page in dump:
            if page.namespace != 0: continue
            else:
                for cite in extract_cite_history(page, extractors):
                    yield cite
        
    # Map call
    return xml_dump.map(dump_files, process_dump)

def extract_cite_history(page, extractors):
    """
    Extracts cites from the history of a `page` (`mw.xml_dump.Page`).
    
    :Parameters:
        page : `iterable`(`mw.xml_dump.Revision`)
            The page to extract cites from
        extractors : `list`(`extractor`)
            A list of extractors to apply to the text
    
    :Returns:
        `iterable` -- a generator of extracted cites
    
    """
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
    """
    Uses `extractors` to extract citation identifiers from a text.
    
    :Parameters:
        text : str
            The text to process
        extractors : `list`(`extractor`)
            A list of extractors to apply to the text
    
    :Returns:
        `iterable` -- a generator of extracted identifiers
    """
    for extractor in extractors:
        for id in extractor.extract(text):
            yield id

def import_from_path(path):
    """
    Imports a specific attribute from a module based on a class path.
    
    :Parameters:
        path : str
            A dot delimited string representing the import path of the desired
            object.
    
    :Returns:
        object -- An imported object
    """
    parts = path.split(".")
    module_path = ".".join(parts[:-1])
    attribute_name = parts[-1]

    module = import_module(module_path)

    attribute = getattr(module, attribute_name)

    return attribute


def tsv_encode(val, none_string="NULL"):
    """
    Encodes a value for inclusion in a TSV.  Basically, it converts the value
    to a string and escapes TABs and linebreaks.
    
    :Parameters:
        val : `mixed`
            The value to encode
        none_string : str
            The string to use when `None` is encountered
    
    :Returns:
        str -- a string representing the encoded value
    """
    if val == "None":
        return null_string
    else:
        if isinstance(val, bytes):
            val = str(val, 'utf-8')
        
        return str(val).replace("\t", "\\t").replace("\n", "\\n")
