import unittest
from datetime import date

from buttle.parser import parse

class FunctionalTests(unittest.TestCase):
    def test_parse_row(self):
        line = """["Jane" "Doe" nil nil (["Mobile" "+61 4123 456 789"]) nil ("someone@example.com") ((creation-date . "2001-01-01") (timestamp . "2002-02-02")) nil]"""
        r = parse(line)
        self.assertEqual(r['firstname'], 'Jane')
        self.assertEqual(r['lastname'], 'Doe')
        self.assertEqual(r['phone']['Mobile'], '+61 4123 456 789')
        self.assertEqual(r['email'], 'someone@example.com')
        self.assertEqual(r['created'], date(2001, 01, 01))
