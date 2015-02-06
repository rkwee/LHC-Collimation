#include "Aperture.h"

Aperture::Aperture()
{
  Dx_align = 0;
  Dy_align = 0;
  Angle = 0;
}

Aperture::~Aperture()
{
  //
}

void Aperture::PutApert(double a1, double a2, double a3, double a4)
{
  double pi = (double)atan2(0.0,-1.0);

  MyApert.clear();
  if ( // a3 ==0 || a4 == 0 || // This case now defines the rectangular aperture!
       (a1 != 0 && a2 == 0) ||
       (a1 == 0 && a2 != 0) ){
    cout<<"ERROR: Invalid aperture definition!!"<<endl;
    cout<<a1<<" "
	<<a2<<" "
	<<a3<<" "
	<<a4<<" "<<endl;
  }
  else {
    MyApert.clear();
    MyApert.push_back(a1);
    MyApert.push_back(a2);
    MyApert.push_back(a3);
    MyApert.push_back(a4);
  }
  // For rectangular aperture, A3=0 and A4=angle!
  if ( a3 == 0 )
    Angle = a4 * pi / 180;
}

void Aperture::PutApert(vector<double> ThisAp)
{
  double pi = (double)atan2(0.0,-1.0);

  MyApert.clear();
  MyApert = ThisAp;
  // For rectangular aperture, A3=0 and A4=angle!
  if ( ThisAp[2] == 0 )
    Angle = ThisAp[3] * pi / 180;
}

double Aperture::GetApert(int n)
{
  return MyApert[n-1];
}

void Aperture::GiveName(string in)
{
  MyName = in;
}

string Aperture::GetName()
{
  return MyName;
}

int Aperture::IsLost(double x, double y)
{
  // New coordinates w.r.t. the aperture centre!
  // First traslation, then the rotation!
  //
  // Check what happens for interpolated aperture, when the 
  // resulting aperture does not correspond to one of the known types.
  // 
  // SR, 07-09-2004
  // In order to avoid the problems with the 'strange' apertures from 
  // the fitting procedure, I add some checks to make the aperture
  // definition compatible with 'known' aperture plots!

  double a1 = MyApert[0], 
    a2 = MyApert[1], 
    a3 = MyApert[2],
    a4 = MyApert[3],

  CorrectDefinition = 0;
  if ( a1 > a3 && a3 != 0 ){
    a1 = a3;
    CorrectDefinition = 1;
  }
  if ( a2 > a4 && a4 > 0){
    a2 = a4;
    CorrectDefinition = 1;
  }
  if ( a1 != 0. && a2 != 0. && a3 != 0. && a1 < a3 && a2 < a4 ){ // Exclude RaceTrack and Coll!
    a3 = a1;
    a4 = a2;
    CorrectDefinition = 1;
  }
  if ( a4 < 0 || a4 > .5 ){ // Collimator with negative angle or angle > .5 (no apertures > 1!)
    a3 = 0;      // -> This will be recognized as a square, tilted aperture!
    CorrectDefinition = 1;
  }
  /*
  // Warning if aperture definition is changed.
  if ( CorrectDefinition ){
    cout<<setw(22)<<"Aperture definition:";
    cout<<setw(10)<<MyApert[0]<<setw(10)<<a2
	<<setw(10)<<MyApert[2]<<setw(10)<<MyApert[3]<<endl;
    cout<<setw(22)<<"corrected to:";
    cout<<setw(10)<<a1<<setw(10)<<a2
	<<setw(10)<<a3<<setw(10)<<a4<<endl;
  }
  */

  // 
  x_n = x - Dx_align;
  y_n = y - Dy_align;
  //
  double theta = atan2(y_n, x_n);
  double R = sqrt( x_n * x_n + y_n * y_n );
  x_n = R * cos( Angle - theta );
  y_n = R * sin( Angle - theta );
  //
  LostFlag = 0;
  if ( a1 != 0.0 && a3 > 0 ){// RectEllipse
    if ( x_n*x_n/a3/a3 + y_n*y_n/a4/a4 >= 1 ||
	 fabs(x_n) >= a1 ||
	 fabs(y_n) >= a2)
      LostFlag = 1;
  }
  else if (a1 == 0.0) { // RaceTrack: remember to use Ap[2]/2!!
    if ( fabs(x_n) <= a3 / 2 ){
      if (fabs(y_n) >= a4 )
	LostFlag = 1;
    }
    else if ( fabs(x_n) > a3/2 ){
      if ( (fabs(x_n)-a3/2)*(fabs(x_n)-a3/2)+y_n*y_n >= a4*a4)
	LostFlag = 1;
    }
  }
  else if ( a1 != 0.0 && a3 == 0 ){
    if ( fabs(x_n) >= a1 || fabs(y_n) >= a2 )
      LostFlag = 1;
  }
  return LostFlag;
}

