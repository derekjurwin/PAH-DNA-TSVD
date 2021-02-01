import numpy as np
import os
import time
import math

import matplotlib.pyplot as plt
  
in_from_file=open('0_3_QM_plot_data_by_angle.txt','r')
QM_data_string_list=in_from_file.readlines()
QM_angles=[]
QM_relative_energies_by_angle=[]
for i in QM_data_string_list:
    c=i.split(',')
    QM_angles.append(float(c[0]))
    QM_relative_energies_by_angle.append(float(c[1]))
in_from_file.close()

##########################################################################################################################
# TOSS DATA HERE
##########################################################################################################################
del QM_angles[18:19]
del QM_relative_energies_by_angle[18:19]

##########################################################################################################################
# TOSS DATA HERE - ADD CASE FOR NONE
##########################################################################################################################
scan_points_to_toss_string=input("Enter line numbers to toss from --0_3_QM_plot_data_by_angle.txt-- separated by spaces only: ")
scan_points_to_toss_string_split=scan_points_to_toss_string.split()

scan_points_to_toss_list=[]
for i in scan_points_to_toss_string_split:
    scan_points_to_toss_list.append(int(i))

for i in sorted(scan_points_to_toss_list,reverse=True):
    print("deleting :", i, " ",QM_angles[i-1])
    del QM_angles[i-1]
    del QM_relative_energies_by_angle[i-1]
##########################################################################################################################
##########################################################################################################################

filename_string='0_3_QM_plot_data_tossed'

for i in scan_points_to_toss_string_split:
    filename_string=filename_string+'_'
    filename_string=filename_string+i

filename_string=filename_string+'.txt'

out_to_file=open(filename_string,'w')
for i in range(len(QM_angles)):
    out_to_file.write(str(QM_angles[i])+','+str(QM_relative_energies_by_angle[i])+'\n')
out_to_file.close()

filename_string2='0_4_QM_PES_plot_tossed'

for i in scan_points_to_toss_string_split:
    filename_string2=filename_string2+'_'
    filename_string2=filename_string2+i

filename_string2=filename_string2+'.png'

plt.figure()
plt.plot(QM_angles,QM_relative_energies_by_angle,"vk-",label='QM')
plt.legend(framealpha=1,frameon=True)
plt.xlabel('Dihedral Angle')
plt.ylabel('Energy (kcal/mol)')
plt.title('QM Torsion Scan')
plt.savefig(filename_string2)





