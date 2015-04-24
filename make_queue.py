#! /usr/bin/env python
import sys

import read_inp

class MakeQueue:
    def __init__(self,_inpfile):
        self.inpfile=_inpfile
        self.shfile=""
        

    def main(self):
        self.readInp()
    

    def readInp(self):
        inpinst=read_inp.inpfile(self.inpfile)
        inpinst.write("outfile")

        
    def readSh(self,_rfile):
        self.shfile=_rfile
        
        
if __name__=="__main__":
    #How to use
    #scirpt.py template.inp
    test=MakeQueue(sys.argv[1])
    test.main()