double Aperture::GiveAperture(double q)
{
  // WARNING: If this memebr is modified, also PlotAperture 
  //          should be change accordingly!!!

  double pi = (double)atan2(0.0,-1.0);
  double T, Tc;
  double Dx_tmp, Dy_tmp, DT_tmp;

  double a1 = MyApert[0], 
    a2 = MyApert[1], 
    a3 = MyApert[2],
    a4 = MyApert[3],
    a3r = a3 / 2;   // ForRaceTrack

  T = q * pi / 180;         // Angle in radiants
  if (T > pi || T < -pi){
    cout<<"Please choose and angle between -pi and pi!"<<endl;
    exit(0);
  }

  // Take the angle into accout
  T = T - Angle;

  // Check to avoid unknown combination of RectEllipse apertures.
  // (this will be repeated in IsLost!)
  CorrectDefinition = 0;
  if ( a1 > a3 && a3 != 0 ){
    a1 = a3;
    CorrectDefinition = 1;
  }
  if ( a2 > a4 && a4 > 0){
    a2 = a4;
    CorrectDefinition = 1;
  }
  if ( a1 != 0. && a2 != 0. && a3 != 0. && a1 < a3 && a2 < a4 ){ // Exclude RaceTrack and Coll!
    a3 = a1;
    a4 = a2;
    CorrectDefinition = 1;
  }
  if ( a4 < 0 || a4 > .5 ){ // Collimator with negative angle or angle > .5 (no apertures > 1!)
    a3 = 0;      // -> This will be recognized as a square, tilted aperture!
    CorrectDefinition = 1;
  }
  /*
  if ( CorrectDefinition ){
    cout<<setw(22)<<"Aperture definition:";
    cout<<setw(10)<<MyApert[0]<<setw(10)<<MyApert[1]
	<<setw(10)<<MyApert[2]<<setw(10)<<MyApert[3]<<endl;
    cout<<setw(22)<<"corrected to:";
    cout<<setw(10)<<a1<<setw(10)<<a2
	<<setw(10)<<a3<<setw(10)<<a4<<endl;
  }
  */

  // Always use an angle in the first quadrant and
  // assign the corresponding sign to the displacements
  double sign_x = 1.0,
    sign_y = 1.0;
  if (T > pi/2 || T < -pi/2)
    sign_x = -1.0;
  if (T < 0.0)
    sign_y = -1.0;
  //
  if ( T < -pi/2 )
    T = pi + T;
  else if ( T >= -pi/2 && T < 0 )
    T = -T;
  else if ( T > pi/2 ) 
    T = pi - T;


  // Elliptical aperture
  if ( a1 == a3 && a2 == a4 ){
    Dx_tmp = sign_x * a3 * sqrt(1/(1+a3*a3*tan(T)*tan(T)/a4/a4));
    Dy_tmp = sign_y * fabs(Dx_tmp * tan(T));
  }
  // Cut parallel to x axis
  else if ( a1 == a3 && a2 < a4 ){
    Tc = atan(a2/a3/sqrt(1-a2*a2/a4/a4));
    //    if ( T <= (Tc-pi) || (T >= -Tc && T <= Tc) || T >= pi-Tc ){    // -> Elliptical part
    if ( T <= Tc ){    // -> Elliptical part
      Dx_tmp = sign_x * a3 / sqrt( 1+a3*a3*tan(T)*tan(T)/a4/a4 );
      Dy_tmp = sign_y * fabs(Dx_tmp * tan(T));
    }
    else {                                                         // -> Straight part
      Dy_tmp = sign_y * a2;
      Dx_tmp = sign_x * fabs(Dy_tmp * tan( pi/2-T ));
    }
  }
  // Cut parallel to y axis
  else if ( a1 < a3 && a2 == a4 ){
      Tc = atan( a4*sqrt(1-a1*a1/a3/a3)/a1 );
      //      if ( T <= (Tc-pi) || (T >= -Tc && T <= Tc) || T >= pi-Tc ){ // -> Straight part
      if ( T <= Tc ){ // -> Straight part
	Dx_tmp = sign_x * a1;
	Dy_tmp = sign_y * fabs(Dx_tmp * tan(T));
      }
      else {                                                      // -> Elliptical part
	Dx_tmp = sign_x * a3 / sqrt( 1+a3*a3*tan(T)*tan(T)/a4/a4 );
	Dy_tmp = sign_y * fabs(Dx_tmp * tan(T));
      }
  }
  // RaceTrack
  else if ( a1 == 0 && a2 == 0 ){
    Tc = atan2( a4, a3r );
    if ( T >= Tc ) { // -> Flat part
      Dx_tmp = sign_x * fabs(a4 * tan( pi/2-T ));
      Dy_tmp = sign_y * a4;
    }
    else {           // -> Circular part
      Dx_tmp = sign_x * (a3r+sqrt(a4*a4-a3r*a3r*tan(T)*tan(T)+a4*a4*tan(T)*tan(T))) / (1+tan(T)*tan(T));
      Dy_tmp = sign_y * Dx_tmp * tan(T);
    }
  }
  // Collimator aperture (rectangular + tilt)
  else if ( a3 == 0 ) {
    Tc = atan2(a2, a1);
    //
    if (T <= Tc){
      Dx_tmp = sign_x * a1;
      Dy_tmp = sign_y * a1 * fabs( tan(T) );
    }
    else {
      Dx_tmp = sign_x * a2 * fabs( tan(pi/2-T) );
      Dy_tmp = sign_y * a2;
    }
  }
  else {
    cout<<"WARNING: The given aperture is not classified among the known types"<<endl;
    cout<<"         A1="<<a1<<" A2="<<a2<<" A3="<<a3<<" A4="<<a4<<endl;
    // Temporary solution: I give the smallest value of x
    if (a1 > a3)
      Dx_tmp = a1;
    else
      Dx_tmp = a3;
    if (a2 > a4)
      Dx_tmp = a4;
    else
      Dx_tmp = a2;
  }
  
  DT_tmp = sqrt(Dx_tmp*Dx_tmp+Dy_tmp*Dy_tmp);

  return DT_tmp;
}

