import numpy as np
import os
import time
import math

import matplotlib.pyplot as plt

sigma_decay_list=[]
DPC_list=[]

in_from_file=open('0_20_decay.txt','r')
decay_string_list=in_from_file.readlines()
in_from_file.close()

populate_sigma_decay_list_bool=False

populate_DPC_list_bool=False

for i in decay_string_list:
    if i == '**DPC:\n':
        populate_sigma_decay_list_bool=False

    if populate_sigma_decay_list_bool:
#        sigma_decay_list.append(math.log(float(i)))
        sigma_decay_list.append(float(i))
        
    if populate_DPC_list_bool:
#        DPC_list.append(math.log(float(i)))
        DPC_list.append(float(i))
        
    if i == '**sigma decay:\n':
        populate_sigma_decay_list_bool=True
        
    if i == '**DPC:\n':
        populate_DPC_list_bool=True

u_over_sigma=[]        
for i in range(len(sigma_decay_list)):
    u_over_sigma.append(DPC_list[i]/sigma_decay_list[i])
#    u_over_sigma.append(math.log(DPC_list[i]/sigma_decay_list[i]))


for i in range(len(sigma_decay_list)):
    sigma_decay_list[i]=math.log(sigma_decay_list[i])
    DPC_list[i]=math.log(DPC_list[i])
    u_over_sigma[i]=math.log(u_over_sigma[i])
    
index=[]
#for j in range(1,25):
for j in range(1,len(DPC_list)+1):
    index.append(j)
        
ticks=[]        
#for j in range(0,26,2):
for j in range(0,len(DPC_list)+2,2):
    ticks.append(j)
        
plt.figure()
plt.plot(index,sigma_decay_list,"sr--",label='log($\sigma_i$)',zorder=3)
plt.plot(index,DPC_list,"ob--",label='log($u_i^T (b+e)$)',zorder=2)
plt.plot(index,u_over_sigma,"vg--",label='log($u_i^T (b+e) / \sigma_i$)',zorder=1)
#plt.plot(sorted_QM_angles_list,Y_LS6_list,"m-",label='LS6')
plt.legend(framealpha=1,frameon=True,loc='upper left',prop={'size':6})
plt.xlabel('Index (i)')
plt.ylabel('log($\sigma_i$) , log($u_i^T (b+e)$)')
plt.xticks(ticks)
#plt.ylim(-5.5,5)
#plt.title('LS6 Difference Potential Fit \n RMSE='+str(RMSE_LS6))
plt.savefig('0_20_DPC_plot.png')


res_norm_matrix_REG_list=[]
soln_norm_matrix_REG_list=[]

in_from_file=open('0_21_reg_norms.txt','r')
REG_norm_string_list=in_from_file.readlines()
in_from_file.close()

populate_res_norm_matrix_REG_list_bool=False

populate_soln_norm_matrix_REG_list_bool=False

for i in REG_norm_string_list:
    if i == '**soln norm:\n':
        populate_res_norm_matrix_REG_list_bool=False

    if populate_res_norm_matrix_REG_list_bool:
        res_norm_matrix_REG_list.append(math.log(float(i)))
#        res_norm_matrix_REG_list.append(float(i))

    if populate_soln_norm_matrix_REG_list_bool:
        soln_norm_matrix_REG_list.append(math.log(float(i)))

    if i == '**res norm:\n':
        populate_res_norm_matrix_REG_list_bool=True
        
    if i == '**soln norm:\n':
        populate_soln_norm_matrix_REG_list_bool=True

res_norm_matrix_TRUNC_list=[]
soln_norm_matrix_TRUNC_list=[]

in_from_file=open('0_22_trunc_norms.txt','r')
TRUNC_norm_string_list=in_from_file.readlines()
in_from_file.close()

populate_res_norm_matrix_TRUNC_list_bool=False

populate_soln_norm_matrix_TRUNC_list_bool=False

for i in TRUNC_norm_string_list:
    if i == '**soln norm:\n':
        populate_res_norm_matrix_TRUNC_list_bool=False

    if populate_res_norm_matrix_TRUNC_list_bool:
        res_norm_matrix_TRUNC_list.append(float(i))

    if populate_soln_norm_matrix_TRUNC_list_bool:
        soln_norm_matrix_TRUNC_list.append(float(i))

    if i == '**res norm:\n':
        populate_res_norm_matrix_TRUNC_list_bool=True
        
    if i == '**soln norm:\n':
        populate_soln_norm_matrix_TRUNC_list_bool=True

del res_norm_matrix_TRUNC_list[-1] 
del soln_norm_matrix_TRUNC_list[-1]

for j in range(len(res_norm_matrix_TRUNC_list)):
    res_norm_matrix_TRUNC_list[j]=math.log(res_norm_matrix_TRUNC_list[j])
    soln_norm_matrix_TRUNC_list[j]=math.log(soln_norm_matrix_TRUNC_list[j])

plt.figure()
plt.plot(res_norm_matrix_REG_list,soln_norm_matrix_REG_list,"k-",label='REG')
#plt.plot(res_norm_matrix_TRUNC_list,soln_norm_matrix_TRUNC_list,"dr",markerfacecolor='none',label='TSVD')
plt.plot(res_norm_matrix_TRUNC_list,soln_norm_matrix_TRUNC_list,"dr",label='TSVD')
#plt.plot(sorted_QM_angles_list,Y_LS6_list,"m-",label='LS6')
#plt.legend(framealpha=1,frameon=True,loc='lower center')
plt.xlabel(r'log($|| \tilde{r}_{\lambda} ||_2$),log($|| \tilde{r}_k ||_2$)')
plt.ylabel(r'log($|| \tilde{x}_{\lambda} ||_2$),log($|| \tilde{x}_k ||_2$)')
#plt.title('LS6 Difference Potential Fit \n RMSE='+str(RMSE_LS6))
plt.savefig('0_22_REG-TSVD_plot.png')

