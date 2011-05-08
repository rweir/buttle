import unittest

from buttle.parser import tokenise

class TokeniserTests(unittest.TestCase):
    def test_tokenise(self):
        line = """["Jane" "Doe" nil "Fake Pty Ltd" (["Mobile" "+61 4123 456 789"] ["Home" "61 2 9876 5432"]) nil ("someone@example.com") ((creation-date . "2001-01-01") (timestamp . "2002-02-02")) nil]"""
        tokens = ["Jane", "Doe", "nil", "Fake Pty Ltd", [["Mobile", "+61 4123 456 789"], ["Home", "61 2 9876 5432"]], 'nil', ["someone@example.com"], [['creation-date', "2001-01-01"], ['timestamp', "2002-02-02"]], 'nil']
        self.assertEqual(tokenise(line), tokens)
