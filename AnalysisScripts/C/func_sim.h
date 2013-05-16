#include <iostream>
#include <string>
#include "TNtuple.h"
#include "TFile.h"
#include "TTree.h"
#include <fstream>
#include <TROOT.h>
#include "TH1D.h"
#include <TStyle.h>
#include "TGaxis.h"
#include "TCanvas.h"
#include "vector"
#include "TProfile.h"
#include "time.h"
#include <TGraph.h>
#include <TF1.h>
#include "stdlib.h"
#include "TSystem.h"
#include <vector>
#include <fstream>
#include "TLine.h"
#include "TEllipse.h"
#include "TGraphErrors.h"
#include "TGraphAsymmErrors.h"
#include "TCanvas.h"
#include "TFrame.h"
#include "TPad.h"
#include "TF1.h"
#include "TH1.h"
#include "TH2.h"
#include "TPolyLine.h"
#include "TProfile.h"
#include "TLegend.h"
#include "TLegendEntry.h"
#include "TLatex.h"
#include "TPaveStats.h"
#include "TStyle.h"
#include "TROOT.h"
#include "TMath.h"
#include "THStack.h"
#include "TSystem.h"
#include "TBenchmark.h"


using namespace std;

Float_t *normalization(TTree *tr,Long64_t n,Int_t *sci,Int_t tmin,Int_t tmax);
Float_t *normalization_f(TTree *tr,Long64_t n,Float_t *sci,Int_t tmin,Int_t tmax);

Int_t count_line(char *filename);
void extr_var_float(char *filename,Int_t dim,Float_t *var,Int_t col, Int_t nh);
void extr_var_int(char *filename,Int_t dim,Int_t *var,Int_t col, Int_t nh);
void extr_names(char *filename,Int_t dim,char **var,Int_t col, Int_t nh);
//void plot_coll_summary(void);