void Aperture::PlotAperture(string output)
{
  double pi = (double)atan2(0.0,-1.0);

  double T, Tc, T_n, Dx_tmp, Dy_tmp, DT_tmp, q;
  double a1 = MyApert[0], 
    a2 = MyApert[1], 
    a3 = MyApert[2], 
    a4 = MyApert[3], 
    a3r = a3 / 2;
  double sign_x,sign_y;

  int N = 200; // number of point to plot

  CorrectDefinition = 0;
  if ( a1 > a3 && a3 != 0 ){
    a1 = a3;
    CorrectDefinition = 1;
  }
  if ( a2 > a4 && a4 > 0){
    a2 = a4;
    CorrectDefinition = 1;
  }
  if ( a1 != 0. && a2 != 0. && a3 != 0. && a1 < a3 && a2 < a4 ){ // Exclude RaceTrack and Coll!
    a3 = a1;
    a4 = a2;
    CorrectDefinition = 1;
  }
  if ( a4 < 0 || a4 > .5 ){ // Collimator with negative angle or angle > .5 (no apertures > 1!)
    a3 = 0;      // -> This will be recognized as a square, tilted aperture!
    CorrectDefinition = 1;
  }
  /*
  if ( CorrectDefinition ){
    cout<<setw(22)<<"Aperture definition:";
    cout<<setw(10)<<MyApert[0]<<setw(10)<<a2
	<<setw(10)<<MyApert[2]<<setw(10)<<MyApert[3]<<endl;
    cout<<setw(22)<<"corrected to:";
    cout<<setw(10)<<a1<<setw(10)<<a2
	<<setw(10)<<a3<<setw(10)<<a4<<endl;
  }
  */

  ofstream out;
  out.open(output.c_str());

  for (int i = 0; i < N; i++){
    q = -180+360*(double)i/(double)N;
    T = q * pi / 180;
    T_n = T; // For later use, I need the angle in [-pi:pi]
    //
    sign_x = 1.0;
    sign_y = 1.0;
    if (T > pi/2 || T < -pi/2)
      sign_x = -1.0;
    if (T < 0.0)
      sign_y = -1.0;
    //
    if ( T < -pi/2 )
      T = pi + T;
    else if ( T >= -pi/2 && T < 0 )
      T = -T;
    else if ( T > pi/2 ) 
      T = pi - T;
    // Elliptical aperture
    if ( a1 == a3 && a2 == a4 ){
      Dx_tmp = sign_x * a3 * sqrt(1/(1+a3*a3*tan(T)*tan(T)/a4/a4));
      Dy_tmp = sign_y * fabs(Dx_tmp * tan(T));
    }
    // Cut parallel to x axis
    else if ( a1 == a3 && a2 < a4 ){
      Tc = atan(a2/a3/sqrt(1-a2*a2/a4/a4));
      if ( T <= Tc ){
	Dx_tmp = sign_x * a3 / sqrt( 1+a3*a3*tan(T)*tan(T)/a4/a4 );
	Dy_tmp = sign_y * fabs(Dx_tmp * tan(T));
      }
      else {
	Dy_tmp = sign_y * a2;
	Dx_tmp = sign_x * fabs(Dy_tmp * tan( pi/2-T ));
      }
    }
    // Cut parallel to y axis
    else if ( a1 < a3 && a2 == a4 ){
      Tc = atan( a4*sqrt(1-a1*a1/a3/a3)/a1 );
      if ( T <= Tc ){
	Dx_tmp = sign_x * a1;
	Dy_tmp = sign_y * fabs(Dx_tmp * tan(T));
      }
      else {
	Dx_tmp = sign_x * a3 / sqrt( 1+a3*a3*tan(T)*tan(T)/a4/a4 );
	Dy_tmp = sign_y * fabs(Dx_tmp * tan(T));
      }
    }
    // RaceTrack
    else if ( a1 == 0 && a2 == 0 ){
      Tc = atan2( a4, a3r );
      if ( T >= Tc ) {
	Dx_tmp = sign_x * fabs(a4 * tan( pi/2-T ));
	Dy_tmp = sign_y * a4;
      }
      else {
	Dx_tmp = sign_x * (a3r+sqrt(a4*a4-a3r*a3r*tan(T)*tan(T)+a4*a4*tan(T)*tan(T))) 
	  / (1+tan(T)*tan(T));
	Dy_tmp = sign_y * Dx_tmp * tan(T);
      }
    }
    // Collimator aperture (rectangular + tilt)
    else if ( a3 == 0 ) {
      Tc = atan2(a2, a1);
      if (T <= Tc){
	Dx_tmp = sign_x * a1;
	Dy_tmp = sign_y * a1 * fabs( tan(T) );
      }
      else {
	Dx_tmp = sign_x * a2 * fabs( tan(pi/2-T) );
	Dy_tmp = sign_y * a2;
      }
    }
    else {
      cout<<"WARNING: The given aperture is not classified among the known types"<<endl;
      cout<<"         A1="<<a1<<" A2="<<a2<<" A3="<<a3<<" A4="<<a4<<endl;
    }
    DT_tmp=sqrt(Dx_tmp*Dx_tmp+Dy_tmp*Dy_tmp);
    //

    // Rotate first, and then displace!
    out<<setw(8)<<q;
    //    out<<setw(15)<<T;
    //    out<<setw(15)<<Dx_tmp;
    //    out<<setw(15)<<Dy_tmp;
    //    out<<setw(15)<<Dx_tmp + Dx_align;
    //    out<<setw(15)<<Dy_tmp + Dy_align;
    //    out<<setw(15)<<Dx_tmp * cos( Angle ) + Dx_align;
    //    out<<setw(15)<<Dy_tmp * sin( Angle + pi / 2 )+ Dy_align;
    out<<setw(15)<< DT_tmp * cos( Angle + T_n ) + Dx_align;
    out<<setw(15)<< DT_tmp * sin( Angle + T_n ) + Dy_align;
    out<<setw(15)<<DT_tmp<<endl; // In aperture frame!
  }
  out.close();
}

void Aperture::SetApertAlign(double dx, double dy)
{
  Dx_align = dx;
  Dy_align = dy;
}

double Aperture::GetApertAlignX()
{
  return Dx_align;
}

double Aperture::GetApertAlignY()
{
  return Dy_align;
}

void Aperture::SetAngle(double ang)
{
  double pi = (double)atan2(0.0,-1.0);
  Angle = ang * pi / 180;
}

double Aperture::GetAngle()
{
  return Angle;
}

void Aperture::empty()
{
  MyApert.clear();
  Dx_align = 0;
  Dy_align = 0;
  Angle = 0;  
}
