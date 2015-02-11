/*
 * CleanInelastic.cpp
 *
 * Clean-up the inelastic impact files of SixTrack.
 * Particles lost in the aperture BEFORE being absorbed
 * in a collimator are disregarded.
 *
 * Required inputs:
 * 1) Inelastic output file from SixTrack
 * 2) Loss pattern file with the loss locations
 * 3) Collimator positions (from Matlab output, for the moment)
 * 4) coll_summary, to get CollNum vs CollName
 *
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
    cout<<"  -> CleanInelastic Impact.file Loss.file Coll.positions coll_summary file <-"<<endl;
    exit(1);
  }

  string inel_file = argv[1];
  string loss_file = argv[2];
  string list_file = argv[3];
  string summ_file = argv[4];

  // Write summary
  cout<<"- - - - - - - -"<<endl;
  cout<<setw(22)<<"Impact file: "<<inel_file<<endl;
  cout<<setw(22)<<"Loss file: "<<loss_file<<endl;
  cout<<setw(22)<<"Collimator file: "<<list_file<<endl;
  cout<<setw(22)<<"\"coll_summary\" file: "<<summ_file<<endl;
  cout<<"- - - - - - - -"<<endl;


  int Nmax = 50000;    // Maximum values of Npart
  int NCollMax = 500;  // Maximum number of collimators

  vector<double> Length;     // Names (and icoll) from SixTrack
  vector<string> Name;

  vector<string> CollName;   // Name and position from matlab 
  vector<double> CollPos;

  vector<double> Position;   // Position vs icoll

  // Location of losses
  vector<int> NPART_lost, NTURN_lost;
  vector<double> POS_lost;

  // Locations of inelastic impacts
  vector<int> NCOLL_inel, FLAG_inel, NPART_inel, NTURN_inel;
  vector<double> ANGLE_inel, POS_inel, X_inel, XP_inel,
    Y_inel, YP_inel;

  // Input/output streams
  ifstream in;
  ofstream out1, out2;

  // Temporary auxiliary variables
  int i1, i2, i3, i4, i5;
  double d1, d2, d3, d4, d5, d6;
  string str_tmp;
  int count = 0, 
    j = 0,
    n_p;
  char c_str[256];


  // Initializations
  for (int i = 0; i <= NCollMax; i++){
    Position.push_back(0.0);
    Length.push_back(0.0);
    Name.push_back("");
  }
  for (int i=0; i<Nmax; i++){
    NPART_lost.push_back(0);
    NTURN_lost.push_back(0);
    POS_lost.push_back(0.0);
  }


  // Get collimator name vs sixtrack number
  in.open(summ_file.c_str(), ios::in);
  if (!in){
    cout<<"Impossible to open the file \""<<summ_file<<"\"!!"<<endl;
    exit(2);
  }
  //
  in.getline(c_str,256); // Skip the header line
  while (!in.eof()){
    in>>i1>>str_tmp>>i2>>i3>>d1>>d2>>d3;
    Length[i1] = d3;
    Name[i1] = str_tmp;
  }
  in.close();
  count = 0;
  for (int i = 0; i<Length.size(); i++)
    if (Length[i] > 0)
      count++;
  cout<<"Number of collimators: "<<count<<endl;


  // Get the collimator positions
  in.open(list_file.c_str(), ios::in);
  if (!in){
    cout<<"Impossible to open the file \""<<list_file<<"\"!!"<<endl;
    exit(2);
  }
  in.getline(c_str,256); // Skip the header line
  while (!in.eof()){
    in>>i1>>str_tmp>>d1;
    CollName.push_back(str_tmp);
    CollPos.push_back(d1);
  }
  in.close();
  cout<<"Number of collimator positions: "<<CollName.size()<<endl;

  // Assign the collimator position.
  for (int i = 0; i < Length.size(); i++) {
    if ( Length[i] > 0 ) {
      j = 0;
      while ( j < CollName.size() && CollName[j] != Name[i] )
	j++;
      if ( j == CollName.size() ) {
	cout<<"Error: Position of collimator \""
	    <<Name[i]<<"\" NOT found!"<<endl;
	exit(3);
      } else {
	Position[i] = CollPos[j];
      }
    }
  }

  // Read loss file
  //
  in.open(loss_file.c_str(), ios::in);
  if (!in){
    cout<<"Impossible to open the file \""<<loss_file<<"\"!!"<<endl;
    exit(2);
  }
  while (!in.eof()){
    in>>i1>>i2>>d1>>d2>>d3>>d4>>d5>>d6>>i3>>i4;
    NPART_lost[i1] = 1;
    NTURN_lost[i1] = i2;
    POS_lost[i1] = d1;
  }
  in.close();

  // Read the impact file
  in.open(inel_file.c_str(), ios::in);
  if (!in){
    cout<<"Impossible to open the file \""<<inel_file<<"\"!!"<<endl;
    exit(2);
  }
  in.getline(c_str,256); // Skip the header line
  while (!in.eof()){
    in>>i1>>d1>>d2>>d3>>d4>>d5>>d6>>i2>>i3>>i4;
    NCOLL_inel.push_back(i1);
    ANGLE_inel.push_back(d1);
    POS_inel.push_back(d2);    // Position WITHIN collimator, no s coordinate!
    X_inel.push_back(d3);
    XP_inel.push_back(d4);
    Y_inel.push_back(d5);
    YP_inel.push_back(d6);
    FLAG_inel.push_back(i2);
    NPART_inel.push_back(i3);
    NTURN_inel.push_back(i4);
  }
  in.close();

  // Write clean files
  // (Use C syntax to have better control of output format)
  FILE *fp1, *fp2;
  fp1=fopen("impacts_real.dat","w");
  fp2=fopen("impacts_fake.dat","w");
  fprintf(fp1,"%s\n","# 1=icoll 2=c_rotation 3=s 4=x 5=xp 6=y 7=yp 8=nabs 9=np 10=ntu");
  fprintf(fp2,"%s\n","# 1=icoll 2=c_rotation 3=s 4=x 5=xp 6=y 7=yp 8=nabs 9=np 10=ntu");
  for (int i = 0; i < NCOLL_inel.size(); i++){
    n_p = NPART_inel[i];
    if ( NPART_lost[n_p] == 1 && 
	 NTURN_lost[n_p] <= NTURN_inel[i] &&
	 POS_lost[n_p] <= Position[NCOLL_inel[i]]) {
      fprintf(fp2, "%4d %5.3f %8.6f %16.7e %16.7e %16.7e %16.7e %2d %5d%5d\n", 
	      NCOLL_inel[i],
	      ANGLE_inel[i],
	      POS_inel[i],
	      X_inel[i],
	      XP_inel[i],
	      Y_inel[i],
	      YP_inel[i],
	      FLAG_inel[i],
	      NPART_inel[i],
	      NTURN_inel[i]);
    } else {
      fprintf(fp1, "%4d %5.3f %8.6f %16.7e %16.7e %16.7e %16.7e %2d %5d%5d\n", 
	      NCOLL_inel[i],
	      ANGLE_inel[i],
	      POS_inel[i],
	      X_inel[i],
	      XP_inel[i],
	      Y_inel[i],
	      YP_inel[i],
	      FLAG_inel[i],
	      NPART_inel[i],
	      NTURN_inel[i]);
    }
  }

  fclose(fp1);
  fclose(fp2);
    
  // Clean-up
  NPART_lost.clear();
  NTURN_lost.clear();
  POS_lost.clear();

  NCOLL_inel.clear(); 
  FLAG_inel.clear();
  NPART_inel.clear();
  NTURN_inel.clear();
  ANGLE_inel.clear();
  POS_inel.clear();
  X_inel.clear();
  XP_inel.clear();    
  Y_inel.clear(); 
  YP_inel.clear();

  return 0;
}
