#!/bin/usr/env python2.7
#coding:utf-8
#editor:ono
#This script makes json-style-input-file from cafemol input file.


import re


class CafemolStyleInp:
    def __init__(self,inpfile):
        ######remove '\n' in each sentence and make list-data
        self.original_data = [iline.strip() for iline in open(inpfile,'r').readlines()]


        ##########Block names
        ##default_styles
        self.b_filenames = True
        self.b_job_cntl = True
        self.b_unit_and_state = True
        self.b_energy_function = True
        self.b_md_information = True

        ##optional flag
        self.electrostatic = False
        self.flexible_local = False
        self.aicg = False

        ##########Content names
        ##filenames contents
        self.filename = False
        self.path_pdb = False
        self.path_ini = False
        self.path_natinfo = False
        self.path_aicg = False
        self.path_para = False
        self.path_msf = False

        ##job_cntl
        self.i_run_mode = False
        self.i_simulate_type = False
        self.i_initial_state = False
        self.i_initial_velo = False
        self.i_periodic = False
        
        ##unit_and_state
        self.i_seq_read_style = False
        self.i_go_native_read_style = False
        self.read_pdb = False

        ##energy_function
        self.local = False
        self.nlocal = False
        ###I need to refine this data structure###
        self.i_use_atom_protein = False
        self.i_use_atom_dna = False
        self.i_output_energy_style = False

        ##md_information
        self.n_step_sim = False
        self.n_tstep = False
        self.tstep_size = False
        self.n_step_save = False
        self.n_step_rst = False
        self.n_step_neighbor = False
        self.tempk = False
        self.i_rand_type = False
        self.n_seed = False
        self.i_com_zeroing_ini = False
        self.i_com_zeroing = False
        self.i_no_trans_rot = 0
        ####optional parameters
        self.i_implig = 0
        self.i_redef_para = 0
        self.i_energy_para = 0
        self.i_neigh_dist = 0
        self.i_mass = 0
        self.i_fric = 0
        self.i_mass_fric = 0
        self.i_del_int = 0
        self.i_anchor = 0
        self.i_rest1d = 0
        self.i_bridge = 0
        self.i_pulling = 0
        self.i_fix = 0
        self.i_in_box = 0
        self.i_in_cap = 0
        self.i_modified_muca = 0
        
    def main(self):
        self.read()
        

    def read(self):
        self._refinement()
        self._readBlock()
        self._readContents()

    def _refinement(self):
        ######  remove empty data.
        while(True):
            try:
                self.original_data.remove("")
            except:
                break

        
    def _readBlock(self):
        for iline in self.original_data:
            stripedline=iline.strip()
            self.filenames = iline.endswith('filenames')
            self.job_cntl = iline.endswith('job_cntl')
            self.unit_and_state = iline.endswith('unit_and_state')
            self.energy_function = iline.endswith('energy_function')
            self.md_information = iline.endswith('md_information')
            #####optional flags
            self.electrostatic = iline.endswith('electrostatic')
            self.flexible_local = iline.endswith('flec')
            self.aicg = iline.endswith('aicg')


            
    def _readContents(self):
        for iline in self.original_data:
            ilist=iline.split(" =")
            ###print ilist
            ###filenames block
            if re.search(r"^filename$",ilist[0]):
                self.filename=ilist
            if re.search(r"^path_pdb$",ilist[0]):
                self.path_pdb=ilist
            if re.search(r"^path_ini$",ilist[0]):
                self.path_ini=ilist
            if re.search(r"^path_natinfo$",ilist[0]):
                self.path_natinfo=ilist
            if re.search(r"^path_aicg$",ilist[0]):
                self.path_aicg=ilist
            if re.search(r"^path_para$",ilist[0]):
                self.path_para=ilist
            if re.search(r"^path_msf$",ilist[0]):
                self.path_msf=ilist

            ###job_cntl
            if re.search(r"^i_run_mode$",ilist[0]):
                self.path_msf=ilist
            if re.search(r"^i_simulate_type$",ilist[0]):
                self.i_simulate_type = ilist
            if re.search(r"^i_initial_state$",ilist[0]):
                self.i_initial_state = ilist
            if re.search(r"^i_initial_velo$",ilist[0]):
                self.i_initial_velo = ilist
            if re.search(r"^self.i_periodic$",ilist[0]):
                self.i_periodic = ilist
            
            ###unit_and_state
            if re.search(r"^i_seq_read_style$",ilist[0]):
                self.i_seq_read_style = ilist
            if re.search(r"^i_go_native_read_style$",ilist[0]):
                self.i_go_native_read_style = ilist
            if re.search(r" protein ",ilist[0]):
                self.read_pdb = ilist[0].split()

            ##energy_function
            if re.search(r"^LOCAL",ilist[0]):
                self.local=ilist[0].split()
            if re.search(r"^NLOCAL",ilist[0]):
                self.nlocal=ilist[0].split()
            if re.search(r"^i_use_atom_protein$",ilist[0]):
                self.i_use_atom_protein = ilist
            if re.search(r"^i_use_atom_dna$",ilist[0]):
                self.i_use_atom_dna = ilist
            if re.search(r"^i_output_energy_style$",ilist[0]):
                self.i_output_energy_style = ilist
        ###I need to refine this data structure###



                
if __name__  ==  "__main__":
    test = CafemolStyleInp("./test/inp/test.inp")
    test.main()
