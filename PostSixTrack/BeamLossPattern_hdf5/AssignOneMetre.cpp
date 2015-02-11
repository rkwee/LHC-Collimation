#include "AssignOneMetre.h"

void AssignOneMetre(vector<OneMetre> *TheSequence, vector<string> K, vector<string> N, 
		    vector<string> Pa, vector<double> P, vector<double> L, 
		    vector<double> A1, vector<double> A2, vector<double> A3, 
		    vector<double> A4)
{
  /*
  // Example
  Aperture Atmp;
  Atmp.PutApert(A1[10], A2[10], A3[10], A4[10]);
  OneMetre Metre_tmp;
  Metre_tmp.DefineAperture(0.5, Atmp);
  // Or simply:
  Metre_tmp.DefineAperture(0.7, A1[10], .1, .1, .1);
  Metre_tmp.DefineAperture(0.7, A1[10], A2[10], A3[10], A4[10]);
  TheSequence->push_back(Metre_tmp);
  Metre_tmp.empty();
  //
  Metre_tmp.DefineAperture(0.2, A1[8], A2[8], A3[8], A4[8]);
  Metre_tmp.DefineAperture(0.3, A1[10], A2[10], A3[10], A4[10]);
  Metre_tmp.DefineAperture(0.7, A1[10], A2[10], A3[10], A4[10]);
  TheSequence->push_back(Metre_tmp);
  Metre_tmp.empty();
  //
  Metre_tmp.DefineAperture(0.2, A1[8], A2[8], A3[8], A4[8]);
  Metre_tmp.DefineAperture(0.3, A1[10], A2[10], A3[10], A4[10]);
  Metre_tmp.DefineAperture(0.7, 0, 1, 1, 2);
  Metre_tmp.DefineAperture(0.7, 0, 1, 1, 2);
  Metre_tmp.DefineAperture(0.7, 0, 1, 1, 2);
  TheSequence->push_back(Metre_tmp);
  Metre_tmp.empty();
  */

  double p, a1, a2, a3, a4,
    a1_e, a2_e, a3_e, a4_e,// tmp apertures at the end of the metre
    P_end, a1_end, a2_end, a3_end, a4_end;
  OneMetre Metre_tmp;

  // Define an auxiliary vector to see if the aperture is zero or not
  // I take the sum squared of the 4 aperture components
  vector<double> ApertMod;
  for (int i = 0; i < (int)A1.size(); i++)
    ApertMod.push_back(A1[i]*A1[i]+A3[i]*A3[i]+A2[i]*A2[i]+A4[i]*A4[i]);

  //  vector<double>  Pos, Ap1, Ap2, Ap3, Ap4;
  //  double p, a1, a2, a3, a4;

  // Beginng on the sequence - I assume that the sequence never starts
  // with an element with length~=0
  int count, The_i;
  int i = 0;
  //
  Metre_tmp.empty();
  //
  while ( ApertMod[i] == 0 )
    i++;
  The_i = i; // first non-zero aperture
  //  p_tmp = P[i];
  a1 = A1[i];
  a2 = A2[i];
  a3 = A3[i];
  a4 = A4[i];
  // First aperture starting from the beginning of the sequence!
  //  cout<<The_i<<" "<<N[i]<<" "<<P[i]<<endl;
  //  cout<<(int)floor(P[i])<<endl;
  for (int k = 0; k < (int)floor(P[i]); k++){
    Metre_tmp.DefineAperture(0.0, a1, a2, a3, a4);
    Metre_tmp.DefineAperture(0.999, a1, a2, a3, a4);
    TheSequence->push_back(Metre_tmp);
    Metre_tmp.empty();
    count++;
  }
  //
  Metre_tmp.DefineAperture(0.0, a1, a2, a3, a4); // Same aperture at beginning 
  
  //  while (count < K.size()){
  for (int j = The_i + 1; j < K.size(); j++){
    // Case 1
    if ( ApertMod[j] != 0 && L[j] == 0.0 && (floor(P[j]) - floor(P[The_i]) == 0.0 ) ){
      Metre_tmp.DefineAperture(P[The_i], A1[The_i], A2[The_i], A3[The_i], A4[The_i]);
      The_i = j;
    }
    // Case 2
    else if ( ApertMod[j] != 0 && L[j] == 0.0 && (floor(P[j])-floor(P[The_i]) > 0.0) ){
      // Close this metre (k=0)
      Metre_tmp.DefineAperture(P[The_i], A1[The_i], A2[The_i], A3[The_i], A4[The_i]);
      a1_e = (A1[j]-A1[The_i])/(P[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]))+A1[The_i];
      a2_e = (A2[j]-A2[The_i])/(P[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]))+A2[The_i];
      a3_e = (A3[j]-A3[The_i])/(P[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]))+A3[The_i];
      a4_e = (A4[j]-A4[The_i])/(P[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]))+A4[The_i];
      Metre_tmp.DefineAperture(0.99999, a1_e, a2_e, a3_e, a4_e);
      TheSequence->push_back(Metre_tmp);
      count++;
      Metre_tmp.empty();
      // Add interpolated apertures to all the empty metres in between (k=1:Delta)
      for (int k = 1; k < (int)(floor(P[j])-floor(P[The_i]) ); k++){ 
	Metre_tmp.DefineAperture(0.0, a1_e, a2_e, a3_e, a4_e);
	a1_e = (A1[j]-A1[The_i])/(P[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]+(double)k))+A1[The_i];
	a2_e = (A2[j]-A2[The_i])/(P[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]+(double)k))+A2[The_i];
	a3_e = (A3[j]-A3[The_i])/(P[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]+(double)k))+A3[The_i];
	a4_e = (A4[j]-A4[The_i])/(P[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]+(double)k))+A4[The_i];
	Metre_tmp.DefineAperture(0.99999, a1_e, a2_e, a3_e, a4_e);
	TheSequence->push_back(Metre_tmp);  // Add new metres, but the index that counts the 
	count++;                            // sequence elements does not change!!
	Metre_tmp.empty();
      }
      // Start a new metre
      Metre_tmp.DefineAperture(0.0, a1_e, a2_e, a3_e, a4_e);
      The_i = j; // P[j] will be added later!
    }
    // Element with length inside the same metre
    else if ( ApertMod[j] != 0 && L[j] > 0.0 && floor(P[j]) == floor(P[The_i]) ){
      Metre_tmp.DefineAperture(P[The_i], A1[The_i], A2[The_i], A3[The_i], A4[The_i]);
      Metre_tmp.DefineAperture(P[j]-L[j], A1[j], A2[j], A3[j], A4[j]);
      The_i = j;  // Aperture at the end of the element to be added later.
    }
    // No empty metres between 'The_i' and beginning of long element
    else if ( ApertMod[j] != 0 && L[j] > 0.0 && 
	      floor(P[j]) > floor(P[The_i]) &&
	      floor(P[j]-L[j]) == floor(P[The_i]) ){
      // Add last points to the definition (also at the end)
      Metre_tmp.DefineAperture(P[The_i], A1[The_i], A2[The_i], A3[The_i], A4[The_i]);
      Metre_tmp.DefineAperture(P[j]-L[j], A1[j], A2[j], A3[j], A4[j]);
      Metre_tmp.DefineAperture(0.99999, A1[j], A2[j], A3[j], A4[j]);
      TheSequence->push_back(Metre_tmp);
      count++;
      Metre_tmp.empty();
      // Fill metres occupied by the element with length
      for (int k = 1; k < (int)( floor(P[j]) - floor(P[The_i]) ); k++){ // Note the values of k!
	Metre_tmp.DefineAperture(0.0, A1[j], A2[j], A3[j], A4[j]);
	Metre_tmp.DefineAperture(0.99999, A1[j], A2[j], A3[j], A4[j]);
	TheSequence->push_back(Metre_tmp);
	count++;
	Metre_tmp.empty();
      }
      // Start the new metre that contains the end of the long element
      Metre_tmp.DefineAperture(0.0, A1[j], A2[j], A3[j], A4[j]);
      The_i = j;
    }
    // There are empty metres between 'The_i' and beginning of long element
    else if ( ApertMod[j] != 0 && L[j] > 0.0 && 
	      floor(P[j]) > floor(P[The_i]) &&
	      floor(P[j]-L[j]) > floor(P[The_i])){
      Metre_tmp.DefineAperture(P[The_i], A1[The_i], A2[The_i], A3[The_i], A4[The_i]);
      // Linear interpolation up to the beginning of the long metre
      a1_e = (A1[j]-A1[The_i])/(P[j]-L[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]))+A1[The_i];
      a2_e = (A2[j]-A2[The_i])/(P[j]-L[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]))+A2[The_i];
      a3_e = (A3[j]-A3[The_i])/(P[j]-L[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]))+A3[The_i];
      a4_e = (A4[j]-A4[The_i])/(P[j]-L[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]))+A4[The_i];
      Metre_tmp.DefineAperture(0.99999, a1_e, a2_e, a3_e, a4_e);
      TheSequence->push_back(Metre_tmp);
      count++;
      Metre_tmp.empty();
      //
      // Fill other metres in between
      for (int k = 1; k < (int)(floor(P[j]-L[j])-floor(P[The_i]) ); k++){ 
	Metre_tmp.DefineAperture(0.0, a1_e, a2_e, a3_e, a4_e);
	a1_e = (A1[j]-A1[The_i])/(P[j]-L[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]+(double)k))+A1[The_i];
	a2_e = (A2[j]-A2[The_i])/(P[j]-L[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]+(double)k))+A2[The_i];
	a3_e = (A3[j]-A3[The_i])/(P[j]-L[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]+(double)k))+A3[The_i];
	a4_e = (A4[j]-A4[The_i])/(P[j]-L[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]+(double)k))+A4[The_i];
	Metre_tmp.DefineAperture(0.99999, a1_e, a2_e, a3_e, a4_e);
	TheSequence->push_back(Metre_tmp);
	count++;
	Metre_tmp.empty();
      }
      // Metre in which the long element starts
      Metre_tmp.DefineAperture(0.0, a1_e, a2_e, a3_e, a4_e);
      Metre_tmp.DefineAperture(P[j]-L[j], A1[j], A2[j], A3[j], A4[j]);
      // All metres along the long element
      if ( floor(P[j]) == floor(P[j]-L[j]) ){
	Metre_tmp.DefineAperture(P[j], A1[j], A2[j], A3[j], A4[j]);
	The_i = j;
      } 
      else if ( floor(P[j]) > floor(P[j]-L[j]) ){
	Metre_tmp.DefineAperture(0.99999, A1[j], A2[j], A3[j], A4[j]);
	TheSequence->push_back(Metre_tmp);
	count++;
	Metre_tmp.empty();
	for (int k = 1; k < (int)( floor(P[j]) - floor(P[j]-L[j]) ); k++){ 
	  Metre_tmp.DefineAperture(0.0, A1[j], A2[j], A3[j], A4[j]);
	  Metre_tmp.DefineAperture(0.99999, A1[j], A2[j], A3[j], A4[j]);
	  TheSequence->push_back(Metre_tmp);
	  count++;
	  Metre_tmp.empty();
	}
	Metre_tmp.DefineAperture(0.0, A1[j], A2[j], A3[j], A4[j]);
	The_i = j;
      }
    }
    if ( ApertMod[j] != 0 ){
      P_end=P[j];  // Store these value: required to use the last define point with aperture
      a1_end=A1[j];
      a2_end=A2[j];
      a3_end=A3[j];
      a4_end=A4[j];
    }
  }
  // Always include the last point with aperture and close the corresponding metre!
  // This only works if the last point is a marker...
  // Not worth to write the code for the general case!
  Metre_tmp.DefineAperture(P_end, a1_end, a2_end, a3_end, a4_end);
  if (floor(P_end) == 26658.0)
    Metre_tmp.DefineAperture(0.8832, a1_end, a2_end, a3_end, a4_end);
  else
    Metre_tmp.DefineAperture(0.99999, a1_end, a2_end, a3_end, a4_end);
  TheSequence->push_back(Metre_tmp);
  count++;
  Metre_tmp.empty();
  //  cout<<TheSequence->size()<<endl;
  //
  // End of the sequence
  if ( (int)TheSequence->size() < 26659){
    for (int k = 1; k <=  26659 - (int)TheSequence->size(); k++){ 
      Metre_tmp.DefineAperture(0.0, a1_end, a2_end, a3_end, a4_end);
      Metre_tmp.DefineAperture(0.99999, a1_end, a2_end, a3_end, a4_end);
      TheSequence->push_back(Metre_tmp);
      count++;
      Metre_tmp.empty();
    }
    Metre_tmp.empty();
    Metre_tmp.DefineAperture(0.0, a1_end, a2_end, a3_end, a4_end);
    if (floor(P_end) == 26658.0)
      Metre_tmp.DefineAperture(P_end, a1_end, a2_end, a3_end, a4_end);
    Metre_tmp.DefineAperture(0.8832, a1_end, a2_end, a3_end, a4_end);
    TheSequence->push_back(Metre_tmp);
    count++;
    Metre_tmp.empty();
  }
  cout<<endl<<"All aperture information has been read and ";
  cout<<"the sequence has been created!"<<endl<<endl;
}

