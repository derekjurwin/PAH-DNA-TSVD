#include <iostream>
#include <fstream>
#include <cstdlib>
#include <string>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <vector>

using namespace std;

int main()
{
	  int NumSteps = 0;
	  int Temp = 0;
	  
	  cout << endl << endl << "Enter number of steps: ";

	  cin >> NumSteps;

          cout << endl << endl << "Enter temperature: ";

	  cin >> Temp;

	  char PAH_top_filename[50];

	  cout << endl << endl << "Enter name of PAH topology file: ";

	  cin >> PAH_top_filename;

  	ifstream Read;	

	char num_scan_points_filename[50];
	strcpy(num_scan_points_filename,"0_6_Number_of_unique_scan_points.txt");

	string string_from_file;
	
	Read.open(num_scan_points_filename,std::ios::app);

	getline(Read,string_from_file);

	int x=stoi(string_from_file);

	  
	for (int loop1=1; loop1<=x; loop1++)
	{	
	  
	        ofstream WriteToFile;
		
		WriteToFile.precision(14);  //14 digits output
		WriteToFile.setf(ios::internal, ios::adjustfield); // internal justification
		WriteToFile.setf(ios::showpoint, ios::showpoint); // show trailing zeros
	  
		char confFileName[50];
		char colvarFileName[50];
		char pdbFileName[50];
		char psfFileName[50];
		char outputFileName[50];
		char fixedAtomsFileName[50];

		strcpy(confFileName, "Scan_Point");
		strcpy(colvarFileName, "Scan_Point");
		strcpy(pdbFileName, "Scan_Point");
		strcpy(psfFileName, "Scan_Point");
		strcpy(outputFileName, "Scan_Point");
		strcpy(fixedAtomsFileName, "Scan_Point");
		

		char FileNumberCharArray[20];

		int FileNumber = loop1;

		sprintf(FileNumberCharArray, "%d",FileNumber);

		strcat(confFileName, FileNumberCharArray);
		strcat(colvarFileName, FileNumberCharArray);
		strcat(pdbFileName,FileNumberCharArray);
		strcat(psfFileName,FileNumberCharArray);
		strcat(outputFileName, FileNumberCharArray);
		strcat(fixedAtomsFileName, FileNumberCharArray);

		strcat(confFileName, ".conf");
		strcat(colvarFileName, "_colvars.conf");
		strcat(pdbFileName, "_sim_new.pdb");
		strcat(psfFileName, "_sim_new.psf");
		strcat(fixedAtomsFileName, "_FixedAtoms.pdb");
		
		WriteToFile.open(confFileName, std::ios::app);

		WriteToFile << "#############################################################" << endl;
		WriteToFile << "## JOB DESCRIPTION                                         ##" << endl;
		WriteToFile << "#############################################################" << endl;
		
		WriteToFile << endl;
		
		WriteToFile << "# Minimize Energy BAP" << endl;
		
		WriteToFile << endl;
		
		WriteToFile << "#############################################################" << endl;
		WriteToFile << "## ADJUSTABLE PARAMETERS                                   ##" << endl;
		WriteToFile << "#############################################################" << endl;

		WriteToFile << endl;

		WriteToFile << "structure          ./" << psfFileName << endl;		
		WriteToFile << "coordinates        ./" << pdbFileName << endl; 

		WriteToFile << "#############################################################" << endl;
		WriteToFile << "## SIMULATION PARAMETERS                                   ##" << endl;
		WriteToFile << "#############################################################" << endl;

		WriteToFile << endl;

		WriteToFile << "colvars on" << endl;
		WriteToFile << "colvarsConfig " << colvarFileName << endl; 

		WriteToFile << endl;
		
		WriteToFile << "paraTypeCharmm	    on" << endl;
		WriteToFile << "#parameters          ./parameters/par_all27_prot_lipid.inp" << endl;
		WriteToFile << "parameters          ./parameters/par_all36_na.prm" << endl;
		//WriteToFile << "parameters	    ./parameters/BCP_res.str" << endl;
		WriteToFile << "parameters	    ./parameters/" << PAH_top_filename << endl;
		WriteToFile << "parameters	    ./parameters/par_all36_cgenff.prm" << endl;

		WriteToFile << endl;

		WriteToFile << "set outputname     " << outputFileName << endl;
		WriteToFile << "outputName          $outputname" << endl;
		WriteToFile << "dcdfile		    $outputname.dcd" << endl;
		WriteToFile << "xstfile		    $outputname.xst" << endl;
		WriteToFile << "dcdfreq   	    10        " << endl;
		WriteToFile << "xstfreq   	    10        " << endl;

		WriteToFile << endl;	

		WriteToFile << "binaryoutput   	    no        " << endl;
		WriteToFile << "binaryrestart       no        " << endl;
		WriteToFile << "outputEnergies      10" << endl;
		WriteToFile << "restartfreq         1000  ;# 500steps = every 1ps" << endl;

		WriteToFile << endl;	

		WriteToFile << "fixedAtoms       	on" << endl;
		WriteToFile << "fixedAtomsForces	on" << endl;
		WriteToFile << "fixedAtomsFile		" << fixedAtomsFileName << endl;
		WriteToFile << "fixedAtomsCol		B" << endl;         

		WriteToFile << endl;

                WriteToFile << "exclude             scaled1-4" << endl;
		WriteToFile << "1-4scaling          1.0" << endl;
                WriteToFile << "COMmotion           no" << endl;
		WriteToFile << "dielectric          1.0" << endl;

		WriteToFile << endl;

		WriteToFile << "switching           on" << endl;
		WriteToFile << "switchdist          9" << endl;
		WriteToFile << "cutoff              10.0 #CHARMM prescribed value" << endl;
		WriteToFile << "pairlistdist        12.0" << endl;

		WriteToFile << endl;

		WriteToFile << "firsttimestep      0" << endl;
                WriteToFile << "timestep            1.0  ;# 2fs/step " << endl;
                WriteToFile << "stepspercycle       20" << endl;
                WriteToFile << "nonbondedFreq       2 " << endl;
                WriteToFile << "fullElectFrequency  4 " << endl;

		WriteToFile << endl;		

		WriteToFile << "set temperature       " << Temp << endl; 
		WriteToFile << "temperature         $temperature" << endl;
		
		WriteToFile << endl;

                WriteToFile << "minimize 	    " << NumSteps << endl;
		
		WriteToFile << endl;

		WriteToFile.close();

	}

	cout << endl << endl;

	return 0;
}
