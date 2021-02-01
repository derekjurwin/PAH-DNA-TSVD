import numpy as np
import os
import time
import math

import matplotlib.pyplot as plt

# READ QM ANGLES FROM QM LOG FILES INTO A LIST
# THESE ARE WRITTEN TO FILE AS THE scan_point#_coord.txt FILES ARE WRITTEN
# HENCE QM ANGLES CORREDPOND TO THOSE IN scan_point#_coord.txt
angles_ordered_by_scan_point_list=[]
angles_ordered_by_scan_point_QM_MM_check_list=[]
in_from_file=open('0_5_angle_rosetta_stone.txt','r')
angle_rosetta_stone_list=in_from_file.readlines()
in_from_file.close()
for i in angle_rosetta_stone_list:
    c=i.split(',')
    angles_ordered_by_scan_point_list.append(float(c[1]))
    angles_ordered_by_scan_point_QM_MM_check_list.append(float(c[1]))

print(angles_ordered_by_scan_point_list)

angles_ordered_by_scan_point_list_complement=[]

################################################################################
################################################################################
################################################################################

in_from_file=open('0_6_Number_of_unique_scan_points.txt','r')
num_unique_scan_points_string=in_from_file.readlines()
in_from_file.close()

num_unique_scan_points=int(num_unique_scan_points_string[0])

#num_unique_scan_points=len(sorted_QM_angles_list)

in_from_file=open('0_0_simulation_data.txt','r')
simulation_data=in_from_file.readlines()
simulation_data[0]=simulation_data[0][:-1]
simulation_data[1]=simulation_data[1][:-1]
simulation_data[2]=simulation_data[2][:-1]
in_from_file.close()

atom_numbers=input("Enter D(#,#,#,#) to match: ")
atom_numbers=atom_numbers[:-1]
atom_numbers=atom_numbers[2:]

dih_atom_numbers=atom_numbers.split(',')

#dih_atom_numbers=['12','35','36','47']

out_to_file=open('0_13_MM_calculated_dih_angles-ALT.txt','w')
for a in range(num_unique_scan_points):
    in_filename='Scan_Point'+str(a+1)+'.pdb'
  
    p0=np.array([0,0,0])
    p1=np.array([0,0,0])
    p2=np.array([0,0,0])
    p3=np.array([0,0,0])
    
    with open(in_filename,'r') as file:
        for line in file:
            string_to_parse=[]
            string_to_parse=line.split()
            if string_to_parse[0]!='END':
                #if '11  C6' in line:
                #    11  C6
                #if atom1 in line:
                if string_to_parse[1]==dih_atom_numbers[0]:
                    #string_to_parse=line.split()
                    x1=float(string_to_parse[6])
                    x2=float(string_to_parse[7])
                    x3=float(string_to_parse[8])
                    p0=np.array([x1,x2,x3])
                    #print('string_to_parse '+string_to_parse[1],dih_atom_numbers[0],'p0',p0)
                
                #if '12  N6' in line:
                #    12  N6
                #if atom2 in line:
                if string_to_parse[1]==dih_atom_numbers[1]:            
                    #string_to_parse=line.split()
                    x1=float(string_to_parse[6])
                    x2=float(string_to_parse[7])
                    x3=float(string_to_parse[8])
                    p1=np.array([x1,x2,x3])
                    #print('string_to_parse '+string_to_parse[1],dih_atom_numbers[1],'p1',p1)
                    
                #if '35  C20' in line:
                #    30  C30
                #if atom3 in line:
                if string_to_parse[1]==dih_atom_numbers[2]:            
                    #string_to_parse=line.split()
                    x1=float(string_to_parse[6])
                    x2=float(string_to_parse[7])
                    x3=float(string_to_parse[8])
                    p2=np.array([x1,x2,x3])
                    #print('string_to_parse '+string_to_parse[1],dih_atom_numbers[2],'p2',p2)                
                        
                #if '36 C20A' in line:
                #    19 C18
                #if atom4 in line:
                if string_to_parse[1]==dih_atom_numbers[3]:            
                    #string_to_parse=line.split()
                    x1=float(string_to_parse[6])
                    x2=float(string_to_parse[7])
                    x3=float(string_to_parse[8])
                    p3=np.array([x1,x2,x3])
                    #print('string_to_parse '+string_to_parse[1],dih_atom_numbers[3],'p3',p3)
                
                            
    b0=-1.0*(p1-p0)
                           
    b1=p2-p1
                            
    b2=p3-p2
                            
    b1 /= np.linalg.norm(b1)
                            
    v=b0-np.dot(b0,b1)*b1
                            
    w=b2-np.dot(b2,b1)*b1
                            
    x=np.dot(v,w)
                            
    y=np.dot(np.cross(b1,v),w)
    
    #PDB_dih_dict[in_filename]=(np.degrees(np.arctan2(y,x)))#keyed by scan point file