void AssignOneMetreAlign(vector<OneMetreAlign> *TheSequence, vector<string> K, vector<string> N, 
			 vector<string> Pa, vector<double> P, vector<double> L, 
			 vector<double> A1, vector<double> A2, vector<double> A3, 
			 vector<double> A4, vector<double> xA, vector<double> yA)
{
  double p, a1, a2, a3, a4, x, y,
    a1_e, a2_e, a3_e, a4_e, x_e, y_e,// tmp apertures at the end of the metre
    P_end, a1_end, a2_end, a3_end, a4_end, x_end, y_end;

  OneMetreAlign Metre_tmp;

  // Define an auxiliary vector to see if the aperture is zero or not
  // I take the sum squared of the 4 aperture components
  // For 'AssignOneMetreAlign', I shall define also zero apertures at the
  // locations where some alignment is defined?
  vector<double> ApertMod;
  for (int i = 0; i < (int)A1.size(); i++)
    ApertMod.push_back(A1[i]*A1[i]+A3[i]*A3[i]+A2[i]*A2[i]+A4[i]*A4[i]);
  //  vector<double> SurveyMod;
  //  for (int i = 0; i < (int)xA.size(); i++)
  //    SurveyMod.push_back(xA[i]*xA[i] + yA[i]*yA[i]);

  // Beginng of the sequence - I assume that the sequence never starts
  // with an element with length~=0
  int count, The_i;
  int i = 0;
  //
  Metre_tmp.empty();
  //
  while ( ApertMod[i] == 0 )
    i++;
  The_i = i; // first non-zero aperture
  a1 = A1[i];
  a2 = A2[i];
  a3 = A3[i];
  a4 = A4[i];
  x = xA[i];
  y = yA[i];
  //cout<<"figa1"<<endl;
  // First aperture starting from the beginning of the sequence!
  for (int k = 0; k < (int)floor(P[i]); k++){
    Metre_tmp.DefineApertureAlign(0.0, a1, a2, a3, a4, x, y);
    Metre_tmp.DefineApertureAlign(0.999, a1, a2, a3, a4, x, y);
    TheSequence->push_back(Metre_tmp);
    Metre_tmp.empty();
    count++;
  }
  //
  Metre_tmp.DefineApertureAlign(0.0, a1, a2, a3, a4, x, y); // Same aperture at beginning 
  //cout<<"figa2"<<endl;
  for (int j = The_i + 1; j < K.size(); j++){
    // Case 1
    if ( ApertMod[j] != 0 && L[j] == 0.0 && (floor(P[j]) - floor(P[The_i]) == 0.0 ) ){
      Metre_tmp.DefineApertureAlign(P[The_i], A1[The_i], A2[The_i], A3[The_i], A4[The_i], xA[The_i], yA[The_i]);
      The_i = j;
    //cout<<"figa3"<<endl;
    }
    // Case 2
    else if ( ApertMod[j] != 0 && L[j] == 0.0 && (floor(P[j])-floor(P[The_i]) > 0.0) ){
      // Close this metre (k=0)
      Metre_tmp.DefineApertureAlign(P[The_i], A1[The_i], A2[The_i], A3[The_i], A4[The_i], xA[The_i], yA[The_i]);
      a1_e = (A1[j]-A1[The_i])/(P[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]))+A1[The_i];
      a2_e = (A2[j]-A2[The_i])/(P[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]))+A2[The_i];
      a3_e = (A3[j]-A3[The_i])/(P[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]))+A3[The_i];
      a4_e = (A4[j]-A4[The_i])/(P[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]))+A4[The_i];
      x_e  = (xA[j]-xA[The_i])/(P[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]))+xA[The_i];
      y_e  = (yA[j]-yA[The_i])/(P[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]))+yA[The_i];
      Metre_tmp.DefineApertureAlign(0.99999, a1_e, a2_e, a3_e, a4_e, x_e, y_e);
      TheSequence->push_back(Metre_tmp);
      count++;
      Metre_tmp.empty();
      // Add interpolated apertures to all the empty metres in between (k=1:Delta)
      for (int k = 1; k < (int)(floor(P[j])-floor(P[The_i]) ); k++){ 
	Metre_tmp.DefineApertureAlign(0.0, a1_e, a2_e, a3_e, a4_e, x_e, y_e);
	a1_e = (A1[j]-A1[The_i])/(P[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]+(double)k))+A1[The_i];
	a2_e = (A2[j]-A2[The_i])/(P[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]+(double)k))+A2[The_i];
	a3_e = (A3[j]-A3[The_i])/(P[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]+(double)k))+A3[The_i];
	a4_e = (A4[j]-A4[The_i])/(P[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]+(double)k))+A4[The_i];
	x_e  = (xA[j]-xA[The_i])/(P[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]+(double)k))+xA[The_i];
	y_e  = (yA[j]-yA[The_i])/(P[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]+(double)k))+yA[The_i];
	Metre_tmp.DefineApertureAlign(0.99999, a1_e, a2_e, a3_e, a4_e, x_e, y_e);
	TheSequence->push_back(Metre_tmp);  // Add new metres, but the index that counts the 
	count++;                            // sequence elements does not change!!
	Metre_tmp.empty();
      }
      // Start a new metre
      Metre_tmp.DefineApertureAlign(0.0, a1_e, a2_e, a3_e, a4_e, x_e, y_e);
      The_i = j; // P[j] will be added later!
    //cout<<"figa4"<<endl;
    }
    // Element with length inside the same metre
    else if ( ApertMod[j] != 0 && L[j] > 0.0 && floor(P[j]) == floor(P[The_i]) ){
      Metre_tmp.DefineApertureAlign(P[The_i], A1[The_i], A2[The_i], A3[The_i], A4[The_i], xA[The_i], yA[The_i]);
      Metre_tmp.DefineApertureAlign(P[j]-L[j], A1[j], A2[j], A3[j], A4[j], xA[j], yA[j]);
      The_i = j;  // Aperture at the end of the element to be added later.
    //cout<<"figa5"<<endl;
    }
    // No empty metres between 'The_i' and beginning of long element
    else if ( ApertMod[j] != 0 && L[j] > 0.0 && 
	      floor(P[j]) > floor(P[The_i]) &&
	      floor(P[j]-L[j]) == floor(P[The_i]) ){
      // Add last points to the definition (also at the end)
      Metre_tmp.DefineApertureAlign(P[The_i], A1[The_i], A2[The_i], A3[The_i], A4[The_i], xA[The_i], yA[The_i]);
      Metre_tmp.DefineApertureAlign(P[j]-L[j], A1[j], A2[j], A3[j], A4[j], xA[j], yA[j]);
      Metre_tmp.DefineApertureAlign(0.99999, A1[j], A2[j], A3[j], A4[j], xA[j], yA[j]);
      TheSequence->push_back(Metre_tmp);
      count++;
      Metre_tmp.empty();
      // Fill metres occupied by the element with length
      for (int k = 1; k < (int)( floor(P[j]) - floor(P[The_i]) ); k++){ // Note the values of k!
	Metre_tmp.DefineApertureAlign(0.0, A1[j], A2[j], A3[j], A4[j], xA[j], yA[j]);
	Metre_tmp.DefineApertureAlign(0.99999, A1[j], A2[j], A3[j], A4[j], xA[j], yA[j]);
	TheSequence->push_back(Metre_tmp);
	count++;
	Metre_tmp.empty();
      }
      // Start the new metre that contains the end of the long element
      Metre_tmp.DefineApertureAlign(0.0, A1[j], A2[j], A3[j], A4[j], xA[j], yA[j]);
      The_i = j;
    //cout<<"figa6"<<endl;
    }
    // There are empty metres between 'The_i' and beginning of long element
    else if ( ApertMod[j] != 0 && L[j] > 0.0 && 
	      floor(P[j]) > floor(P[The_i]) &&
	      floor(P[j]-L[j]) > floor(P[The_i])){
      Metre_tmp.DefineApertureAlign(P[The_i], A1[The_i], A2[The_i], A3[The_i], A4[The_i], xA[The_i], yA[The_i]);
      // Linear interpolation up to the beginning of the long metre
      a1_e = (A1[j]-A1[The_i])/(P[j]-L[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]))+A1[The_i];
      a2_e = (A2[j]-A2[The_i])/(P[j]-L[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]))+A2[The_i];
      a3_e = (A3[j]-A3[The_i])/(P[j]-L[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]))+A3[The_i];
      a4_e = (A4[j]-A4[The_i])/(P[j]-L[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]))+A4[The_i];
      x_e  = (xA[j]-xA[The_i])/(P[j]-L[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]))+xA[The_i];
      y_e  = (yA[j]-yA[The_i])/(P[j]-L[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]))+yA[The_i];
      Metre_tmp.DefineApertureAlign(0.99999, a1_e, a2_e, a3_e, a4_e, x_e, y_e);
      TheSequence->push_back(Metre_tmp);
      count++;
      Metre_tmp.empty();
      //
      //cout<<"figa7"<<endl;
      // Fill other metres in between
      for (int k = 1; k < (int)(floor(P[j]-L[j])-floor(P[The_i]) ); k++){ 
	Metre_tmp.DefineApertureAlign(0.0, a1_e, a2_e, a3_e, a4_e, x_e, y_e);
	a1_e = (A1[j]-A1[The_i])/(P[j]-L[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]+(double)k))+A1[The_i];
	a2_e = (A2[j]-A2[The_i])/(P[j]-L[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]+(double)k))+A2[The_i];
	a3_e = (A3[j]-A3[The_i])/(P[j]-L[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]+(double)k))+A3[The_i];
	a4_e = (A4[j]-A4[The_i])/(P[j]-L[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]+(double)k))+A4[The_i];
	x_e  = (xA[j]-xA[The_i])/(P[j]-L[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]+(double)k))+xA[The_i];
	y_e  = (yA[j]-yA[The_i])/(P[j]-L[j]-P[The_i])*(1.0-P[The_i]+floor(P[The_i]+(double)k))+yA[The_i];
	Metre_tmp.DefineApertureAlign(0.99999, a1_e, a2_e, a3_e, a4_e, x_e, y_e);
	TheSequence->push_back(Metre_tmp);
	count++;
	Metre_tmp.empty();
      }
      // Metre in which the long element starts
      Metre_tmp.DefineApertureAlign(0.0, a1_e, a2_e, a3_e, a4_e, x_e, y_e);
      Metre_tmp.DefineApertureAlign(P[j]-L[j], A1[j], A2[j], A3[j], A4[j], xA[j], yA[j]);
      // All metres along the long element
      if ( floor(P[j]) == floor(P[j]-L[j]) ){
	Metre_tmp.DefineApertureAlign(P[j], A1[j], A2[j], A3[j], A4[j], xA[j], yA[j]);
	The_i = j;
      //cout<<"figa8"<<endl;
      } 
      else if ( floor(P[j]) > floor(P[j]-L[j]) ){
	Metre_tmp.DefineApertureAlign(0.99999, A1[j], A2[j], A3[j], A4[j], xA[j], yA[j]);
	TheSequence->push_back(Metre_tmp);
	count++;
	Metre_tmp.empty();
	for (int k = 1; k < (int)( floor(P[j]) - floor(P[j]-L[j]) ); k++){ 
	  Metre_tmp.DefineApertureAlign(0.0, A1[j], A2[j], A3[j], A4[j], xA[j], yA[j]);
	  Metre_tmp.DefineApertureAlign(0.99999, A1[j], A2[j], A3[j], A4[j], xA[j], yA[j]);
	  TheSequence->push_back(Metre_tmp);
	  count++;
	  Metre_tmp.empty();
	}
	Metre_tmp.DefineApertureAlign(0.0, A1[j], A2[j], A3[j], A4[j], xA[j], yA[j]);
	The_i = j;
      }
    }
    if ( ApertMod[j] != 0 ){
      P_end=P[j];  // Store these value: required to use the last define point with aperture
      a1_end=A1[j];
      a2_end=A2[j];
      a3_end=A3[j];
      a4_end=A4[j];
      x_end=yA[j];
      y_end=yA[j];
    }
  }
  // Always include the last point with aperture and close the corresponding metre!
  // This only works if the last point is a marker...
  // Not worth to write the code for the general case!
  //cout<<"figa9"<<endl;
  Metre_tmp.DefineApertureAlign(P_end, a1_end, a2_end, a3_end, a4_end, x_end, y_end);
  if (floor(P_end) == 26658.0)
    Metre_tmp.DefineApertureAlign(0.8832, a1_end, a2_end, a3_end, a4_end, x_end, y_end);
  else
    Metre_tmp.DefineApertureAlign(0.99999, a1_end, a2_end, a3_end, a4_end, x_end, y_end);
  TheSequence->push_back(Metre_tmp);
  count++;
  Metre_tmp.empty();
  cout<<TheSequence->size()<<endl;
  //
  // End of the sequence
  if ( (int)TheSequence->size() < 26659){
    for (int k = 1; k <=  26659 - (int)TheSequence->size(); k++){ 
      Metre_tmp.DefineApertureAlign(0.0, a1_end, a2_end, a3_end, a4_end, x_end, y_end);
      Metre_tmp.DefineApertureAlign(0.99999, a1_end, a2_end, a3_end, a4_end, x_end, y_end);
      TheSequence->push_back(Metre_tmp);
      count++;
      Metre_tmp.empty();
    }
    Metre_tmp.empty();
    Metre_tmp.DefineApertureAlign(0.0, a1_end, a2_end, a3_end, a4_end, x_end, y_end);
    if (floor(P_end) == 26658.0)
      Metre_tmp.DefineApertureAlign(P_end, a1_end, a2_end, a3_end, a4_end, x_end, y_end);
    Metre_tmp.DefineApertureAlign(0.8832, a1_end, a2_end, a3_end, a4_end, x_end, y_end);
    TheSequence->push_back(Metre_tmp);
    count++;
    Metre_tmp.empty();
  }
  cout<<endl<<"All aperture information has been read and ";
  cout<<"the sequence has been created!"<<endl<<endl;
}

