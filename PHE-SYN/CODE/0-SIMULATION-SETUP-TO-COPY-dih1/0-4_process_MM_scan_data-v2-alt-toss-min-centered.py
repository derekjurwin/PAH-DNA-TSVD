import numpy as np
import os
import time
import math

import matplotlib.pyplot as plt

#os.system('./8_Read_log')

#time.sleep(2)

#os.system('./9_ReadData')

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

shifted_angles_ordered_by_scan_point=[]
    
for i in range(len(angles_ordered_by_scan_point_list)):
    if i>len(angles_ordered_by_scan_point_list)/2-1 and angles_ordered_by_scan_point_list[i]<0.0:
        shifted_angles_ordered_by_scan_point.append(angles_ordered_by_scan_point_list[i]+360.0)
    else:
        shifted_angles_ordered_by_scan_point.append(angles_ordered_by_scan_point_list[i])

#print(angles_ordered_by_scan_point_list)

#print('\n')

#print(shifted_angles_ordered_by_scan_point)

#print('\n')


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
    del MM_relative_energies_by_scan_point[i-1]
    del QM_relative_energies_by_scan_point[i-1]
    del shifted_angles_ordered_by_scan_point[i-1]

    #print(shifted_angles_ordered_by_scan_point)

    #print(angles_ordered_by_scan_point_list)
    #print(MM_relative_energies_by_scan_point)
    #print(QM_relative_energies_by_scan_point)
##########################################################################################################################
##########################################################################################################################

#print(angles_ordered_by_scan_point_list)

#print('\n')

#print(shifted_angles_ordered_by_scan_point)

#print('\n')

# PUT QM ANGLES AND MM ENERGIES IN A DICTIONARY SO THEY ARE MARRIED
dict_MM_relative_energies_QM_angle_keyed={}
index_counter=0
for i in angles_ordered_by_scan_point_list:
    dict_MM_relative_energies_QM_angle_keyed[i]=(MM_relative_energies_by_scan_point[index_counter],QM_relative_energies_by_scan_point[index_counter])
    index_counter+=1

#print(dict_MM_relative_energies_QM_angle_keyed)

#print('\n')
    
dict_scan_point_keyed_shifted_angles={}

for i in range(len(shifted_angles_ordered_by_scan_point)):
    dict_scan_point_keyed_shifted_angles[i+1]=(shifted_angles_ordered_by_scan_point[i],MM_relative_energies_by_scan_point[i],QM_relative_energies_by_scan_point[i])

#print(dict_scan_point_keyed_shifted_angles)

#print('\n')

    
all_scan_points_sorted_by_angles=sorted(dict_scan_point_keyed_shifted_angles.items(),key=lambda x: x[1], reverse=True)

#print(all_scan_points_sorted_by_angles)

#print('\n')

shifted_angles=[]
shifted_QM_energy=[]
shifted_MM_energy=[]

for i in all_scan_points_sorted_by_angles:
    shifted_angles.append(i[1][0])
    shifted_MM_energy.append(i[1][1])
    shifted_QM_energy.append(i[1][2])


    
# SORT THE DICTIONARY AND CREATE NEW LISTS WHERE QM ANGLES AND MM ENERGIES ARE SORTED BY QM ANGLE
# IMPERATIVE FOR DIFFERENCE POTENTIAL AND PLOTTING
sorted_QM_angles_list=[]
sorted_MM_relative_energies_list=[]
QM_relative_energies_by_angle=[]
for key in sorted(dict_MM_relative_energies_QM_angle_keyed):
    sorted_QM_angles_list.append(key)
    sorted_MM_relative_energies_list.append(dict_MM_relative_energies_QM_angle_keyed[key][0])
    QM_relative_energies_by_angle.append(dict_MM_relative_energies_QM_angle_keyed[key][1])
    
