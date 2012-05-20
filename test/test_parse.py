"""
Ensures the parser interprets the tokens correctly.
"""
import unittest
import re
from checklistdsl.parse import get_tag, get_form, make_html_safe, make_id_safe
from checklistdsl.lex import Token


class TestMakeHTMLSafe(unittest.TestCase):
    """
    Checks the make_safe function works correctly.
    """

    def test_converts_ampersand(self):
        """
        & becomes &amp;
        """
        result = make_html_safe('&')
        self.assertEqual(result, '&amp;')

    def test_converts_lessthan(self):
        """
        < becomes &lt;
        """
        result = make_html_safe('<')
        self.assertEqual(result, '&lt;')

    def test_converts_greaterthan(self):
        """
        > becomes &gt;
        """
        result = make_html_safe('>')
        self.assertEqual(result, '&gt;')

    def test_converts_singlequote(self):
        """
        ' becomes &#39;
        """
        result = make_html_safe("'")
        self.assertEqual(result, '&#39;')

    def test_converts_doublequote(self):
        """
        " becomes &#34;
        """
        result = make_html_safe('"')
        self.assertEqual(result, '&#34;')

    def test_convert_unsafe_html(self):
        """
        <script>alert('Hello');</script> & a "test"
        """
        raw = "<script>alert('Hello');</script> & a \"test\""
        result = make_html_safe(raw)
        expected = ('&lt;script&gt;alert(&#39;Hello&#39;);&lt;/script&gt; ' +
            '&amp; a &#34;test&#34;')
        self.assertEqual(result, expected)


class TestMakeIdSafe(unittest.TestCase):
    """
    Ensures the make_id_safe function works as expected.
    """

    def test_removes_all_non_alpha_numerics(self):
        raw = ';:"hello@<>/&'
        result = make_id_safe(raw)
        self.assertEqual('hello', result)

    def test_replaces_spaces_with_minus(self):
        raw = 'hello world'
        result = make_id_safe(raw)
        self.assertEqual('hello-world', result)

    def test_strips_whitespace(self):
        raw = ' hello world!'
        result = make_id_safe(raw)
        self.assertEqual('hello-world', result)

    def test_to_lower_case(self):
        raw = 'HELLO WORLD'
        result = make_id_safe(raw)
        self.assertEqual('hello-world', result)


