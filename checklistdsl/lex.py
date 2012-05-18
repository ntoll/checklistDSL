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

    def __init__(self, token, value, roles=None, size=None):
        """
        token - the type of token this is.
        value - the matched value.
        roles - named roles who have authority to action the item.
        size - the "size" of the heading. 1 = big, 6 = small.
        """
        self.token = token
        self.value = value
        self.roles = roles
        self.size = size

    def __repr__(self):
        return '%s: "%s"' % (self.token, self.value)

"""
A dictionary that contains the regex used to match tokens and the associated
token types.
"""
MATCHER = {
    # == Heading == (becomes an h* element where * is number of equal signs)
    '(?P<depth_start>=+)(?P<value>(\\s|\\w)*)(?P<depth_end>=+)': 'HEADING',
    # // This is a comment (ignored)
    '\/\/(?P<value>.*)': 'COMMENT',
    # [] item 1 (becomes a check box)
    '\[\] *(?P<roles>{.*}|) *(?P<value>.*)': 'AND_ITEM',
    # () item 1 (becomes a radio button)
    '\(\) *(?P<roles>{.*}|) *(?P<value>.*)': 'OR_ITEM',
    # --- (becomes an <hr/>)
    '^-{3,}$': 'BREAK',
    # Some text (becomes a <p>)
    '(?P<value>[^=\/\[\(].*)': 'TEXT'
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
                # Grab the named groups.
                val = match.groupdict().get('value', '').strip()
                roles = match.groupdict().get('roles', '').replace(
                    '{', '').replace('}', '').strip()
                depth_start = match.groupdict().get('depth_start', '')

                # Post process roles.
                if roles:
                    roles = [role.lower().strip() for role in roles.split(',')]
                else:
                    roles = None

                # Post process depth_start to give the size of the heading.
                if depth_start:
                    size = len(depth_start)
                else:
                    size = None

                # Instantiate the token depending on the match for the val
                # named group.
                if val:
                    token = Token(MATCHER[regex], val, roles=roles, size=size)
                else:
                    token = Token(MATCHER[regex], match.string)
                # Ignore comments
                if token.token != 'COMMENT':
                    result.append(token)
                break
    return result
