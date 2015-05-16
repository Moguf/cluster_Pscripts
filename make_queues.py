#!/usr/bin/env python2.7
#coding:utf-8
#editor:ono
#This script makes input files and submits queue.
import os
import argparse
import subprocess


class Queue:
    def __init__(self):
        self.core=1
        self.name="test"
        self.queue=""
        self.exedir=""
        self.inpdir=""
        

    def write(self,ofile="test.sh"):
        wfile=open(ofile,'w')
        otxt=""
        otxt+="#!/bin/sh\n\n"
        otxt+="#$ -S /bin/sh\n"
        otxt+="#$ -cwd\n"
        otxt+="#$ -V\n"
        otxt+="#$ -N "+self.name+"\n"
        otxt+="#$ -o "+self.inpdir+"log/"+self.name+".log"+"\n"
        otxt+="#$ -e "+self.inpdir+"err/"+self.name+".err"+"\n"
        otxt+="#$ -q "+self.queue+"\n"
        otxt+="#$ -pe smp "+str(self.core)+"\n\n"

        otxt+="OMP_NUM_THREADS="+str(self.core)+"\n"
        otxt+=self.exedir+"/cafemol"+" "+self.inpdir+self.name+".inp"+"\n"

        wfile.write(otxt)
        wfile.close()



class MakeQueues:
    def __init__(self):
        self.WORKDIR=""
        self.exedir=""
        self.core="1"
        self.queue="all.q"


    def main(self,workdir,exedir):       ## from other scripts
        self.exedir=exedir
        self.setWORKDIR(workdir)
        self.mkdirErrLog()
        self.makeShfiles()


    def test(self):       ## from commndline
        self._initArg()
        self.mkdirErrLog()
        self.makeShfiles()


    def makeShfiles(self):
        cmdline="ls "+self.WORKDIR+"*.inp"
        inplist=subprocess.check_output([cmdline],shell=True).split()
        queue=Queue()
        queue.exedir=self.exedir
        queue.core=self.core
        queue.inpdir=self.WORKDIR
        queue.queue=self.queue
        for iinp in inplist:
            inpname=iinp.split('/')[-1].split('.')[0]
            queue.name=inpname
            queue.write(self.WORKDIR+inpname+".sh")
    

    def setQueue(self,queuename):
        self.queue=str(queuename)


    def setCore(self,num):
        self.core=str(num)

        
    def mkdirErrLog(self):
        if not os.path.exists(self.WORKDIR+"log"):
            os.mkdir(self.WORKDIR+"log")
        if not os.path.exists(self.WORKDIR+"err"):
            os.mkdir(self.WORKDIR+"err")


    def setWORKDIR(self,workdir):
        if workdir[-1]!='/':
            workdir=workdir+'/'
        if workdir[0]!='/':
            workdir='/'+workdir
        if os.path.exists(workdir):
            self.WORKDIR=workdir
            print "WORKDIR is set to "+self.WORKDIR
            return True

        self.WORKDIR=os.path.dirname(os.path.abspath(__file__))+workdir
        print "WORKDIR is set to "+self.WORKDIR

        if not os.path.exists(self.WORKDIR):
            raise Exception("CAUTION!! Check input directory path.")


    def _initArg(self):
        parser = argparse.ArgumentParser(description='make queue.sh')
        parser.add_argument('inputdir',nargs='?',help="input dir-path which has cafemol-inputsfile[.inp]")
        self.setWORKDIR(parser.parse_args().inputdir)


if __name__=="__main__":
    ###python make_queues.py test/inp/mvmmon400/
    test=MakeQueues()
    test.test()
