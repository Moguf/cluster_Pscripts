#!/usr/bin/env python2.7
#coding:utf-8
#editor:ono
#This script makes input files and submits queue.

import sys
import subprocess
import json
import os

from cafemol_style import CafemolStyleInp

class SubmitQueue:
    def __init__(self,inpfile):
        _jdata=open(inpfile,"r")
        self.jsondata=json.load(_jdata)
        
        self.iterlist=[]
        #This list is needed to make input file on many value.
        #If there is a list in json, iterlist.the list).
        
        self.BASEDIR=""
        self.WORKDIR=""


    def main(self):
        self._makeInputFile()
        self._submitQueue()


    def _makeInputFile(self):
        self.jsondata["inputfile"]
        self.cafestyle=CafemolStyleInp()
        
        self._checkBlock()
        #self._checkDir()

        self._readFilenames()
        self._readJobCntl()
        self._readEnergyFunction()
        self._readUnitAndState()
        self._readMdInformation()
        self._readOptionalBlock()


        
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


        ###I need to refine this data structure###
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
        self.cafestyle.n_step_sim = self.jsondata["inputfile"]["mf_information"]["read_pdb"] 
        self.cafestyle.n_tstep = False
        self.cafestyle.tstep_size = False
        self.cafestyle.n_step_save = False
        self.cafestyle.n_step_rst = False
        self.cafestyle.n_step_neighbor = False
        self.cafestyle.tempk = False
        self.cafestyle.i_rand_type = False
        self.cafestyle.n_seed = False
        self.cafestyle.i_com_zeroing_ini = False
        self.cafestyle.i_com_zeroing = False
        self.cafestyle.i_no_trans_rot = False
        
        ####optional parameters
        self.cafestyle.i_implig = False
        self.cafestyle.i_redef_para = False
        self.cafestyle.i_energy_para = False
        self.cafestyle.i_neigh_dist = False
        self.cafestyle.i_mass = False
        self.cafestyle.i_fric = False
        self.cafestyle.i_mass_fric = False
        self.cafestyle.i_del_int = False
        self.cafestyle.i_anchor = False
        self.cafestyle.i_rest1d = False
        self.cafestyle.i_bridge = False
        self.cafestyle.i_pulling = False
        self.cafestyle.i_fix = False
        self.cafestyle.i_in_box = False
        self.cafestyle.i_in_cap = False
        self.cafestyle.i_modified_muca = False


    def _readOptionalBlock(self):
        self.cafestyle.i_aicg = False
        #### electrostatic
        self.cafestyle.cutoff = False
        self.cafestyle.ionic_strength = False
        self.cafestyle.diele_water = False
        self.cafestyle.i_diele= False
        #### flexible_local
        self.cafestyle.k_dih = False
        self.cafestyle.k_ang = False

        
    def _makeShFile(self):
        _shfdata=self.jsondata["queue"]


    def _checkBlock(self):
        print "check Block ...",

        self.b_filenames = self.jsondata["inputfile"].has_key("filenames")
        self.b_job_cntl = self.jsondata["inputfile"].has_key("filenames")
        self.b_unit_and_state = self.jsondata["inputfile"].has_key("filenames")
        self.b_energy_function = self.jsondata["inputfile"].has_key("filenames")
        self.b_md_information = self.jsondata["inputfile"].has_key("filenames")

        ##optional flag
        self.b_electrostatic = self.jsondata["inputfile"]["optional_block"].has_key("filenames")
        self.b_flexible_local = self.jsondata["inputfile"]["optional_block"].has_key("filenames")
        self.b_aicg = self.jsondata["inputfile"]["optional_block"].has_key("filenames")
        
        if not (self.b_filenames and \
           self.b_job_cntl and \
           self.b_unit_and_state and \
           self.b_energy_function and \
           self.b_md_information):
            raise Exception("Bock fields Error, Please check it.")
        
        print " OK!!!"


    def _checkDir(self):
        pass

    def _submitQueue(self):
        pass
    
    def _determineCount(self):
        
        pass


if __name__ == "__main__":
    test=SubmitQueue('./test/inp/inp.json')
    test.main()
    