class TestGetForm(unittest.TestCase):
    """
    Checks the get_form function works correctly.
    """

    def test_returns_empty_no_tokens(self):
        """
        If no tokens were passed into the function, an empty string is
        returned.
        """
        tokens = []
        result = get_form(tokens)
        self.assertEqual(result, '')

    def test_radio_button_name_not_form_id(self):
        """
        Ensure that radio button tags don't use the form_id for their
        name attribute.
        """
        tokens = [Token('OR_ITEM', 'foo'), Token('OR_ITEM', 'bar'),
            Token('OR_ITEM', 'baz')]
        form_id = 'test'
        result = get_form(tokens, form_id)
        regex = re.compile(r'name="(?P<id>[\w-]+)"')
        ids = set(regex.findall(result))
        self.assertNotEqual(form_id, list(ids)[0],
            'The form_id must not be used as name attribute of radio buttons')

    def test_radio_buttons_in_same_group(self):
        """
        A list of adjacent radio button (OR) items have the same name
        attribute.
        """
        tokens = [Token('OR_ITEM', 'foo'), Token('OR_ITEM', 'bar'),
            Token('OR_ITEM', 'baz')]
        result = get_form(tokens, 'test')
        regex = re.compile(r'name="(?P<id>[\w-]+)"')
        ids = set(regex.findall(result))
        self.assertEqual(1, len(ids))

    def test_radio_button_group_name_changes(self):
        """
        Non-adjacent radio button (OR) items have different name attributes.
        """
        tokens = [Token('OR_ITEM', 'foo'), Token('OR_ITEM', 'bar'),
            Token('OR_ITEM', 'baz'), Token('BREAK', '----'),
            Token('OR_ITEM', 'foo'), Token('OR_ITEM', 'bar'),
            Token('OR_ITEM', 'baz')]
        result = get_form(tokens, 'test')
        regex = re.compile(r'name="(?P<id>[\w-]+)"')
        ids = set(regex.findall(result))
        self.assertEqual(2, len(ids))

    def test_uses_designated_id(self):
        """
        If a form_id is provided, will be used as the form's id and name
        attribute in checkboxes.
        """
        tokens = [Token('AND_ITEM', 'foo'), Token('AND_ITEM', 'bar'),
            Token('AND_ITEM', 'baz')]
        form_id = 'test'
        result = get_form(tokens, form_id)
        regexID = re.compile(r'id="(?P<id>[\w-]+)"')
        regexName = re.compile(r'name="(?P<id>[\w-]+)"')
        # find the id attribute.
        ids = regexID.findall(result)
        # find all the name attributes.
        names = regexName.findall(result)
        # The id attribute is only used once (the form tag).
        self.assertEqual(1, len(ids))
        # Found the name attributes for each of the checkbox items.
        self.assertEqual(3, len(names))
        # There is only one value for the name attributes.
        self.assertEqual(1, len(set(names)))
        # The id is the form_id.
        self.assertTrue(form_id in ids)
        # The names are the form_id.
        self.assertTrue(form_id in names)

    def test_creates_uuid_if_no_form_id(self):
        """
        If no form id is given, the function invents one (in the form of a
        uuid4).
        """
        tokens = [Token('AND_ITEM', 'foo'), Token('AND_ITEM', 'bar'),
            Token('AND_ITEM', 'baz')]
        result = get_form(tokens)
        regexID = re.compile(r'id="(?P<id>[\w-]+)"')
        regexName = re.compile(r'name="(?P<id>[\w-]+)"')
        # find the id attribute.
        ids = regexID.findall(result)
        # find all the name attributes.
        names = regexName.findall(result)
        # The id attribute is only used once (the form tag).
        self.assertEqual(1, len(ids))
        # Found the name attributes for each of the checkbox items.
        self.assertEqual(3, len(names))
        # There is only one value for the name attributes.
        self.assertEqual(1, len(set(names)))
        # The id is the same for ids and names.
        self.assertEqual(ids[0], names[0])

    def test_returns_items_in_correct_order(self):
        """
        Ensures that the tags appear in the correct order in the form.
        """
        tokens = [Token('TEXT', 'foo'), Token('TEXT', 'bar'),
            Token('TEXT', 'baz')]
        form_id = 'test'
        result = get_form(tokens, form_id)
        self.assertTrue(result.find('foo') < result.find('bar') <
            result.find('baz'))

    def test_given_form_id_is_sanitized(self):
        """
        Ensure the (potentially user derived) form_id is sanitized to avoid
        the possibility of XSS.
        """
        tokens = [Token('TEXT', 'foo')]
        form_id = '<script>alert("hello");</script>'
        result = get_form(tokens, form_id)
        regexID = re.compile(r'id="(?P<id>[\w-]+)"')
        ids = regexID.findall(result)
        self.assertEqual('script-alert-hello-script', ids[0])

    def test_csrf_token_is_included(self):
        """
        Ensures that if a CSRF token is passed in the correct hidden input
        tag is added to the form.
        """
        tokens = [Token('TEXT', 'foo')]
        form_id = 'test'
        csrf_token = '12345'
        result = get_form(tokens, form_id, csrf_token)
        expected = ('<input type="hidden" name="csrfmiddlewaretoken"' +
            ' value="12345"/>')
        self.assertTrue(expected in result)

    def test_default_attrs(self):
        """
        Make sure the default attributes for the form tag are as expected.
        """
        tokens = [Token('TEXT', 'foo')]
        form_id = 'test'
        csrf_token = '12345'
        result = get_form(tokens, form_id)
        expected = '<form id="test" action="." method="POST">'
        self.assertTrue(expected in result)

    def test_attrs_are_set_from_kwargs(self):
        """
        Check that any further named args are turned into attribites of the
        form tag.
        """
        tokens = [Token('TEXT', 'foo')]
        form_id = 'test'
        csrf_token = '12345'
        result = get_form(tokens, form_id, action='/foo',
            method='get')
        expected = '<form id="test" action="/foo" method="get">'
        self.assertTrue(expected in result)


