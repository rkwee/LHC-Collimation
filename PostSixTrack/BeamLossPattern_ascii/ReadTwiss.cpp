#include "ReadTwiss.h"

void ReadTwiss(string in, vector<string> *K, vector<string> *N, 
	       vector<string> *Pa, vector<string> *Kn, vector<string> *Nn, 
	       vector<string> *Pan, vector<double> *P, vector<double> *L, 
	       vector<double> *A1, vector<double> *A2, vector<double> *A3, 
	       vector<double> *A4)

{
  K->clear();
  N->clear();
  Pa->clear();
  P->clear();
  L->clear();
  A1->clear();
  A2->clear();
  A3->clear();
  A4->clear();
  
  char tK[256], tN[256], tT[256], tP[256], tL[256],
    tA1[256], tA2[256], tA3[256], tA4[256];

  char chr_tmp[256];
  string str_tmp;

  int len;
  ostringstream ost;

  ifstream InputFile(in.c_str());

  while (InputFile.getline(chr_tmp,256)){
    str_tmp = chr_tmp;
    if (str_tmp.find("KEYWORD",0) != string::npos){
      InputFile.getline(chr_tmp,256);
      break;
    }
  }
  while (InputFile.getline(chr_tmp,256)){
    sscanf(chr_tmp,"%s%s%s%s%s%s%s%s%s",tK,tN,tT,tP,tL,tA1,tA2,tA3,tA4);
    //
    K->push_back(tK);
    N->push_back(tN);
    Pa->push_back(tT);
    P->push_back(atof(tP));
    L->push_back(atof(tL));
    A1->push_back(atof(tA1));
    A2->push_back(atof(tA2));
    A3->push_back(atof(tA3));
    A4->push_back(atof(tA4));
    // 
    // Element names without quotes
    ost.str("");
    len=(int)strlen(tK);
    for (int i = 1; i < len-1; i++)
      ost<<tK[i];
    Kn->push_back(ost.str());
    ost.str("");
    len=(int)strlen(tN);
    for (int i = 1; i < len-1; i++)
      ost<<tN[i];
    Nn->push_back(ost.str());
    ost.str("");
    len=(int)strlen(tT);
    for (int i = 1; i < len-1; i++)
      ost<<tT[i];
    Pan->push_back(ost.str());

  }
  InputFile.close();

  cout<<endl;
  cout<<"Reading from \""<<in<<"\""<<endl;
  cout<<"Total number of read elements: "<<K->size()<<endl;
  cout<<endl;

}

void ReadTwissNoDrifts(string in, vector<string> *K, vector<string> *N, 
		       vector<string> *Pa, vector<string> *Kn, vector<string> *Nn, 
		       vector<string> *Pan, vector<double> *P, vector<double> *L, 
		       vector<double> *A1, vector<double> *A2, vector<double> *A3, 
		       vector<double> *A4)

{
  K->clear();
  N->clear();
  Pa->clear();
  P->clear();
  L->clear();
  A1->clear();
  A2->clear();
  A3->clear();
  A4->clear();
  
  char tK[256], tN[256], tT[256], tP[256], tL[256],
    tA1[256], tA2[256], tA3[256], tA4[256];

  char chr_tmp[256];
  string str_tmp;

  int len;
  ostringstream ost;

  ifstream InputFile(in.c_str());

  while (InputFile.getline(chr_tmp,256)){
    str_tmp = chr_tmp;
    if (str_tmp.find("KEYWORD",0) != string::npos){
      InputFile.getline(chr_tmp,256);
      break;
    }
  }
  while (InputFile.getline(chr_tmp,256)){
    sscanf(chr_tmp,"%s%s%s%s%s%s%s%s%s",tK,tN,tT,tP,tL,tA1,tA2,tA3,tA4);
    //
    str_tmp = tK;
    if ( str_tmp.find("DRIFT",0) == string::npos ){
      K->push_back(tK);
      N->push_back(tN);
      Pa->push_back(tT);
      P->push_back(atof(tP));
      L->push_back(atof(tL));
      A1->push_back(atof(tA1));
      A2->push_back(atof(tA2));
      A3->push_back(atof(tA3));
      A4->push_back(atof(tA4));
    }
    // 
    // Element names without quotes
    ost.str("");
    len=(int)strlen(tK);
    for (int i = 1; i < len-1; i++)
      ost<<tK[i];
    Kn->push_back(ost.str());
    ost.str("");
    len=(int)strlen(tN);
    for (int i = 1; i < len-1; i++)
      ost<<tN[i];
    Nn->push_back(ost.str());
    ost.str("");
    len=(int)strlen(tT);
    for (int i = 1; i < len-1; i++)
      ost<<tT[i];
    Pan->push_back(ost.str());

  }
  InputFile.close();

  cout<<endl;
  cout<<"Reading from \""<<in<<"\""<<endl;
  cout<<"Total number of read elements: "<<K->size()<<endl;
  cout<<endl;

}


