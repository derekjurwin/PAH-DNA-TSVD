import matplotlib.pyplot as plt

dict_scan_point_keyed={}

def Parse_Scan_File(scan_filename,dih_to_match_string,scan_point_counter):
    energy_token_string='MP2='
    energy_token_string2='EUMP2 ='
    matched_line_from_file_list=[]

    angles_list=[]
    energies_list_to_parse=[]
    energies_list=[]
    energy_summary_string=''

    energies_list2=[]

    dih_to_match_counter=0

    read_energy_line_bool=False

    with open(scan_filename,'r') as file:
        
        for line in file:
            
            if dih_to_match_string in line:                
                dih_to_match_counter+=1
                x=line.split()
                
                if dih_to_match_counter>1:                    
                    angles_list.append(x[3])

            if energy_token_string2 in line:
                x=line.split()
                energy_string=''

                for i in x[5]:
                    if i=='D':
                        energy_string=energy_string+'E'
                    else:
                        energy_string=energy_string+i
                        
                energies_list2.append(float(energy_string))
                
#            if energy_token_string in line:
#                read_energy_line_bool=True
#
#            if read_energy_line_bool:
#                energy_summary_string=energy_summary_string+line
#
#            if 'RMSD=' in line:
#                read_energy_line_bool=False
#
#    a,b,c=energy_summary_string.partition('=')
#
#    d,e,f=c.partition('\RMSD')
#
#    energies_list_to_parse=d.split(',')
#
#    for i in energies_list_to_parse:
#
#        if '\n' in i:
#            energies_list.append(i.replace('\n ',''))
#            
#        else:
#            energies_list.append(i)
#
#    energies_list_float=[]
#
#    for i in energies_list:
#        energies_list_float.append(float(i))

    angles_list_float=[]

    for i in angles_list:
        angles_list_float.append(float(i))

    out_filename='0_1_QM_scan_data_'+scan_filename+'.txt'
        
    out_to_file=open(out_filename,'w')

    for i in range(len(angles_list)):
        scan_point_counter+=1
#        dict_angle_keyed[angles_list_float[i]]=(scan_point_counter,energies_list_float[i])
#        dict_scan_point_keyed[scan_point_counter]=(angles_list_float[i],energies_list_float[i])
        dict_scan_point_keyed[scan_point_counter]=(angles_list_float[i],energies_list2[i])
        out_to_file.write(str(scan_point_counter))
        out_to_file.write(',')
        out_to_file.write(angles_list[i])
        out_to_file.write(',')
        out_to_file.write(str(energies_list2[i]))
        out_to_file.write('\n')
    
    out_to_file.close()

#    out_filename='0_1_QM_scan_data_'+scan_filename+'.txt.ffTK'
#        
#    out_to_file=open(out_filename,'w')
#
#    for i in range(len(angles_list)):
#        out_to_file.write(angles_list[i])
#        out_to_file.write(',')
#        out_to_file.write(str(energies_list2[i]))
#        out_to_file.write('\n')
#    
#    out_to_file.close()

    
    return scan_point_counter

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
dih_to_match_string=simulation_data[2]

# UNCOMMENT FOR FINAL VERSION
#neg_scan_filename=input("Enter neg log file name: ")
#pos_scan_filename=input("Enter pos log file name: ")
#dih_to_match_string=input("Enter D(#,#,#,#) to match: ")

# DELETE FOR FINAL VERSION
#neg_scan_filename='BCP.scan1.neg.fixed-SYN.150deg-start.log'
#pos_scan_filename='BCP.scan1.pos.fixed-SYN.150deg-start.log'
#dih_to_match_string='D(11,12,35,36)'


scan_point_counter=0
scan_point_counter=Parse_Scan_File(neg_scan_filename,dih_to_match_string,scan_point_counter)
scan_point_counter=Parse_Scan_File(pos_scan_filename,dih_to_match_string,scan_point_counter)

num_unique_scan_points=scan_point_counter

#out_to_file=open('0_0_simulation_data.txt','w')
#out_to_file.write(neg_scan_filename)
#out_to_file.write('\n')
#out_to_file.write(pos_scan_filename)
#out_to_file.write('\n')
#out_to_file.write(dih_to_match_string)
#out_to_file.write('\n')
#out_to_file.write(str(num_unique_scan_points))
#out_to_file.write('\n')
#out_to_file.close()

scan_point_angles_list_float=[]
scan_point_energies_list_float=[]
scan_point_relative_energies_list_kcal_float=[]

all_scan_points_sorted_by_angles=sorted(dict_scan_point_keyed.items(),key=lambda x: x[1], reverse=True)

for i in all_scan_points_sorted_by_angles:
    scan_point_angles_list_float.append(i[1][0])
    scan_point_energies_list_float.append(i[1][1])

