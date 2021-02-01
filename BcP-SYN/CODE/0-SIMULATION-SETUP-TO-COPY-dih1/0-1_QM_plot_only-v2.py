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

plt.figure()
plt.plot(QM_angles,QM_relative_energies_by_angle,"vk-",label='QM')
plt.legend(framealpha=1,frameon=True)
plt.xlabel('Dihedral Angle')
plt.ylabel('Energy (kcal/mol)')
plt.title('QM Torsion Scan')
plt.savefig('0_4_QM_PES_plot_all_scan_points_plot_only.png')





