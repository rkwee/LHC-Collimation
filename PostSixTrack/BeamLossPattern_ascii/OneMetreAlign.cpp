#include "OneMetreAlign.h"

OneMetreAlign::OneMetreAlign()
{ 
}

OneMetreAlign::~OneMetreAlign()
{
}

void OneMetreAlign::DefineApertureAlign(double p, double a1, double a2, double a3, double a4, double Dx, double Dy)
{
  if ( p == 1.0 )
    p = 0.99999;
  if ( Pos.size() > 0 && (p-floor(p)) < Pos[ Pos.size()-1 ] - 0.000001 ){
    cout<<"ERROR: New position is smaller than previously defined aperture locations!"<<endl;
    cout<<"       New position must be larger than the last one previously defined."<<endl;
    cout<<"       Old position: "<<Pos[ Pos.size()-1 ]<<" - new position: "<<p<<" -> "<<p-floor(p)<<endl;
    exit(0);
  }
  Pos.push_back( p-floor(p) );
  //
  Atmp.empty();
  Atmp.PutApert(a1, a2, a3, a4);
  Apert.push_back(Atmp);
  Atmp.empty();
  // 
  DxAlign.push_back( Dx );
  DyAlign.push_back( Dy );
}

void OneMetreAlign::DefineApertureAlign(double p, Aperture Ap, double Dx, double Dy)
{
  if ( p == 1.0 )
    p = 0.99999;

  if ( Pos.size() > 0 && (p-floor(p)) < Pos[ Pos.size()-1 ]  - 0.000001 ){
    cout<<"ERROR: New position is smaller than previously defined aperture locations!"<<endl;
    cout<<"       New position must be larger than the last one previously defined."<<endl;
    cout<<"       Old position: "<<Pos[ Pos.size()-1 ]<<" - new position: "<<p<<" -> "<<p-floor(p)<<endl;
    exit(0);
  }
  Pos.push_back( p-floor(p) );
  Apert.push_back(Ap);
  DxAlign.push_back( Dx );
  DyAlign.push_back( Dy );
}

void OneMetreAlign::DefineApertureAlign(double p, vector<double> A4, double Dx, double Dy)
{
  if ( p == 1.0 )
    p = 0.99999;
  if ( Pos.size() > 0 && (p-floor(p)) < Pos[ Pos.size()-1 ]  - 0.000001 ){
    cout<<"ERROR: New position is smaller than previously defined aperture locations!"<<endl;
    cout<<"       New position must be larger than the last one previously defined."<<endl;
    cout<<"       Old position: "<<Pos[ Pos.size()-1 ]<<" - new position: "<<p<<" -> "<<p-floor(p)<<endl;
    exit(0);
  }
  Pos.push_back( p-floor(p) );
  //
  Atmp.empty();
  Atmp.PutApert(A4);
  Apert.push_back(Atmp);
  Atmp.empty();
  //
  DxAlign.push_back( Dx );
  DyAlign.push_back( Dy );
}

void OneMetreAlign::DefineAperture(double p, double a1, double a2, double a3, double a4)
{
  if ( p == 1.0 )
    p = 0.99999;
  if ( Pos.size() > 0 && (p-floor(p)) < Pos[ Pos.size()-1 ] - 0.000001 ){
    cout<<"ERROR: New position is smaller than previously defined aperture locations!"<<endl;
    cout<<"       New position must be larger than the last one previously defined."<<endl;
    cout<<"       Old position: "<<Pos[ Pos.size()-1 ]<<" - new position: "<<p<<" -> "<<p-floor(p)<<endl;
    exit(0);
  }
  Pos.push_back( p-floor(p) );
  //
  Atmp.empty();
  Atmp.PutApert(a1, a2, a3, a4);
  Apert.push_back(Atmp);
  Atmp.empty();
  // 
  DxAlign.push_back(0.0); // Add zero if align is not defined
  DyAlign.push_back(0.0);
}

void OneMetreAlign::DefineAperture(double p, Aperture Ap)
{
  if ( p == 1.0 )
    p = 0.99999;

  if ( Pos.size() > 0 && (p-floor(p)) < Pos[ Pos.size()-1 ]  - 0.000001 ){
    cout<<"ERROR: New position is smaller than previously defined aperture locations!"<<endl;
    cout<<"       New position must be larger than the last one previously defined."<<endl;
    cout<<"       Old position: "<<Pos[ Pos.size()-1 ]<<" - new position: "<<p<<" -> "<<p-floor(p)<<endl;
    exit(0);
  }
  Pos.push_back( p-floor(p) );
  Apert.push_back(Ap);
  DxAlign.push_back(0.0);
  DyAlign.push_back(0.0);
}

