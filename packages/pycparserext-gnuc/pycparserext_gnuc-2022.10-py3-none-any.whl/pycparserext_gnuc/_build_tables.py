#-----------------------------------------------------------------
# pycparser: _build_tables.py
#
# A dummy for generating the lexing/parsing tables and and
# compiling them into .pyc for faster execution in optimized mode.
# Also generates AST code from the configuration file.
# Should be called from the pycparser directory.
#
# Eli Bendersky [https://eli.thegreenplace.net/]
# License: BSD
#-----------------------------------------------------------------

# Insert '.' and '..' as first entries to the search path for modules.
# Restricted environments like embeddable python do not include the
# current working directory on startup.
import sys
sys.path[0:0] = ['.', '..']

from pycparserext_gnuc import ext_c_parser

# Generates the tables
#
parser = ext_c_parser.GnuCParser(
    lex_optimize=True,
    yacc_debug=False,
    yacc_optimize=True)
# parser.parse("int main() {}")

# Load to compile into .pyc
#
import lextab
import yacctab
