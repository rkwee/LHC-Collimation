#include "OneMetre.h"

OneMetre::OneMetre()
{ 
}

OneMetre::~OneMetre()
{
}

void OneMetre::DefineAperture(double p, double a1, double a2, double a3, double a4)
{
  if ( p == 1.0 )
    p = 0.99999;
  // Only add new positions with larger amplitudes than the last aperture defined
  if ( Pos.size() > 0 && (p-floor(p)) < Pos[ Pos.size()-1 ] - 0.000001 ){
    // Note: I added "-0.000001" to avoid some rounding problems when reading MADX table
    cout<<"ERROR: New position is smaller than previously defined aperture locations!"<<endl;
    cout<<"       New position must be larger than the last one previously defined."<<endl;
    cout<<"       Old position: "<<Pos[ Pos.size()-1 ]<<" - new position: "<<p<<" -> "<<p-floor(p)<<endl;
    //    cout.precision(15);
    //    cout<<Pos[ Pos.size()-1 ]<<endl;
    //    cout<<p-floor(p)<<endl;
    exit(0);
  }
  //
  Pos.push_back( p-floor(p) ); // Insert the fractional part of the position
  //
  Atmp.empty();
  Atmp.PutApert(a1, a2, a3, a4);
  Apert.push_back(Atmp);
  Atmp.empty();
  //  cout<<"Aperture definition inserted at the position "<<p<<" -> "<<p-floor(p)<<"."<<endl;
  //  cout<<"Total number of aperture definitions: "<<Pos.size()<<"."<<endl;
}

void OneMetre::DefineAperture(double p, Aperture Ap)
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
  //  cout<<"Aperture definition inserted at the position "<<p<<" -> "<<p-floor(p)<<"."<<endl;
  //  cout<<"Total number of aperture definitions: "<<Pos.size()<<"."<<endl;
}

void OneMetre::DefineAperture(double p, vector<double> A4)
{
  if ( p == 1.0 )
    p = 0.99999;
  // Only add new positions with larger amplitudes than the last aperture defined
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
  //  cout<<"Aperture definition inserted at the position "<<p<<" -> "<<p-floor(p)<<"."<<endl;
  //  cout<<"Total number of aperture definitions: "<<Pos.size()<<"."<<endl;
}

Aperture OneMetre::GetAperture(double p)
{
  int done = 0,
    do_special = 0;
  int k = 0;

  //  if ( p = 1.0 )  // Add this to avoid some segmentation fault (SR, 13/09/2004)
  //    p=0.9999;     // I have to understand yet what causes troubles.

  if ( p > 1 )
    p = p - floor(p);

  if ( p > 0.9999 ) // I get some segmentation fault otherwise... (SR, 11/04/2005)
    p = 0.9999;

  // Preliminary checks:
  if ( (int)Pos.size() == 0){
    cout<<"ERROR: The aperture has not been initialized properly:"<<endl;
    cout<<"       No aperture has been defined in this OneMetre"<<endl;
    cout<<"       Aperture asked at the position: "<<p<<endl;
    exit(0);
  }
  else if ( (int)Pos.size() == 1 ){ // one aperture only -> same aperture in all the metre!
    Atmp = Apert[0];
    done = 1;
  }

  if ( !done ){
    // Clean-up!
    Atmp.empty();
    Atmp_vec.clear();
    
    // Add 'flat' aperture definitions if the point at '0.0' and '0.99' are not given
    // Only if this has not been done yet (i.e., only if Pos_ex.size()==0 )
    if ( Pos_ex.size() == 0 ){
      if ( Pos.size() > 0 && Pos[0] > 0.001 ){
	cout<<"Warning: aperture definition added at the beginning of the metre!"<<endl;
	Pos_ex.push_back(0.0);
	Apert_ex.push_back(Apert[0]);
	for (int q = 0; q < Pos.size(); q++){
	  Pos_ex.push_back( Pos[q] );
	  Apert_ex.push_back( Apert[q] );
	}
      } else {
	Pos_ex = Pos;
	Apert_ex = Apert;
      }
      if ( Pos.size() > 0 && Pos[ Pos.size()-1 ] < 0.99 ){
	cout<<"Warning: aperture definition added at the end of the metre!"<<endl;
	Pos_ex.push_back( 0.999999999 );
	Apert_ex.push_back( Apert[Apert.size()-1] );
      }
    }
    //
    if ( p == 0.0 )
      Atmp = Apert_ex[0];
    else if ( p == 1.0 )
      Atmp = Apert_ex[Apert_ex.size()-1];
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
      Atmp.PutApert( Atmp_vec );
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
  } 
  return Atmp;
}

void OneMetre::GetApertDef(vector<double> *Position, vector<Aperture> *ThisApert)
{
  Position->clear();
  ThisApert->clear();
  for (int i = 0; i < (int) Pos.size(); i++){
    Position -> push_back( Pos[i] );
    ThisApert -> push_back( Apert[i] );
  }
  /*
  // Example of usage :
  OneMetre Test;
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

void OneMetre::status(){
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

void OneMetre::empty(){
  // Clear all the vectors which allocate memory dynamically!!!
  Pos.clear();
  Apert.clear();
  Pos_ex.clear();
  Apert_ex.clear();
  Atmp.empty();
  Atmp_vec.clear();
}
