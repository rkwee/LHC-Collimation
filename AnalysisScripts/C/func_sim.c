#include"func_sim.h"

Float_t *normalization(TTree *tr,Long64_t n,Float_t *sci,Int_t tmin,Int_t tmax){

  Int_t dim=tmax-tmin;

  Float_t b[dim];
  Float_t be;
  Int_t time;
  Int_t i;
  Float_t *norm;

  norm=(Float_t *)malloc(dim*sizeof(Float_t));

  tr->SetBranchAddress("t",&time);
  tr->SetBranchAddress("beam_low",&be);

  Int_t j=0;
	
	Float_t b_temp=0.0;

  for(i=0;i<n;i++){

    tr->GetEntry(i);

    if(time>=tmin && time<tmax){
      b[j]=be;
		
      if(b[j]>0.0)
	b_temp=b[j];
		
      if(b[j]<0.0)
	b[j]=b_temp;
		
      j+=1;
    
    }

  }

  TH1F *ints=new TH1F("ints","intensity",dim,0,dim);

  for(i=0;i<dim;i++)
    ints->SetBinContent(i,b[i]);

  ints->Draw();
  
  
  TF1 * fitfunc = new TF1("fitfunc","[0]+[1]*x + [2]*TMath::Power(x,2) + [3]*TMath::Power(x,3)",tmin,tmax);

  ints->Fit(fitfunc);
  
  for(i=0;i<dim;i++)
    norm[i]=sci[i]/fitfunc->Eval(i);

  return norm;

}

/*-----------------------------------------------------------*/


Float_t *normalization_f(TTree *tr,Long64_t n,Float_t *sci,Int_t tmin,Int_t tmax){

  Int_t dim=tmax-tmin;

  Float_t b[dim];
  Float_t be;
  Int_t time;
  Int_t i;
  Float_t *norm;

  norm=(Float_t *)malloc(dim*sizeof(Float_t));

  tr->SetBranchAddress("t",&time);
  tr->SetBranchAddress("beam_low",&be);

  Int_t j=0;

	Float_t b_temp;
	
  for(i=0;i<n;i++){

    tr->GetEntry(i);

    if(time>tmin && time<=tmax){
      b[j]=be;
		
		
      if(b[j]>0.0)
	b_temp=b[j];
		
      if(b[j]<0.0)
	b[j]=b_temp;
		
      j+=1;

    }

  }

  TH1F *ints=new TH1F("ints","intensity",dim,0,dim);

  for(i=0;i<dim;i++)
    ints->SetBinContent(i,b[i]);

  ints->Draw();
  
  
  TF1 * fitfunc = new TF1("fitfunc","[0]+[1]*x + [2]*TMath::Power(x,2) + [3]*TMath::Power(x,3)",tmin,tmax);

  ints->Fit(fitfunc);
  
  for(i=0;i<dim;i++)
    norm[i]=sci[i]/(-fitfunc->Derivative(i));
  
  return norm;

}

/*-----------------------------------------------------------*/

Int_t count_line(char *filename){

  char line[1000000];
  Int_t i=0;
  FILE *ptr;

  ptr=fopen(filename,"r");

  while( fgets(line,sizeof(line),ptr) != '\0' )
    i++;

  fclose(ptr);

  return i;

}



/*-----------------------------------------------------------*/

void extr_var_float(char *filename,Int_t dim,Float_t *var,Int_t col, Int_t nh){   //col = colonna da prendere, nh = n linee di header

  FILE *ptr;
  char *field;
  char line[100000];
  Int_t i;
  Int_t j;

  ptr=fopen(filename,"r");

  for(i=0;i<nh;i++)
    fgets(line,sizeof(line),ptr);

  for(i=0;i<dim-nh;i++){

    fgets(line,sizeof(line),ptr);

    for(j=1;j<=col;j++){

      if(j==1)
	field = strtok(line," ");
      else
	field = strtok(NULL," ");

      if(j==col)
	var[i]=atof(field);

    }

  }

  fclose(ptr);

}


/*-----------------------------------------------*/

void extr_var_int(char *filename,Int_t dim,Int_t *var,Int_t col, Int_t nh){   //col = colonna da prendere, nh = n linee di header

  FILE *ptr;
  char *field;
  char line[100000];
  Int_t i;
  Int_t j;

  ptr=fopen(filename,"r");

  for(i=0;i<nh;i++)
    fgets(line,sizeof(line),ptr);

  for(i=0;i<dim-nh;i++){

    fgets(line,sizeof(line),ptr);

    for(j=1;j<=col;j++){

      if(j==1)
	field = strtok(line," ");
      else
	field = strtok(NULL," ");

      if(j==col)
	var[i]=atoi(field);

    }

  }

  fclose(ptr);

}

/*-----------------------------------------------*/

void extr_names(char *filename,Int_t dim,char **var,Int_t col, Int_t nh){   //col = colonna da prendere, nh = n linee di header

  FILE *ptr;
  char *field;
  char line[100000];
  Int_t i;
  Int_t j,k;

  field=(char *)malloc(sizeof(var[0])*sizeof(char));

  ptr=fopen(filename,"r");

  for(i=0;i<nh;i++)
    fgets(line,sizeof(line),ptr);

  for(i=0;i<dim-nh;i++){

    fgets(line,sizeof(line),ptr);

    for(j=1;j<=col;j++){

      if(j==1)
	field = strtok(line," ");
      else
	field = strtok(NULL," ");

      if(j==col)
	strcpy(var[i],field);
      
    }

  }

  fclose(ptr);

}

/*-----------------------------------------------*/
/*
void plot_coll_summary(void){

  char* filename;
  Int_t nhead,dim,i;
  char **names;
  Int_t *nimp,*nabs,*imp_av,*imp_sig;

  filename="coll_summary.dat";
  nhead=1;

  dim=count_line(filename);

  names=(char **)malloc((dim-nhead)*sizeof(char *));

  for(i=0;i<dim-nhead;i++)
    names[i]=(char *)malloc(100*sizeof(char));

  nimp=(Int_t *)malloc((dim-nhead)*sizeof(Int_t));
  nabs=(Int_t *)malloc((dim-nhead)*sizeof(Int_t));
  imp_av=(Int_t *)malloc((dim-nhead)*sizeof(Int_t));
  imp_sig=(Int_t *)malloc((dim-nhead)*sizeof(Int_t));

  extr_names(filename,dim,names,2,nhead);
  extr_var_int(filename,dim,nimp,3,nhead);
  extr_var_int(filename,dim,nabs,4,nhead);
  extr_var_int(filename,dim,imp_av,5,nhead);
  extr_var_int(filename,dim,imp_sig,6,nhead);

 /*-------------------*/
/*
  TCanvas *c1 = new TCanvas("c1","number of impacts",1);

  c1->cd();
  
  TPad *padc1 = new TPad("padc1","",0,0,1,1);

  padc1->SetFillColor(10);

  padc1->Draw();

  padc1->cd();

  gStyle->SetOptStat(kFALSE);
  gStyle->SetOptTitle(kFALSE);  

  TH1I *imp=new TH1I("imp","number of impacts",dim-nhead,0,dim-nhead);

  imp->SetFillColor(2);

  for(i=0;i<dim-nhead;i++){
    imp->SetBinContent(i,nimp[i]);
    imp->GetXaxis()->SetBinLabel(i,names[i]);
  }

  imp->Draw();

  /*--------------------------*/
/*
  for(i=0;i<dim-nhead;i++)
    free(names[i]);

  free(names);
  free(nimp);
  free(nabs);
  free(imp_av);
  free(imp_sig);

}
*/
