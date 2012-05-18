"""
Parser for a checklist DSL. Parses the tokens generated by lex.py and creates
a block of HTML to display.

(c) 2012 Nicholas H.Tollervey
"""
import uuid
import re


# Templates.
FORM = '<form id="%(id)s" %(attrs)s>%(content)s</form>'
ROLES = '<span class="roles">(%(roles)s)</span>'
HEADER = '<h%(size)d>%(title)s</h%(size)d>'
PARA = '<p>%(content)s</p>'
BREAK = '<hr/>'
RADIO = ('<input type="radio" name="%(name)s" value="%(value)s">' +
    '%(text)s</input>%(roles)s<br/>')
CHECKBOX = ('<input type="checkbox" name="%(name)s" value="%(value)s">' +
    '%(text)s</input>%(roles)s<br/>')
CSRF = '<input type="hidden" name="csrfmiddlewaretoken" value="%(token)s"/>'


def make_html_safe(raw):
    """
    Given some raw input will make it HTML safe by encoding the <, >, ", ' and
    & characters.
    """
    return (raw.replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace("'", '&#39;')
        .replace('"', '&#34;'))


def make_id_safe(raw):
    """
    Given a potential form id will make it safe to use as an id or name
    attribute of an HTML tag.
    """
    no_alphanumerics = re.sub(r'\W+', ' ', raw).strip().lower()
    return no_alphanumerics.replace(' ', '-')


def get_tag(token, name=None):
    """
    Given a token will return a string containing an HTML representation of it.
    If the name argument is given, this will be used as the 'name' attribute
    of an input HTML tag.
    """
    # The default result to return.
    tag = ''

    # Some sanitization operations on token attributes that derive from user
    # input.
    safe_value = make_html_safe(token.value)
    safe_roles = ''
    if token.roles:
        safe_roles = ROLES % {'roles': make_html_safe(', '.join(token.roles))}

    # Parse the correct template depending on the type of token.
    if token.token == 'HEADING':
        if token.size > 6:
            token.size = 6
        tag = HEADER % {
            'size': token.size,
            'title': safe_value
        }
    elif token.token == 'AND_ITEM':
        tag = CHECKBOX % {
            'name': name,
            'value': safe_value,
            'text': safe_value,
            'roles': safe_roles
        }
    elif token.token == 'OR_ITEM':
        tag = RADIO % {
            'name': name,
            'value': safe_value,
            'text': safe_value,
            'roles': safe_roles
        }
    elif token.token == 'BREAK':
        tag = BREAK
    elif token.token == 'TEXT':
        tag = PARA % {
            'content': safe_value
        }
    else:
        pass
    return tag


def get_form(tokens, form_id=None, csrf_token=None, **kwargs):
    """
    Given a list of tokens produced by the lexer, will return a string
    containing an HTML representation of the checklist. If provided,
    the form_id will be used as the id attribute of the form tag and also as
    the name attribute for radio buttton tags. If provided, the csrf_token
    will be used in a hidden input element to help avoid cross site request
    forgery. Any further named arguments passed via **kwargs will become an
    attribute of the form tag.
    """
    if not tokens:
        return ''

    if form_id:
        # Ensure the form's id can be used in an id or name attribute in HTML.
        form_id = make_id_safe(form_id)
    else:
        # if no form_id is given then use something random and unique.
        form_id = str(uuid.uuid4())

    html_tags = []

    # Handle the CSRF token if it exists.
    if csrf_token:
        html_tags.append(CSRF % { 'token': csrf_token})

    # Used to track the name of the current radio button group.
    radio_name = ''

    for token in tokens:
        # Radio button group state check
        if token.token == 'OR_ITEM':
            if not radio_name:
                # Currently not in a radio button group so create a new name.
                radio_name = str(uuid.uuid4())
            tag = get_tag(token, radio_name)
        else:
            # Not in a radio button group so reset it and use form_id for name
            # attributes.
            radio_name = ''
            tag = get_tag(token, form_id)
        if tag:
            html_tags.append(tag)

    # Default form attributes.
    attributes = {
        'action': '.',
        'method': 'POST'
    }
    # Overridden with the named arguments into this function.
    if kwargs:
        attributes.update(kwargs)

    attr_list = []
    for name, value in attributes.iteritems():
        attr_list.append(
            '%(name)s="%(value)s"' % {'name': name, 'value': value})

    attrs = ' '.join(attr_list)

    return FORM % {
        'content': ''.join(html_tags),
        'id': form_id,
        'attrs': attrs
    }
