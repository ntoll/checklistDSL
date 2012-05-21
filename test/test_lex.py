"""
Checks that the ChecklistLexer class works as expected. Mainly full of sanity
checks to make sure I've got the regex correct.
"""
import unittest
from checklistdsl.lex import Token, get_tokens


class TestToken(unittest.TestCase):
    """
    Ensures the Token class works as expected.
    """

    def test_instantiation(self):
        """
        Check the object is set up correctly.
        """
        token = 'TOKEN'
        value = 'VALUE'
        result = Token(token, value)
        self.assertEqual(token, result.token)
        self.assertEqual(value, result.value)
        self.assertEqual(None, result.roles)

    def test_instantiation_with_roles(self):
        """
        Ensures roles get assigned correctly.
        """
        token = 'TOKEN'
        value = 'VALUE'
        roles = ['doctor', 'patient']
        result = Token(token, value, roles)
        self.assertEqual(token, result.token)
        self.assertEqual(value, result.value)
        self.assertEqual(roles, result.roles)

    def test_instantiation_with_size(self):
        """
        Ensures size attribute gets assigned correctly.
        """
        token = 'TOKEN'
        value = 'VALUE'
        size = 1
        result = Token(token, value, size=size)
        self.assertEqual(token, result.token)
        self.assertEqual(value, result.value)
        self.assertEqual(size, result.size)

    def test_repr(self):
        """
        Ensure the repr is meaningful.
        """
        token = Token('foo', 'bar')
        result = repr(token)
        self.assertEqual('foo: "bar"', result)