void OneMetreAlign::DefineAperture(double p, vector<double> A4)
{
  if ( p == 1.0 )
    p = 0.99999;
  if ( Pos.size() > 0 && (p-floor(p)) < Pos[ Pos.size()-1 ]  - 0.000001 ){
    cout<<"ERROR: New position is smaller than previously defined aperture locations!"<<endl;
    cout<<"       New position must be larger than the last one previously defined."<<endl;
    cout<<"       Old position: "<<Pos[ Pos.size()-1 ]<<" - new position: "<<p<<" -> "<<p-floor(p)<<endl;
    exit(0);
  }
  Pos.push_back( p-floor(p) );
  //
  Atmp.empty();
  Atmp.PutApert(A4);
  Apert.push_back(Atmp);
  Atmp.empty();
  //
  DxAlign.push_back(0.0);
  DyAlign.push_back(0.0);
}

Aperture OneMetreAlign::GetAperture(double p)
{
  int done = 0,
    do_special = 0,
    k = 0;

  double Dx_tmp, Dy_tmp;

  if ( p > 1.0 )
    p = p - floor(p);

  // Preliminary checks:
  if ( (int)Pos.size() == 0){
    cout<<"ERROR: The aperture has not been initialized properly:"<<endl;
    cout<<"       No aperture has been defined in this OneMetreAlign"<<endl;
    exit(0);
  }
  else if ( (int)Pos.size() == 1 ){ // one aperture only -> same aperture in all the metre!
    Atmp = Apert[0];
    Atmp.SetApertAlign(DxAlign[0], DyAlign[0]);
    done = 1;
  }

  if ( !done ){
    if ( Pos_ex.size() == 0 ){ // Only if it has not been defined yet!
      // Add 'flat' aperture definitions if the point at '0.0' and '0.99' are not given
      // Only if this has not been done yet (i.e., only if Pos_ex.size()==0 )
      if ( Pos.size() > 0 && Pos[0] > 0.001 ){
	cout<<"Warning: aperture definition added at the beginning of the metre!"<<endl;
	Pos_ex.push_back(0.0);
	Apert_ex.push_back(Apert[0]);
	DxAlign_ex.push_back(DxAlign[0]);
	DyAlign_ex.push_back(DyAlign[0]);
	for (int q = 0; q < Pos.size(); q++){
	  Pos_ex.push_back( Pos[q] );
	  Apert_ex.push_back( Apert[q] );
	  DxAlign_ex.push_back(DxAlign[q]);
	  DyAlign_ex.push_back(DyAlign[q]);
	}
      } else {
	Pos_ex = Pos;
	Apert_ex = Apert;
	DxAlign_ex = DxAlign;
	DyAlign_ex = DyAlign;
      }
      if ( Pos.size() > 0 && Pos[ Pos.size()-1 ] < 0.99 ){
	cout<<"Warning: aperture definition added at the end of the metre!"<<endl;
	Pos_ex.push_back( 0.999999999 );
	Apert_ex.push_back( Apert[Apert.size()-1] );
	DxAlign_ex.push_back( DxAlign[DxAlign.size()-1] );
	DyAlign_ex.push_back( DyAlign[DyAlign.size()-1] );
      }
    }
    // Clean-up!
    Atmp.empty();
    Atmp_vec.clear();
    //
    if ( p == 0.0 ){
      Atmp = Apert_ex[0];
      Atmp.SetApertAlign(DxAlign[0], DyAlign[0]);
    }
    else if ( p == 1.0 ){
      Atmp = Apert_ex[Apert_ex.size()-1];
      Atmp.SetApertAlign(DxAlign[DxAlign.size()-1], DyAlign[DyAlign.size()-1]);
    }
    else if ( (int)Pos_ex.size() >= 2 ){
      // Find the 'bin' of the position 'p'
      k = 0;
      while ( Pos_ex[k] <= p && k < Pos_ex.size() ) 
	k++;
      // Different apertures at the same location: jump to the next interval
      if (Pos_ex[k] == Pos_ex[k-1] && k < Pos_ex.size()-2 )
	k++;
      // Assign the aperture as a linar interpolation
      Atmp_vec.clear();
      for (int i = 1; i <= 4; i++) // Here, I would have [k=Pos_ex.size() => 'Bus error'] if p=1!!
	Atmp_vec.push_back( Apert_ex[k-1].GetApert(i) + 
			    (Apert_ex[k].GetApert(i)-Apert_ex[k-1].GetApert(i))/(Pos_ex[k]-Pos_ex[k-1])
			    * ((p-floor(p))-Pos_ex[k-1]) );
      // This includes the case that p=Pos_ex[i] for some i
      //
      Dx_tmp = DxAlign_ex[k-1] + (DxAlign_ex[k]-DxAlign_ex[k-1])/(Pos_ex[k]-Pos_ex[k-1]) 
	* ((p-floor(p))-Pos_ex[k-1]);
      Dy_tmp = DyAlign_ex[k-1] + (DyAlign_ex[k]-DyAlign_ex[k-1])/(Pos_ex[k]-Pos_ex[k-1]) 
	* ((p-floor(p))-Pos_ex[k-1]);
      Atmp.PutApert( Atmp_vec );
      Atmp.SetApertAlign(Dx_tmp, Dy_tmp);
      Atmp_vec.clear();
    }
  }
  // Special case - required position correspond to a defined position where
  // two apertures are given (transition between elements
  // => I take the smallest of the 4 rectellipse numbers
  for (int i = 0; i < Pos_ex.size()-1; i++){
    if ( Pos_ex[i] == Pos_ex[i+1] && Pos_ex[i+1] == p){
      k = i;
      do_special = 1;
    }
  }
  if ( do_special ){
    cout<<"Special case: aperture definitions at "<<Pos_ex[k]
	<<" and "<<Pos_ex[k+1]<<" are identical!"<<endl;
    Atmp_vec.clear();
    for (int i = 1; i <= 4; i++){
      if ( Apert_ex[k].GetApert(i) > Apert_ex[k+1].GetApert(i))
	Atmp_vec.push_back(Apert_ex[k+1].GetApert(i));
      else 
	Atmp_vec.push_back(Apert_ex[k].GetApert(i));
    }
    Atmp.PutApert( Atmp_vec );
    Atmp.SetApertAlign(DxAlign[k], DyAlign[k]);
  } 
  return Atmp;
}

