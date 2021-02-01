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
	  
	  cout << endl << endl << "Enter number of steps: ";

	  cin >> NumSteps;
	  
  	ifstream Read;	

	char num_scan_points_filename[50];
	strcpy(num_scan_points_filename,"0_6_Number_of_unique_scan_points.txt");

	string string_from_file;
	
	Read.open(num_scan_points_filename,std::ios::app);

	getline(Read,string_from_file);

	int x=stoi(string_from_file);

	for (int loop1=1; loop1<=x; loop1++)
	{	
	  
	        ifstream ReadFromFile;
		
		ofstream WriteToFile;

		WriteToFile.precision(14);  //14 digits output
		WriteToFile.setf(ios::internal, ios::adjustfield); // internal justification
		WriteToFile.setf(ios::showpoint, ios::showpoint); // show trailing zeros
		
		cout.precision(14);  //14 digits output
		cout.setf(ios::internal, ios::adjustfield); // internal justification
		cout.setf(ios::showpoint, ios::showpoint); // show trailing zeros
		
		char DataFileName[50];
		char MinimaFileName[50];

		strcpy(DataFileName, "multiplot");
		strcpy(MinimaFileName, "minima.dat");

		char FileNumberCharArray[20];

		int FileNumber = loop1;

		sprintf(FileNumberCharArray, "%d",FileNumber);

		strcat(DataFileName, FileNumberCharArray);

		strcat(DataFileName, ".dat");

		ReadFromFile.open(DataFileName, std::ios::app);
		
		int    Read_int=0;
		double Read_double1=0;
		double Read_double2=0;
		double diff=0;
		double min=0;

		ReadFromFile >> Read_int;
		
		ReadFromFile >> Read_double1;
		
		ReadFromFile >> Read_double2;

		diff = Read_double2-Read_double1;

		min = diff;
		
		for (int loop2=1; loop2<=NumSteps; loop2++)
		{
		    ReadFromFile >> Read_int;
		
		    ReadFromFile >> Read_double1;
		
		    ReadFromFile >> Read_double2;
		
		//		string StringFromFile;
		
		//		getline(ReadFromFile,StringFromFile);
		
		//    cout << endl << " " << Read_int << " " << Read_double1 << " " << Read_double2 << " diff: " << Read_double2-Read_double1 << endl;
		    diff = Read_double2-Read_double1;

		    if (diff < min)
		      min = diff;			      
		}

		cout << endl << "multiplot" << FileNumber << " min: " << min << endl;

		ReadFromFile.close();

		WriteToFile.open(MinimaFileName, std::ios::app);
		
		WriteToFile << FileNumber << " " << min << endl;
		
		WriteToFile.close();				
		

	}

	cout << endl << endl;

	return 0;
}
