/*
 * SR, 26-04-2005
 * Change the program to do a tracking in the beam direction
 * instead of the backwards tracking used so far.
 * Include also the possibility of saving the trajectories of 
 * lost particles.
 *
 * SR, 21-04-2005
 * Add the count of the halo file lines, the check the size of
 * halo files on the LSF system pools.
 *
 * SR, 18-04-2005
 * Fix small bug for particles lost at the very first point were
 * their trajectory is recorded.
 * Small bug on the storage of OldXP,... variables also fixed.
 *
 * SR, 17-04-2005
 * Add in the output the number of the turn when the halo particle
 * was created, to calculate the number of surviving turns.
 *
 * SR, 15-04-2005
 * Update the program to read the new trajectory format with
 * particle energy and flag for halo type.
 *
 * SR, 14-04-2005
 * Major change in the code: check upstream of the interpolated
 * loss point to verify if there are hit aperture locations 
 * between two Sixtrack markers. This also fixes the problem
 * that the second half of a magnet, downstream of the thin
 * lens/marker location, can never see losses (see logbook,
 * page 114).
 *
 * SR, 15-02-2005
 * Full name of aperture file added as an argument in the
 * command line (before, only the energy had to be specified).
 *
 * SR, 18-11-2004
 * The size of the vectors that count the particle number has to
 * be increased to take into account the numbering used by 
 * Guillaume:
 * NPART = NLOOP*100 + i (1 <= i <= 64).
 * Ex.: tracking studies with 157*64 particles require vectors
 * with more than 15764 elements!!
 *
 * SR, 08-10-2004
 * A round aperture of 40mm is assignet to all collimators. Otherwise,
 * more particles are lost at IR7. In principle, the correct tracking
 * inside the collimator jaws is carried out in CollTrack!
 *
 */

#include "ReadTwiss.h"
#include "Aperture.h"
#include "OneMetre.h"
#include "AssignOneMetre.h"
#include "Survey.h"

double CheckPos(double pp); // See CheckPos.cpp