double OneMetreAlign::GetAlignX( double p )
{
  int done = 0,
    do_special = 0,
    k = 0;

  if ( p > 1.0 )
    p = p - floor(p);

  // Preliminary checks:
  if ( (int)Pos.size() == 0){
    cout<<"ERROR: The aperture has not been initialized properly:"<<endl;
    cout<<"       No aperture has been defined in this OneMetreAlign"<<endl;
    exit(0);
  }
  else if ( (int)Pos.size() == 1 ){ // one aperture only -> same aperture in all the metre!
    DxA = DxAlign[0];
    done = 1;
  }
  
  if ( !done ){
    if ( Pos_ex.size() == 0 ){ // Only if it has not been defined yet!
      // Add 'flat' aperture definitions if the point at '0.0' and '0.99' are not given
      // Only if this has not been done yet (i.e., only if Pos_ex.size()==0 )
      if ( Pos.size() > 0 && Pos[0] > 0.001 ){
	cout<<"Warning: aperture definition added at the beginning of the metre!"<<endl;
	Pos_ex.push_back(0.0);
	Apert_ex.push_back(Apert[0]);
	DxAlign_ex.push_back(DxAlign[0]);
	DyAlign_ex.push_back(DyAlign[0]);
	for (int q = 0; q < Pos.size(); q++){
	  Pos_ex.push_back( Pos[q] );
	  Apert_ex.push_back( Apert[q] );
	  DxAlign_ex.push_back(DxAlign[q]);
	  DyAlign_ex.push_back(DyAlign[q]);
	}
      } else {
	Pos_ex = Pos;
	Apert_ex = Apert;
	DxAlign_ex = DxAlign;
	DyAlign_ex = DyAlign;
      }
      if ( Pos.size() > 0 && Pos[ Pos.size()-1 ] < 0.99 ){
	cout<<"Warning: aperture definition added at the end of the metre!"<<endl;
	Pos_ex.push_back( 0.999999999 );
	Apert_ex.push_back( Apert[Apert.size()-1] );
	DxAlign_ex.push_back( DxAlign[DxAlign.size()-1] );
	DyAlign_ex.push_back( DyAlign[DyAlign.size()-1] );
      }
    }
    //
    if ( p == 0.0 )
      DxA = DxAlign_ex[0];
    else if ( p == 1.0 )
      DxA = DxAlign_ex[DxAlign_ex.size()-1];
    else if ( (int)Pos_ex.size() >= 2 ){
      // Find the 'bin' of the position 'p'
      k = 0;
      while ( Pos_ex[k] <= p && k < Pos_ex.size() ) 
	k++;
      // Different apertures at the same location: jump to the next interval
      if (Pos_ex[k] == Pos_ex[k-1] && k < Pos_ex.size()-2 )
	k++;
      DxA = DxAlign_ex[k-1] + (DxAlign_ex[k]-DxAlign_ex[k-1])/(Pos_ex[k]-Pos_ex[k-1]) 
	* ((p-floor(p))-Pos_ex[k-1]);
    }
  }
  // Special case - required position correspond to a defined position where
  // two apertures are given (transition between elements
  // => I take the smallest of the 4 rectellipse numbers
  for (int i = 0; i < Pos_ex.size()-1; i++){
    if ( Pos_ex[i] == Pos_ex[i+1] && Pos_ex[i+1] == p){
      k = i;
      do_special = 1;
    }
  }
  if ( do_special ){
    cout<<"Special case: aperture definitions at "<<Pos_ex[k]
	<<" and "<<Pos_ex[k+1]<<" are identical!"<<endl;
    DxA = DxAlign_ex[k]; // ??
  } 
  return DxA;
}

