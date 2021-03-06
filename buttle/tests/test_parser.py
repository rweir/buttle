import unittest

from buttle.parser import tokenise, parse, fix_up_from_shlex

class TokeniserTests(unittest.TestCase):
    def test_trivial_tokenise(self):
        line = """["Hi" "There"]"""
        self.assertEqual(tokenise(line), ['Hi', 'There'])

    def test_trivial_tokenise_with_spaces(self):
        line = """["Hi There"]"""
        self.assertEqual(tokenise(line), ['Hi There'])

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

class ParserTests(unittest.TestCase):
    def test_parse_pair(self):
        tokens = ['[', 'foo', 'bar', ']']
        self.assertEqual(parse(tokens), [('foo', 'bar')])

    def test_parse_multi(self):
        tokens = ['(', 'foo', ')']
        self.assertEqual(parse(tokens), [['foo']])

    def test_parse_a_bit_complicated(self):
        tokens = tokenise("""["Jane" "Doe" nil nil (["Mobile" "+61 4123 456 789"])]""")
        self.assertEqual(parse(tokens), ['Jane', 'Doe', 'nil', 'nil', [("Mobile", "+61 4123 456 789")]])

    def test_parse_multi_pairs(self):
        tokens = ["(", "[", "foo", "bar", "]", ")", "(", "[", "baz", "bong", "]", ")"]
        self.assertEqual(parse(tokens), [[("foo", "bar")], [("baz", "bong")]])

    def test_parse_assoc_array(self):
        tokens = ["(", "(", "foo", ".", "bar", ")", "(", "baz", ".", "bong", ")", ")"]
        self.assertEqual(parse(tokens), [{'foo': 'bar', 'baz': 'bong'}])

    def test_parse_full_tokenise(self):
        line = """["Jane" "Doe" nil "Fake Pty Ltd" (["Mobile" "+61 4123 456 789"] ["Home" "61 2 9876 5432"]) nil ("someone@example.com") ((creation-date . "2001-01-01") (timestamp . "2002-02-02")) nil]"""
        self.assertEqual(parse(tokenise(line)), ["Jane", "Doe", "nil", "Fake Pty Ltd", [('Mobile', "+61 4123 456 789"), ("Home", "61 2 9876 5432")], 'nil', ["someone@example.com"], {'creation-date': "2001-01-01", 'timestamp': "2002-02-02"}, 'nil'])

class FixUpTests(unittest.TestCase):
    def test_fix_empty(self):
        self.assertEqual(fix_up_from_shlex([]), [])

    def test_fix_ok(self):
        self.assertEqual(fix_up_from_shlex([[1,2]]), [[1,2]])

    def test_fix_single_element_broken(self):
        self.assertEqual(fix_up_from_shlex([[1]]), [[1, ""]])

    def test_fix_multi_element_broken(self):
        self.assertEqual(fix_up_from_shlex([[1], [2]]), [[1, ""], [2, ""]])

    def test_fix_multi_element_tuples_broken(self):
        self.assertEqual(fix_up_from_shlex([(1,), (2,)]), [(1, ""), (2, "")])
