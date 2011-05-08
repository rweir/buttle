import unittest
from datetime import date

from buttle.parser import parse_line

class FunctionalTests(unittest.TestCase):
    def test_parse_row(self):
        line = """["Jane" "Doe" nil "Fake Pty Ltd" (["Mobile" "+61 4123 456 789"] ["Home" "61 2 9876 5432"]) nil ("someone@example.com") ((creation-date . "2001-01-01") (timestamp . "2002-02-02")) nil]"""
        r = parse_line(line)
        self.assertEqual(r['firstname'], 'Jane')
        self.assertEqual(r['lastname'], 'Doe')
        self.assertEqual(r['company'], 'Fake Pty Ltd')
        self.assertEqual(r['phone']['Mobile'], '+61 4123 456 789')
        self.assertEqual(r['phone']['Home'], '61 2 9876 5432')
        self.assertEqual(r['email'], 'someone@example.com')
        self.assertEqual(r['created'], date(2001, 01, 01))
