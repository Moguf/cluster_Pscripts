#!/home/ono/Python-2.7.9/python
####!/rei_fs1/ono/python/bin/python
#coding:utf-8
#editor:ono
#This script makes json-style-input-file from cafemol input file.

import json
import sys
import argparse
import os

from cafemol_style import CafemolStyleInp

class MakeCafeJson(CafemolStyleInp):
    def __init__(self):
        CafemolStyleInp.__init__(self)
        self.job_core="1"
        self.job_queue="all.q"
        self.inpfile=""

    def main(self):
        self._initArg()
        self.read(self.inpfile)
        self.check()
        self.makeJson(self.outfile)

    def makeJson(self,outjson):
        
        inputdict={"filenames":self._makeFilnames(),
                   "job_cntl":self._makeJobcntl(),
                   "unit_and_state":self._makeUnitandstate(),
                   "energy_function":self._makeEnergyfunction(),
                   "md_information":self._makeMdinformation(),
                   "optional_block":self._makeOptBlock()
                   }

        jsondict={
            "BASEDIR":".",
            "inputfile":inputdict,
            "queue":self._makeQueue()
        }

        jsondata=json.dumps(jsondict,indent=4)
        outfile=open(outjson,"w")
        outfile.write(jsondata)
        outfile.close()
        

    def _makeFilnames(self):
        _filenamesdict={
            "filename":{
                "prefix":"",
                "name":self.filename,
                "index":"",
            },
            "path":self.path,
            "OUTPUT":self.OUTPUT,
            "path_pdb":self.path_pdb,
            "path_ini":self.path_ini,
            "path_para":self.path_para,
        }
        
        ####optional keys
        if self.path_aicg:
            _filenamesdict["path_aicg"]=self.path_aicg

        if self.path_msf:
            _filenamesdict["path_msf"]=self.path_msf

        if self.path_natinfo:
            _filenamesdict["path_natinfo"]=self.path_natinfo
        ####

        return _filenamesdict
        

    def _makeJobcntl(self):
        _jobcntldict={
            "i_run_mode":self.i_run_mode,
            "i_simulate_type":self.i_simulate_type,
            "i_initial_state":self.i_initial_state,
            }

        ####optional keys        
        if self.i_initial_velo:
            _jobcntldict["i_initial_velo"]=self.i_initial_velo
        if self.i_periodic:
            _jobcntldict["i_periodic"]=self.i_periodic
        ####
        return _jobcntldict
        

    def _makeUnitandstate(self):
        _unitandstatedict={
            "i_seq_read_style":self.i_seq_read_style,
            "i_go_native_read_style":self.i_go_native_read_style,
            "read_pdb":self.read_pdb,
        }

        ####optional keys        
        ####

        return _unitandstatedict


    def _makeEnergyfunction(self):
        _energyfunctiondict={
            "LOCAL":self.LOCAL,
            "NLOCAL":self.NLOCAL,
            "i_use_atom_protein":self.i_use_atom_protein
        }

        ####optional keys        
        if self.i_use_atom_dna:
            _energyfunctiondict["i_use_atom_dna"]=self.i_use_atom_dna
        if self.i_output_energy_style:
            _energyfunctiondict["i_output_energy_style"]=self.i_output_energy_style
        if self.i_flp:
            _energyfunctiondict["i_flp"]=self.i_flp
        if self.i_triple_angle_term:
            _energyfunctiondict["i_triple_angle_term"]=self.i_triple_angle_term
        if self.i_coef_from_ninfo:
            _energyfunctiondict["i_coef_from_ninfo"]=self.i_coef_from_ninfo

        ####

        return _energyfunctiondict


    def _makeMdinformation(self):
        _mdinformationdict={
            'n_step_sim':self.n_step_sim,
            'n_tstep':self.n_tstep,
            'tstep_size':self.tstep_size,
            'n_step_save':self.n_step_save,
            'n_step_neighbor':self.n_step_neighbor,
            'tempk':self.tempk,
            'n_seed':self.n_seed,
            'i_com_zeroing':self.i_com_zeroing,
            'i_no_trans_rot':self.i_no_trans_rot,
        }
        
        ####optional keys        
        if self.n_step_rst:
            _mdinformationdict['n_step_rst']=self.n_step_rst
        if self.i_rand_type:
            _mdinformationdict['i_rand_type']=self.i_rand_type
        if self.i_com_zeroing_ini:
            _mdinformationdict['i_com_zeroing_ini']=self.i_com_zeroing_ini
        if self.i_del_int:
            _mdinformationdict['i_del_int']=self.i_del_int
        ####
        
        return _mdinformationdict


    def _makeOptBlock(self):
        _optblockdict={}
        
        if self.b_aicg:
            _optblockdict["aicg"]={
                "i_aicg":self.i_aicg
            }
            
        if self.b_electrostatic:
            _optblockdict["electrostatic"]={
                "cutoff":self.cutoff,
                "ionic_strength":self.ionic_strength,
                "diele_water":self.diele_water,
                "i_diele":self.i_diele,
            }

        if self.b_flexible_local:
            _optblockdict["flexible_local"]={
                "k_dih":self.k_dih,
                "k_ang":self.k_ang,
            }
            
        if self.b_del_interaction:
            _optblockdict["del_interaction"]={
                "DEL_GO":self.DEL_GO,
                "DEL_LGO":self.DEL_LGO
            }
        if self.b_native_info_sim1:
            _optblockdict["native_info_sim1"]={
                "NINFO":self.NINFO
            }


        return _optblockdict


    def _makeQueue(self):
        _queuedic={
            "1":"#!/bin/sh",
            "2":"#$ -S /bin/sh",
            "3":"#$ -V", 
            "4":"#$ -N ",
            "5":"#$ -o ",
            "6":["#$ -q ",self.job_queue],
            "7":["#$ -pe smp ",self.job_core],
            "8":["OMP_NUM_THREADS =",self.job_core],
            "9":"./cafemol ./inp/test.inp",
        }
        
        return _queuedic
        

    def _initArg(self):
        parser = argparse.ArgumentParser(description='This script make json-style of cafemol-inputs')
        parser.add_argument('inputfile',nargs='?',help="input-file[.inp]")
        parser.add_argument('-o','--output',nargs='?',help="output-file[.json]",default='out.json')
        parser.add_argument('-q','--queue',help="you can choice queue",default='all.q')
        parser.add_argument('-c','--core',type=int,choices=range(1,21),help="How many core do you use?In rei up to12.In cyrus upt to 20",default='1')
        

        self.job_core=parser.parse_args().core
        self.job_queue=parser.parse_args().queue
        self.inpfile=parser.parse_args().inputfile
        self.outfile=parser.parse_args().output
        
if __name__ == "__main__":
    #### !!!TEST COMMAND HERE!!!
    #### python make_cafejson.py ./test/inp/test.inp -c 3 -q node01-08.q
    test = MakeCafeJson()
    test.main()
    

