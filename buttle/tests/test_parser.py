import unittest

from buttle.parser import tokenise

class TokeniserTests(unittest.TestCase):
    def test_trivial_tokenise(self):
        line = """["Hi" "There"]"""
        self.assertEqual(tokenise(line), ['Hi', 'There'])

    def test_tokenise_with_multis_that_have_one_value(self):
        line = """[("foo")]"""
        self.assertEqual(tokenise(line), ['(', 'foo', ')'])

    def test_tokenise_with_multis_with_multiple_values(self):
        line = """[("foo" "bar")]"""
        self.assertEqual(tokenise(line), ['(', 'foo', 'bar', ')'])

    def test_tokenise_pair(self):
        line = """[["foo" "bar"]]"""
        self.assertEqual(tokenise(line), ['[', 'foo', 'bar', ']'])

    def test_tokenise_pairs_in_multis(self):
        line = """[(["Mobile" "123"] ["Home" "456"])]"""
        self.assertEqual(tokenise(line), ['(', '[', 'Mobile', '123', ']', '[', 'Home', '456', ']', ')'])

    def test_full_tokenise(self):
        line = """["Jane" "Doe" nil "Fake Pty Ltd" (["Mobile" "+61 4123 456 789"] ["Home" "61 2 9876 5432"]) nil ("someone@example.com") ((creation-date . "2001-01-01") (timestamp . "2002-02-02")) nil]"""
        tokens = ["Jane", "Doe", "nil", "Fake Pty Ltd", '(', '[', "Mobile", "+61 4123 456 789", ']', '[', "Home", "61 2 9876 5432", ']', ')', 'nil', '(', "someone@example.com", ')', '(', '(', 'creation-date', '.', "2001-01-01", ')', '(', 'timestamp', '.', "2002-02-02", ')', ')', 'nil']
        self.assertEqual(tokenise(line), tokens)