void ReadTwissK(string in, vector<string> *K, vector<string> *N, 
		vector<string> *Pa, vector<string> *Kn, vector<string> *Nn, 
		vector<string> *Pan, vector<double> *P, vector<double> *L, 
		vector<double> *KL, vector<double> *A1, vector<double> *A2, 
		vector<double> *A3, vector<double> *A4)
{
  K->clear();
  N->clear();
  Pa->clear();
  P->clear();
  L->clear();
  KL->clear();
  A1->clear();
  A2->clear();
  A3->clear();
  A4->clear();

  char tK[256], tN[256], tT[256], tP[256], tL[256], tKL[256],
    tA1[256], tA2[256], tA3[256], tA4[256];

  char chr_tmp[256];
  string str_tmp;

  int len;
  ostringstream ost;

  ifstream InputFile(in.c_str());

  while (InputFile.getline(chr_tmp,256)){
    str_tmp = chr_tmp;
    if (str_tmp.find("KEYWORD",0) != string::npos){
      InputFile.getline(chr_tmp,256);
      break;
    }
  }
  while (InputFile.getline(chr_tmp,256)){
    sscanf(chr_tmp,"%s%s%s%s%s%s%s%s%s%s",tK,tN,tT,tP,tL,tKL,tA1,tA2,tA3,tA4);
    //
    K->push_back(tK);
    N->push_back(tN);
    Pa->push_back(tT);
    P->push_back(atof(tP));
    L->push_back(atof(tL));
    KL->push_back(atof(tKL));
    A1->push_back(atof(tA1));
    A2->push_back(atof(tA2));
    A3->push_back(atof(tA3));
    A4->push_back(atof(tA4));
    // 
    // Element names without quotes
    ost.str("");
    len=(int)strlen(tK);
    for (int i = 1; i < len-1; i++)
      ost<<tK[i];
    Kn->push_back(ost.str());
    ost.str("");
    len=(int)strlen(tN);
    for (int i = 1; i < len-1; i++)
      ost<<tN[i];
    Nn->push_back(ost.str());
    ost.str("");
    len=(int)strlen(tT);
    for (int i = 1; i < len-1; i++)
      ost<<tT[i];
    Pan->push_back(ost.str());

  }
  InputFile.close();

  cout<<endl;
  cout<<"Reading from \""<<in<<"\""<<endl;
  cout<<"Total number of read elements: "<<K->size()<<endl;
  cout<<endl;

}