double OneMetreAlign::GetAlignY( double p )
{
  int done = 0,
    do_special = 0,
    k = 0;

  if ( p > 1.0 )
    p = p - floor(p);

  // Preliminary checks:
  if ( (int)Pos.size() == 0){
    cout<<"ERROR: The aperture has not been initialized properly:"<<endl;
    cout<<"       No aperture has been defined in this OneMetreAlign"<<endl;
    exit(0);
  }
  else if ( (int)Pos.size() == 1 ){ // one aperture only -> same aperture in all the metre!
    DyA = DyAlign[0];
    done = 1;
  }
  
  if ( !done ){
    if ( Pos_ex.size() == 0 ){ // Only if it has not been defined yet!
      // Add 'flat' aperture definitions if the point at '0.0' and '0.99' are not given
      // Only if this has not been done yet (i.e., only if Pos_ex.size()==0 )
      if ( Pos.size() > 0 && Pos[0] > 0.001 ){
	cout<<"Warning: aperture definition added at the beginning of the metre!"<<endl;
	Pos_ex.push_back(0.0);
	Apert_ex.push_back(Apert[0]);
	DxAlign_ex.push_back(DxAlign[0]);
	DyAlign_ex.push_back(DyAlign[0]);
	for (int q = 0; q < Pos.size(); q++){
	  Pos_ex.push_back( Pos[q] );
	  Apert_ex.push_back( Apert[q] );
	  DxAlign_ex.push_back(DxAlign[q]);
	  DyAlign_ex.push_back(DyAlign[q]);
	}
      } else {
	Pos_ex = Pos;
	Apert_ex = Apert;
	DxAlign_ex = DxAlign;
	DyAlign_ex = DyAlign;
      }
      if ( Pos.size() > 0 && Pos[ Pos.size()-1 ] < 0.99 ){
	cout<<"Warning: aperture definition added at the end of the metre!"<<endl;
	Pos_ex.push_back( 0.999999999 );
	Apert_ex.push_back( Apert[Apert.size()-1] );
	DxAlign_ex.push_back( DxAlign[DxAlign.size()-1] );
	DyAlign_ex.push_back( DyAlign[DyAlign.size()-1] );
      }
    }
    //
    if ( p == 0.0 )
      DyA = DyAlign_ex[0];
    else if ( p == 1.0 )
      DyA = DyAlign_ex[DyAlign_ex.size()-1];
    else if ( (int)Pos_ex.size() >= 2 ){
      // Find the 'bin' of the position 'p'
      k = 0;
      while ( Pos_ex[k] <= p && k < Pos_ex.size() ) 
	k++;
      // Different apertures at the same location: jump to the next interval
      if (Pos_ex[k] == Pos_ex[k-1] && k < Pos_ex.size()-2 )
	k++;
      DyA = DyAlign_ex[k-1] + (DyAlign_ex[k]-DyAlign_ex[k-1])/(Pos_ex[k]-Pos_ex[k-1]) 
	* ((p-floor(p))-Pos_ex[k-1]);
    }
  }
  // Special case - required position correspond to a defined position where
  // two apertures are given (transition between elements
  // => I take the smallest of the 4 rectellipse numbers
  for (int i = 0; i < Pos_ex.size()-1; i++){
    if ( Pos_ex[i] == Pos_ex[i+1] && Pos_ex[i+1] == p){
      k = i;
      do_special = 1;
    }
  }
  if ( do_special ){
    cout<<"Special case: aperture definitions at "<<Pos_ex[k]
	<<" and "<<Pos_ex[k+1]<<" are identical!"<<endl;
    DyA = DyAlign_ex[k]; // ??
  } 
  return DyA;
}