void PlotSomeMetres(vector<OneMetre> TheSequence, double s1, double s2, string output)
{
  // check that s2 < (double) sequence.size()

  double pos;

  vector<double> position;
  vector<Aperture> aperture;
  
  if ( s1 > 1.0 )
    s1 = s1 - 1.0;
  if ( s2 < 26657.0 )
    s2 = s2 + 1.0;

  cout<<"Apertures between s1 = "<<s1<<" and s2 = "<<s2
      <<" are being saved in the file \""<<output<<"\""<<endl;

  ofstream out;
  out.precision(8); // At least this precision, otherwise not enough
                    // digits for the longitudinal coordinate s!!
  out.open(output.c_str());
  for (int i = (int) s1; i < (int) s2; i++){
    pos = double( i );
    position.clear();
    aperture.clear();
    TheSequence[i].GetApertDef(&position, &aperture);
    for( int j = 1; j < (int) position.size(); j++){ // Starts from 1 otherwise point at the extremities
      out<<setw(12)<<pos + position[j]               // of the metre are repeated twice
	 <<setw(12)<<aperture[j].GetApert(1)
	 <<setw(12)<<aperture[j].GetApert(2)
	 <<setw(12)<<aperture[j].GetApert(3)
	 <<setw(12)<<aperture[j].GetApert(4)<<endl;
    }
  }
  out.close();
}

