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
                   "md_infortmation":self._makeMdinformation(),
                   "optional_block":self._makeOptBlock()
                   }

        jsondict={
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
                "name":self.filename[-1],
                "index":"",
            },
            "path":self.path[-1],
            "output":self.output,
            "path_pdb":self.path_pdb[-1],
            "path_ini":self.path_ini[-1],

            "path_para":self.path_para[-1],
        }
        
        ####optional keys
        if self.path_aicg:
            _filenamesdict["path_aicg"]=self.path_aicg[-1]

        if self.path_msf:
            _filenamesdict["path_msf"]=self.path_msf[-1]

        if self.path_natinfo:
            _filenamesdict["path_natinfo"]=self.path_natinfo[-1]
        ####

        return _filenamesdict
        

    def _makeJobcntl(self):
        _jobcntldict={
            "i_run_mode":self.i_run_mode[-1],
            "i_simulate_type":self.i_simulate_type[-1],
            "i_initial_state":self.i_initial_state[-1],
            }

        ####optional keys        
        if self.i_initial_velo:
            _jobcntldict["i_initial_velo"]=self.i_initial_velo[-1]
        if self.i_periodic:
            _jobcntldict["i_periodic"]=self.i_periodic[-1]
        ####
        return _jobcntldict
        

    def _makeUnitandstate(self):
        _unitandstatedict={
            "i_seq_read_style":self.i_seq_read_style[-1],
            "i_go_native_read_style":self.i_go_native_read_style[-1],
            "read_pdb":self.read_pdb[-1],
        }

        ####optional keys        
        ####

        return _unitandstatedict


    def _makeEnergyfunction(self):
        _energyfunctiondict={
            "local":self.local,
            "nlocal":self.nlocal,
            "i_use_atom_protein":self.i_use_atom_protein[-1]
        }

        ####optional keys        
        if self.i_use_atom_dna:
            _energyfunctiondict["i_use_atom_dna"]=self.i_use_atom_dna[-1]
        if self.i_output_energy_style:
            _energyfunctiondict["i_output_energy_style"]=self.i_output_energy_style[-1]
        if self.i_flp:
            _energyfunctiondict["i_flp"]=self.i_flp[-1]
        if self.i_triple_angle_term:
            _energyfunctiondict["i_triple_angle_term"]=self.i_triple_angle_term[-1]
        ####

        return _energyfunctiondict


    def _makeMdinformation(self):
        _mdinformationdict={
            'n_step_sim':self.n_step_sim[-1],
            'n_tstep':self.n_tstep[-1],
            'tstep_size':self.tstep_size[-1],
            'n_step_save':self.n_step_save[-1],
            'n_step_neighbor':self.n_step_neighbor[-1],
            'tempk':self.tempk[-1],
            'n_seed':self.n_seed[-1],
            'i_com_zeroing':self.i_com_zeroing[-1],
            'i_no_trans_rot':self.i_no_trans_rot[-1],
        }
        
        ####optional keys        
        if self.n_step_rst:
            _mdinformationdict['n_step_rst']=self.n_step_rst[-1]
        if self.i_rand_type:
            _mdinformationdict['i_rand_type']=self.i_rand_type[-1]
        if self.i_com_zeroing_ini:
            _mdinformationdict['i_com_zeroing_ini']=self.i_com_zeroing_ini[-1]
        ####
        
        return _mdinformationdict


    def _makeOptBlock(self):
        _optblockdict={}
        
        if self.b_aicg:
            _optblockdict["aicg"]={
                "i_aicg":self.i_aicg[-1]
            }
            
        if self.b_electrostatic:
            _optblockdict["electrostatic"]={
                "cutoff":self.cutoff[-1],
                "ionic_strength":self.ionic_strength[-1],
                "diele_water":self.diele_water[-1],
                "i_diele":self.diele_water[-1],
            }

        if self.b_flexible_local:
            _optblockdict["flexible_local"]={
                "k_dih":self.k_dih[-1],
                "k_ang":self.k_ang[-1],
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
    

