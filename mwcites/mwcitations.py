"""
This script provides access to a set of utilities for processing academic
citations in Wikipedia.

Right now, there's only one utility, but there will be more to come.

* extract -- Extracts citations from an XML database dump

Usage:
    mwcitations (-h | --help)
    mwcitations <utility> [-h | --help]
    
Options:
    -h | --help  Shows this documentation
    <utility>    The name of the utility to run
"""
import sys
import traceback
from importlib import import_module

import docopt


USAGE = """Usage:
    mwcitations (-h | --help)
    mwcitations <utility> [-h | --help]\n"""


def main():
    
    if len(sys.argv) < 2:
        sys.stderr.write(USAGE)
        sys.exit(1)
    elif sys.argv[1] in ("-h", "--help"):
        sys.stderr.write(__doc__ + "\n")
        sys.exit(1)
    elif sys.argv[1][:1] == "-":
        sys.stderr.write(USAGE)
        sys.exit(1)
    
    module_name = sys.argv[1]
    try:
        module = import_module(".utilities." + module_name, package="mwcites")
    except ImportError:
        sys.stderr.write(traceback.format_exc())
        sys.stderr.write("Could not find utility {0}.\n".format(module_name))
        sys.exit(1)
    
    module.main(sys.argv[2:])
