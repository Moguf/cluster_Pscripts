#!/usr/bin/env python2.7
#coding:utf-8
#editor:ono
#This script makes input files and submits queue.

import sys
import subprocess
import json
import os
import copy
import itertools

from cafemol_style import CafemolStyleInp

class SubmitQueue:
    def __init__(self,inpfile):
        _jdata=open(inpfile,"r")
        self.jsondata=json.load(_jdata)
        
        self.iterlist=[]
        #This list is needed to make input file on many value.
        #If there is a list in json, iterlist.the list).
        
        self.BASEDIR=""
        self.OUTDIR=""
        self.INPDIR=""


    def main(self):
        self._makeInputFile()
        self._submitQueue()


    def _makeInputFile(self):
        self.jsondata["inputfile"]
        self.cafestyle=CafemolStyleInp()
        
        self._checkBlock()
        self._checkBasedir()

        self._readFilenames()
        self._readJobCntl()
        self._readEnergyFunction()
        self._readUnitAndState()
        self._readMdInformation()
        self._readOptionalBlock()
        
        self._makeInputs()
        
        
    def _readFilenames(self):
        txtlist=[]
        self.cafestyle.filename=self.jsondata["inputfile"]["filenames"]["filename"]
        self.cafestyle.path = self.jsondata["inputfile"]["filenames"]["path"]
        self.cafestyle.OUTPUT = self.jsondata["inputfile"]["filenames"]["OUTPUT"]
        self.cafestyle.path_pdb = self.jsondata["inputfile"]["filenames"]["path_pdb"]
        self.cafestyle.path_ini = self.jsondata["inputfile"]["filenames"]["path_ini"]
        self.cafestyle.path_para = self.jsondata["inputfile"]["filenames"]["path_para"]
        
        ### optional parts
        if self.jsondata["inputfile"]["filenames"].has_key("path_aicg"):
            self.cafestyle.path_aicg = self.jsondata["inputfile"]["filenames"]["path_aicg"]
        if self.jsondata["inputfile"]["filenames"].has_key("path_msf"):
            self.cafestyle.path_msf = self.jsondata["inputfile"]["filenames"]["path_msf"]
        if self.jsondata["inputfile"]["filenames"].has_key("path_natinfo"):
            self.cafestyle.path_natinfo = self.jsondata["inputfile"]["filenames"]["path_natinfo"]        
            

    def _readJobCntl(self):
        self.cafestyle.i_run_mode = self.jsondata["inputfile"]["job_cntl"]["i_run_mode"]
        self.cafestyle.i_simulate_type = self.jsondata["inputfile"]["job_cntl"]["i_simulate_type"]
        self.cafestyle.i_initial_state = self.jsondata["inputfile"]["job_cntl"]["i_initial_state"]

        ### optional parts
        if self.jsondata["inputfile"]["job_cntl"].has_key("i_initial_velo"):
            self.cafestyle.i_initial_velo = self.jsondata["inputfile"]["job_cntl"]["i_initial_velo"]
        if self.jsondata["inputfile"]["job_cntl"].has_key("i_periodic"):
            self.cafestyle.i_periodic = self.jsondata["inputfile"]["job_cntl"]["i_periodic"]


    def _readEnergyFunction(self):
        self.cafestyle.LOCAL = self.jsondata["inputfile"]["energy_function"]["LOCAL"]
        self.cafestyle.NLOCAL = self.jsondata["inputfile"]["energy_function"]["NLOCAL"]
        self.cafestyle.i_use_atom_protein = self.jsondata["inputfile"]["energy_function"]["i_use_atom_protein"]
        ### optional parts
        if self.jsondata["inputfile"]["energy_function"].has_key("i_use_atom_dna"):
            self.cafestyle.i_use_atom_dna = self.jsondata["inputfile"]["energy_function"]["i_use_atom_dna"]
        if self.jsondata["inputfile"]["energy_function"].has_key("i_output_energy_style"):
            self.cafestyle.i_output_energy_style = self.jsondata["inputfile"]["energy_function"]["i_output_energy_style"]
        if self.jsondata["inputfile"]["energy_function"].has_key("i_flp"):
            self.cafestyle.i_flp = self.jsondata["inputfile"]["energy_function"]["i_flp"]
        if self.jsondata["inputfile"]["energy_function"].has_key("i_triple_angle_term"):
            self.cafestyle.i_triple_angle_term = self.jsondata["inputfile"]["energy_function"]["i_triple_angle_term"]


    def _readUnitAndState(self):
        self.cafestyle.i_seq_read_style = self.jsondata["inputfile"]["unit_and_state"]["i_seq_read_style"]
        self.cafestyle.i_go_native_read_style = self.jsondata["inputfile"]["unit_and_state"]["i_go_native_read_style"]
        self.cafestyle.read_pdb = self.jsondata["inputfile"]["unit_and_state"]["read_pdb"]


    def _readMdInformation(self):
        self.cafestyle.n_step_sim = self.jsondata["inputfile"]["md_information"]["n_step_sim"] 
        self.cafestyle.n_tstep = self.jsondata["inputfile"]["md_information"]["n_tstep"] 
        self.cafestyle.tstep_size = self.jsondata["inputfile"]["md_information"]["tstep_size"] 
        self.cafestyle.n_step_save = self.jsondata["inputfile"]["md_information"]["n_step_save"] 

        self.cafestyle.n_step_neighbor = self.jsondata["inputfile"]["md_information"]["n_step_neighbor"]
        self.cafestyle.tempk = self.jsondata["inputfile"]["md_information"]["tempk"] 
        self.cafestyle.n_seed = self.jsondata["inputfile"]["md_information"]["n_seed"] 
        self.cafestyle.i_com_zeroing = self.jsondata["inputfile"]["md_information"]["i_com_zeroing"] 
        self.cafestyle.i_no_trans_rot = self.jsondata["inputfile"]["md_information"]["i_no_trans_rot"] 
        
        ####optional parameters
        if self.jsondata["inputfile"]["md_information"].has_key("i_com_zeroing_ini"):
            self.cafestyle.i_com_zeroing_ini = self.jsondata["inputfile"]["md_information"]["i_com_zeroing_ini"] 
        if self.jsondata["inputfile"]["md_information"].has_key("i_rand_type"):
            self.cafestyle.i_rand_type = self.jsondata["inputfile"]["md_information"]["i_rand_type"]
        if self.jsondata["inputfile"]["md_information"].has_key("n_step_rst"):
            self.cafestyle.n_step_rst = self.jsondata["inputfile"]["md_information"]["n_step_rst"] 
        if self.jsondata["inputfile"]["md_information"].has_key("i_implig"):
            self.cafestyle.i_implig = self.jsondata["inputfile"]["md_information"]["i_implig"] 
        if self.jsondata["inputfile"]["md_information"].has_key("i_redef_para"):
            self.cafestyle.i_redef_para = self.jsondata["inputfile"]["md_information"]["i_redef_para"] 
        if self.jsondata["inputfile"]["md_information"].has_key("i_energy_para"):
            self.cafestyle.i_energy_para = self.jsondata["inputfile"]["md_information"]["i_energy_para"] 
        if self.jsondata["inputfile"]["md_information"].has_key("i_neigh_dist"):
            self.cafestyle.i_neigh_dist = self.jsondata["inputfile"]["md_information"]["i_neigh_dist"] 
        if self.jsondata["inputfile"]["md_information"].has_key("i_mass"):
            self.cafestyle.i_mass = self.jsondata["inputfile"]["md_information"]["i_mass"] 
        if self.jsondata["inputfile"]["md_information"].has_key("i_fric"):
            self.cafestyle.i_fric = self.jsondata["inputfile"]["md_information"]["i_fric"] 
        if self.jsondata["inputfile"]["md_information"].has_key("i_mass_fric"):
            self.cafestyle.i_mass_fric = self.jsondata["inputfile"]["md_information"]["i_mass_fric"]
        if self.jsondata["inputfile"]["md_information"].has_key("i_del_int"): 
            self.cafestyle.i_del_int = self.jsondata["inputfile"]["md_information"]["i_del_int"] 
        if self.jsondata["inputfile"]["md_information"].has_key("i_anchor"):
            self.cafestyle.i_anchor = self.jsondata["inputfile"]["md_information"]["i_anchor"] 
        if self.jsondata["inputfile"]["md_information"].has_key("i_rest1d"):
            self.cafestyle.i_rest1d = self.jsondata["inputfile"]["md_information"]["i_rest1d"] 
        if self.jsondata["inputfile"]["md_information"].has_key("i_bridge"):
            self.cafestyle.i_bridge = self.jsondata["inputfile"]["md_information"]["i_bridge"] 
        if self.jsondata["inputfile"]["md_information"].has_key("i_pulling"):
            self.cafestyle.i_pulling = self.jsondata["inputfile"]["md_information"]["i_pulling"] 
        if self.jsondata["inputfile"]["md_information"].has_key("i_fix"):
            self.cafestyle.i_fix = self.jsondata["inputfile"]["md_information"]["i_fix"] 
        if self.jsondata["inputfile"]["md_information"].has_key("i_in_box"):
            self.cafestyle.i_in_box = self.jsondata["inputfile"]["md_information"]["i_in_box"] 
        if self.jsondata["inputfile"]["md_information"].has_key("i_in_cap"):
            self.cafestyle.i_in_cap = self.jsondata["inputfile"]["md_information"]["i_in_cap"] 
        if self.jsondata["inputfile"]["md_information"].has_key("i_modified_muca"):
            self.cafestyle.i_modified_muca = self.jsondata["inputfile"]["md_information"]["i_modified_muca"] 


    def _readOptionalBlock(self):
        #### aicg 
        if self.b_aicg:
            self.cafestyle.i_aicg = self.jsondata["inputfile"]["optional_block"]["aicg"]["i_aicg"]
        #### electrostatic
        if self.b_electrostatic:
            self.cafestyle.cutoff = self.jsondata["inputfile"]["optional_block"]["electrostatic"]["cutoff"]
            self.cafestyle.ionic_strength = self.jsondata["inputfile"]["optional_block"]["electrostatic"]["ionic_strength"]
            self.cafestyle.diele_water = self.jsondata["inputfile"]["optional_block"]["electrostatic"]["diele_water"]
            self.cafestyle.i_diele= self.jsondata["inputfile"]["optional_block"]["electrostatic"]["i_diele"]
        #### flexible_local
        if self.b_flexible_local:
            self.cafestyle.k_dih = self.jsondata["inputfile"]["optional_block"]["flexible_local"]["k_dih"]
            self.cafestyle.k_ang = self.jsondata["inputfile"]["optional_block"]["flexible_local"]["k_ang"]

        
    def _makeShFile(self):
        _shfdata=self.jsondata["queue"]


    def _checkBlock(self):
        print "check Block ...",

        self.b_filenames = self.jsondata["inputfile"].has_key("filenames")
        self.b_job_cntl = self.jsondata["inputfile"].has_key("job_cntl")
        self.b_unit_and_state = self.jsondata["inputfile"].has_key("unit_and_state")
        self.b_energy_function = self.jsondata["inputfile"].has_key("energy_function")
        self.b_md_information = self.jsondata["inputfile"].has_key("md_information")

        ##optional flag
        self.b_electrostatic = self.jsondata["inputfile"]["optional_block"].has_key("electrostatic")
        self.b_flexible_local = self.jsondata["inputfile"]["optional_block"].has_key("flexible_local")
        self.b_aicg = self.jsondata["inputfile"]["optional_block"].has_key("aicg")
        
        if not (self.b_filenames and \
           self.b_job_cntl and \
           self.b_unit_and_state and \
           self.b_energy_function and \
           self.b_md_information):
            raise Exception("Bock fields Error, Please check it.")
        
        print " OK!!!"


    def _checkBasedir(self):
        self.BASEDIR=self.jsondata["BASEDIR"]
        if not self.BASEDIR:
            self.BASEDIR=os.path.os.path.abspath(os.path.dirname(__file__))
            print "BASEDIR is set to current dir(%s)."  % self.BASEDIR
        else:
            tmp=self.jsondata["BASEDIR"]
            self.BASEDIR=os.path.os.path.abspath(os.path.expanduser(tmp))
            print "BASEDIR is set to dir(%s)."  % self.BASEDIR
            

    def _makeInputs(self):
        looplist=[]
        ignorelist=["OUTPUT","NLOCAL","LOCAL","n_tstep","read_pdb"]
        for ikey in self.cafestyle.__dict__.keys():
            if isinstance(self.cafestyle.__dict__[ikey],list):
                if not ikey in ignorelist:
                    tmplist=self._listsubsitution(self.cafestyle.__dict__[ikey])
                    looplist.append(tmplist)
                    


    def _listsubsitution(self,inlist):
        if len(inlist)==1:
            return range(1,inlist[0]+1)
        elif len(inlist)==3:
            return range(int(inlist[0]),int(inlist[1])+int(inlist[2]),int(inlist[2]))
        else:
            return inlist
            

    def _submitQueue(self):
        pass
    
    def _determineCount(self):
        
        pass


if __name__ == "__main__":
    test=SubmitQueue('./test/inp/inp.json')
    test.main()
    