#    out_to_file.write('Scan point '+str(a+1)+' dihedral angle: '+str(np.degrees(np.arctan2(y,x)))+' QM(dih)-MM(dih) = '+str(np.degrees(np.arctan2(y,x))-angles_ordered_by_scan_point_list[a]))

#    if a+1 in scan_points_to_toss_list:  
#       print('Tossed scan point '+str(a+1)+'\n')

#    else:
       #out_to_file.write('Scan point '+str(a+1)+' dihedral angle: '+str(np.degrees(np.arctan2(y,x))))
    out_to_file.write(str(a+1)+' '+str(np.degrees(np.arctan2(y,x))))
    out_to_file.write('\n')

    angles_ordered_by_scan_point_list_complement.append(np.degrees(np.arctan2(y,x)))
       
out_to_file.close()

################################################################################
################################################################################
################################################################################

print(angles_ordered_by_scan_point_list_complement)


# READ MM ENERGIES FROM minima.dat
# THESE ARE READ FROM THE NAMD LOG FILES THE CORRESPOND TO scan_point#_coord.txt
# HENCE THE ENERGIES CORRESPOND TO THE QM ANGLES ABOVE IN THE SAME ORDER
MM_energies_by_scan_point=[]
in_from_file=open('minima.dat','r')
minima_string_list=in_from_file.readlines()
in_from_file.close()
for i in minima_string_list:
    c=i.split()
    MM_energies_by_scan_point.append(float(c[1]))

MM_relative_energies_by_scan_point=[]
min_MM_energy=min(MM_energies_by_scan_point)
for i in MM_energies_by_scan_point:
    MM_relative_energies_by_scan_point.append(i-min_MM_energy)

QM_relative_energies_by_scan_point=[]
in_from_file=open('0_2_QM_scan_data_sorted_by_all_scan_points.txt','r')
QM_energies_string_list=in_from_file.readlines()
in_from_file.close()

for i in QM_energies_string_list:
    c=i.split(',')
    QM_relative_energies_by_scan_point.append(float(c[4]))

##########################################################################################################################
# TOSS DATA HERE - ADD CASE FOR NONE
##########################################################################################################################

scan_points_to_toss_string=input("Enter scan points to toss separated by spaces only: ")
scan_points_to_toss_string_split=scan_points_to_toss_string.split()

scan_points_to_toss_list=[]
for i in scan_points_to_toss_string_split:
    scan_points_to_toss_list.append(int(i))

    #print(angles_ordered_by_scan_point_list)
    #print(MM_relative_energies_by_scan_point)
    #print(QM_relative_energies_by_scan_point)

for i in sorted(scan_points_to_toss_list,reverse=True):
    print("deleting :", i, " ",angles_ordered_by_scan_point_list[i-1])
    del angles_ordered_by_scan_point_list[i-1]
    del angles_ordered_by_scan_point_list_complement[i-1]
    del MM_relative_energies_by_scan_point[i-1]
    del QM_relative_energies_by_scan_point[i-1]

    #print(angles_ordered_by_scan_point_list)
    #print(MM_relative_energies_by_scan_point)
    #print(QM_relative_energies_by_scan_point)
##########################################################################################################################
##########################################################################################################################
                                           
# PUT QM ANGLES AND MM ENERGIES IN A DICTIONARY SO THEY ARE MARRIED
dict_MM_relative_energies_QM_angle_keyed={}
index_counter=0
for i in angles_ordered_by_scan_point_list:
    dict_MM_relative_energies_QM_angle_keyed[i]=(MM_relative_energies_by_scan_point[index_counter],QM_relative_energies_by_scan_point[index_counter],angles_ordered_by_scan_point_list_complement[index_counter])
    index_counter+=1
   
# SORT THE DICTIONARY AND CREATE NEW LISTS WHERE QM ANGLES AND MM ENERGIES ARE SORTED BY QM ANGLE
# IMPERATIVE FOR DIFFERENCE POTENTIAL AND PLOTTING
sorted_QM_angles_list=[]
sorted_MM_relative_energies_list=[]
QM_relative_energies_by_angle=[]