class TestGetTag(unittest.TestCase):
    """
    Checks the get_tag function works correctly.
    """

    def test_with_unsafe_value(self):
        """
        Ensure the token's value is sanitized to make it HTML safe (to avoid
        the potential for XSS).
        """
        token = Token('HEADING', '<script>alert("hello");</script>', size=1)
        result = get_tag(token)
        self.assertEqual(result,
            '<h1>&lt;script&gt;alert(&#34;hello&#34;);&lt;/script&gt;</h1>')

    def test_with_unsafe_roles(self):
        """
        Ensure that any roles associated with a token are sanitized to make
        them HTML safe (to avoid the potential for XSS).
        """
        token = Token('AND_ITEM', 'Foo',
            roles=['<script>alert("hello");</script>', 'baz'])
        result = get_tag(token, 'name_value')
        expected = ('<label class="checkbox">' +
            '<input type="checkbox" name="name_value" value="Foo">' +
            'Foo</input> <span class="roles">(&lt;script&gt;' +
            'alert(&#34;hello&#34;);&lt;/script&gt;, baz)</span></label><br/>')
        self.assertEqual(expected, result)

    def test_heading_token_size1(self):
        """
        Ensure a heading token is parsed correctly to <h1>.
        """
        token = Token('HEADING', 'A header', size=1)
        result = get_tag(token)
        self.assertEqual('<h1>A header</h1>', result)

    def test_heading_token_size6(self):
        """
        Ensure a heading token is parsed correctly to <h6>.
        """
        token = Token('HEADING', 'A header', size=6)
        result = get_tag(token)
        self.assertEqual('<h6>A header</h6>', result)

    def test_heading_token_size_too_big(self):
        """
        Ensure a heading token that is too big is parsed correctly to <h6>.
        """
        token = Token('HEADING', 'A header', size=7)
        result = get_tag(token)
        self.assertEqual('<h6>A header</h6>', result)

    def test_and_item(self):
        """
        Ensures an AND_ITEM is parsed to a checkbox.
        """
        token = Token('AND_ITEM', 'Foo')
        result = get_tag(token, 'name_value')
        expected = ('<label class="checkbox">' +
            '<input type="checkbox" name="name_value" value="Foo">' +
            'Foo</input> </label><br/>')
        self.assertEqual(expected, result)

    def test_and_item_with_roles(self):
        """
        Ensures an AND_ITEM with associated roles is parsed correctly.
        """
        token = Token('AND_ITEM', 'Foo', roles=['bar', 'baz'])
        result = get_tag(token, 'name_value')
        expected = ('<label class="checkbox">' +
            '<input type="checkbox" name="name_value" value="Foo">' +
            'Foo</input> <span class="roles">(bar, baz)</span></label><br/>')
        self.assertEqual(expected, result)

    def test_or_item(self):
        """
        Ensures an OR_ITEM is parsed to a radiobutton.
        """
        token = Token('OR_ITEM', 'Foo')
        result = get_tag(token, 'name_value')
        expected = ('<label class="radio">'+
            '<input type="radio" name="name_value" value="Foo">' +
            'Foo</input> </label><br/>')
        self.assertEqual(expected, result)

    def test_or_item_with_roles(self):
        """
        Ensures an OR_ITEM with associated roles is parsed correctly.
        """
        token = Token('OR_ITEM', 'Foo', roles=['bar', 'baz'])
        result = get_tag(token, 'name_value')
        expected = ('<label class="radio">' +
            '<input type="radio" name="name_value" value="Foo">' +
            'Foo</input> <span class="roles">(bar, baz)</span></label><br/>')
        self.assertEqual(expected, result)

    def test_break(self):
        """
        Ensures a BREAK token becomes an <hr/> tag.
        """
        token = Token('BREAK', '----')
        result = get_tag(token)
        self.assertEqual('<hr/>', result)

    def test_text(self):
        """
        Ensures a TEXT token is correctly parsed into a <p>...</p> tag.
        """
        token = Token('TEXT', 'This is a test')
        result = get_tag(token)
        self.assertEqual('<p class="help-block">This is a test</p>', result)

    def test_unknown_token_type(self):
        """
        Ensures an unrecognized token is ignored and results in an empty
        string.
        """
        token = Token('FOO', 'bar')
        result = get_tag(token)
        self.assertEqual('', result)
