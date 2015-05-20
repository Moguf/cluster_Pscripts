#!/usr/bin/env python
import unittest

from calc_RMSF_dcd import CalcRmsf

class TestCalcRMSF(unittest.TestCase):
    def test_read(self):
        pass

    def test_doPy(self):
        pass
    


def test_suite():
    """builds the test suite."""
    def _suite(test_class):
        return unittest.makeSuite(test_class)
    suite =unittest.TestSuite()
    suite.addTests(_suite(TestDcdFile))

if __name__=="__main__":
    #unittest.main(defaultTest='test_suite')
    unittest.main()
