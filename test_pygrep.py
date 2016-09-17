import re
import unittest

from pygrep import search


class TestPygrep(unittest.TestCase):

    def test_num_matches_single_file(self):
        query = 'laugh'
        pattern = re.compile(r'(' + query + ')')
        matches = search('examples/sherlock.txt', pattern)
        self.assertEqual(len(list(matches)), 48)

    def test_num_matches_directory(self):
        query = 'Author:'
        pattern = re.compile(r'(' + query + ')')
        matches = search('examples', pattern)
        self.assertEqual(len(list(matches)), 6)


if __name__ == '__main__':
    unittest.main()
