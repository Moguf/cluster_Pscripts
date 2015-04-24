#! /usr/bin/env python
# coding:utf-8
import sys
import subprocess

import read_inp
import read_sh

class GoQueue:
    def __init__(self,_inpfile,_shfile):
        self.inpfile=_inpfile
        self.shfile=_shfile


    def main(self):
        self.makeInp()


    def makeInp(self):
        inp_instance=read_inp.InpFile(self.inpfile)
        sh_instance=read_sh.ReadSh(self.shfile)

        for index,data in enumerate(xrange(300,445,5)):
            #for inp
            for seed in range(10):
                inp_instance.filename('mvmmon'+str(data)+str(seed))
                inp_instance.temp(float(str(data)+".0"))
                inp_instance.seed(seed)
                inp_instance.write("out.inp")
                #for sh
                sh_instance.change_name("mvm"+str(data)+"r"+str(seed))
                sh_instance.write("out.sh")
                #do shell
                #subprocess.call('qsub mvm.sh',shell=True)
        
if __name__=="__main__":
    #How to use
    #scirpt.py template.inp template.sh

    test=GoQueue(sys.argv[1],sys.argv[2])
    test.main()
