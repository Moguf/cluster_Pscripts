#!/usr/bin/env python

import unittest

from calc_interintra_contacts import CalcInterIntraContacts as ciic

class TestCalcInterIntraContacts(unittest.TestCase):
    def setUp(self):
        print 'Creating new CalcInterIntraContacts ...'
        self.ciic = ciic()

    def test_readPDB(self):
        self.ciic.readPDB()

    def tearDown(self):
        print 'Destroying the CalcInterIntraContacts ...'
        self.ciic = None

if __name__ == '__main__':
    unittest.main()
