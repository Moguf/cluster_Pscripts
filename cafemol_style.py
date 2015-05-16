#!/bin/usr/env python2.7
#coding:utf-8
#editor:ono
#This script makes json-style-input-file from cafemol input file.
import re

import myutil

class CafemolStyleInp:
    def __init__(self):
        ##########Block names
        ##default_styles
        self.b_filenames = False
        self.b_job_cntl = False
        self.b_unit_and_state = False
        self.b_energy_function = False
        self.b_md_information = False

        ##optional flag
        self.b_electrostatic = False
        self.b_flexible_local = False
        self.b_aicg = False
        self.b_del_interaction = False

        ##########Content names
        ##filenames contents
        self.filename = False
        self.path = False
        self.OUTPUT = False
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
        self.LOCAL = False
        self.NLOCAL = False
        ###I need to refine this data structure###
        self.i_use_atom_protein = False
        self.i_use_atom_dna = False
        self.i_output_energy_style = False
        self.i_flp = False
        self.i_triple_angle_term = False

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
        self.i_no_trans_rot = False
        ####optional parameters
        self.i_implig = False
        self.i_redef_para = False
        self.i_energy_para = False
        self.i_neigh_dist = False
        self.i_mass = False
        self.i_fric = False
        self.i_mass_fric = False
        self.i_del_int = False
        self.i_anchor = False
        self.i_rest1d = False
        self.i_bridge = False
        self.i_pulling = False
        self.i_fix = False
        self.i_in_box = False
        self.i_in_cap = False
        self.i_modified_muca = False

        ##optional blocks
        #### aicg
        self.i_aicg = False
        #### electrostatic
        self.cutoff = False
        self.ionic_strength = False
        self.diele_water = False
        self.i_diele= False
        #### flexible_local
        self.k_dih = False
        self.k_ang = False
        #### DEL_GO
        self.DEL_GO = []
        self.DEL_LGO = []
        
    def test(self):
        self.read("./test/inp/test.inp")
        self.check()
        self.write("./test/out/testinp.out")


    def read(self,inpfile):
        ######remove '\n' in each sentence and make list-data
        self.original_data = [iline.strip() for iline in open(inpfile,'r').readlines()]
        self._refinement()
        self._readBlock()
        self._readContents()


    def check(self):
        print "check block statements....",
        if not self.b_filenames:
            raise Exception,"filenames block is not in your input file."
        if not self.b_job_cntl:
            raise Exception,"job_cntl block is not in your input file."
        if not self.b_unit_and_state:
            raise Exception,"unit_and_state block is not in your input file."
        if not self.b_energy_function:
            raise Exception,"energy_function block is not in your input file."
        if not self.b_md_information:
            raise Exception,"md_infortmation block is not in your input file."
        print " OK !!!"
        
    def write(self,outfile="testinp.out"):
        ofile=open(outfile,'w')
        otxt=""

        ## filenamse Block
        otxt+="<<<< filenames\n"
        otxt+=self._writeContents("filename")
        otxt+=self._writeContents("path")
        otxt+=self._writeContents("OUTPUT")
        otxt+=self._writeContents("path_pdb")
        otxt+=self._writeContents("path_ini")
        otxt+=self._writeContents("path_natinfo")
        otxt+=self._writeContents("path_aicg")
        otxt+=self._writeContents("path_para")
        otxt+=self._writeContents("path_msf")
        otxt+=">>>>\n\n"
        
        ##job_cntl
        otxt+="<<<< job_cntl\n"
        otxt+=self._writeContents("i_run_mode")
        otxt+=self._writeContents("i_simulate_type")
        otxt+=self._writeContents("i_initial_state")
        otxt+=self._writeContents("i_initial_velo")
        otxt+=self._writeContents("i_periodic")
        otxt+=">>>>\n\n"
        
        ##unit_and_state
        otxt+="<<<< unit_and_state\n"
        otxt+=self._writeContents("i_seq_read_style")
        otxt+=self._writeContents("i_go_native_read_style")
        otxt+=self._writeContents("read_pdb")
        otxt+=">>>>\n\n"

        ##energy_function
        otxt+="<<<< energy_function\n"
        otxt+=self._writeContents("LOCAL")
        otxt+=self._writeContents("NLOCAL")
        ###I need to refine this data structure###
        otxt+=self._writeContents("i_use_atom_protein")
        otxt+=self._writeContents("i_use_atom_dna")
        otxt+=self._writeContents("i_output_energy_style")
        otxt+=self._writeContents("i_flp")
        otxt+=self._writeContents("i_triple_angle_term")
        otxt+=">>>>\n\n"
        
        ##md_information
        otxt+="<<<< md_information\n"
        otxt+=self._writeContents("n_step_sim")
        otxt+=self._writeContents("n_tstep")
        otxt+=self._writeContents("tstep_size")
        otxt+=self._writeContents("n_step_save")
        otxt+=self._writeContents("n_step_rst")
        otxt+=self._writeContents("n_step_neighbor")
        otxt+=self._writeContents("tempk")
        otxt+=self._writeContents("i_rand_type")
        otxt+=self._writeContents("n_seed")
        otxt+=self._writeContents("i_com_zeroing_ini")
        otxt+=self._writeContents("i_com_zeroing")
        otxt+=self._writeContents("i_no_trans_rot")
        otxt+=self._writeContents("i_del_int")
        otxt+=">>>>\n\n"
        
        ## optional_block
        otxt+=self._writeOptionalBlock("b_aicg")
        otxt+=self._writeOptionalBlock("b_flexible_local")
        otxt+=self._writeOptionalBlock("b_electrostatic")
        otxt+=self._writeOptionalBlock("b_del_interaction")

        ofile.write(otxt)
        ofile.close()

    def _writeOptionalBlock(self,bkey):
        otxt=""
        key=bkey[2:]
        ### bkey is 'b_aicg' , key is aicg
        ### aicg in inp.json
        if self.__dict__[bkey]:
            ### Caution!!! This part is not good!!!!!
            ### I shuld make optional dictonary.
            ### because of I don't have to use if-sentence.
            ### I have only to use for-sentence.
            otxt+="<<<< "+key+"\n"
            if bkey=="b_aicg":
                otxt+=self._writeContents("i_aicg")
            elif bkey=="b_electrostatic":
                otxt+=self._writeContents("ionic_strength")
                otxt+=self._writeContents("cutoff")
                otxt+=self._writeContents("diele_water")
                otxt+=self._writeContents("i_diele")
            elif bkey=="b_flexible_local":
                otxt+=self._writeContents("k_dih")
                otxt+=self._writeContents("k_ang")
            elif bkey=="b_del_interaction":
                otxt+=self._writeContents("DEL_GO")
                otxt+=self._writeContents("DEL_LGO")
            otxt+=">>>>\n\n"
            return otxt
        else:
            return otxt
    
        
    def _writeContents(self,key):
        ignorelist=["OUTPUT","NLOCAL","LOCAL","n_tstep","read_pdb","DEL_GO","DEL_LGO"]
        if self.__dict__[key]:
            if not key in ignorelist:
                if key == "tempk":
                    return key+" = "+self.__dict__[key]+".0\n"
                return key+" = "+self.__dict__[key]+"\n"
            else:
                if key in ["DEL_GO","DEL_LGO"]:
                    return "\n".join(self.__dict__[key])+"\n"
                else:
                    return " ".join(self.__dict__[key])+"\n"
        else:
            return ""
        

    
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
            if iline.endswith('filenames'):
                self.b_filenames = iline.endswith('filenames')

            if iline.endswith('job_cntl'):
                self.b_job_cntl = iline.endswith('job_cntl')

            if iline.endswith('unit_and_state'):
                self.b_unit_and_state = iline.endswith('unit_and_state')

            if iline.endswith('energy_function'):
                self.b_energy_function = iline.endswith('energy_function')
                
            if iline.endswith('md_information'):
                self.b_md_information = iline.endswith('md_information')

            #####optional flags
            if iline.endswith('electrostatic'):
                self.b_electrostatic = iline.endswith('electrostatic')
            if iline.endswith('flexible_local'):
                self.b_flexible_local = iline.endswith('flexible_local')
            if iline.endswith('aicg'):
                self.b_aicg = iline.endswith('aicg')
            if iline.endswith('del_interaction'):
                self.b_del_interaction = iline.endswith('del_interaction')

            
    def _readContents(self):
        for iline in self.original_data:
            ilist=myutil.mySplit(iline,"=")
            
            ###print ilist
            ###filenames block
            if re.search(r"^filename$",ilist[0]):
                self.filename=ilist[-1]
            if re.search(r"^path$",ilist[0]):
                self.path=ilist[-1]
            if re.search(r"^path_pdb$",ilist[0]):
                self.path_pdb=ilist[-1]
            if re.search(r"^OUTPUT",ilist[0]):
                self.OUTPUT=ilist
            if re.search(r"^path_ini$",ilist[0]):
                self.path_ini=ilist[-1]
            if re.search(r"^path_natinfo$",ilist[0]):
                self.path_natinfo=ilist[-1]
            if re.search(r"^path_aicg$",ilist[0]):
                self.path_aicg=ilist[-1]
            if re.search(r"^path_para$",ilist[0]):
                self.path_para=ilist[-1]
            if re.search(r"^path_msf$",ilist[0]):
                self.path_msf=ilist[-1]

            ###job_cntl
            if re.search(r"^i_run_mode$",ilist[0]):
                self.i_run_mode=ilist[-1]
            if re.search(r"^i_simulate_type$",ilist[0]):
                self.i_simulate_type = ilist[-1]
            if re.search(r"^i_initial_state$",ilist[0]):
                self.i_initial_state = ilist[-1]
            if re.search(r"^i_initial_velo$",ilist[0]):
                self.i_initial_velo = ilist[-1]
            if re.search(r"^self.i_periodic$",ilist[0]):
                self.i_periodic = ilist[-1]
            
            ###unit_and_state
            if re.search(r"^i_seq_read_style$",ilist[0]):
                self.i_seq_read_style = ilist[-1]
            if re.search(r"^i_go_native_read_style$",ilist[0]):
                self.i_go_native_read_style = ilist[-1]
            if "protein" in ilist:
                ####  FUTURE: I need to change this sentence in future.
                self.read_pdb = ilist
                
            ##energy_function
            if re.search(r"^LOCAL",ilist[0]):
                self.LOCAL=ilist
            if re.search(r"^NLOCAL",ilist[0]):
                self.NLOCAL=ilist
            if re.search(r"^i_use_atom_protein$",ilist[0]):
                self.i_use_atom_protein = ilist[-1]
            if re.search(r"^i_use_atom_dna$",ilist[0]):
                self.i_use_atom_dna = ilist[-1]
            if re.search(r"^i_output_energy_style$",ilist[0]):
                self.i_output_energy_style = ilist[-1]
            if re.search(r"^i_flp$",ilist[0]):
                self.i_flp = ilist[-1]
            if re.search(r"^i_triple_angle_term$",ilist[0]):
                self.i_triple_angle_term = ilist[-1]
                
            ##md_information
            if re.search(r"^n_step_sim$",ilist[0]):
                self.n_step_sim = ilist[-1]
            if re.search(r"^n_tstep",ilist[0]):
                self.n_tstep = ilist
            if re.search(r"^tstep_size$",ilist[0]):
                self.tstep_size = ilist[-1]
            if re.search(r"^n_step_save$",ilist[0]):
                self.n_step_save = ilist[-1]
            if re.search(r"^n_step_rst$",ilist[0]):
                self.n_step_rst = ilist[-1]
            if re.search(r"^n_step_neighbor$",ilist[0]):
                self.n_step_neighbor = ilist[-1]
            if re.search(r"^tempk$",ilist[0]):
                self.tempk = ilist[-1]
            if re.search(r"^i_rand_type$",ilist[0]):
                self.i_rand_type = ilist[-1]
            if re.search(r"^n_seed$",ilist[0]):
                self.n_seed = ilist[-1]
            if re.search(r"^i_com_zeroing_ini$",ilist[0]):
                self.i_com_zeroing_ini = ilist[-1]
            if re.search(r"^i_com_zeroing$",ilist[0]):
                self.i_com_zeroing = ilist[-1]
            if re.search(r"^i_no_trans_rot$",ilist[0]):
                self.i_no_trans_rot = ilist[-1]
            if re.search(r"^i_del_int$",ilist[0]):
                self.i_del_int = ilist[-1]

            ##### optional blocks
            ###### aicg
            if re.search(r"^i_aicg$",ilist[0]):
                self.i_aicg = ilist[-1]
            ###### electrostatic
            if re.search(r"^cutoff$",ilist[0]):
                self.cutoff = ilist[-1]
            if re.search(r"^ionic_strength$",ilist[0]):
                self.ionic_strength = ilist[-1]
            if re.search(r"^diele_water$",ilist[0]):
                self.diele_water = ilist[-1]
            if re.search(r"^i_diele$",ilist[0]):
                self.i_diele = ilist[-1]
            ###### flexible_local
            if re.search(r"^k_dih$",ilist[0]):
                self.k_dih = ilist[-1]
            if re.search(r"^k_ang$",ilist[0]):
                self.k_ang = ilist[-1]
            ###### del_interaction
            if re.search(r"^DEL_GO",ilist[0]):
                self.DEL_GO.append(ilist[0])
            if re.search(r"^DEL_LGO",ilist[0]):
                self.DEL_LGO.append(ilist[0])

    def show(self):
        for i in self.__dict__.keys():
            print i,'\t\t\t',
            print self.__dict__[i]
            
if __name__  ==  "__main__":
    test = CafemolStyleInp()
    test.test()

