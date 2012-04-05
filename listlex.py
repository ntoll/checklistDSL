"""
Tokeniser for a checklist DSL
"""
from ply import lex

# Token names
tokens = (
    'WHITESPACE', # To indicate scope
    'HEADING', # == HEADING ==
    'ITEM', # * An item
    'ORDERED_ITEM', # 1 An item
    'MULTI_ITEM', # () An item
    'CONST_ITEM', # [] An item
    'ROLE_LIST', # {foo, bar}
    'INDENT', # \t or spaces
    'COMMENT', # A comment
)

# Regex to match the tokens
t_WHITESPACE = r'^\ +'
t_HEADING = r'==.*=='
t_ITEM = r'\* .*'
t_ORDERED_ITEM = r'\d .*'
t_MULTI_ITEM = r'\(\) .*'
t_CONST_ITEM = r'\[\] .*'
t_ROLE_LIST = r'\{.*\}'
t_INDENT = r'^[\t| ]+'
t_COMMENT = r'^.+$'

def t_error(t):
    #print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

lexer = lex.lex()

data = """
== A Heading ==

Some explanatory text at the start of the list.

This can be several paragraphs.

* A single item with no constraints
1 An item that needs to be done in order (first)
2 An item that needs to be done in order (second)

Some more explanatory text. It can go anywhere in the list.

It's possible to choose 0-all of the following items.

() Item A of a multiple choice
() Item B of a multiple choice
() Item C of a multiple choice

It's possible to select only one of the following items:

[] Item A in a constrained multiple choice
[] Item B in a constrained multiple choice
[] Item C in a constrained multiple choice

* Another single item with no constraints. Note the indentation for nesting.

    == A Sub-heading ==

    A sub description

    () Item A in a nested multiple choice
    () Item B in a nested multiple choice
    () Item C in a nested multiple choice

The following items have (case insensitive) roles assigned to them:

* {doctor, nurse} Take blood pressure.
* {patient} Give consent for something.
* {cleaner} Wipe up the blood and gore.
"""

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print tok
