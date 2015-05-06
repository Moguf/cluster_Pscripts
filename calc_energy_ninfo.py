#!/usr/bin/env pythn2.7
import argparse

from read_ninfo import ReadNinfo

class CalcEnergyNinfo(ReadNinfo):
    def __init__(self):
        ReadNinfo.__init__(self)
        self.args = []
        self.inputfile= ""

        self._initArg()
        self._checkArg()
        
        self.read(self.inputfile)


    def calc(self):
        # I need to refine this part in future:
        # I can't calcurate contact 1 2 or 19 29 ...
        if len(self.protein_number)<2:
            energy=0
            for ilist in self.data[self.datatype]:
                if (ilist[1] == int(self.protein_number[0])) and (ilist[1]==ilist[2]):
                    ### (protein number == unit1) and (unit1 == unit2)
                    energy+=ilist[-2]
                    ### energy+= coef_** from ninfo
            return energy;
        else:
            energy=0            
            partial_energy={}
            for ilist in self.data[self.datatype]:
                if (ilist[1] == int(self.protein_number[0])) and (self.protein_number[1]=="all"):
                    if ilist[1]!=ilist[2]:
                        key="%d-%d" % (ilist[1],ilist[2])
                        try:
                            partial_energy[key][0]+=1
                            partial_energy[key][1]+=ilist[-2]
                        except:
                            partial_energy[key]=[1,ilist[-2]]
                            
                        energy+=ilist[-2]
            partial_energy['all']=energy
            return partial_energy
            
            
    def _initArg(self):
        parser = argparse.ArgumentParser(description='calculate total interaction energy from native-information')
        parser.add_argument('inputfile',nargs='?',help="input-file[.ninfo]")
        parser.add_argument('-t','--datatype',choices=["bond","angl","aicg13","aicgdih","dihd","contact"],help="you can choice one type. Default is contact",default='contact')
        parser.add_argument('-n','--number',nargs="*",help="Chocie protein number index. If you enter 1 3, caluculate 1-3 energy in contacts",default='1')
        self.args = parser.parse_args()
        self.inputfile=self.args.inputfile
        self.datatype=self.args.datatype
        self.protein_number=self.args.number


    def _checkArg(self):
        if len(self.protein_number)>=2 and (self.datatype != "contact"):
            raise NameError("if you input -n 1 2 3 ... all, you can must choice 'contact' in -t.")

        
if __name__=="__main__":
    #python calc_energy_ninfo.py ./test/inp/test.ninfo --datatype contact -n 1 all
    test=CalcEnergyNinfo()
    print test.calc()


