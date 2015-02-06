/*
 * OneMetre.h (SR, May 2004)
 *
 * Definition of one object that contains the aaperture
 * definition along one metre of the LHC sequence.
 * The aperture of the all sequence can be defined with 
 * a vector of OneMetre objects.
 *
 * The aperture is defined by specifying an arbitrary
 * number of 'Aperture' objects within the OneMetre, at 
 * a given longitudinal position. Only the fractional
 * part of the position ( p-floor(p) ) is taken into 
 * accont. The idea is that the position along the LHC
 * sequence will be given by the index 'i' that number the 
 * various OneMetres in the vector that defines the all
 * sequence (i=0:27000).
 *
 * In order to be able to calculate the aperture in any
 * position along the considered metre, and not only at
 * the positions where the aperture is defined, the
 * member funtion "GetAperture(double p)" can be used
 * It calculate the aperture as interpolation of the
 * point where the aperture as been defined.
 *
 */

#include "Aperture.h"

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

using namespace std;

#ifndef OneMetre_h
#define OneMetre_h 1

class OneMetre {
private:
  //
  vector<double> Pos;       // Position where aperture is defined.
  vector<Aperture> Apert;   // Corresponding apertures.
  vector<double> Pos_ex;    // Extended position and aperture vector with additional
  vector<Aperture> Apert_ex;// definitions at 0.0 and 1.0, for aperture interpolation.
                            // Defined once for all the fist time that 'GetAperture' is called
  //  vector<double> Apert_vec; // Aperture in vector format - useful later
  Aperture Atmp;
  //  vector<int> ind; // Index of positions with defined aperture
  vector<double> Atmp_vec; // Temporary vector for various internal uses

public:
  OneMetre();
  ~OneMetre();
  void DefineAperture(double p, double a1, double a2, double a3, double a4);
  void DefineAperture(double p, Aperture Ap);
  void DefineAperture(double p, vector<double> A4);
  //
  void GetApertDef(vector<double> *Position, vector<Aperture> *ThisApert);
  //
  Aperture GetAperture(double p); // Get aperture at a given position
  //
  void empty();
  void status();
};

#endif
