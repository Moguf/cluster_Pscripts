#!/bin/usr/env python
#coding:utf-8
#editor:ono
#This script makes json-style-input-file from cafemol input file.
import json

from cafemol_style import CafemolStyleInp


class MakeCafeJson(CafemolStyleInp):
    def __init__(self):
        CafemolStyleInp.__init__(self)
        self.job_name=""
        self.job_core=1
        self.job_quete=""
        

    def main(self,inpfile):
        self.read(inpfile)
        self.check()
        self.makeJson()
        

    def makeJson(self,outjson="./test/out/out.json"):
        inputdict={"filenames":self._makeFilnames(),
                   "job_cntl":self._makeJobcntl(),
                   "unit_and_state":self._makeUnitandstate(),
                   "energy_function":self._makeEnergyfunction(),
                   "md_information":self._makeMdinformation(),
                   "optional_block":self._makeOptBlock()
                   }

        jsondict={
            "BASEDIR":"",
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
                "i_diele":self.diele_water,
            }

        if self.b_flexible_local:
            _optblockdict["flexible_local"]={
                "k_dih":self.k_dih,
                "k_ang":self.k_ang,
            }
            

        return _optblockdict


    def _makeQueue(self):
        _queuedic={
            "1":"#!/bin/sh",
            "2":"#$ -S /bin/sh",
            "3":"#$ -V", 
            "4":"#$ -N ",
            "5":"#$ -o ",
            "6":"#$ -q ",
            "7":"#$ -pe smp ",
            "8":"OMP_NUM_THREADS =",
            "9":"./cafemol ./inp/test.inp"
        }
        
        return _queuedic
        
if __name__ == "__main__":
    test = MakeCafeJson()
    test.main("./test/inp/test.inp")
    

