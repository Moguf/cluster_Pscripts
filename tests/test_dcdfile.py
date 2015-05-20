#!/usr/bin/env python
import unittest

from dcdfile import DcdFile,DcdFile2,DcdHeader

class TestDcdHeader(unittest.TestCase):
    def test_show(self):
        pass

    def test_iter(self):
        pass


class TestDcdFile(unittest.TestCase):
    def setUp(self):
        self.dcd=DcdFile()
        
    def test_read(self):
        self.dcd.read("../test/inp/2gxa.dcd")
        self.dcd.read("../test/inp/test.dcd")
        self.assertEquals(1,1)
        
    def test_readOneStep(self):
        pass
        
    def test_close(self):
        pass

    def test_getitem(self):
        pass
        
    def test_iter(self):
        pass

    def test_str(self):
        pass

    def test_setUnit(self):
        pass


class TestDcdFile2(unittest.TestCase):
    def setUp(self):
        self.dcd2=DcdFile2()


    def test_unitSet(self):
        self.dcd2.read("../test/inp/mc1z14t300n1.dcd")
        self.assertEquals(self.dcd2.unitSet(1),2)


def test_suite():
    """builds the test suite."""
    def _suite(test_class):
        return unittest.makeSuite(test_class)
    suite =unittest.TestSuite()
    suite.addTests(_suite(TestDcdFile))

if __name__=="__main__":
    #unittest.main(defaultTest='test_suite')
    unittest.main()
