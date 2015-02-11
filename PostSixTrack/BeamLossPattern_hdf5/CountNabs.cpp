/*
 * SR, 22-04-2005
 * New version of the program to count the ACTUAL number of 
 * absorbed particles in the collimators by comparison with 
 * the loss locations in the LPI files.
 * This program uses the new SixTrack output 'all_absorptions.dat',
 * which contains already the absorption locations (an not the
 * full list of impacts...).
 * The program does the analysis for one file (no loops) and hence
 * it is suitable for performing the analysis on batch!
 *
 * *******************
 * FindNabs.cpp
 * Like in the script style, it takes as input seed numbers,
 * energy, halo type and optics.
 * The program compares the LPI files and the impacts files
 * to count the actual number of absorbed particles by 
 * excluding from the impact files the protons that have 
 * touched the aperture somewhere before impacting on
 * the collimators. 
 * *************************
 */

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

int main (int argc, char* argv[])
{

  if (argc < 5){
    cout<<"Some input is missing!"<<endl;
    cout<<"The command line should look like:"<<endl;
    cout<<"  -> CountNabs s1 halo EN optics <-"<<endl;
    exit(0);
  }

  int s1;
  string halo, EN, optics;

  s1 = (int) atof(argv[1]);
  halo = argv[2];
  EN = argv[3];
  optics = argv[4];

  cout<<endl<<" Summary of input parameters: "<<endl;
  cout<<setw(20)<<"Seed:"<<setw(9)<<s1<<endl;
  cout<<setw(20)<<"Halo type:"<<"    "<<halo<<endl;
  cout<<setw(20)<<"Beam energy:"<<"    "<<EN<<endl;
  cout<<setw(20)<<"Optics:"<<"    "<<optics<<endl<<endl;

  int Np_t, Ntu_t, Hflag_t, Nsurv_t;
  double S_t, x_t, xp_t, y_t, yp_t, e_t;
  vector<int> NPART, NTURN;
  vector<double> POS;
  int Nmax = 50000;
  vector<int> NPART_lost, NTURN_lost;
  vector<double> POS_lost;
  vector<int> NPART_real, NTURN_real;
  vector<double> POS_real;
  vector<int> NPART_fake, NTURN_fake;
  vector<double> POS_fake;
  int count_ir7, count_ir3;
  double p;

  ostringstream ost;
  ifstream in, inn;
  ofstream out;
  char c_str[256];
  string input, output;


  // Set input/output names for the impact files
  ost<<"all_absorptions."<<s1<<"."<<halo<<"."<<EN<<"."<<optics<<".dat";
  input = ost.str();
  ost.str("");
    
  // Read input file, create clean output and prepare required vector
  in.open(input.c_str(), ios::in);
  if (!in){
    cout<<"Impossible to open the file \""<<input<<"\"!!"<<endl;
    exit(0);
  }
  cout<<"-> Reading impact file: \""<<input<<"\" <-"<<endl<<endl;
  in.getline(c_str,256); // Skip the header line
  while (!in.eof()){
    in>>Np_t>>Ntu_t>>S_t;
    NPART.push_back(Np_t);
    NTURN.push_back(Ntu_t);
    POS.push_back(S_t);
  }
  in.close();
  //  cout<<NPART.size()<<endl;
    
  // Read the loss file
  // Initialization
  for (int i=0; i<Nmax; i++){
    NPART_lost.push_back(0);
    NTURN_lost.push_back(0);
    POS_lost.push_back(0.0);
  }
    
  ost<<"LPI_BeamLoss."<<s1<<"."<<halo<<"."<<EN<<"."<<optics<<".s";
  input = ost.str();
  ost.str("");
  inn.open(input.c_str(), ios::in);
  if (!inn){
    cout<<"Impossible to open the file \""<<input<<"\"!!"<<endl;
    exit(0);
  }
  cout<<"-> Reading loss file: \""<<input<<"\" <-"<<endl<<endl;
  while (1){
    inn>>Np_t>>Ntu_t>>S_t>>x_t>>xp_t>>y_t>>yp_t>>e_t>>Hflag_t>>Nsurv_t;
    if (!inn.good())
      break;
    NPART_lost[Np_t] = 1;
    NTURN_lost[Np_t] = Ntu_t;
    POS_lost[Np_t] = S_t;
  }
  inn.close();
  
  // Compare the positions of loss particles with the impact locations
  for (int i = 0; i < NPART.size(); i++) {
    Np_t = NPART[i];
    if (NPART_lost[Np_t] == 0) {
      NPART_real.push_back( Np_t );
      NTURN_real.push_back( NTURN[i] );
      POS_real.push_back( POS[i] );
    } else { 
      if ( NTURN[i] <= NTURN_lost[Np_t] && POS[i] < POS_lost[Np_t] ) { 
	NPART_real.push_back( Np_t );
	NTURN_real.push_back( NTURN[i] );
	POS_real.push_back( POS[i] );
      } else { 
	NPART_fake.push_back( Np_t );
	NTURN_fake.push_back( NTURN[i] );
	POS_fake.push_back( POS[i] );
      }
    }
  }
  cout<<"Number of particles touching the aperture before being lost "
      <<"in a collimator: "<<NPART.size()-NPART_real.size()<<endl<<endl;
  if ( NPART_real.size() != NPART_fake.size() )
    cout<<"Warning: sum of real and fake impacts does not give the total"<<endl
	<<"         number of absorbed particles!"<<endl;
  
  // Count the losses in IR3/IR7
  count_ir3 = 0;
  count_ir7 = 0;
  for (int i = 0; i < NPART_real.size(); i++){
    p = POS_real[i];
    if ( p > 6395.8168 && p < 6933.6248 )
      count_ir3++;
    else if ( p > 19725.2584 && p < 20263.0664)
      count_ir7++;
  }
  cout<<"*******************************************************"<<endl;
  cout<<"*  Summary of partile absorptions in the collimators  *"<<endl; 
  cout<<"*******************************************************"<<endl;
  cout<<"*"<<setw(40)<<"Total number of SixTrack impacts:"<<setw(12)<<NPART.size()<<" *"<<endl;
  cout<<"*"<<setw(40)<<"Total number of REAL impacts:"<<setw(12)<<NPART_real.size()<<" *"<<endl;
  cout<<"*"<<setw(40)<<"Total number of FAKE impacts:"<<setw(12)<<NPART_fake.size()<<" *"<<endl;
  cout<<"*"<<setw(40)<<"Absorptions in the IR7 collimators:"<<setw(12)<<count_ir7<<" *"<<endl;
  cout<<"*"<<setw(40)<<"Absorptions in the IR3 collimators:"<<setw(12)<<count_ir3<<" *"<<endl;
  cout<<"*******************************************************"<<endl;
    
  // Write output file for REAL impacts
  ost<<"all_absorptions."<<s1<<"."<<halo<<"."<<EN<<"."<<optics<<".real.dat";
  output = ost.str();
  ost.str("");
  cout<<"Name of the REAL impact file: \""<<output<<"\"."<<endl<<endl;
  out.open(output.c_str());
  out<<"%*******************************************************"<<endl;
  out<<"%*  Summary of partile absorptions in the collimators  *"<<endl; 
  out<<"%*******************************************************"<<endl;
  out<<"%*"<<setw(40)<<"Total number of SixTrack impacts:"<<setw(12)<<NPART.size()<<" *"<<endl;
  out<<"%*"<<setw(40)<<"Total number of REAL impacts:"<<setw(12)<<NPART_real.size()<<" *"<<endl;
  out<<"%*"<<setw(40)<<"Total number of FAKE impacts:"<<setw(12)<<NPART_fake.size()<<" *"<<endl;
  out<<"%*"<<setw(40)<<"Absorptions in the IR7 collimators:"<<setw(12)<<count_ir7<<" *"<<endl;
  out<<"%*"<<setw(40)<<"Absorptions in the IR3 collimators:"<<setw(12)<<count_ir3<<" *"<<endl;
  out<<"%*******************************************************"<<endl;
  out<<setw(6)<<"%Np"<<setw(4)<<"Ntu"<<setw(12)<<"Spos [ m ]"<<endl;
  out.precision(10);
  
  for (int i = 0; i < NPART_real.size(); i++)
    out<<setw(6)<<NPART_real[i]
       <<setw(4)<<NTURN_real[i]
       <<setw(12)<<POS_real[i]<<endl;
  out.close();
  
  // Write output file for FAKE impacts
  ost<<"all_absorptions."<<s1<<"."<<halo<<"."<<EN<<"."<<optics<<".fake.dat";
  output = ost.str();
  ost.str("");
  cout<<"Name of the FAKE impact file: \""<<output<<"\"."<<endl<<endl;
  out.open(output.c_str());
  out<<"%*******************************************************"<<endl;
  out<<"%*  Summary of partile absorptions in the collimators  *"<<endl; 
  out<<"%*******************************************************"<<endl;
  out<<"%*"<<setw(40)<<"Total number of SixTrack impacts:"<<setw(12)<<NPART.size()<<" *"<<endl;
  out<<"%*"<<setw(40)<<"Total number of REAL impacts:"<<setw(12)<<NPART_real.size()<<" *"<<endl;
  out<<"%*"<<setw(40)<<"Total number of FAKE impacts:"<<setw(12)<<NPART_fake.size()<<" *"<<endl;
  out<<"%*"<<setw(40)<<"Absorptions in the IR7 collimators:"<<setw(12)<<count_ir7<<" *"<<endl;
  out<<"%*"<<setw(40)<<"Absorptions in the IR3 collimators:"<<setw(12)<<count_ir3<<" *"<<endl;
  out<<"%*******************************************************"<<endl;
  out<<setw(6)<<"%Np"<<setw(4)<<"Ntu"<<setw(12)<<"Spos [ m ]"<<endl;
  out.precision(10);
  
  for (int i = 0; i < NPART_fake.size(); i++)
    out<<setw(6)<<NPART_fake[i]
       <<setw(4)<<NTURN_fake[i]
       <<setw(12)<<POS_fake[i]<<endl;
  out.close();

  // Clean up vectors for the next file
  NPART.clear();
  NTURN.clear();
  POS.clear();
  NPART_lost.clear();
  NTURN_lost.clear();
  POS_lost.clear();
  NPART_real.clear();
  NTURN_real.clear();
  POS_real.clear();
  NPART_fake.clear();
  NTURN_fake.clear();
  POS_fake.clear();

  return 0;
}
