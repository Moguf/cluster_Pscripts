#!/usr/bin/env python2.7
#coding:utf-8
#editor:ono
#This script makes input files and submits queue.
import os
import argparse

class MakeQueue:
    def __init__(self):
        self.core=1
        self.name="test"
        self.logdir=""
        self.queue=""
        self.exedir=""
        self.inpdir=""
        

    def write(self,ofile="test.sh"):
        wfile=open(ofile,'w')
        otxt=""
        otxt+="""#!/bin/sh
        #$ -S /bin/sh
        #$ -cwd
        #$ -V
        """
        otxt+="#$ -N "+self.name+"\n"
        otxt+="#$ -o "+self.logdir+"/log"+self.name+".log"+"\n"
        otxt+="#$ -e "+self.logdir+"/log"+self.name+".err"+"\n"
        otxt+="#$ -q "+self.queue+"\n"
        otxt+="#$ -pe smp "+str(self.core)+"\n\n"

        otxt+="OMP_NUM_THREADS="+str(self.core)+"\n"
        otxt+=exedir+"cafemol"+" "+inpdir+self.name+".inp"+"\n"

        wfile.write(otxt)
        wfile.close()

    def _checkDir(self):
        pass
        


class MakeQueues:
    def __init__(self):
        self.WORKDIR=""

    def main(self):
        self._initArg()
        self._checkArg()

    def _initArg(self):
        parser = argparse.ArgumentParser(description='make queue.sh')
        parser.add_argument('inputdir',nargs='?',help="input dir-path which has cafemol-inputsfile[.inp]")
        self.args = parser.parse_args()
        
    def _checkArg(self):
        if self.args.inputdir[-1]!='/':
            self.args.inputdir=self.args.inputdir+'/'
        if self.args.inputdir[0]!='/':
            self.args.inputdir='/'+self.args.inputdir
        
        print os.path.dirname(os.path.abspath(__file__))+self.args.inputdir
        os.path.exists(self.WORKDIR)


if __name__=="__main__":
    ###python make_queues.py test/inp/mvmmon400/
    test=MakeQueues()
    test.main()
