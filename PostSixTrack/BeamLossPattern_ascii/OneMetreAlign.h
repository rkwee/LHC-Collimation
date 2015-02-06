/*
 * OneMetreAlign.h (SR, June 2004)
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

#ifndef OneMetreAlign_h
#define OneMetreAlign_h 1

class OneMetreAlign {
private:
  vector<double> Pos;       // Position where aperture is defined.
  vector<Aperture> Apert;   // Corresponding apertures.
  vector<double> DxAlign,   // Corresponding alignment statements.
    DyAlign;
  vector<double> Pos_ex;    // Extended position and aperture vector with additional
  vector<Aperture> Apert_ex;// definitions at 0.0 and 1.0, for aperture interpolation.
  vector<double> DxAlign_ex,// Defined once for all the fist time that 'GetAperture' is called
    DyAlign_ex;
                            
  //  vector<double> Apert_vec; // Aperture in vector format - useful later
  Aperture Atmp;
  //  vector<int> ind; // Index of positions with defined aperture
  vector<double> Atmp_vec; // Temporary vector for various internal uses
  double DxA, DyA;

public:
  OneMetreAlign();
  ~OneMetreAlign();
  // If alignment is not defined, put it to zero!
  void DefineAperture(double p, double a1, double a2, double a3, double a4);
  void DefineAperture(double p, Aperture Ap);
  void DefineAperture(double p, vector<double> A4);
  //
  void DefineApertureAlign(double p, double a1, double a2, double a3, double a4, double Dx, double Dy);
  void DefineApertureAlign(double p, Aperture Ap, double Dx, double Dy);
  void DefineApertureAlign(double p, vector<double> A4, double Dx, double Dy);
  //
  void GetApertDef(vector<double> *Position, vector<Aperture> *ThisApert);
  //
  Aperture GetAperture(double p); // Get aperture at a given position
  double GetAlignX(double p);
  double GetAlignY(double p);
  //
  void empty();
  void status();
};

#endif
