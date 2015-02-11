/*
 * Write the LHC aperture along the ring for various 
 * azimuthal angles.
 */

#include "ReadTwiss.h"
#include "Aperture.h"
#include "OneMetre.h"
#include "AssignOneMetre.h"

double CheckPos(double pp); // See CheckPos.cpp

int main (int argc, char* argv[])
{

  if (argc < 2){
    cout<<"ERROR in the input definition!"<<endl;
    cout<<"Command line should look like:"<<endl;
    cout<<"      -> GetAperture ApertureFile.dat <-"<<endl;
    return 1;
  }

  double Dl = 0.100; // Precision to identify longitudinal loss positions
  double LHCLength = 26658.8832;


  //////////////////////////////
  // Setup the aperture model //
  //////////////////////////////

  // Load the LHC sequence with apertures
  vector<OneMetre> LHC;
  vector<string> Keyword, Name, Parent;
  vector<string> KeywordNoQuotes, NameNoQuotes, ParentNoQuotes;
  vector<double> Position, Length, Apert1, Apert2, Apert3, Apert4;
  // Read twiss file with apertures (no drifts!)
  //  ReadTwissNoDrifts("allaper_inj_20041008.b1", &Keyword, &Name, &Parent, &KeywordNoQuotes, 
  cout<<"Reading aperture file "<<argv[1]<<endl;
  ReadTwissNoDrifts(argv[1], &Keyword, &Name, &Parent, &KeywordNoQuotes, 
  		    &NameNoQuotes, &ParentNoQuotes, &Position, &Length, 
  		    &Apert1, &Apert2, &Apert3, &Apert4);
  AssignOneMetre(&LHC, Keyword, Name, Parent, Position, Length, 
		 Apert1, Apert2, Apert3, Apert4);
  cout<<"Length of the read sequence: "<<LHC.size()<<" metres."<<endl<<endl;
  // Clean-up here the variable no longer needed:
  Keyword.clear();
  Name.clear();
  Parent.clear();
  KeywordNoQuotes.clear();
  NameNoQuotes.clear();
  ParentNoQuotes.clear();
  Position.clear();
  Length.clear();
  Apert1.clear();
  Apert2.clear();
  Apert3.clear();
  Apert4.clear();
  //

  // Write Aperture vs s every 10 cm
  ofstream out_lhc("LHCAperture.dat");
  out_lhc<<"%1=s [km]; 2=Ax [m]; 3=Ay [m]; 4=A45deg [m]"<<endl;
  Aperture Atmp;
  double s;
  for (int i = 0; i < LHC.size(); i++){
    for (int j = 0; j < 10; j++){
      s = (double)i+(double)j/10;
      Atmp = LHC[(int)s].GetAperture((double)j/10);
      out_lhc.precision(7);
      out_lhc<<setw(12)<<s;
      out_lhc.precision(6);
      out_lhc<<setw(14)<<Atmp.GiveAperture( 0.0 );
      out_lhc<<setw(14)<<Atmp.GiveAperture( 90.0 );
      out_lhc<<setw(14)<<Atmp.GiveAperture( 45.0 )<<endl;
      Atmp.empty();
    }
  }
  out_lhc.close();

  return 0;
}

double CheckPos (double pp)
{
  double LHCLength = 26658.8832;
  if ( pp < 0.0 )
    pp = LHCLength + pp;
  if ( pp > LHCLength )
    pp = pp - LHCLength;
  return pp;
}