sorted_QM_angles_list_complement=[]

for key in sorted(dict_MM_relative_energies_QM_angle_keyed):
    sorted_QM_angles_list.append(key)
    sorted_MM_relative_energies_list.append(dict_MM_relative_energies_QM_angle_keyed[key][0])
    QM_relative_energies_by_angle.append(dict_MM_relative_energies_QM_angle_keyed[key][1])
    sorted_QM_angles_list_complement.append(dict_MM_relative_energies_QM_angle_keyed[key][2])

out_to_file=open('0_12_MM_plot_data-ALT.txt','w')
for i in range(len(sorted_QM_angles_list)):
    out_to_file.write(str(sorted_QM_angles_list[i]))
    out_to_file.write(',')
    out_to_file.write(str(sorted_MM_relative_energies_list[i]))
    out_to_file.write('\n')
out_to_file.close()

out_to_file=open('0_12_QM_plot_data-ALT.txt','w')
for i in range(len(sorted_QM_angles_list)):
    out_to_file.write(str(sorted_QM_angles_list[i]))
    out_to_file.write(',')
    out_to_file.write(str(QM_relative_energies_by_angle[i]))
    out_to_file.write('\n')
out_to_file.close()

#in_from_file=open('0_3_QM_plot_data.txt')
#QM_data_string_list=in_from_file.readlines()
#QM_relative_energies_by_angle=[]
#for i in QM_data_string_list:
#    c=i.split(',')
#    QM_relative_energies_by_angle.append(float(c[1]))
#in_from_file.close()

difference_potential_list=[]
difference_potential_squared_list=[]
out_to_file1=open('0_10_matlab_sorted_angles_data_ALT.txt','w')
out_to_file3=open('0_10_matlab_sorted_angles_data_ALT2.txt','w')
out_to_file2=open('0_11_matlab_diff_pot_data_ALT.txt','w')
for i in range(len(sorted_MM_relative_energies_list)):
    difference_potential_list.append(QM_relative_energies_by_angle[i]-sorted_MM_relative_energies_list[i])
    difference_potential_squared_list.append(difference_potential_list[i]*difference_potential_list[i])
    out_to_file1.write(str(sorted_QM_angles_list[i]))
    out_to_file1.write(',')
#    out_to_file1.write('\n')
    out_to_file2.write(str(difference_potential_list[i]))
    out_to_file2.write(',')
    out_to_file3.write(str(sorted_QM_angles_list_complement[i]))
    out_to_file3.write(',')
#    out_to_file3.write('\n') 
out_to_file1.close
out_to_file2.close
out_to_file3.close

difference_potential_squared_avg=sum(difference_potential_squared_list)/len(difference_potential_squared_list)

RMSE=math.sqrt(difference_potential_squared_avg)

image_name_string='0_12_QM_MM_PES_plot'
for i in scan_points_to_toss_list:
    image_name_string=image_name_string+'-'
    image_name_string=image_name_string+str(i)

image_name_string=image_name_string+'-tossed-ALT.png'

plt.figure()
plt.plot(sorted_QM_angles_list,QM_relative_energies_by_angle,"vk-",label='QM')
plt.plot(sorted_QM_angles_list,sorted_MM_relative_energies_list,"or-",label='MM')
plt.plot(sorted_QM_angles_list,difference_potential_list,"sb--",label='diff')
plt.legend(framealpha=1,frameon=True)
plt.xlabel('Dihedral Angle')
plt.ylabel('Energy (kcal/mol)')
plt.title('Torsional PES Scans \n RMSE='+str(RMSE))
#plt.savefig('0_12_QM_MM_PES_plot.png')
plt.savefig(image_name_string)

image_name_string='0_12_QM_MM_PES_plot_no_diff_pot'
for i in scan_points_to_toss_list:
    image_name_string=image_name_string+'-'
    image_name_string=image_name_string+str(i)

image_name_string=image_name_string+'-tossed-ALT.png'

plt.figure()
plt.plot(sorted_QM_angles_list,QM_relative_energies_by_angle,"vk-",label='QM')
plt.plot(sorted_QM_angles_list,sorted_MM_relative_energies_list,"or-",label='MM')
plt.legend(framealpha=1,frameon=True)
plt.xlabel('Dihedral Angle')
plt.ylabel('Energy (kcal/mol)')
plt.title('Torsional PES Scans \n RMSE='+str(RMSE))
#plt.savefig('0_12_QM_MM_PES_plot_no_diff_pot.png')
plt.savefig(image_name_string)





