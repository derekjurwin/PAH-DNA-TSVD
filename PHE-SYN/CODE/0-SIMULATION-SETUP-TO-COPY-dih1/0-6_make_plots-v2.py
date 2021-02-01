import numpy as np
import os
import time
import math

import matplotlib.pyplot as plt

angles_list=[]
difference_potential_list=[]
difference_potential_squared_list=[]
sorted_QM_angles_list=[]

in_from_file=open('0_10_matlab_sorted_angles_data.txt','r')
sorted_angles_string_list=in_from_file.readlines()
in_from_file.close()

string_to_split=sorted_angles_string_list[0]

string_list_to_convert_to_float=string_to_split.split(',')

del string_list_to_convert_to_float[-1]

for i in string_list_to_convert_to_float:
    sorted_QM_angles_list.append(float(i))


in_from_file=open('0_11_matlab_diff_pot_data.txt','r')
diff_pot_string_list=in_from_file.readlines()
in_from_file.close()

string_to_split=diff_pot_string_list[0]

string_list_to_convert_to_float=string_to_split.split(',')

del string_list_to_convert_to_float[-1]

for i in string_list_to_convert_to_float:
    difference_potential_list.append(float(i))
    difference_potential_squared_list.append(float(i)*float(i))

difference_potential_squared_avg=sum(difference_potential_squared_list)/len(difference_potential_squared_list)

RMSE=math.sqrt(difference_potential_squared_avg)
    
#re-write these with loops when you're not tired
in_from_file=open('0_14_matlab_output_LS3.txt','r')
LS3_string_list=in_from_file.readlines()
LS3_c1=float(LS3_string_list[1])
LS3_c2=float(LS3_string_list[2])
LS3_c3=float(LS3_string_list[3])
LS3_delta1=float(LS3_string_list[5])*math.pi/180
LS3_delta2=float(LS3_string_list[6])*math.pi/180
LS3_delta3=float(LS3_string_list[7])*math.pi/180
RMSE_LS3=float(LS3_string_list[9])
in_from_file.close()

in_from_file=open('0_15_matlab_output_LS6.txt','r')
LS6_string_list=in_from_file.readlines()
LS6_c1=float(LS6_string_list[1])
LS6_c2=float(LS6_string_list[2])
LS6_c3=float(LS6_string_list[3])
LS6_c4=float(LS6_string_list[4])
LS6_c5=float(LS6_string_list[5])
LS6_c6=float(LS6_string_list[6])
LS6_delta1=float(LS6_string_list[8])*math.pi/180.0
LS6_delta2=float(LS6_string_list[9])*math.pi/180.0
LS6_delta3=float(LS6_string_list[10])*math.pi/180.0
LS6_delta4=float(LS6_string_list[11])*math.pi/180.0
LS6_delta5=float(LS6_string_list[12])*math.pi/180.0
LS6_delta6=float(LS6_string_list[13])*math.pi/180.0
RMSE_LS6=float(LS6_string_list[15])
in_from_file.close()

out_to_file=open('0_18_parameters.txt','w')
out_to_file.write('LS3 parameters RMSE='+str(RMSE_LS3)+'\n')
for i in range(1,4,1):    
    out_to_file.write(LS3_string_list[i][:-1]+'  '+str(i)+'  '+LS3_string_list[i+4][:-1]+'     \n')    
out_to_file.write('LS6 parameters RMSE='+str(RMSE_LS6)+'\n')
for i in range(1,7,1): 
    out_to_file.write(LS6_string_list[i][:-1]+'  '+str(i)+'  '+LS6_string_list[i+7][:-1]+'     \n')    
out_to_file.close()

Ycgff_list=[]
Yfftk_list=[]
Y_LS3_list=[]
Y_LS6_list=[]
for j in sorted_QM_angles_list:
    Ycgff_list.append(2.5*(1+math.cos(1*j*math.pi/180-math.pi))+1.5*(1+math.cos(2*j*math.pi/180-0))+0.5*(1+math.cos(3*j*math.pi/180-0)))
    Yfftk_list.append(2.536*(1+math.cos(1*j*math.pi/180-math.pi))+1.686*(1+math.cos(2*j*math.pi/180-math.pi))+0.809*(1+math.cos(3*j*math.pi/180-math.pi)))
    Y_LS3_list.append(LS3_c1*(1+math.cos(1*j*math.pi/180-LS3_delta1))+LS3_c2*(1+math.cos(2*j*math.pi/180-LS3_delta2))+LS3_c3*(1+math.cos(3*j*math.pi/180-LS3_delta3)))
    Y_LS6_list.append(LS6_c1*(1+math.cos(1*j*math.pi/180-LS6_delta1))+LS6_c2*(1+math.cos(2*j*math.pi/180-LS6_delta2))+LS6_c3*(1+math.cos(3*j*math.pi/180-LS6_delta3))+LS6_c4*(1+math.cos(4*j*math.pi/180-LS6_delta4))+LS6_c5*(1+math.cos(5*j*math.pi/180-LS6_delta5))+LS6_c6*(1+math.cos(6*j*math.pi/180-LS6_delta6)))

