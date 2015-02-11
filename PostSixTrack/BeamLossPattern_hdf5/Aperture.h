/*
 * Aperture.m (SR, May 2004)
 *
 * Definition of the 'Aperture' object. 
 * This objects contains the definition of 4 numbers that define
 * the aperture according to the MADX "RectEllipse" notation.
 *
 * One can also define the name of an aperture object (possible 
 * useful for later studies, when the aperture of some type 
 * could be displaced according to some models for the magnet 
 * misalignment).
 *
 * Other members of this class are the following:
 *
 *   int IsLost(double x, double y); -> Says if a particle is lost
 *
 *   double ApertVsAngle(double alpha); -> gives the radias aperture
 *                                         at the angle theta
 *
 * ***********
 * * UPDATES *
 * ***********
 *
 * SR, 24 June 2004: Add RECTANGULAR aperture to treat 
 * ================  collimators and other movable elements!
 *                   Skew collimators are not included yet!
 *
 *   Rectangular aperture is denoted with A3=0 ans A4=0;
 * 
 *   Modified member functions: -> IsLost(double, double)
 *                              -> GiveAperture(double)
 *                              -> PlotAperture(string)
 *                 (Update also the others AS SOON AS POSSIBLE)
 *
 *
 * SR, 25 June 2004: Add ANGLE as aperture property.
 * ================  For rectangular apertures, it is assumed that 
 *                   A4 is the angle!
 *
 *
 * Remark: For later studies, it will be potentially useful to add
 *         an 'Alignment' property of the aperture, which says
 *         the closed-orbit position as calculated with 'Survey'.
 *
 *
 * SR, 07 September 2004: Add checks to eliminate the unknown aperture types 
 * =====================  created in the fitting procedure. This is done 
 *                        by adding some checks before running the 'IsLost'
 *                        function.
 *
 *
 * SR, 18 February 2005: The 'GiveAperture' function takes now into account 
 * ====================  the TILT angle. The alignment error is not taken into
 *                       account. Still have to decide how to treat the alignment...
 *
 */

#include <string>
#include <sstream>
#include <iostream>
#include <fstream>
#include <vector>

#include <iomanip>
//#include <algorithm>

#include <stdio.h>
#include <stdlib.h> 
#include <string.h> 
#include <ctype.h>
#include <math.h>

#ifndef Aperture_h
#define Aperture_h 1

using namespace std;

class Aperture {
private:
  vector<double> MyApert;
  string MyName;
  double Dx_align, Dy_align;
  double Angle;

  int LostFlag;
  double x_n, y_n;

  int CorrectDefinition;

public:
  Aperture();
  ~Aperture();
  //
  void PutApert(double a1, double a2, double a3, double a4);
  void PutApert(vector<double> ThisAp);
  double GetApert(int n);
  vector<double> GetApert();
  //
  void GiveName(string in);
  string GetName();
  //
  int IsLost(double x, double y);
  //
  double GiveAperture(double q);    // Give aperture at a given angle theta
  void PlotAperture(string output); // Plot the aperture profile
  //
  void SetApertAlign(double dx, double dy);
  double GetApertAlignX();
  double GetApertAlignY();
  //
  void SetAngle(double ang);
  double GetAngle();
  //
  void empty();
};

#endif
