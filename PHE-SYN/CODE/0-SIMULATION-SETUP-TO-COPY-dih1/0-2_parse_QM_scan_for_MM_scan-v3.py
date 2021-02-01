import pandas as pd
import numpy as np
import os
import time

dict_scan_point_keyed={}

def Parse_File(scan_filename,out_to_file,input_orientation_cutoff_string,dih_scan_string,scan_point_counter):
    Opt_Param_String='Optimized Parameters'
    Input_Orient_String='Input orientation:'

    Collect_Input_Orient_bool=False

    hold_input_orient_list=[]

    write_input_orient_bool=False

    dict_angle_key_tracker=''

    with open(scan_filename,'r') as file:
        for line in file:
            if Input_Orient_String in line:
                hold_input_orient_list=[]
                Collect_Input_Orient_bool=True
            if input_orientation_cutoff_string in line:
                Collect_Input_Orient_bool=False
            if Opt_Param_String in line:
                write_input_orient_bool=True
                Collect_Input_Orient_bool=False
            if Collect_Input_Orient_bool:
                hold_input_orient_list.append(line)
                
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
                    out_to_file.write('\n')               
                hold_input_orient_list=[]

    return scan_point_counter

def Write_Scan_Point_Coordinates_To_File():
    unique_scan_point_counter=0
    out_to_angle_rosetta_stone=open('0_5_angle_rosetta_stone.txt','w')
    # note the dictionary is not sorted in the for loop below
    # hence the keys go in the same order they were read from the scan files
    # this leaves them in scan point order (neg scan file then pos scan file)
    for key in dict_scan_point_keyed.keys():
        unique_scan_point_counter+=1
        print('Writing coordinates for angle: ',dict_scan_point_keyed[key][0],' and MM scan point: ',unique_scan_point_counter)
        input_orient_string_to_write=dict_scan_point_keyed[key][1]
        out_filename='Scan_Point'+str(unique_scan_point_counter)+'_coords.txt'
        out_to_scan_point_file=open(out_filename,'w')
        out_to_angle_rosetta_stone.write(str(unique_scan_point_counter))
        out_to_angle_rosetta_stone.write(',')
        out_to_angle_rosetta_stone.write(dict_scan_point_keyed[key][0])
        out_to_angle_rosetta_stone.write('\n')
        for text_line in input_orient_string_to_write:
            out_to_scan_point_file.write(text_line)
            out_to_scan_point_file.write('\n')
        out_to_scan_point_file.close()
    out_to_angle_rosetta_stone.close()
    
def generate_PDBs(num_unique_scan_points):
    # UNCOMMENT IN FINAL VERSION
    input_PDB_template_filename=input("Enter template PDB file name: ")
    in_PDB_file=open(input_PDB_template_filename,'r')

    # DELETE IN FINAL VERSION
    #in_PDB_file=open('0_BcP_ADE.pdb','r')
    
    strings_from_PDB=in_PDB_file.readlines()
    in_PDB_file.close()
    
    for a in range(num_unique_scan_points):
        in_filename='Scan_Point'+str(a+1)+'_coords.txt'
        df=pd.read_csv(in_filename,sep='\s+',skiprows=10,skipfooter=2,header=None)
        df=df.round(3)
        df=df[[3,4,5]]        
        out_filename='Scan_Point'+str(a+1)+'_coords_parsed.txt'
        np.savetxt(out_filename,df,fmt='%7.3f')

        merged_string_list=[]
        in_TXT_filename=out_filename
        in_TXT_file=open(in_TXT_filename,'r')
        strings_from_TXT=in_TXT_file.readlines()
        merged_string_list.append(strings_from_PDB[0])
        for c in range(len(strings_from_PDB)-2):
            merged_string_list.append(strings_from_PDB[c+1][0:32]+strings_from_TXT[c][1:23]+strings_from_PDB[c+1][54:79])
        in_TXT_file.close()
        merged_string_list.append(strings_from_PDB[len(strings_from_PDB)-1])
        out_PDB_filename='Scan_Point'+str(a+1)+'.pdb'
        out_PDB_file=open(out_PDB_filename,'w')
        out_PDB_file.writelines(merged_string_list)
        out_PDB_file.close()

