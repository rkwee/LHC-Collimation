/*
 * SR, 18-11-2004
 * 1) Fix Constructor and distructor (hope it's okay...)
 * 2) Include in the Survey class the possibility of loading
 *    closed-orbits. This is done by following the same 
 *    philosophy as for the other class members: A function
 *    to load the orbit files and two functions to get the
 *    x and y positions are added (again, it is assumed that
 *    the inputs devine the orbit avery 10 cm, as generate
 *    in Matlab with interpolations).
 * 3) The "Clear" function is created to clean-up the memory 
 *    (this as to be used in the main when, for a given halo,
 *    the loss pattern are generated for different orbits!)
 *
 * SR, 03-06-2004
 *
 * Simple object that read and stores the Xsurvey obtained 
 * from MADX with a 'straight. LHC.
 *
 * This class should be used to read the spline interpolation
 * of the MADX output, as generated with Matlab. This allows
 * knowing the survey position every 10 cm.
 * In principle, higher spatial resolution should be used. This
 * would nevertheless require large input files!
 *
 * See 'main_testSurvey.cpp" for an example.
 */

#include "Survey.h"

Survey::Survey()
{
  // Nothing to be done for the initializetion ...
}

Survey::~Survey()
{
  S.clear(); 
  Xsurvey.clear();
  Xcrossing.clear(); 
  Ycrossing.clear();
  XPcrossing.clear(); 
  YPcrossing.clear();
  COx.clear(); 
  COy.clear(); 
}

void Survey::LoadLHC(string in)
{
  S.clear();
  Xsurvey.clear();

  double s, p;

  ifstream input;
  input.open(in.c_str(), ios::in);

  if (!input){
    cout<<"Impossible to open the file "<<in<<" !!"<<endl;
    exit(0);
  }

  while (1){
    input>>s>>p;
    if (!input.good())
      break;
    S.push_back(s);
    Xsurvey.push_back(p);
    //    cout<<i<<") "<<s<<" "<<p<<endl;
    //    i++;
  }
  input.close();

  //  cout<<S.size()<<"/"<<Xsurvey.size()<<" survey positions read from file:"<<endl;
  //  cout<<in<<endl;
  //
  // Test
  //  for (int i = 0; i < S.size(); i++)
  //    cout<<setw(20)<<S[i]<<setw(20)<<Xsurvey[i]<<endl;
  //  for (int i = 0; i < 10; i++)
  //    cout<<setw(20)<<S[S.size()-1-i]<<setw(20)<<Xsurvey[Xsurvey.size()-1-i]<<endl;
}

double Survey::GetSurvey(double pos)
{
  if ( S.size() < 1 ) {
    cout<<"Error: LHC survey has not been initialized"<<endl;
    exit(0);
  }
  // I assume that pos is give in metre, with spacing of 10 cm!
  int n = (int)(pos*10);
  return Xsurvey[n];
}

void Survey::LoadLHC_Crossing(string in)
{
  S.clear();
  Xsurvey.clear();
  Xcrossing.clear();
  Ycrossing.clear();

  double s, Xx, Yx, Xs;
  char chr_tmp[256];

  ifstream input;
  input.open(in.c_str(), ios::in);

  if (!input){
    cout<<"Impossible to open the file "<<in<<" !!"<<endl;
    exit(0);
  }

  input.getline(chr_tmp,256); // Skip first line with header

  while (1){
    input>>s>>Xx>>Yx>>Xs;
    if (!input.good())
      break;
    S.push_back(s);
    Xsurvey.push_back(Xs);
    Xcrossing.push_back(Xx);
    Ycrossing.push_back(Yx);
  }
  input.close();
  //  cout<<S.size()<<"/"<<Xsurvey.size()<<" survey positions read from file:"<<endl;
  //  cout<<in<<endl;
}

