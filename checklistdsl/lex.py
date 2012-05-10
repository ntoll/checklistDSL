"""
Tokeniser for a checklist DSL. (I was using Ply, but it sucked and this is a
*lot* simpler.)

(c) 2012 Nicholas H.Tollervey
"""
import re

class Token(object):
    """
    Represents a token matched by the lexer.
    """

    def __init__(self, token, value, roles=None):
        """
        token - the type of token this is.
        value - the matched value.
        roles - named roles who have authority to action the item.
        """
        self.token = token
        self.value = value
        self.roles = roles

    def __repr__(self):
        return '%s: "%s"' % (self.token, self.value)

"""
A dictionary that contains the regex used to match tokens and the associated
token types.
"""
MATCHER = {
    r'=+(?P<value>(\s|\w)*)=+': 'HEADING', # == Heading ==
    r'\/\/(?P<value>.*)': 'COMMENT', # // This is a comment
    r'\[\] *(?P<roles>{.*}|) *(?P<value>.*)': 'AND_ITEM', # [] item 1
    r'\(\) *(?P<roles>{.*}|) *(?P<value>.*)': 'OR_ITEM', # () item 1
    r'^-{3,}$': 'BREAK', # ---
    r'(?P<value>[^\/\[\(].*)': 'TEXT'# Some text
}

def get_tokens(data):
    """
    Given some raw data will return a list of matched tokens. An example of the
    simplest possible lexer.
    """
    result = []
    # Split on newline and throw away empty (un-needed) lines
    split_by_lines = [line.strip() for line in data.split('\n')
        if line.strip()]
    for line in split_by_lines:
        for regex in MATCHER.keys():
            match = re.match(regex, line)
            if match:
                # Grab the named groups
                val = match.groupdict().get('value', '').strip()
                roles = match.groupdict().get('roles', '').replace(
                    '{', '').replace('}', '').strip()
                # Post process roles
                if roles:
                    roles = [role.lower().strip() for role in roles.split(',')]
                else:
                    roles = None
                # Instantiate the token depending on the match for the val
                # named group
                if val:
                    token = Token(MATCHER[regex], val, roles)
                else:
                    token = Token(MATCHER[regex], match.string)
                # Ignore comments
                if token.token != 'COMMENT':
                    result.append(token)
                break
    return result
