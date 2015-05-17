#!/bin/usr/env python
# coding: utf-8
# editor: ono

# Standard libraries
import argparse

# Third party libraries

# My libraries


class MyTemplateClass:
    def __init__(self):
        self.inputfile=""


    def main(self):
        self._initArg()
        self.func1(self.inputfile)
        

    def func1(self,inputfile):
        self._funcInFunc1()


    def _funcInFunc1(self):
        pass


    def _initArg(self):
        self.inputfile="argparse......."


    def test(self):
        self.func1("./test/test.inp")


if __name__=="__main__":
    test=DcdFile()
    #test.test()
    test.main()
