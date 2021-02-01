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
		ifstream ReadFromFile;
		
		WriteToFile.precision(14);  //14 digits output
		WriteToFile.setf(ios::internal, ios::adjustfield); // internal justification
		WriteToFile.setf(ios::showpoint, ios::showpoint); // show trailing zeros	  
	       
		char pdbFileName[50];
		char psfgenFileName[50];
		char psfFileName[50];
		char new_pdbFileName[50];		
		
		strcpy(pdbFileName, "Scan_Point");
		strcpy(psfFileName, "Scan_Point");
		strcpy(psfgenFileName, "psfgen_Scan_Point");
		strcpy(new_pdbFileName, "Scan_Point");

		char FileNumberCharArray[20];

		int FileNumber = loop1;

		sprintf(FileNumberCharArray, "%d",FileNumber);

		strcat(pdbFileName,FileNumberCharArray);
		strcat(psfFileName,FileNumberCharArray);
		strcat(psfgenFileName,FileNumberCharArray);
		strcat(new_pdbFileName, FileNumberCharArray);

		strcat(pdbFileName, ".pdb");
		strcat(psfFileName, "_sim_new.psf");
		strcat(psfgenFileName, ".pgn");
		strcat(new_pdbFileName, "_sim_new.pdb");

		WriteToFile.open(psfgenFileName, std::ios::app);

		WriteToFile << "package require psfgen" << endl;

		//WriteToFile << "topology ./parameters/BCP_res.str" << endl;
		
		WriteToFile << "topology ./parameters/" << PAH_top_filename << endl;

		WriteToFile << "topology ./parameters/top_all36_na.rtf" << endl;

		WriteToFile << "segment U {pdb " << pdbFileName << "}" << endl;

		WriteToFile << "coordpdb " << pdbFileName << " U" << endl;

		WriteToFile << "guesscoord" << endl;

                WriteToFile << "writepdb " << new_pdbFileName << endl;

		WriteToFile << "writepsf " << psfFileName << endl;
		
		WriteToFile.close();

	}

	cout << endl << endl;

	return 0;
}