void PlotAll(vector<OneMetre> TheSequence, string output)
{
  double pos;

  vector<double> position;
  vector<Aperture> aperture;
  
  cout<<"The aperture definitions of all the sequence "
      <<" are being saved in the file \""<<output<<"\""<<endl;

  ofstream out;
  out.precision(8);
  out.open(output.c_str());
  for (int i = 0; i < (int) TheSequence.size(); i++){
    pos = double( i );
    position.clear();
    aperture.clear();
    TheSequence[i].GetApertDef(&position, &aperture);
    for( int j = 0; j < (int) position.size(); j++){
      out<<setw(12)<<pos + position[j]
	 <<setw(12)<<aperture[j].GetApert(1)
	 <<setw(12)<<aperture[j].GetApert(2)
	 <<setw(12)<<aperture[j].GetApert(3)
	 <<setw(12)<<aperture[j].GetApert(4)<<endl;
    }
  }
  out.close();
}

void PlotSomeMetres(vector<OneMetre> TheSequence, double s1, double s2, double Ds, string output)
{
  if ( Ds > 1.0 ){
    cout<<"You have chosen a Ds larger than 1 metre!"<<endl;
    cout<<"Ds = 0.10 m will be chosen instead"<<endl;
    Ds = 0.10;
  }

  double pos;
  vector<double> position;
  vector<Aperture> aperture;
  
  if ( s1 > 1.0 )
    s1 = s1 - 1.0;
  if ( s2 < 26657.0 )
    s2 = s2 + 1.0;

  cout<<"Apertures between s1 = "<<s1<<" and s2 = "<<s2
      <<" are being saved in the file \""<<output<<"\""<<endl;

  ofstream out;
  out.open(output.c_str());
  out.precision(8);
  Aperture Atmp;
  for (int i = (int) s1; i < (int) s2; i++){
    for (int j = 0; j < (int) 1/Ds; j++){
      pos = double( j ) * Ds + (double) i;
      Atmp.empty();
      Atmp = TheSequence[i].GetAperture( pos );
      out<<setw(12)<<pos;
      out<<setw(12)<<Atmp.GetApert(1);
      out<<setw(12)<<Atmp.GetApert(2);
      out<<setw(12)<<Atmp.GetApert(3);
      out<<setw(12)<<Atmp.GetApert(4)<<endl;
    }
  }
  out.close();

  /*
  for (int i = (int) s1; i < (int) s2; i++){
    //    position.clear();
    //    aperture.clear();
    for (int j = 0; j < (int) 1/Ds; j++){
       pos = double( j ) * Ds + (double) i;
       position.push_back( pos );
       aperture.push_back( TheSequence[i].GetAperture( pos ) );
    }
  }
  ofstream out;
  out.open(output.c_str());
  for( int k = 0; k < (int) position.size(); k++){
    out<<setw(12)<<position[k]
       <<setw(12)<<aperture[k].GetApert(1)
       <<setw(12)<<aperture[k].GetApert(2)
       <<setw(12)<<aperture[k].GetApert(3)
       <<setw(12)<<aperture[k].GetApert(4)<<endl;
  }
  out.close();
  */
}

