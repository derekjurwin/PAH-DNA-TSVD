#include <iostream>
#include <fstream>
#include <cstdlib>
#include <string>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <vector>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <chrono>
#include <thread>


using namespace std;

using namespace std::this_thread;
using namespace std::chrono_literals;
using std::chrono::system_clock;

int main()
{
       	ifstream Read;	

	char num_scan_points_filename[50];
	strcpy(num_scan_points_filename,"0_6_Number_of_unique_scan_points.txt");

	string string_from_file;
	
	Read.open(num_scan_points_filename,std::ios::app);

	getline(Read,string_from_file);

	int x=stoi(string_from_file);
  
	for (int loop1=1; loop1<=x; loop1++)
	{	
		char psfgenFileName[50];

		strcpy(psfgenFileName, "psfgen_Scan_Point");

		char FileNumberCharArray[20];

		int FileNumber = loop1;

		sprintf(FileNumberCharArray, "%d",FileNumber);

		strcat(psfgenFileName, FileNumberCharArray);

		strcat(psfgenFileName, ".pgn");
		
		char SystemCallText[200];

		strcpy(SystemCallText, "vmd -dispdev text -e ");
		
		strcat(SystemCallText, psfgenFileName);
		
		strcat(SystemCallText, " & ");
		
		system(SystemCallText);

		sleep_for(5s);

	}

	cout << endl << endl;

	return 0;
}
