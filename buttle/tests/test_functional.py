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
        self.assertEqual(r['email'], ['someone@example.com'])
        self.assertEqual(r['random']['creation-date'], date(2001, 01, 01))

    def test_parse_has_no_phone_number(self):
        line = """["Jane" "Doe" nil "Fake Pty Ltd" nil nil ("someone@example.com") ((creation-date . "2001-01-01") (timestamp . "2002-02-02")) nil]"""
        r = parse_line(line)
        self.assertEqual(r['phone'], {})

    def test_parse_comment_line(self):
        line = """;; this is a comment"""
        r = parse_line(line)
        self.assertEqual(r, {})

    def test_parse_has_no_surname(self):
        line = """["Jane" "" nil "Fake Pty Ltd" nil nil ("someone@example.com") ((creation-date . "2001-01-01") (timestamp . "2002-02-02")) nil]"""
        r = parse_line(line)
        self.assertEqual(r['firstname'], 'Jane')
        self.assertEqual(r['lastname'], '')
        self.assertEqual(r['company'], 'Fake Pty Ltd')

    def test_parse_multiple_emails(self):
        line = """["Jane" "" nil "Fake Pty Ltd" nil nil ("someone@example.com" "someoneelse@example.com") ((creation-date . "2001-01-01") (timestamp . "2002-02-02")) nil]"""
        r = parse_line(line)
        self.assertEqual(r['email'][0], 'someone@example.com')
        self.assertEqual(r['email'][1], 'someoneelse@example.com')
