
#include <string>
#include <sstream>
#include <iostream>
#include <fstream>
/*
 * Definition of a series of functions to define and plot 
 * the aperture of the all LHC sequence.
 *
 *
 *
 *
 *
 *
 * Alternative: Generate a 'Sequence' object instead of usinf functions??
 */

#include <vector>

#include <iomanip>
#include <algorithm>

#include <stdio.h>
#include <stdlib.h> 
#include <string.h> 
#include <ctype.h>
#include <math.h>

#include "Aperture.h"
#include "OneMetre.h"
#include "OneMetreAlign.h"
#include "ReadTwiss.h"

#ifndef AssignOneMetre_h
#define AssignOneMetre_h 1

using namespace std;

void AssignOneMetre(vector<OneMetre> *TheSequence, vector<string> K, vector<string> N, 
		    vector<string> Pa, vector<double> P, vector<double> L, 
		    vector<double> A1, vector<double> A2, vector<double> A3, 
		    vector<double> A4);

void AssignOneMetreAlign(vector<OneMetreAlign> *TheSequence, vector<string> K, vector<string> N, 
			 vector<string> Pa, vector<double> P, vector<double> L, 
			 vector<double> A1, vector<double> A2, vector<double> A3, 
			 vector<double> A4, vector<double> DxA, vector<double> DyA);

// Write on a file the aperture from (s1-1) to (s2+1)
// Give only the points where the aperture is defined
void PlotSomeMetres(vector<OneMetre> TheSequence, double s1, double s2, string output);
void PlotAll(vector<OneMetre> TheSequence, string output);
// Intepolate the define aperture to get the information every Ds
void PlotSomeMetres(vector<OneMetre> TheSequence, double s1, double s2, double Ds, string output);
void PlotAll(vector<OneMetre> TheSequence, double Ds, string output);

#endif