void OneMetreAlign::GetApertDef(vector<double> *Position, vector<Aperture> *ThisApert)
{
  Position->clear();
  ThisApert->clear();
  for (int i = 0; i < (int) Pos.size(); i++){
    Position -> push_back( Pos[i] );
    ThisApert -> push_back( Apert[i] );
  }
  /*
  // Example of usage :
  OneMetreAlign Test;
  Test.DefineAperture(0.0, 1, 1, 1, 1);
  Test.DefineAperture(0.1, 2, 2, 2, 2);
  Test.DefineAperture(0.2, 3, 3, 3, 3);
  Test.DefineAperture(0.3, 4, 4, 4, 4);
  Test.DefineAperture(0.99999, .4, .4, .4, .4);
  Test.status();

  vector<double> pos;
  vector<Aperture> pippo;

  Test.GetApertDef(&pos, &pippo);
  for( int i = 0; i < (int) pos.size(); i++){
    cout<<pos[i]<<" "
	<<pippo[i].GetApert(1)<<" "
	<<pippo[i].GetApert(2)<<" "
	<<pippo[i].GetApert(3)<<" "
	<<pippo[i].GetApert(4)<<endl;
  }
  */
}

void OneMetreAlign::status(){
  cout<<endl;
  cout<<"**** Present aperture definitions ****"<<endl;
  cout<<"Number of aperture definitions = "<<Pos.size()<<endl;
  cout.precision(4);
  for (int i = 0; i < Pos.size(); i++)
    cout<<setw(10)<<Pos[i]
	<<setw(10)<<Apert[i].GetApert(1)
	<<setw(10)<<Apert[i].GetApert(2)
	<<setw(10)<<Apert[i].GetApert(3)
	<<setw(10)<<Apert[i].GetApert(4)<<endl;
  cout<<endl;

  cout<<"**** Present definitions of aperture misalignments ****"<<endl;
  cout<<"Number of aperture definitions = "<<Pos.size()<<endl;
  cout.precision(4);
  for (int i = 0; i < Pos.size(); i++)
    cout<<setw(10)<<Pos[i]
	<<setw(4)<<"Dx"<<setw(10)<<DxAlign[i]
	<<setw(6)<<"Dy"<<setw(10)<<DyAlign[i]<<endl;
  cout<<endl;

  if ( Pos_ex.size() > 0 ){
    cout<<endl;
    cout<<"**** Aperture definitions of Extended aperture vector ****"<<endl;
    cout<<"Number of aperture definitions = "<<Pos_ex.size()<<endl;
    cout.precision(4);
    for (int i = 0; i < Pos_ex.size(); i++)
      cout<<setw(10)<<Pos_ex[i]
	  <<setw(10)<<Apert_ex[i].GetApert(1)
	  <<setw(10)<<Apert_ex[i].GetApert(2)
	  <<setw(10)<<Apert_ex[i].GetApert(3)
	  <<setw(10)<<Apert_ex[i].GetApert(4)<<endl;
    cout<<endl;
  }
}

void OneMetreAlign::empty(){
  Pos.clear();
  Apert.clear();
  Pos_ex.clear();
  Apert_ex.clear();
  DxAlign.clear();
  DyAlign.clear();
  DxAlign_ex.clear();
  DyAlign_ex.clear();
  Atmp.empty();
  Atmp_vec.clear();
}
