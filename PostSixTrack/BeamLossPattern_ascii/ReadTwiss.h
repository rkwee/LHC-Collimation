
#include <string>
#include <sstream>
#include <iostream>
#include <fstream>
#include <vector>

#include <iomanip>
#include <algorithm>

#include <stdio.h>
#include <stdlib.h> 
#include <string.h> 
#include <ctype.h>
#include <math.h>

#ifndef ReadTwiss_h
#define ReadTwiss_h 1

using namespace std;

void ReadTwiss(string in, vector<string> *K, vector<string> *N, 
	       vector<string> *Pa, vector<string> *Kn, vector<string> *Nn, 
	       vector<string> *Pan, vector<double> *P, vector<double> *L, 
	       vector<double> *A1, vector<double> *A2, vector<double> *A3, 
	       vector<double> *A4);

void ReadTwissNoDrifts(string in, vector<string> *K, vector<string> *N, 
		       vector<string> *Pa, vector<string> *Kn, vector<string> *Nn, 
		       vector<string> *Pan, vector<double> *P, vector<double> *L, 
		       vector<double> *A1, vector<double> *A2, vector<double> *A3, 
		       vector<double> *A4);

void ReadTwissK(string in, vector<string> *K, vector<string> *N, 
		vector<string> *Pa, vector<string> *Kn, vector<string> *Nn, 
		vector<string> *Pan, vector<double> *P, vector<double> *L, 
		vector<double> *KL, vector<double> *A1, vector<double> *A2, 
		vector<double> *A3, vector<double> *A4);

// Read also the aperture offset.
// Also used to read the x and y offsets due to the crossing scheme!
void ReadTwissDX(string in, vector<string> *K, vector<string> *N, vector<string> *Pa, 
		 vector<string> *Kn, vector<string> *Nn, vector<string> *Pan, 
		 vector<double> *P, vector<double> *L, vector<double> *A1, 
		 vector<double> *A2, vector<double> *A3, vector<double> *A4, 
		 vector<double> *DX, vector<double> *DY);

void ReadTwissDXNoDrifts(string in, vector<string> *K, vector<string> *N, vector<string> *Pa, 
			 vector<string> *Kn, vector<string> *Nn, vector<string> *Pan, 
			 vector<double> *P, vector<double> *L, vector<double> *A1, 
			 vector<double> *A2, vector<double> *A3, vector<double> *A4, 
			 vector<double> *DX, vector<double> *DY);
#endif