int main (int argc, char* argv[])
{
  if (argc < 5){
    cout<<"Some input is missing!"<<endl;
    cout<<"The command line should look like:"<<endl;
    cout<<"  -> main_Ralph_2004-09-12 inj input.dat output.txt ApertureFile.txt <-"<<endl;
    exit(0);
  }

  double Dl = 0.100; // Precision to identify longitudinal loss positions
  double LHCLength = 26658.8832;

  int _S_ = 1;       // Flag for using survey
  int _X_ = 0;       // Flag for using crossing

  int _SaveLost_ = 0; // Save the trajectories of losdt particles (last turn)

  // add flag for survey only (Guillaume runs)

  ifstream in;
  ofstream out,
    out_part; // SR, 26-04-2005 
  char c_str[256];
  double s_t, x_t, xp_t, y_t, yp_t, en_t;
  int n_t, n_tu, n_h;
  int count = 0;
  //  int k_i,
  //    k_i_max; //Corresponds to the distance to the previous trajectory definition...
  double new_s_t, new_x_t, new_y_t;
  double smallD;
  double Xorb, Yorb;          // Total orbit offset
  double Xsur, Ysur, Xx, Yx;  // Contributions fron survey and crossing
  double DxXing = 0.0,        // Step in trajectory due to kick only
    DyXing = 0.0;             // Initialize them to zero here!

  //  double s_t_save, x_t_save, y_t_save; // SR, 14-04-2005
  //  int found_loss = 0;

  int line_number = 0;

  vector<double> Slost, Xlost, XPlost, Ylost, YPlost,
    ENlost; // SR, 15-04-2005
  vector<int> Nlost, Tlost,
    Hlost, LastTurn;
  vector<double> Slost2, Xlost2, XPlost2, Ylost2, YPlost2,
    ENlost2;
  vector<int> Nlost2, Tlost2, 
    Hlost2;

  // Initialize flags
  int Np = 30000; //  int Np = 500000;
  vector<int> Flag, FirstTurn;
  vector<double> OldXP, OldYP, OldS, OldXsur; // Need to store in memory 
  for (int i = 0; i < Np; i++){               // old xp, yp, s and Xsur.
    Flag.push_back(0);                        // to reconstruct trajectory.
    //
    FirstTurn.push_back(0);
    //
    OldXP.push_back(0.0);
    OldYP.push_back(0.0);
    OldS.push_back(-1.0); // SR, 18-04-2005: To find particles that are absorbed at the first appearance
    OldXsur.push_back(0.0);
  }

  // Initialize input file from command line
  string EN = argv[1];
  string File = argv[2];
  string Twiss = argv[4];
  string output = "LP_",
    output2 = "LPI_";
  output += argv[3];
  output2 += argv[3];
  if ( _S_ | _X_ ){
    output += ".";
    output2 += ".";
  }
  if ( _S_ ){
    output += "s";
    output2 += "s";
  }
  if ( _X_ ){
    output += "x";
    output2 += "x";
  }
  cout<<"Summary of input parameters:"<<endl;
  cout<<setw(50)<<"Beam energy: "<<EN<<endl;
  cout<<setw(50)<<"Twiss file: "<<Twiss<<endl;
  cout<<setw(50)<<"Input file: "<<File<<endl;
  cout<<setw(50)<<"Output files -> "<<endl;
  cout<<setw(50)<<"Loss patterns with 1m resolution: "<<output<<endl;
  cout<<setw(50)<<"Interpolated loss patterns with 0.10 m resol.: "<<output2<<endl;
  //  return 0;

  //////////////////////////////
  // Setup the aperture model //
  //////////////////////////////

  // Load the LHC sequence with apertures
  vector<OneMetre> LHC;
  vector<string> Keyword, Name, Parent;
  vector<string> KeywordNoQuotes, NameNoQuotes, ParentNoQuotes;
  vector<double> Position, Length, Apert1, Apert2, Apert3, Apert4;
  // Read twiss file with apertures (no drifts!)
  ReadTwissNoDrifts(Twiss, &Keyword, &Name, &Parent, &KeywordNoQuotes, 
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

  // Read Survey data for the orbit position (Survey + Crossing + derivatives)
  Survey LHC_sur;
  string IN_sur = "SurveyWithCrossing_XP_" + EN + ".dat";
  cout<<"Reading: "<<IN_sur<<endl<<endl;
  LHC_sur.LoadLHC_Crossing_XP( IN_sur );

  /////////////////////////////////////////////////
  // Find the positions where particles are lost //
  /////////////////////////////////////////////////
  cout<<"-> Processing data <-"<<endl;
  cout<<"Reading the halo file: \""<<File<<"\""<<endl;
  in.open(File.c_str(), ios::in);
  if (!in){
    cout<<"Impossible to open the file !"<<endl;
    cout<<"Error status: "<<in<<endl;
    exit(0);
  }
  in.getline(c_str,256); // Skip the first line with the header
  while (1){
    in>>n_t>>n_tu>>s_t>>x_t>>xp_t>>y_t>>yp_t>>en_t>>n_h; // Don't need to ChechPos(s_t): 
    x_t = x_t / 1000;                         // SixTrack output should be ok!
    y_t = y_t / 1000;
    xp_t = xp_t / 1000;
    yp_t = yp_t / 1000;
    // This is not needed, later I check if OldS<0
    //    if (OldXP[n_t]==0.0 & OldYP[n_t]==0.0) {
    //      OldXP[n_t] = xp_t;  // First time that the particle is considered...
    //      OldYP[n_t] = yp_t; // Check here!
    //    }
    if (!in.good())
      break;
    line_number++;
    if (Flag[n_t] != 2){
      //
      if (Flag[n_t] == 0)      // Save the number of the turn when the particle 
	FirstTurn[n_t] = n_tu; // was created (the first time that it is found:flag=0)
      //
      Flag[n_t] = 1; // Use another number to skip the first point (inside collimators)
      //
      Xsur = 0.0;
      Ysur = 0.0;
      Xx = 0.0;
      Yx = 0.0;
      if ( _S_ ){
	Xsur = LHC_sur.GetSurvey( s_t );
	Ysur = 0.0;
      }
      if ( _X_ ){
	Xx = LHC_sur.GetCrossX( s_t );
	Yx = LHC_sur.GetCrossY( s_t );
      }
      Xorb = Xsur + Xx;
      Yorb = Ysur + Yx;
      if ( (LHC[(int)s_t].GetAperture(s_t-floor(s_t))).IsLost(x_t + Xorb, y_t + Yorb) ){
	// Store coordinates of lost particles 
	// (no interpolation - location of sixtrack lens)
	Nlost.push_back(n_t);
	Tlost.push_back(n_tu);
	Slost.push_back(s_t);
	Xlost.push_back(x_t + Xorb);
	XPlost.push_back(OldXP[n_t]);
	Ylost.push_back(y_t + Yorb);
	YPlost.push_back(OldYP[n_t]);
	ENlost.push_back(en_t);
	Hlost.push_back(n_h);
	//
	LastTurn.push_back(n_tu-FirstTurn[n_t]);
	//
	Flag[n_t] = 2;	// Update the flag for lost particles (flag=2)
	//
	// Interpolation for a resolution of Dl
	if ( OldS[n_t] < 0.0 ){
	  cout<<"Particle "<<n_t<<" lost at the first point where it is encountered! ";
	  cout<<"Old coordinates are used (no backwards tracking)!"<<endl;
	  Nlost2.push_back(n_t);
	  Tlost2.push_back(n_tu);// Turn number might change if we cross IP1 - neglect 
	  Slost2.push_back(s_t); // this detail for the moment...
	  Xlost2.push_back(x_t + Xorb);
	  XPlost2.push_back(xp_t); // Put the derivative at this point
	  Ylost2.push_back(y_t + Yorb);
	  YPlost2.push_back(yp_t);
	  //
	  ENlost2.push_back(en_t);
	  Hlost2.push_back(n_h);
	} else { 
	  // fix the case of two points around the end of the ring... 
	  // maybe it is okay like this...
	  smallD = (1 - (OldS[n_t]*10-floor(OldS[n_t]*10)))/10; // To get the multiple of 0.1
	  //	  cout<<smallD<<endl;
	  new_s_t = OldS[n_t] + smallD + 0.0000000001;
	  new_x_t = x_t - (s_t-new_s_t) * OldXP[n_t];
	  new_y_t = y_t - (s_t-new_s_t) * OldYP[n_t];
	  if ( _S_ )
	    new_x_t = new_x_t + LHC_sur.GetSurvey( new_s_t ); // Add survey
	  if ( _X_ ){
	    new_x_t = new_x_t + LHC_sur.GetCrossX( new_s_t ); // Add Xing
	    new_y_t = new_y_t + LHC_sur.GetCrossY( new_s_t );
	  }
	  //	  cout<<setw(12)<<new_s_t<<setw(15)<<new_x_t<<setw(15)<<new_y_t<<endl;
	  //	  cout<<(LHC[(int)new_s_t].GetAperture(new_s_t-floor(new_s_t))).IsLost(new_x_t, new_y_t)<<endl;
	  // This requires changes for the case with old/new point before/after end of the ring
	  while ( new_s_t < s_t && 
		  ! (LHC[(int)new_s_t].GetAperture(new_s_t-floor(new_s_t))).IsLost(new_x_t, new_y_t) ){
	    //	    cout<<setw(12)<<new_s_t<<setw(12)<<new_x_t<<setw(12)<<new_y_t<<endl;
	    new_s_t = CheckPos( new_s_t + Dl);
	    new_x_t = x_t - (s_t-new_s_t) * OldXP[n_t];
	    new_y_t = y_t - (s_t-new_s_t) * OldYP[n_t];
	    if ( _S_ )
	      new_x_t = new_x_t + LHC_sur.GetSurvey( new_s_t );
	    if ( _X_ ){
	      new_x_t = new_x_t + LHC_sur.GetCrossX( new_s_t );
	      new_y_t = new_y_t + LHC_sur.GetCrossY( new_s_t );
	    }
	  }
	  Nlost2.push_back(n_t);
	  Tlost2.push_back(n_tu);     // Turn number might change if we cross IP1 - neglect 
	  Slost2.push_back(new_s_t);  // this detail for the moment...
	  Xlost2.push_back(new_x_t);
	  XPlost2.push_back(OldXP[n_t]);
	  Ylost2.push_back(new_y_t);
	  YPlost2.push_back(OldYP[n_t]);
	  ENlost2.push_back(en_t);
	  Hlost2.push_back(n_h);
	} 
      }
    }
    OldXP[n_t] = xp_t; // Store "old" variables of particle n_t before reading new line, 
    OldYP[n_t] = yp_t; // for later reconstructin of the particle's trajectory
    OldS[n_t] = s_t;
    if ( _S_ )
      OldXsur[n_t] = LHC_sur.GetSurvey( s_t );
  }
  in.close();

  // Write the outputs
  cout<<"Writing outputs ...."<<endl;
  //
  out.open(output.c_str());
  out.precision(6);
  for (int i = 0; i < Nlost.size(); i++)
    out<<setw(10)<<Nlost[i]
       <<setw(10)<<Tlost[i]
       <<setw(10)<<Slost[i]
       <<setw(15)<<Xlost[i]
       <<setw(15)<<XPlost[i]
       <<setw(15)<<Ylost[i]
       <<setw(15)<<YPlost[i]
       <<setw(15)<<ENlost[i]
       <<setw(5)<<Hlost[i]
       <<setw(4)<<LastTurn[i]<<endl;
  out.close();
  //
  out.open(output2.c_str());
  out.precision(6);
  for (int i = 0; i < Nlost2.size(); i++)
    out<<setw(10)<<Nlost2[i]
       <<setw(10)<<Tlost2[i]
       <<setw(10)<<Slost2[i]
       <<setw(15)<<Xlost2[i]
       <<setw(15)<<XPlost2[i]
       <<setw(15)<<Ylost2[i]
       <<setw(15)<<YPlost2[i]
       <<setw(15)<<ENlost2[i]
       <<setw(5)<<Hlost2[i]
       <<setw(4)<<LastTurn[i]<<endl;
  out.close();
  //

  cout<<"Total number of read lines: "<<line_number<<endl;

  if ( _SaveLost_ ) {
    // Write down the trajectories of lost particles (in one single file)
    // Create a vector with the lost turn number and the same size as the Flag
    cout<<"Writing the trajectories of lost particles..."<<endl;
    vector<int> LostTurn;
    for (int i = 0; i < Np; i++)
      LostTurn.push_back(0);
    for (int i = 0; i < Tlost.size(); i++)
      LostTurn[ Nlost[i] ] = Tlost[i];
    //
    out_part.open("LostParticles.dat", ios::out);
    //
    in.open(File.c_str(), ios::in);
    if (!in){
      cout<<"Impossible to open the file!!"<<endl;
      exit(0);
    }
    in.getline(c_str,256); // Skip the first line with the header
    // Write file header
    out_part<<"%Total number of particles: "<<Tlost.size()<<endl<<"%"<<endl;
    out_part<<"%Particle's numbers for the saved trajectories: "<<endl;
    for (int i = 0; i < Tlost.size(); i++)
      out_part<<"% "<<Nlost[i]<<endl;
    out_part<<"% "<<c_str<<endl;
    //
    while (1){
      in>>n_t>>n_tu>>s_t>>x_t>>xp_t>>y_t>>yp_t>>en_t>>n_h;
      if (!in.good())
	break;
      if (Flag[n_t] == 2 && n_tu >= LostTurn[n_t]-1 )
	out_part<<setw(8)<<n_t
		<<setw(4)<<n_tu
		<<setw(10)<<s_t
		<<setw(15)<<x_t / 1000
		<<setw(15)<<xp_t / 1000
		<<setw(15)<<y_t / 1000
		<<setw(15)<<yp_t / 1000
		<<setw(15)<<en_t
		<<setw(10)<<n_h<<endl;
    }
    in.close();
    out_part.close();
    LostTurn.clear();
  }

  // Clean-up
  Flag.clear();
  OldXP.clear(); 
  OldYP.clear();
  OldS.clear();
  //
  FirstTurn.clear();
  LastTurn.clear();
  //
  LHC.clear();
  //
  Slost.clear(); 
  Xlost.clear(); 
  XPlost.clear(); 
  Ylost.clear(); 
  YPlost.clear();
  Nlost.clear(); 
  Tlost.clear();
  Slost2.clear(); 
  Xlost2.clear(); 
  XPlost2.clear(); 
  Ylost2.clear(); 
  YPlost2.clear();
  Nlost2.clear(); 
  Tlost2.clear();
  //
  ENlost.clear();
  Hlost.clear();
  ENlost2.clear();
  Hlost2.clear();

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