cTcgff=sum(Ycgff_list)/(len(sorted_QM_angles_list))
cTfftk=sum(Yfftk_list)/(len(sorted_QM_angles_list))
cT_LS3=sum(Y_LS3_list)/(len(sorted_QM_angles_list))
cT_LS6=sum(Y_LS6_list)/(len(sorted_QM_angles_list))
cT=sum(difference_potential_list)/(len(sorted_QM_angles_list))

difference_potential_list_shifted=[]
for i in range(len(sorted_QM_angles_list)):
    Ycgff_list[i]=Ycgff_list[i]-cTcgff;
    Yfftk_list[i]=Yfftk_list[i]-cTfftk;
    Y_LS3_list[i]=Y_LS3_list[i]-cT_LS3
    Y_LS6_list[i]=Y_LS6_list[i]-cT_LS6
    difference_potential_list_shifted.append(difference_potential_list[i]-cT)
    
r_cgff=[]
r_fftk=[]
r_cgff_squared=[]
r_fftk_squared=[]
for i in range(len(sorted_QM_angles_list)):
    r_cgff.append(Ycgff_list[i]-difference_potential_list_shifted[i])
    r_cgff_squared.append((Ycgff_list[i]-difference_potential_list_shifted[i])*(Ycgff_list[i]-difference_potential_list_shifted[i]))
    r_fftk.append(Yfftk_list[i]-difference_potential_list_shifted[i])
    r_fftk_squared.append((Yfftk_list[i]-difference_potential_list_shifted[i])*(Yfftk_list[i]-difference_potential_list_shifted[i]))
  
r_cgff_squared_avg=sum(r_cgff_squared)/len(r_cgff_squared)
r_fftk_squared_avg=sum(r_fftk_squared)/len(r_fftk_squared)

RMSE_cgff=math.sqrt(r_cgff_squared_avg)
RMSE_fftk=math.sqrt(r_fftk_squared_avg)
    
plt.figure()
plt.plot(sorted_QM_angles_list,difference_potential_list_shifted,"sb--",label='QM-MM diff')
plt.plot(sorted_QM_angles_list,Ycgff_list,"m-",label='CGenFF')
plt.legend(framealpha=1,frameon=True)
plt.xlabel('Dihedral Angle')
plt.ylabel('Energy (kcal/mol)')
plt.title('CGenFF Difference Potential Fit \n RMSE='+str(RMSE_cgff))
plt.savefig('0_16_diff_pot_CGenFF-fit_plot.png')

plt.figure()
plt.plot(sorted_QM_angles_list,difference_potential_list_shifted,"sb--",label='QM-MM diff')
plt.plot(sorted_QM_angles_list,Yfftk_list,"m-",label='FFTK')
plt.legend(framealpha=1,frameon=True)
plt.xlabel('Dihedral Angle')
plt.ylabel('Energy (kcal/mol)')
plt.title('FFTK Difference Potential Fit \n RMSE='+str(RMSE_fftk))
plt.savefig('0_16_diff_pot_FFTK-fit_plot.png')
  
plt.figure()
plt.plot(sorted_QM_angles_list,difference_potential_list_shifted,"sb--",label='QM-MM diff')
plt.plot(sorted_QM_angles_list,Y_LS3_list,"m-",label='LS3')
plt.legend(framealpha=1,frameon=True)
plt.xlabel('Dihedral Angle')
plt.ylabel('Energy (kcal/mol)')
plt.title('LS3 Difference Potential Fit \n RMSE='+str(RMSE_LS3))
plt.savefig('0_17_diff_pot_LS3-fit_plot.png')

plt.figure()
plt.plot(sorted_QM_angles_list,difference_potential_list_shifted,"sb--",label='QM-MM diff')
plt.plot(sorted_QM_angles_list,Y_LS6_list,"m-",label='LS6')
plt.legend(framealpha=1,frameon=True)
plt.xlabel('Dihedral Angle')
plt.ylabel('Energy (kcal/mol)')
plt.title('LS6 Difference Potential Fit \n RMSE='+str(RMSE_LS6))
plt.savefig('0_17_diff_pot_LS6-fit_plot.png')