void ReadTwissDX(string in, vector<string> *K, vector<string> *N, vector<string> *Pa, 
		 vector<string> *Kn, vector<string> *Nn, vector<string> *Pan, 
		 vector<double> *P, vector<double> *L, vector<double> *A1, 
		 vector<double> *A2, vector<double> *A3, vector<double> *A4, 
		 vector<double> *DX, vector<double> *DY)
{
  K->clear();
  N->clear();
  Pa->clear();
  P->clear();
  L->clear();
  A1->clear();
  A2->clear();
  A3->clear();
  A4->clear();
  DX->clear();
  DY->clear();

  char tK[256], tN[256], tT[256], tP[256], tL[256],
    tA1[256], tA2[256], tA3[256], tA4[256], tDX[256], tDY[256];

  char chr_tmp[256];
  string str_tmp;

  int len;
  ostringstream ost;

  ifstream InputFile(in.c_str());

  while (InputFile.getline(chr_tmp,256)){
    str_tmp = chr_tmp;
    if (str_tmp.find("KEYWORD",0) != string::npos){
      InputFile.getline(chr_tmp,256);
      break;
    }
  }
  while (InputFile.getline(chr_tmp,256)){
    sscanf(chr_tmp,"%s%s%s%s%s%s%s%s%s%s%s",tK,tN,tT,tP,tL,tA1,tA2,tA3,tA4,tDX,tDY);
    //
    str_tmp = tK;
    K->push_back(tK);
    N->push_back(tN);
    Pa->push_back(tT);
    P->push_back(atof(tP));
    L->push_back(atof(tL));
    A1->push_back(atof(tA1));
    A2->push_back(atof(tA2));
    A3->push_back(atof(tA3));
    A4->push_back(atof(tA4));
    DX->push_back(atof(tDX));
    DY->push_back(atof(tDY));
    // 
    // Element names without quotes
    ost.str("");
    len=(int)strlen(tK);
    for (int i = 1; i < len-1; i++)
      ost<<tK[i];
    Kn->push_back(ost.str());
    ost.str("");
    len=(int)strlen(tN);
    for (int i = 1; i < len-1; i++)
      ost<<tN[i];
    Nn->push_back(ost.str());
    ost.str("");
    len=(int)strlen(tT);
    for (int i = 1; i < len-1; i++)
      ost<<tT[i];
    Pan->push_back(ost.str());

  }
  InputFile.close();

  cout<<endl;
  cout<<"Reading from \""<<in<<"\""<<endl;
  cout<<"Total number of read elements: "<<K->size()<<endl;
  cout<<endl;
}

void ReadTwissDXNoDrifts(string in, vector<string> *K, vector<string> *N, vector<string> *Pa, 
			 vector<string> *Kn, vector<string> *Nn, vector<string> *Pan, 
			 vector<double> *P, vector<double> *L, vector<double> *A1, 
			 vector<double> *A2, vector<double> *A3, vector<double> *A4, 
			 vector<double> *DX, vector<double> *DY)
{
  K->clear();
  N->clear();
  Pa->clear();
  P->clear();
  L->clear();
  A1->clear();
  A2->clear();
  A3->clear();
  A4->clear();
  DX->clear();
  DY->clear();

  char tK[256], tN[256], tT[256], tP[256], tL[256],
    tA1[256], tA2[256], tA3[256], tA4[256], tDX[256], tDY[256];

  char chr_tmp[256];
  string str_tmp;

  int len;
  ostringstream ost;

  ifstream InputFile(in.c_str());

  while (InputFile.getline(chr_tmp,256)){
    str_tmp = chr_tmp;
    if (str_tmp.find("KEYWORD",0) != string::npos){
      InputFile.getline(chr_tmp,256);
      break;
    }
  }
  while (InputFile.getline(chr_tmp,256)){
    sscanf(chr_tmp,"%s%s%s%s%s%s%s%s%s%s%s",tK,tN,tT,tP,tL,tA1,tA2,tA3,tA4,tDX,tDY);
    //
    str_tmp = tK;
    if ( str_tmp.find("DRIFT",0) == string::npos ){
      K->push_back(tK);
      N->push_back(tN);
      Pa->push_back(tT);
      P->push_back(atof(tP));
      L->push_back(atof(tL));
      A1->push_back(atof(tA1));
      A2->push_back(atof(tA2));
      A3->push_back(atof(tA3));
      A4->push_back(atof(tA4));
      DX->push_back(atof(tDX));
      DY->push_back(atof(tDY));
    }
    // 
    // Element names without quotes
    ost.str("");
    len=(int)strlen(tK);
    for (int i = 1; i < len-1; i++)
      ost<<tK[i];
    Kn->push_back(ost.str());
    ost.str("");
    len=(int)strlen(tN);
    for (int i = 1; i < len-1; i++)
      ost<<tN[i];
    Nn->push_back(ost.str());
    ost.str("");
    len=(int)strlen(tT);
    for (int i = 1; i < len-1; i++)
      ost<<tT[i];
    Pan->push_back(ost.str());

  }
  InputFile.close();

  cout<<endl;
  cout<<"Reading from \""<<in<<"\""<<endl;
  cout<<"Total number of read elements: "<<K->size()<<endl;
  cout<<endl;
}