def generate_FixedAtoms_PDBs(num_unique_scan_points,dih_scan_string):
    atom_numbers_to_fix=dih_scan_string
    atom_numbers_to_fix=atom_numbers_to_fix[:-1]
    atom_numbers_to_fix=atom_numbers_to_fix[2:]
    line_numbers_to_fix=atom_numbers_to_fix.split(',')
    line_numbers_to_fix[0]=int(line_numbers_to_fix[0])-1
    line_numbers_to_fix[1]=int(line_numbers_to_fix[1])-1
    line_numbers_to_fix[2]=int(line_numbers_to_fix[2])-1
    line_numbers_to_fix[3]=int(line_numbers_to_fix[3])-1
    
    #10 11 29 18 in NAP
    #10 11 34 35 in BCP,PHE
    #get_atom_line_nums_to_fix=input("Enter LINE NUMBERS of atoms to fix: ")
    #x=get_atom_line_nums_to_fix.split()
    #print(line_numbers_to_fix[0],line_numbers_to_fix[1],line_numbers_to_fix[2],line_numbers_to_fix[3])
    for a in range(num_unique_scan_points):
        OriginalPDB='Scan_Point'+str(a+1)+'_sim_new.pdb'
        NewPDB='Scan_Point'+str(a+1)+'_FixedAtoms.pdb'
        in_file=open(OriginalPDB,'r')
        strings_from_OriginalPDB=in_file.readlines()
        merged_string_list=[]
        merged_string_list.append(strings_from_OriginalPDB[0])
        for c in range(len(strings_from_OriginalPDB)-2):
            if c==line_numbers_to_fix[0] or c==line_numbers_to_fix[1] or c==line_numbers_to_fix[2] or c==line_numbers_to_fix[3]:
                merged_string_list.append(strings_from_OriginalPDB[c+1][0:20]+' B'+strings_from_OriginalPDB[c+1][22:61]+' 1'+strings_from_OriginalPDB[c+1][63:79])
            else:
                merged_string_list.append(strings_from_OriginalPDB[c+1][0:20]+' B'+strings_from_OriginalPDB[c+1][22:79])
        merged_string_list.append(strings_from_OriginalPDB[len(strings_from_OriginalPDB)-1])
        out_file=open(NewPDB,'w')
        out_file.writelines(merged_string_list)
        in_file.close()
        out_file.close()

def generate_NAMD_COLVARS_noHARMONIC(num_unique_scan_points,dih_scan_string):
    # 11 12 30 19
    # 11 12 35 36 BCP,PHE
    #get_atom_nums_to_fix=input("Enter atom numbers to fix: ")
    #x=get_atom_nums_to_fix.split()
    atom_numbers_to_fix=dih_scan_string
    atom_numbers_to_fix=atom_numbers_to_fix[:-1]
    atom_numbers_to_fix=atom_numbers_to_fix[2:]
    line_numbers_to_fix=atom_numbers_to_fix.split(',')
    for a in range(num_unique_scan_points):
        out_filename='Scan_Point'+str(a+1)+'_colvars.conf'
        out_to_file=open(out_filename,'w')
        out_to_file.write('colvarsTrajFrequency 10')
        out_to_file.write('\n')
        out_to_file.write('colvar {')
        out_to_file.write('\n')
        out_to_file.write('name dih ')
        out_to_file.write('\n')
        out_to_file.write('outputValue on ')
        out_to_file.write('\n')
        out_to_file.write('dihedral {')
        out_to_file.write('\n')
        out_to_file.write('group1 { atomNumbers '+line_numbers_to_fix[0]+' }')
        out_to_file.write('\n')
        out_to_file.write('group2 { atomNumbers '+line_numbers_to_fix[1]+' }')
        out_to_file.write('\n')
        out_to_file.write('group3 { atomNumbers '+line_numbers_to_fix[2]+' }')
        out_to_file.write('\n')
        out_to_file.write('group4 { atomNumbers '+line_numbers_to_fix[3]+' }')
        out_to_file.write('\n')
        out_to_file.write('}')
        out_to_file.write('\n')
        out_to_file.write('}')
        out_to_file.write('\n')
        out_to_file.close()

    
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################

in_from_file=open('0_0_simulation_data.txt','r')

simulation_data=in_from_file.readlines()

in_from_file.close()

simulation_data[0]=simulation_data[0][:-1]
simulation_data[1]=simulation_data[1][:-1]
simulation_data[2]=simulation_data[2][:-1]
simulation_data[3]=simulation_data[3][:-1]

neg_scan_filename=simulation_data[0]
pos_scan_filename=simulation_data[1]
dih_scan_string=simulation_data[2]

#NEEDED?
#num_unique_scan_points=int(simulation_data[3])
#print(num_unique_scan_points)

# UNCOMMENT FOR FINAL VERSION
#input_orientation_cutoff_string=input("Enter Input orientation cutoff string: ")
#input_orientation_cutoff_string='Stoichiometry'
input_orientation_cutoff_string='SCF Done'

scan_point_counter=0
out_to_file=open('0_5_Input_orient.txt','w')
scan_point_counter=Parse_File(neg_scan_filename,out_to_file,input_orientation_cutoff_string,dih_scan_string,scan_point_counter)
scan_point_counter=Parse_File(pos_scan_filename,out_to_file,input_orientation_cutoff_string,dih_scan_string,scan_point_counter)
out_to_file.close()

num_unique_scan_points=scan_point_counter

Write_Scan_Point_Coordinates_To_File()

out_to_file=open('0_6_Number_of_unique_scan_points.txt','w')
out_to_file.write(str(num_unique_scan_points))
out_to_file.close()

generate_PDBs(num_unique_scan_points)

os.system('./2_MultiWrite_psfgen')

time.sleep(5)

os.system('./3_MultiExec_psfgen')

time.sleep(5)

generate_FixedAtoms_PDBs(num_unique_scan_points,dih_scan_string)

time.sleep(5)

generate_NAMD_COLVARS_noHARMONIC(num_unique_scan_points,dih_scan_string)