scan_point_min_energy_value=min(scan_point_energies_list_float)

for i in range(len(scan_point_energies_list_float)):
    scan_point_relative_energies_list_kcal_float.append(scan_point_energies_list_float[i]*627.5095-scan_point_min_energy_value*627.5095)
 
plt.figure()
plt.plot(scan_point_angles_list_float,scan_point_relative_energies_list_kcal_float,"vk--")
plt.xlabel('dihedral angle')
plt.ylabel('relative E (kcal/mol)')
plt.title('QM Torsion Scan - All Scan Points')

out_to_file=open('0_3_QM_plot_data_by_angle.txt','w')
for i in range(len(scan_point_angles_list_float)):
    out_to_file.write(str(scan_point_angles_list_float[i]))
    out_to_file.write(',')
    out_to_file.write(str(scan_point_relative_energies_list_kcal_float[i]))
    out_to_file.write('\n')
out_to_file.close()

plt.savefig('0_4_QM_PES_plot_all_scan_points.png')

out_to_file=open('0_2_QM_scan_data_sorted_by_all_scan_points.txt','w')
    
for key in dict_scan_point_keyed.keys():
    out_to_file.write('Scan Point '+str(key))
    out_to_file.write(',')
    out_to_file.write(str(dict_scan_point_keyed[key][0]))
    out_to_file.write(',')
    out_to_file.write(str(float(dict_scan_point_keyed[key][1])))
    out_to_file.write(',')
    out_to_file.write(str(float(dict_scan_point_keyed[key][1])*627.5095))
    out_to_file.write(',')
    out_to_file.write(str(float(dict_scan_point_keyed[key][1])*627.5095-scan_point_min_energy_value*627.5095))
    out_to_file.write('\n')

out_to_file.close()


#MINIMUM CENTERED PLOTS - DECIDE WHICH VERSION TO KEEP...  ABOVE OR THIS...  
scan_point_angles_list_float=[]
scan_point_energies_list_float=[]
scan_point_relative_energies_list_kcal_float=[]

dict_scan_point_keyed_shifted_angles={}

for key in dict_scan_point_keyed.keys():
    if int(key)>num_unique_scan_points/2 and float(dict_scan_point_keyed[key][0]<0):
        dict_scan_point_keyed_shifted_angles[key]=(dict_scan_point_keyed[key][0]+360.0,dict_scan_point_keyed[key][1]) #THIS IS DUMB...
    else:
        dict_scan_point_keyed_shifted_angles[key]=(dict_scan_point_keyed[key][0],dict_scan_point_keyed[key][1])

all_scan_points_sorted_by_angles=sorted(dict_scan_point_keyed_shifted_angles.items(),key=lambda x: x[1], reverse=True)

for i in all_scan_points_sorted_by_angles:
    scan_point_angles_list_float.append(i[1][0])
    scan_point_energies_list_float.append(i[1][1])
     
scan_point_min_energy_value=min(scan_point_energies_list_float)

for i in range(len(scan_point_energies_list_float)):
    scan_point_relative_energies_list_kcal_float.append(scan_point_energies_list_float[i]*627.5095-scan_point_min_energy_value*627.5095)
 
plt.figure()
plt.plot(scan_point_angles_list_float,scan_point_relative_energies_list_kcal_float,"vk--")
plt.xlabel('dihedral angle')
plt.ylabel('relative E (kcal/mol)')
plt.title('QM Torsion Scan - Minimum Centered')

out_to_file=open('0_3_QM_plot_data_minimum_centered.txt','w')
for i in range(len(scan_point_angles_list_float)):
    out_to_file.write(str(scan_point_angles_list_float[i]))
    out_to_file.write(',')
    out_to_file.write(str(scan_point_relative_energies_list_kcal_float[i]))
    out_to_file.write('\n')
out_to_file.close()

plt.savefig('0_4_QM_PES_plot_minimum_centered.png')

out_to_file=open('0_2_QM_scan_data_minimum_centered.txt','w')
    
for key in dict_scan_point_keyed.keys():
    out_to_file.write('Scan Point '+str(key))
    out_to_file.write(',')
    out_to_file.write(str(dict_scan_point_keyed[key][0]))
    out_to_file.write(',')
    out_to_file.write(str(float(dict_scan_point_keyed[key][1])))
    out_to_file.write(',')
    out_to_file.write(str(float(dict_scan_point_keyed[key][1])*627.5095))
    out_to_file.write(',')
    out_to_file.write(str(float(dict_scan_point_keyed[key][1])*627.5095-scan_point_min_energy_value*627.5095))
    out_to_file.write('\n')

out_to_file.close()
