void Survey::LoadLHC_Crossing_XP(string in)
{
  S.clear();
  Xsurvey.clear();
  Xcrossing.clear();
  Ycrossing.clear();
  XPcrossing.clear();
  YPcrossing.clear();

  double s, Xx, Yx, Xs, XPx, YPx;
  char chr_tmp[256];

  ifstream input;
  input.open(in.c_str(), ios::in);

  if (!input){
    cout<<"Impossible to open the file "<<in<<" !!"<<endl;
    exit(0);
  }

  input.getline(chr_tmp,256); // Skip first line with header

  while (1){
    input>>s>>Xx>>Yx>>Xs>>XPx>>YPx;
    if (!input.good())
      break;
    S.push_back(s);
    Xsurvey.push_back(Xs);
    Xcrossing.push_back(Xx);
    Ycrossing.push_back(Yx);
    XPcrossing.push_back(XPx);
    YPcrossing.push_back(YPx);
  }
  input.close();
  //  cout<<S.size()<<"/"<<Xsurvey.size()<<" survey positions read from file:"<<endl;
  //  cout<<in<<endl;
}

double Survey::GetCrossX(double pos)
{
  if ( Xcrossing.size() < 1 ) {
    cout<<"Error: LHC positions due to crossing schemes have not been initialized"<<endl;
    exit(0);
  }
  // I assume that pos is given in metre, with spacing of 10 cm!
  int n = (int)(pos*10);
  return Xcrossing[n];
}


double Survey::GetCrossY(double pos)
{
  if ( Ycrossing.size() < 1 ) {
    cout<<"Error: LHC positions due to crossing schemes have not been initialized"<<endl;
    exit(0);
  }
  // I assume that pos is given in metre, with spacing of 10 cm!
  int n = (int)(pos*10);
  return Ycrossing[n];
}

double Survey::GetCrossXP(double pos)
{
  if ( XPcrossing.size() < 1 ) {
    cout<<"Error: LHC positions due to crossing schemes have not been initialized"<<endl;
    exit(0);
  }
  // I assume that pos is given in metre, with spacing of 10 cm!
  int n = (int)(pos*10);
  return XPcrossing[n];
}


double Survey::GetCrossYP(double pos)
{
  if ( YPcrossing.size() < 1 ) {
    cout<<"Error: LHC positions due to crossing schemes have not been initialized"<<endl;
    exit(0);
  }
  // I assume that pos is given in metre, with spacing of 10 cm!
  int n = (int)(pos*10);
  return YPcrossing[n];
}

void Survey::LoadCO(string in)
{
  S.clear();
  COx.clear();
  COy.clear();

  double s, cox, coy;
  char chr_tmp[256];

  ifstream input;
  input.open(in.c_str(), ios::in);

  if (!input){
    cout<<"Impossible to open the file "<<in<<" !!"<<endl;
    exit(0);
  }

  input.getline(chr_tmp,256); // Skip first line with header

  while (1){
    input>>s>>cox>>coy;
    if (!input.good())
      break;
    S.push_back(s);
    COx.push_back(cox);
    COy.push_back(coy);
  }
  input.close();

  //  cout<<"Closed orbit loaded from \""<<in<<"\"!"<<endl;
}

double Survey::GetCOx(double pos)
{
  if ( COx.size() < 1 ) {
    cout<<"Error: The closed orbit has not been initialized!"<<endl;
    exit(0);
  }
  // I assume that pos is given in metre, with spacing of 10 cm!
  int n = (int)(pos*10);
  return COx[n];
}

double Survey::GetCOy(double pos)
{
  if ( COy.size() < 1 ) {
    cout<<"Error: The closed orbit has not been initialized!"<<endl;
    exit(0);
  }
  // I assume that pos is given in metre, with spacing of 10 cm!
  int n = (int)(pos*10);
  return COy[n];
}

void Survey::Clear()
{
  // This is probably not required because each vector is 
  // cleaned up before loading the sequence...
  S.clear(); 
  Xsurvey.clear();
  Xcrossing.clear(); 
  Ycrossing.clear();
  XPcrossing.clear(); 
  YPcrossing.clear();
  COx.clear(); 
  COy.clear(); 
}



