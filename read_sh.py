#! /usr/bin/env python

import sys

class ReadSh:
    def __init__(self,rfile):
        self.data=open(rfile).readlines()

    def main(self):
        self.change_name("hello")
        self.write("out.sh")


    def change_name(self,name):
        for index,iline in enumerate(self.data):
            if "#$ -N"==iline[:5]:
                self.data[index]="#$ -N %s\n"% str(name)

                
    def change_inp(self,name):
        for index,iline in enumerate(self.data):
            if iline[0]=="/":
                ilist=iline.split()
                _ilist=ilist[1].split("/")
                _ilist[-1]=name
                ilist[1]="/".join(_ilist)
                self.data[index]=" ".join(ilist)

            
    def write(self,ofile):
        otxt=''
        for iline in self.data:
            otxt+=iline
        odata=open(ofile,'w')
        odata.write(otxt)
        odata.close()
        
if __name__=="__main__":
    test=ReadSh(sys.argv[1])
    test.main()
    
