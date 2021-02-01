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
		
		char logFileName[50];
		char datFileName[50];

		strcpy(logFileName, "Scan_Point");
		strcpy(datFileName, "multiplot");

		char FileNumberCharArray[20];

		int FileNumber = loop1;

		sprintf(FileNumberCharArray, "%d",FileNumber);

		strcat(logFileName, FileNumberCharArray);
		strcat(datFileName, FileNumberCharArray);

		strcat(logFileName, ".log");
		strcat(datFileName, ".dat");

		ReadFromFile.open(logFileName, std::ios::app);
		
		string StringFromFile;
		
		bool ContinueWhileLoop1 = true;
		
		int StepNumber = -1;
		double DoubleFromFile = -1.0;

		while(ContinueWhileLoop1)
		{
		  ReadFromFile >> StringFromFile;
		  if (StringFromFile == "ETITLE:")
		    {
		      cout << endl << "Read thru intro" << endl;
		      ContinueWhileLoop1 = false;
		    }
		}
		
		bool ContinueWhileLoop2 = true;
		
		double MISCdouble = -1.0;
		double POTENTIALdouble = -1.0;

		while(ContinueWhileLoop2)
		{
		  ReadFromFile >> StringFromFile;
		  
		  if (StringFromFile == "ENERGY:")
		  {		     
		      ReadFromFile >> StepNumber;
		   
		      if (StepNumber == NumSteps)
			ContinueWhileLoop2 = false;

		      for (int loop2 = 1; loop2 <= 8; loop2++)
		      {
			  ReadFromFile >> DoubleFromFile;
		      }	
		      
		      MISCdouble = DoubleFromFile; 
		      
		      for (int loop3 = 1; loop3 <= 4; loop3++)
		      {
			  ReadFromFile >> DoubleFromFile;
		      }
		      
		      POTENTIALdouble = DoubleFromFile;	      
	            
		      WriteToFile.open(datFileName, std::ios::app);
		      
		      WriteToFile << StepNumber << " " << MISCdouble << " " << POTENTIALdouble << endl;
		      
		      WriteToFile.close();

		  }		  
		}
	
		ReadFromFile.close();	

	}

	cout << endl << endl;

	return 0;
}
