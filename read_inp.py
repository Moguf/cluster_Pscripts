#!/usr/bin/env python
#2012-11-30:editer@tanaka
#This scirpts is made for Cafemol
#-----------------------------------------
#test=inpfile("template.inp")
#test.path="~/tmp/tmp"
#tset.pathinit="~/pdb"
#-----------------------------------------


import copy
class inpfile:
    def __init__(self,defalut_input):
        self.data = open(defalut_input.split("\n")).readlines()
        self.original_data=copy.deepcopy(self.data)
        
        for dummy in self.data:
            if dummy[0:7] == 'tempk =':
                self.T = float(dummy[8:14])


    
    def show(self):
        for line in self.data:
            print line
            
    def path(self,dirc):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:6] == 'path =':
                self.data[dummy] = 'path = %s'%dirc
                
    def pathpdb(self,dirp):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:8] == 'path_pdb':
                self.data[dummy] = 'path_pdb = %s'%dirp

    def pathini(self,dirp):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:8] == 'path_ini':
                self.data[dummy] = 'path_ini = %s'%dirp
                
    def pathpara(self,dirp):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:9] == 'path_para':
                self.data[dummy] = 'path_para = %s'%dirp
                
                
    def pathninfo(self,dirp):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:12] == 'path_natinfo':
                self.data[dummy] = 'path_natinfo = %s'%dirp
    

    def filename(self,name):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:8] == 'filename':
                self.data[dummy] = 'filename = %s'%name
    
    def output(self,files):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:6] == 'OUTPUT':
                self.data[dummy] = 'OUTPUT %s'%files
    
    def pathpara(self,para):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:9] == 'path_para':
                self.data[dummy] = 'path_para = %s'%para
    
    def run_mode(self,mode):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:10] == 'i_rum_mode':
                self.data[dummy] = 'i_rum_mode = %d'%mode
    
    def simu_type(self,mode):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:15] == 'i_simulate_type':
                self.data[dummy] = 'i_simulate_type = %d'%mode
    
    def initial(self,state):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:15] == 'i_initial_state':
                self.data[dummy] = 'i_initial_state = %d'%state
            if state == 6:
                txt="**<<<< initial_struct"
                if self.data[dummy][0:len(txt)] == txt:
                    self.data[dummy] = '<<<< initial_struct'
    def initial_struct(self,num,pdb_name):
        for dummy in xrange(len(self.data)):
            txt="<<<< initial_struct"
            if self.data[dummy][0:len(txt)] == txt:
                insert_txt="1-%d     %s" %(num,pdb_name)
                self.data.insert(dummy+1,insert_txt)
    def seq_read(self,state):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:16] == 'i_seq_read_style':
                self.data[dummy] = 'i_seq_read_style = %d'%state
                
    def go_read(self,state):
        for dummy in xrange(len(self.data)):
            if state == 2:
                txt="**<<<< native_info_sim1"
                if self.data[dummy][0:len(txt)] == txt:
                    self.data[dummy] = '<<<< native_info_sim1'
                txt="i_para_from_ninfo"
                if self.data[dummy][0:len(txt)] == txt:
                    self.data[dummy] = 'i_para_from_ninfo = 1'
            if self.data[dummy][0:22] == 'i_go_native_read_style':
                self.data[dummy] = 'i_go_native_read_style = %d'%state
            
        
                
    def protein(self,pdb,pdb2=None,num=1,style=1):
        for dummy in xrange(len(self.original_data)):
            if self.original_data[dummy][0:12] == '1    protein':
                if style==1:
                    self.data[dummy] = '%d    protein       %s'%(num,pdb)
                    print "in style 1"
                elif style==2:
                    self.data[dummy] = '1    protein       %s \n2     protein       %s'%(pdb,pdb2)
                elif style==3:
                    self.data[dummy] = '1-%d    protein       %s'%(num,pdb)
    

                    
    def local(self,pro_num,potential):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:5] == 'LOCAL':
                self.data[dummy] = 'LOCAL(1-%d)  %s'%(pro_num,potential)
                
    
    def nlocal(self,pro_num,style,potential):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:6] == 'NLOCAL':
                if style==1:
                     self.data[dummy]='NLOCAL(1-%d/1-%d)  %s'%(pro_num,pro_num,potential)
                elif style==2:
                    self.data[dummy] ='NLOCAL(%d/%d)  %s'%(1,1,potential)
                    for i in xrange(2,pro_num+1):
                        self.data.insert(dummy+1,'NLOCAL(%d/%d)  %s'%(i,i,potential))
                    break
                    
                
    def flp(self):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:5] == 'i_flp':
                self.data[dummy] = 'i_flp = 1'
    def para_ninfo(self):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:5] == 'i_para_from_ninfo':
                self.data[dummy] = 'i_para_from_ninfo = 1'
    
    
    def tstep(self,step):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:7] == 'n_tstep':
                self.data[dummy] = 'n_tstep(1) = %d'%step
    
    def save(self,step):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:13] == 'n_step_save =':
                self.data[dummy] = 'n_step_save = %d'%step
    
    def rst_save(self,step):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:10] == 'n_step_rst':
                self.data[dummy] = 'n_step_rst = %d'%step
    
    def temp(self,t):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:7] == 'tempk =':
                self.data[dummy] = 'tempk = %s'%float(t)
    
    def zeroing(self,t):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:13] == 'i_com_zeroing':
                self.data[dummy] = 'i_com_zeroing = %s'%int(t)
    
    def seed(self,s):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:6] == 'n_seed':
                self.data[dummy] = 'n_seed = %s'%str(s)
    
    
    def critical(self,upper,lower):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:11] == 'tempk_upper':
                self.data[dummy] = 'tempk_upper = %s'%float(upper)
            if self.data[dummy][0:11] == 'tempk_lower':
                self.data[dummy] = 'tempk_lower = %s'%float(lower)
    
    def delgo_addflp(self,*s):
        self.flp()
        for dummy in range(len(self.data)):
            match_string='**<<<< flexible_local'
            length=len(match_string)
            if self.data[dummy][0:length] == match_string:
                    self.data[dummy] = '<<<< flexible_local'
            match_string='DEL_LGO_ADD_FLP'
            length=len(match_string)
            if self.data[dummy][0:length] == 'DEL_LGO_ADD_FLP':
                if s[0]==0 and s[1]==0 :
                    self.data[dummy] = ''
                    break
                for i in xrange(0,len(s)-1,2):
                    if i>1:
                        self.data.insert(dummy+1,'DEL_LGO_ADD_FLP(%s-%s)   '%(s[i],s[i+1]))
                    else:
                        self.data[dummy] = 'DEL_LGO_ADD_FLP(%s-%s)   '%(s[i],s[i+1])
                break
    
    def fix(self,flag,s,e):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:7] == 'i_fix =':
                self.data[dummy] = 'i_fix = %d   '%flag
            if flag == 1:
                if self.data[dummy][0:15] == '**<<<< fix_para':
                    self.data[dummy] = '<<<< fix_para '
                if self.data[dummy][0:6] == 'FIX_MP':
                    self.data[dummy] = 'FIX_MP(%d-%d) '%(s,e)
            if flag == 0:
                if self.data[dummy][0:13] == '<<<< fix_para':
                    self.data[dummy] = '**<<<< fix_para '
                if self.data[dummy][0:6] == 'FIX_MP':
                    self.data[dummy] = 'FIX_MP(%d-%d) '%(1,1)
    
    def box(self,box_x,box_y,box_z,sigma):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:10] == 'i_in_box =':
                self.data[dummy] = 'i_in_box =  1'
            
            if self.data[dummy][0:13] == 'i_com_zeroing':
                self.data[dummy] = 'i_com_zeroing = 0 '
            if self.data[dummy][0:13] == '**<<<< in_box':
                self.data[dummy] = '<<<< in_box '
            if self.data[dummy][0:4] == 'xbox':
                self.data[dummy] = 'xbox = %s'%(box_x)
            if self.data[dummy][0:4] == 'ybox':
                self.data[dummy] = 'ybox = %s'%(box_y)
            if self.data[dummy][0:4] == 'zbox':
                self.data[dummy] = 'zbox = %s'%(box_z)
            if self.data[dummy][0:8] == 'boxsigma':
                self.data[dummy] = 'boxsigma = %s'%(sigma)

    def cap(self,radius):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:10] == 'i_in_cap =':
                self.data[dummy] = 'i_in_cap = 1'
            if self.data[dummy][0:13] == 'i_com_zeroing':
                self.data[dummy] = 'i_com_zeroing = 0 '
            if self.data[dummy][0:13] == '**<<<< in_cap':
                self.data[dummy] = '<<<< in_cap '
            if self.data[dummy][0:4] == 'rcap':
                self.data[dummy] = 'rcap = %s.0'%(radius)
    
    def anchor(self,flag,ID,k,l,x,y,z):
        for dummy in xrange(len(self.data)):
            if self.data[dummy][0:10] == 'i_anchor =':
                self.data[dummy] = 'i_anchor = %d   '%flag
            if flag == 1:
                if self.data[dummy][0:18] == '**<<<< anchor_para':
                    self.data[dummy] = '<<<< anchor_para '
                if self.data[dummy][0:5] == 'ANCH ':
                    self.data[dummy] = 'ANCH %d %05.2f %05.2f %05.2f %05.2f %05.2f '%(ID,k,l,x,y,z)
            if flag == 0:
                if self.data[dummy][0:16] == '<<<< anchor_para':
                    self.data[dummy] = '**<<<< anchor_para '
                if self.data[dummy][0:5] == 'ANCH ':
                    self.data[dummy] = 'ANCH  '
    
    def write(self,filename):
        outfile = open(filename,'w')
        for dummy in self.data:
            outfile.write(dummy+"\n")