void PlotAll(vector<OneMetre> TheSequence, double Ds, string output)
{
  if ( Ds > 1.0 ){
    cout<<"You have chosen a a Ds smaller than 1 metre!"<<endl;
    cout<<"Ds = 0.10 m will be chosen instead"<<endl;
    Ds = 0.10;
  }

  double pos;
  vector<double> position;
  vector<Aperture> aperture;

  cout<<"The aperture definitions of all the sequence "
      <<" are being saved in the file \""<<output<<"\""<<endl;

  ofstream out;
  out.precision(8);
  out.open(output.c_str());
  for (int i = 0; i < (int) TheSequence.size(); i++){
    position.clear();
    aperture.clear();
    for (int j = 0; j < (int) 1/Ds; j++){
       pos = double( j ) * Ds + (double) i;
       position.push_back( pos );
       aperture.push_back( TheSequence[i].GetAperture( pos ) );
    }
    for( int k = 0; k < (int) position.size(); k++){
      out<<setw(12)<<position[k]
	 <<setw(12)<<aperture[k].GetApert(1)
	 <<setw(12)<<aperture[k].GetApert(2)
	 <<setw(12)<<aperture[k].GetApert(3)
	 <<setw(12)<<aperture[k].GetApert(4)<<endl;
    }
  }
  out.close();
}

