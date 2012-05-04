"""
Tokeniser for a checklist DSL
"""
from ply import lex

# Token names
tokens = (
    'HEADING', # = Heading =
    'COMMENT', # // A comment
    'AND_ITEM', # [] An item
    'OR_ITEM', # () An item
    'ROLE_LIST', # {foo, bar}
    'CONTEXT', # Some text immediately above list items
    'TEXT', # Some floating text.
)

# Regex to match the tokens
t_HEADING = r'=.*='
t_COMMENT = r'\/\/.*'
t_AND_ITEM = r'\[\] .*'
t_OR_ITEM = r'\(\) .*'
t_ROLE_LIST = r'\{.*\}'
t_CONTEXT = r'(^|\n\n)[^=\/\[\(].*\n'
t_TEXT = r'(^|\n\n)[^=\/\[\(].*(\n\n|$)'

def t_error(t):
    #print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

lexer = lex.lex()

data = """= A Heading =

// A comment that isn't rendered.

Some explanatory text at the start of the list.

This can be several paragraphs.

[] A single item in a checklist

Each item immediately below belongs to this comment.
[] Item 1
[] Item 2
[] Item 3

The following items are OR'd (rather than AND'd).
() Item 1
() Item 2
() Item 3

The following items have case insensitive roles assigned to them.
[] {doctor, nurse} Check the machine that goes ping.
[] {patient} Give consent.
[] {surgeon} Make the incision.
[] {cleaner} Tidy up the gore.
"""

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print tok