class TestGetTokens(unittest.TestCase):
    """
    Tests to exercise the get_tokens function.
    """

    def test_good_case(self):
        """
        Process a checklist with all the various tokenisable elements in it.
        """

        data = """= A Heading =

        // A comment that isn't rendered.

        Some explanatory text at the start of the list.

        This can be several paragraphs.

        [] A single item in a checklist

        Each item immediately below belongs to a single choice list.
        [] Item 1
        [] Item 2
        [] Item 3

        The following items are OR'd (rather than AND'd) together.
        () {doctor, nurse} Item 1
        () {doctor} Item 2
        () Item 3

        Roles authorised to fulfil items are listed in curly brackets.

        ---

        You can crete a break with three or more minus signs.
        """

        tokens = get_tokens(data)
        # Simply check we get the right number of tokens of the right type.
        self.assertEqual(15, len(tokens), tokens)
        self.assertEqual('HEADING', tokens[0].token)
        self.assertEqual('TEXT', tokens[1].token)
        self.assertEqual('TEXT', tokens[2].token)
        self.assertEqual('AND_ITEM', tokens[3].token)
        self.assertEqual('TEXT', tokens[4].token)
        self.assertEqual('AND_ITEM', tokens[5].token)
        self.assertEqual('AND_ITEM', tokens[6].token)
        self.assertEqual('AND_ITEM', tokens[7].token)
        self.assertEqual('TEXT', tokens[8].token)
        self.assertEqual('OR_ITEM', tokens[9].token)
        self.assertEqual('OR_ITEM', tokens[10].token)
        self.assertEqual('OR_ITEM', tokens[11].token)
        self.assertEqual('TEXT', tokens[12].token)
        self.assertEqual('BREAK', tokens[13].token)
        self.assertEqual('TEXT', tokens[14].token)

    def test_heading(self):
        """
        Ensures headings are correctly identified in various contexts.
        """
        # A heading that will eventually become <h1>
        data = "= A heading ="
        tokens = get_tokens(data)
        self.assertEqual("HEADING", tokens[0].token)
        self.assertEqual("A heading", tokens[0].value)
        self.assertEqual(1, tokens[0].size)
        # A heading that will eventually become <h6>
        data = "====== A small heading ======"
        tokens = get_tokens(data)
        self.assertEqual("HEADING", tokens[0].token)
        self.assertEqual("A small heading", tokens[0].value)
        self.assertEqual(6, tokens[0].size)
        # A heading can include punctuation characters too
        data = "== This is a heading! (Or so it would seem) =="
        tokens = get_tokens(data)
        self.assertEqual("HEADING", tokens[0].token)
        self.assertEqual("This is a heading! (Or so it would seem)",
            tokens[0].value)
        self.assertEqual(2, tokens[0].size)

    def test_text(self):
        """
        Ensures paragraphs of text are correctly identified in various contexts.

        Since this is a rather greedy regex I'm testing that it doesn't gobble
        up the others too.
        """
        # Do not misidentify headers
        data ="= Not text ="
        tokens = get_tokens(data)
        self.assertNotEqual("TEXT", tokens[0].token)
        # Do not misidentify comments
        data ="// Not text"
        tokens = get_tokens(data)
        self.assertEqual(0, len(tokens))
        # Do not misidentify AND items
        data ="[] Not text"
        tokens = get_tokens(data)
        self.assertNotEqual("TEXT", tokens[0].token)
        # Do not misidentify OR items
        data ="() Not text"
        tokens = get_tokens(data)
        self.assertNotEqual("TEXT", tokens[0].token)
        # Do not misidentify breaks
        data ="----"
        tokens = get_tokens(data)
        self.assertNotEqual("TEXT", tokens[0].token)
        # Some real text
        data = "This is some text"
        tokens = get_tokens(data)
        self.assertEqual("TEXT", tokens[0].token)
        self.assertEqual("This is some text", tokens[0].value)

    def test_comments_ignored(self):
        """
        Ensures comments (//) are ignored.
        """
        data = "// This is a comment\n// So is this\n\n// One final comment."
        tokens = get_tokens(data)
        self.assertEqual(0, len(tokens),
            "Got tokens when none were expected: %s" % tokens)

    def test_and_item(self):
        """
        Ensures items that can be ANDed together are correctly identified.
        """
        data = "[] An item\n[] An item\n\n[] An item"
        tokens = get_tokens(data)
        self.assertEqual(3, len(tokens),
            "Got the wrong number of tokens: %s" % tokens)
        for t in tokens:
            self.assertEqual("AND_ITEM", t.token)
            self.assertEqual("An item", t.value)

    def test_and_item_with_roles(self):
        """
        Ensures items may have roles assigned to them via a list in curly
        brackets.
        """
        data = "[] {doctor, nurse} An item\n[] An item"
        tokens = get_tokens(data)
        self.assertEqual(2, len(tokens),
            "Got the wrong number of tokens: %s" % tokens)
        self.assertEqual("AND_ITEM", tokens[0].token)
        self.assertEqual("An item", tokens[0].value)
        self.assertEqual(['doctor', 'nurse'], tokens[0].roles)
        self.assertEqual("AND_ITEM", tokens[1].token)
        self.assertEqual("An item", tokens[1].value)
        self.assertEqual(None, tokens[1].roles)

    def test_or_item(self):
        """
        Ensures items that can be ORed together are correctly identified.
        """
        data = "() An item\n() An item\n\n() An item"
        tokens = get_tokens(data)
        self.assertEqual(3, len(tokens),
            "Got the wrong number of tokens: %s" % tokens)
        for t in tokens:
            self.assertEqual("OR_ITEM", t.token)
            self.assertEqual("An item", t.value)

    def test_or_item_with_roles(self):
        """
        Ensures items may have roles assigned to them via a list in curly
        brackets.
        """
        data = "() {doctor, nurse} An item\n() An item"
        tokens = get_tokens(data)
        self.assertEqual(2, len(tokens),
            "Got the wrong number of tokens: %s" % tokens)
        self.assertEqual("OR_ITEM", tokens[0].token)
        self.assertEqual("An item", tokens[0].value)
        self.assertEqual(['doctor', 'nurse'], tokens[0].roles)
        self.assertEqual("OR_ITEM", tokens[1].token)
        self.assertEqual("An item", tokens[1].value)
        self.assertEqual(None, tokens[1].roles)

    def test_break(self):
        """
        Ensures that break token is correctly identified.
        """
        # Breaks need to be 3 or more minus signs otherwise they match TEXT
        data = "--"
        tokens = get_tokens(data)
        self.assertEqual("TEXT", tokens[0].token)
        # A legitimate break
        data = "---"
        tokens = get_tokens(data)
        self.assertEqual("BREAK", tokens[0].token)
