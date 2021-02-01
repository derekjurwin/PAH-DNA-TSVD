import pandas as pd
import numpy as np
import os
import time

dict_scan_point_keyed={}

def Parse_File(scan_filename,out_to_file,input_orientation_cutoff_string,dih_scan_string,scan_point_counter):
    Opt_Param_String='Optimized Parameters'
    Initial_Param_String='Initial Parameters'
    Input_Orient_String='Input orientation:'
    SCF_Done_String='SCF Done:'
    EUMP2_String='EUMP2 ='
    Opt_Completed_String='Optimization completed.'

    Collect_Input_Orient_bool=False
    Collect_SCF_Done_bool=False
    Collect_Initial_Param_bool=False

    hold_Initial_Param_String_list=[]
    hold_input_orient_list=[]
    hold_SCF_Done_String=''
    hold_EUMP2_String=''
    hold_Opt_Completed_String=''
    hold_Opt_Param_String=''

    Initial_Parameter_cutoff_string='Trust Radius'
    
    write_input_orient_bool=False
    write_Initial_Param_bool=False

    dict_angle_key_tracker=''

    with open(scan_filename,'r') as file:
        for line in file:
            if Initial_Param_String in line:
                Collect_Initial_Param_bool=True
            if Input_Orient_String in line:
                hold_input_orient_list=[]
                Collect_Input_Orient_bool=True
            if SCF_Done_String in line:
                hold_SCF_Done_String=line
            if EUMP2_String in line:
                hold_EUMP2_String=line
            if Opt_Completed_String in line:
                hold_Opt_Completed_String=line
            if input_orientation_cutoff_string in line:
                Collect_Input_Orient_bool=False
            if Initial_Parameter_cutoff_string in line:
                Collect_Initial_Param_bool=False
                write_Initial_Param_bool=True
            if Opt_Param_String in line:
                hold_Opt_Param_String=line
                write_input_orient_bool=True
                Collect_Input_Orient_bool=False
            if Collect_Input_Orient_bool:
                hold_input_orient_list.append(line)
            if Collect_Initial_Param_bool:
                hold_Initial_Param_String_list.append(line)

            if write_Initial_Param_bool:
                for text_line in hold_Initial_Param_String_list:
                    out_to_file.write(text_line)
                out_to_file.write(Initial_Parameter_cutoff_string)
                out_to_file.write('\n')
                write_Initial_Param_bool=False
                    
            # note all input orientations are written to 0_5_Input_orient.txt
            # but any identical angle keys will result in overwrites in the dictionary
            # the scan point coordinates written out in the Write_Scan_Point_Coordinates_To_File
            # are thus the correct coordinates (I think...)
            if write_input_orient_bool and dih_scan_string in line:
                x=line.split()
                dict_angle_key_tracker=x[3]
                scan_point_counter+=1
#                print(scan_point_counter)
                dict_scan_point_keyed[scan_point_counter]=(dict_angle_key_tracker,hold_input_orient_list)
#                print(dict_scan_point_keyed[scan_point_counter][1])
                out_to_file.write('dihedral='+str(dict_angle_key_tracker))
                out_to_file.write('\n')
                for text_line in hold_input_orient_list:
                    out_to_file.write(text_line)
#                    out_to_file.write('\n')
                out_to_file.write(hold_SCF_Done_String)
                out_to_file.write('\n')
                out_to_file.write(hold_EUMP2_String)
                out_to_file.write('\n')
                out_to_file.write(hold_Opt_Completed_String)
                out_to_file.write('\n')
                out_to_file.write(hold_Opt_Param_String)
                out_to_file.write('\n')
                out_to_file.write(line)
                out_to_file.write('\n\n')
                hold_input_orient_list=[]

    return scan_point_counter

    
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################

# UNCOMMENT FOR FINAL VERSION
neg_scan_filename=input("Enter neg log file name: ")
#neg_scan_filename="BCP.scan1.pos.150deg-start.log"
pos_scan_filename=input("Enter pos log file name: ")
dih_scan_string=input("Enter D(#,#,#,#) to match: ")
#dih_scan_string="D(11,12,35,36)"

# UNCOMMENT FOR FINAL VERSION
input_orientation_cutoff_string=input("Enter Input orientation cutoff string: ")
#input_orientation_cutoff_string='Distance matrix'
#input_orientation_cutoff_string='Stoichiometry'

scan_point_counter=0

out_to_file=open(neg_scan_filename+'.ffTK','w')
scan_point_counter=Parse_File(neg_scan_filename,out_to_file,input_orientation_cutoff_string,dih_scan_string,scan_point_counter)
out_to_file.close()

out_to_file=open(pos_scan_filename+'.ffTK','w')
scan_point_counter=Parse_File(pos_scan_filename,out_to_file,input_orientation_cutoff_string,dih_scan_string,scan_point_counter)
out_to_file.close()

num_unique_scan_points=scan_point_counter

neg_scan_filename=neg_scan_filename+'.ffTK'

pos_scan_filename=pos_scan_filename+'.ffTK'

out_to_file=open('0_0_simulation_data.txt','w')
out_to_file.write(neg_scan_filename)
out_to_file.write('\n')
out_to_file.write(pos_scan_filename)
out_to_file.write('\n')
out_to_file.write(dih_scan_string)
out_to_file.write('\n')
out_to_file.write(str(num_unique_scan_points))
out_to_file.write('\n')
out_to_file.close()