#out_to_file=open('0_12_MM_plot_data-1.txt','w')
#for i in range(len(sorted_QM_angles_list)):
#    out_to_file.write(str(sorted_QM_angles_list[i]))
#    out_to_file.write(',')
#    out_to_file.write(str(sorted_MM_relative_energies_list[i]))
#    out_to_file.write('\n')
#out_to_file.close()

#out_to_file=open('0_12_QM_plot_data-1.txt','w')
#for i in range(len(sorted_QM_angles_list)):
#    out_to_file.write(str(sorted_QM_angles_list[i]))
#    out_to_file.write(',')
#    out_to_file.write(str(QM_relative_energies_by_angle[i]))
#    out_to_file.write('\n')
#out_to_file.close()

#in_from_file=open('0_3_QM_plot_data.txt')
#QM_data_string_list=in_from_file.readlines()
#QM_relative_energies_by_angle=[]
#for i in QM_data_string_list:
#    c=i.split(',')
#    QM_relative_energies_by_angle.append(float(c[1]))
#in_from_file.close()


difference_potential_list=[]
difference_potential_squared_list=[]
#out_to_file1=open('0_10_matlab_sorted_angles_data-1.txt','w')
#out_to_file2=open('0_11_matlab_diff_pot_data-1.txt','w')
for i in range(len(sorted_MM_relative_energies_list)):
    difference_potential_list.append(QM_relative_energies_by_angle[i]-sorted_MM_relative_energies_list[i])
    difference_potential_squared_list.append(difference_potential_list[i]*difference_potential_list[i])
#    out_to_file1.write(str(sorted_QM_angles_list[i]))
#    out_to_file1.write(',')
#    out_to_file2.write(str(difference_potential_list[i]))
#    out_to_file2.write(',')
#out_to_file1.close
#out_to_file2.close

difference_potential_squared_avg=sum(difference_potential_squared_list)/len(difference_potential_squared_list)

RMSE=math.sqrt(difference_potential_squared_avg)
    
#plt.figure()
#plt.plot(sorted_QM_angles_list,QM_relative_energies_by_angle,"vk-",label='QM')
#plt.plot(sorted_QM_angles_list,sorted_MM_relative_energies_list,"or-",label='MM')
#plt.plot(sorted_QM_angles_list,difference_potential_list,"sb--",label='diff')
#plt.legend(framealpha=1,frameon=True)
#plt.xlabel('Dihedral Angle')
#plt.ylabel('Energy (kcal/mol)')
#plt.title('Torsional PES Scans \n RMSE='+str(RMSE))
#plt.savefig('0_12_QM_MM_PES_plot-1.png')
#
#plt.figure()
#plt.plot(sorted_QM_angles_list,QM_relative_energies_by_angle,"vk-",label='QM')
#plt.plot(sorted_QM_angles_list,sorted_MM_relative_energies_list,"or-",label='MM')
#plt.legend(framealpha=1,frameon=True)
#plt.xlabel('Dihedral Angle')
#plt.ylabel('Energy (kcal/mol)')
#plt.title('Torsional PES Scans \n RMSE='+str(RMSE))
#plt.savefig('0_12_QM_MM_PES_plot_no_diff_pot-1.png')

image_name_string='0_12_QM_MM_PES_plot_no_diff_pot-min-centered'
for i in scan_points_to_toss_list:
    image_name_string=image_name_string+'-'
    image_name_string=image_name_string+str(i)

image_name_string=image_name_string+'-tossed.png'

#MINIMUM CENTETED PLOTS
plt.figure()
plt.plot(shifted_angles,shifted_QM_energy,"vk-",label='QM')
plt.plot(shifted_angles,shifted_MM_energy,"or-",label='MM')
plt.legend(framealpha=1,frameon=True)
plt.xlabel('Dihedral Angle')
plt.ylabel('Energy (kcal/mol)')
plt.title('Torsional PES Scans \n RMSE='+str(RMSE))
#plt.savefig('0_12_QM_MM_PES_plot_no_diff_pot-min-centered.png')    
plt.savefig(image_name_string)

################################################################################
################################################################################
################################################################################

