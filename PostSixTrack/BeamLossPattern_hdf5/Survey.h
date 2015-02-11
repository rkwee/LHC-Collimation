/*
 * fix creator and distructor!
 *
 *
 *
 *
 *
 *
 *
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

#ifndef Survey_h
#define Survey_h 1

using namespace std;

class Survey {
 private:
  vector<double> S, Xsurvey;
  vector<double> Xcrossing, Ycrossing;
  vector<double> XPcrossing, YPcrossing;
  vector<double> COx, COy;

  public: 
  Survey();
  ~Survey();
  //
  void LoadLHC(string in);
  void LoadLHC_Crossing(string in);
  void LoadLHC_Crossing_XP(string in);
  double GetSurvey(double pos);
  double GetCrossX(double pos);
  double GetCrossY(double pos);
  double GetCrossXP(double pos);
  double GetCrossYP(double pos);
  void Clear();
  //
  void LoadCO(string in);
  double GetCOx(double pos);
  double GetCOy(double pos);
};

#endif
