#include"func_sim.h"
#include"func_sim.c"

void loss_map(){

  char* filename;
  Int_t nhead,dim,i,j,k, kval;
  Float_t *losses;

  /*------------*/

  Int_t n_warm=94;

  Float_t warm[94]={0.0,22.5365,54.853,152.489,172.1655,192.39999999999998,199.48469999999998,224.3,3095.454284,3155.628584,3167.740084,3188.4330840000002,3211.4445840000003,3263.867584,3309.9000840000003,3354.9740840000004,3401.005584,3453.4285840000002,3476.440084,3494.065584,3505.885284,3568.318584,6405.4088,6457.9138,6468.7785,6859.513800000001,6870.3785,6923.5338,9735.907016000001,9824.730516000001,9830.832016,9861.730516,9878.732016,9939.985516,9950.548016,10043.462016,10054.024516,10115.278016,10132.279516,10163.970516,10170.072016,10257.603016,13104.989233,13129.804533,13136.889233,13157.123733,13176.800233,13271.647233,13306.752733,13351.825733,13386.931233000001,13481.778233000001,13501.454732999999,13522.784533,13529.869233,13554.684533,16394.637816,16450.871316,16456.972816,16487.271316000002,16493.372816,16830.871316,16836.972815999998,16867.271316,16873.372816,16928.294816,19734.8504,19760.6997,19771.5644,20217.9087,20228.773400000002,20252.9744,23089.979683999998,23138.576984,23150.396684,23171.375484,23194.386984,23246.809984,23292.842484,23337.915484,23383.947984,23436.370984,23459.382483999998,23480.082484,23492.193984,23553.115984,26433.4879,26458.3032,26465.387899999998,26486.7177,26506.3942,26601.2412,26636.346700000002,26658.883199999997};




  /*-----------------*/

  filename="LPI_BLP_out.s";
  nhead=0;

  dim=count_line(filename);

  losses=(Float_t *)malloc((dim-nhead)*sizeof(Float_t));

  extr_var_float(filename,dim,losses,3,nhead);


  /*---------------*/

  char* filename_c_s,*filename_c_p,*filename_f_i;
  Int_t nhead_c_s,dim_c_s,nhead_c_p,dim_c_p,dim_f_i,nhead_f_i;
  char **names_c_s,**names_c_p;
  Int_t *nabs;
  Float_t *pos,*length;
  
  filename_c_s="coll_summary.dat";
  nhead_c_s=1;

  dim_c_s=count_line(filename_c_s);



  names_c_s=(char **)malloc((dim_c_s-nhead_c_s)*sizeof(char *));

  for(i=0;i<dim_c_s-nhead_c_s;i++)
    names_c_s[i]=(char *)malloc(100*sizeof(char));

  nabs=(Int_t *)malloc((dim_c_s-nhead_c_s)*sizeof(Int_t));

  length=(Float_t *)malloc((dim_c_s-nhead_c_s)*sizeof(Float_t));


  extr_names(filename_c_s,dim_c_s,names_c_s,2,nhead_c_s);
  extr_var_int(filename_c_s,dim_c_s,nabs,4,nhead_c_s);
  extr_var_float(filename_c_s,dim_c_s,length,7,nhead_c_s);

  
  filename_c_p="CollPositions.b1.dat";
  nhead_c_p=1;

  dim_c_p=count_line(filename_c_p);

  names_c_p=(char **)malloc((dim_c_p-nhead_c_p)*sizeof(char *));

  for(i=0;i<dim_c_p-nhead_c_p;i++)
    names_c_p[i]=(char *)malloc(100*sizeof(char));

  pos=(Float_t *)malloc((dim_c_p-nhead_c_p)*sizeof(Float_t));

  extr_names(filename_c_p,dim_c_p,names_c_p,2,nhead_c_p);
  extr_var_float(filename_c_p,dim_c_p,pos,3,nhead_c_p);


  filename_f_i="FirstImpacts.dat";
  nhead_f_i=1;

  dim_f_i=count_line(filename_f_i);

  //Int_t norm_f_i=dim_f_i-dim_f_i;

  /*----------------------*/


  TCanvas *los = new TCanvas("los","LHC loss map",1);

  los->cd();
  
  TPad *pad_l = new TPad("pad_l","",0,0,1,1);

  pad_l->SetFillColor(10);

  pad_l->Draw();

  pad_l->cd();

  gStyle->SetOptStat(kFALSE);
  gStyle->SetOptTitle(kFALSE);  

  TH1F *warm_loss=new TH1F("warm_loss","warm loss map",26659/0.1,0,26659);
  warm_loss->SetFillColor(2);
  warm_loss->SetLineColor(2);


  TH1F *cold_loss=new TH1F("cold_loss","cold loss map",26659/0.1,0,26659);
  cold_loss->SetFillColor(4);
  cold_loss->SetLineColor(4);

  TH1F *coll_loss=new TH1F("coll_loss","coll loss map",26659/0.1,0,26659);
  coll_loss->SetFillColor(12);
  coll_loss->SetLineColor(12);


  for(j=0;j<10;j++){
    for(i=0;i<dim-nhead;i++){
      for(k=0;k<n_warm;k+=2){

	if(losses[i] >= warm[k] && losses[i] <= warm[k+1])
	  warm_loss->Fill(losses[i]);
	if(k<n_warm-1 && losses[i] >= warm[k+1] && losses[i] <= warm[k+2])
	  cold_loss->Fill(losses[i]);
      }
    }
  }
  
  for(i=0;i<dim_c_s-nhead_c_s;i++){
    for(j=0;j<dim_c_p-nhead_c_p;j++){

      if(strcmp(names_c_s[i],names_c_p[j])==0){

	kval = (Int_t)(nabs[i]/length[i]);

	//	cout << "kval =" << kval << "nabs["<< i<< "] = " << nabs[i] << "length[i] = " << length[i] << endl;

	for(k=0;k<kval;k++)
	  //for(k=0;k<nabs[i];k++)
	  coll_loss->Fill(pos[j]);

      }

    }
  }

  pad_l->SetLogy(1);
  pad_l->SetGridy(1);

  Float_t max;
 
  max=dim_f_i-nhead_f_i;

  coll_loss->Scale(1.0/max);
  coll_loss->GetXaxis()->SetLabelFont(132);
  coll_loss->GetYaxis()->SetLabelFont(132);
  coll_loss->GetYaxis()->SetRangeUser(1.0e-7,5.0);
  coll_loss->GetXaxis()->SetTitleFont(132);
  coll_loss->GetYaxis()->SetTitleFont(132);
  coll_loss->GetXaxis()->SetTitle("s [m]");
  coll_loss->GetYaxis()->SetTitle("losses (#frac{n}{n_{T} length}) [1/m]");
  coll_loss->Draw();


  warm_loss->Scale(1.0/max);
  warm_loss->Draw("same");


  cold_loss->Scale(1.0/max);
  cold_loss->Draw("same");

  TLegend *leg = new TLegend(0.8,0.8,0.95,0.95);
  leg->SetHeader("LHC Loss Map");
  leg->AddEntry(coll_loss,"Collimator losses","l");
  leg->AddEntry(warm_loss,"Warm losses","l");
  leg->AddEntry(cold_loss,"Cold losses","l");

  leg->SetFillColor(10);
  leg->SetTextFont(132);

  leg->Draw();

  los->Print("/afs/cern.ch/user/r/rkwee/public/www/HL-LHC/losses_example_01.png");

  /*---------------*/

  TCanvas *ld = new TCanvas("ld","LHC loss map divided",1);

  ld->cd();
  ld->SetFillColor(10);

  TPad *pad_ld = new TPad("pad_ld","",0,0,1,1);

  pad_ld->SetFillColor(10);

  pad_ld->Draw();

  pad_ld->Divide(2,4);

  gStyle->SetOptStat(kFALSE);
  gStyle->SetOptTitle(kFALSE);

  pad_ld->cd(1);  
  
  TH1F *warm_loss1=new TH1F("warm_loss1","warm loss map IP1-IP2",3332.44/0.1,0,3332.44);
  warm_loss1->SetFillColor(2);
  warm_loss1->SetLineColor(2);


  TH1F *cold_loss1=new TH1F("cold_loss1","cold loss map IP1-IP2",3332.44/0.1,0,3332.44);
  cold_loss1->SetFillColor(4);
  cold_loss1->SetLineColor(4);

  TH1F *coll_loss1=new TH1F("coll_loss1","coll loss map IP1-IP2",3332.44/0.1,0,3332.44);
  coll_loss1->SetFillColor(12);
  coll_loss1->SetLineColor(12);


  for(j=0;j<10;j++){
    for(i=0;i<dim-nhead;i++){
      for(k=0;k<n_warm;k+=2){

	if(losses[i] >= warm[k] && losses[i] <= warm[k+1])
	  warm_loss1->Fill(losses[i]);
	if(k<n_warm-1 && losses[i] >= warm[k+1] && losses[i] <= warm[k+2])
	  cold_loss1->Fill(losses[i]);
      }
    }
  }
  
  for(i=0;i<dim_c_s-nhead_c_s;i++){
    for(j=0;j<dim_c_p-nhead_c_p;j++){

      if(strcmp(names_c_s[i],names_c_p[j])==0){

	for(k=0;k<(Int_t)(nabs[i]/length[i]);k++)
	  //for(k=0;k<nabs[i];k++)
	  coll_loss1->Fill(pos[j]);

      }

    }
  }

  pad_ld->cd(1)->SetLogy(1);
  pad_ld->cd(1)->SetGridy(1);
  
  coll_loss1->Scale(1.0/max);
  coll_loss1->GetXaxis()->SetLabelFont(132);
  coll_loss1->GetYaxis()->SetLabelFont(132);
  coll_loss1->GetYaxis()->SetRangeUser(1.0e-7,5.0);
  coll_loss1->GetXaxis()->SetTitleFont(132);
  coll_loss1->GetYaxis()->SetTitleFont(132);
  coll_loss1->GetXaxis()->SetTitle("s [m]");
  coll_loss1->GetYaxis()->SetTitle("losses (#frac{n}{n_{T} length}) [1/m]");
  coll_loss1->Draw();


  warm_loss1->Scale(1.0/max);
  warm_loss1->Draw("same");


  cold_loss1->Scale(1.0/max);
  cold_loss1->Draw("same");

  TLegend *leg1 = new TLegend(0.8,0.8,0.95,0.95);
  leg1->SetHeader("LHC Loss Map IP1-IP2");
  leg1->AddEntry(coll_loss,"Collimator losses","l");
  leg1->AddEntry(warm_loss,"Warm losses","l");
  leg1->AddEntry(cold_loss,"Cold losses","l");

  leg1->SetFillColor(10);
  leg1->SetTextFont(132);

  leg1->Draw();

  /*---------------*/

  pad_ld->cd(2);  
  
  TH1F *warm_loss2=new TH1F("warm_loss2","warm loss map IP2-IP3",(6664.72-3332.44)/0.1,3332.44,6664.72);
  warm_loss2->SetFillColor(2);
  warm_loss2->SetLineColor(2);


  TH1F *cold_loss2=new TH1F("cold_loss2","cold loss map IP2-IP3",(6664.72-3332.44)/0.1,3332.44,6664.72);
  cold_loss2->SetFillColor(4);
  cold_loss2->SetLineColor(4);

  TH1F *coll_loss2=new TH1F("coll_loss2","coll loss map IP2-IP3",(6664.72-3332.44)/0.1,3332.44,6664.72);
  coll_loss2->SetFillColor(12);
  coll_loss2->SetLineColor(12);


  for(j=0;j<10;j++){
    for(i=0;i<dim-nhead;i++){
      for(k=0;k<n_warm;k+=2){

	if(losses[i] >= warm[k] && losses[i] <= warm[k+1])
	  warm_loss2->Fill(losses[i]);
	if(k<n_warm-1 && losses[i] >= warm[k+1] && losses[i] <= warm[k+2])
	  cold_loss2->Fill(losses[i]);
      }
    }
  }
  
  for(i=0;i<dim_c_s-nhead_c_s;i++){
    for(j=0;j<dim_c_p-nhead_c_p;j++){

      if(strcmp(names_c_s[i],names_c_p[j])==0){

	for(k=0;k<(Int_t)(nabs[i]/length[i]);k++)
	  //for(k=0;k<nabs[i];k++)
	  coll_loss2->Fill(pos[j]);

      }

    }
  }

  pad_ld->cd(2)->SetLogy(1);
  pad_ld->cd(2)->SetGridy(1);
  
  coll_loss2->Scale(1.0/max);
  coll_loss2->GetXaxis()->SetLabelFont(132);
  coll_loss2->GetYaxis()->SetLabelFont(132);
  coll_loss2->GetYaxis()->SetRangeUser(1.0e-7,5.0);
  coll_loss2->GetXaxis()->SetTitleFont(132);
  coll_loss2->GetYaxis()->SetTitleFont(132);
  coll_loss2->GetXaxis()->SetTitle("s [m]");
  coll_loss2->GetYaxis()->SetTitle("losses (#frac{n}{n_{T} length}) [1/m]");
  coll_loss2->Draw();


  warm_loss2->Scale(1.0/max);
  warm_loss2->Draw("same");


  cold_loss2->Scale(1.0/max);
  cold_loss2->Draw("same");

  TLegend *leg2 = new TLegend(0.8,0.8,0.95,0.95);
  leg2->SetHeader("LHC Loss Map IP2-IP3");
  leg2->AddEntry(coll_loss,"Collimator losses","l");
  leg2->AddEntry(warm_loss,"Warm losses","l");
  leg2->AddEntry(cold_loss,"Cold losses","l");

  leg2->SetFillColor(10);
  leg2->SetTextFont(132);

  leg2->Draw();

  /*---------------*/

  pad_ld->cd(3);  
  
  TH1F *warm_loss3=new TH1F("warm_loss3","warm loss map IP3-IP4",(9997.0-6664.72)/0.1,6664.72,9997.0);
  warm_loss3->SetFillColor(2);
  warm_loss3->SetLineColor(2);


  TH1F *cold_loss3=new TH1F("cold_loss3","cold loss map IP3-IP4",(9997.0-6664.72)/0.1,6664.72,9997.0);
  cold_loss3->SetFillColor(4);
  cold_loss3->SetLineColor(4);

  TH1F *coll_loss3=new TH1F("coll_loss3","coll loss map IP3-IP4",(9997.0-6664.72)/0.1,6664.72,9997.0);
  coll_loss3->SetFillColor(12);
  coll_loss3->SetLineColor(12);


  for(j=0;j<10;j++){
    for(i=0;i<dim-nhead;i++){
      for(k=0;k<n_warm;k+=2){

	if(losses[i] >= warm[k] && losses[i] <= warm[k+1])
	  warm_loss3->Fill(losses[i]);
	if(k<n_warm-1 && losses[i] >= warm[k+1] && losses[i] <= warm[k+2])
	  cold_loss3->Fill(losses[i]);
      }
    }
  }
  
  for(i=0;i<dim_c_s-nhead_c_s;i++){
    for(j=0;j<dim_c_p-nhead_c_p;j++){

      if(strcmp(names_c_s[i],names_c_p[j])==0){

	for(k=0;k<(Int_t)(nabs[i]/length[i]);k++)
	  //for(k=0;k<nabs[i];k++)
	  coll_loss3->Fill(pos[j]);

      }

    }
  }

  pad_ld->cd(3)->SetLogy(1);
  pad_ld->cd(3)->SetGridy(1);
  
  coll_loss3->Scale(1.0/max);
  coll_loss3->GetXaxis()->SetLabelFont(132);
  coll_loss3->GetYaxis()->SetLabelFont(132);
  coll_loss3->GetYaxis()->SetRangeUser(1.0e-7,5.0);
  coll_loss3->GetXaxis()->SetTitleFont(132);
  coll_loss3->GetYaxis()->SetTitleFont(132);
  coll_loss3->GetXaxis()->SetTitle("s [m]");
  coll_loss3->GetYaxis()->SetTitle("losses (#frac{n}{n_{T} length}) [1/m]");
  coll_loss3->Draw();


  warm_loss3->Scale(1.0/max);
  warm_loss3->Draw("same");


  cold_loss3->Scale(1.0/max);
  cold_loss3->Draw("same");

  TLegend *leg3 = new TLegend(0.8,0.8,0.95,0.95);
  leg3->SetHeader("LHC Loss Map IP3-IP4");
  leg3->AddEntry(coll_loss,"Collimator losses","l");
  leg3->AddEntry(warm_loss,"Warm losses","l");
  leg3->AddEntry(cold_loss,"Cold losses","l");

  leg3->SetFillColor(10);
  leg3->SetTextFont(132);

  leg3->Draw();
  /*---------------*/

  pad_ld->cd(4);  
  
  TH1F *warm_loss4=new TH1F("warm_loss4","warm loss map IP4-IP5",(13329.29-9997.0)/0.1,9997.0,13329.29);
  warm_loss4->SetFillColor(2);
  warm_loss4->SetLineColor(2);


  TH1F *cold_loss4=new TH1F("cold_loss4","cold loss map IP4-IP5",(13329.29-9997.0)/0.1,9997.0,13329.29);
  cold_loss4->SetFillColor(4);
  cold_loss4->SetLineColor(4);

  TH1F *coll_loss4=new TH1F("coll_loss4","coll loss map IP4-IP5",(13329.29-9997.0)/0.1,9997.0,13329.29);
  coll_loss4->SetFillColor(12);
  coll_loss4->SetLineColor(12);


  for(j=0;j<10;j++){
    for(i=0;i<dim-nhead;i++){
      for(k=0;k<n_warm;k+=2){

	if(losses[i] >= warm[k] && losses[i] <= warm[k+1])
	  warm_loss4->Fill(losses[i]);
	if(k<n_warm-1 && losses[i] >= warm[k+1] && losses[i] <= warm[k+2])
	  cold_loss4->Fill(losses[i]);
      }
    }
  }
  
  for(i=0;i<dim_c_s-nhead_c_s;i++){
    for(j=0;j<dim_c_p-nhead_c_p;j++){

      if(strcmp(names_c_s[i],names_c_p[j])==0){

	for(k=0;k<(Int_t)(nabs[i]/length[i]);k++)
	  //for(k=0;k<nabs[i];k++)
	  coll_loss4->Fill(pos[j]);

      }

    }
  }

  pad_ld->cd(4)->SetLogy(1);
  pad_ld->cd(4)->SetGridy(1);
  
  coll_loss4->Scale(1.0/max);
  coll_loss4->GetXaxis()->SetLabelFont(132);
  coll_loss4->GetYaxis()->SetLabelFont(132);
  coll_loss4->GetYaxis()->SetRangeUser(1.0e-7,5.0);
  coll_loss4->GetXaxis()->SetTitleFont(132);
  coll_loss4->GetYaxis()->SetTitleFont(132);
  coll_loss4->GetXaxis()->SetTitle("s [m]");
  coll_loss4->GetYaxis()->SetTitle("losses (#frac{n}{n_{T} length}) [1/m]");
  coll_loss4->Draw();


  warm_loss4->Scale(1.0/max);
  warm_loss4->Draw("same");


  cold_loss4->Scale(1.0/max);
  cold_loss4->Draw("same");

  TLegend *leg4 = new TLegend(0.8,0.8,0.95,0.95);
  leg4->SetHeader("LHC Loss Map IP4-IP5");
  leg4->AddEntry(coll_loss,"Collimator losses","l");
  leg4->AddEntry(warm_loss,"Warm losses","l");
  leg4->AddEntry(cold_loss,"Cold losses","l");

  leg4->SetFillColor(10);
  leg4->SetTextFont(132);

  leg4->Draw();

  /*---------------*/

  pad_ld->cd(5);  
  
  TH1F *warm_loss5=new TH1F("warm_loss5","warm loss map IP5-IP6",(16661.73-13329.29)/0.1,13329/29,16661.73);
  warm_loss5->SetFillColor(2);
  warm_loss5->SetLineColor(2);


  TH1F *cold_loss5=new TH1F("cold_loss5","cold loss map IP5-IP6",(16661.73-13329.29)/0.1,13329/29,16661.73);
  cold_loss5->SetFillColor(4);
  cold_loss5->SetLineColor(4);

  TH1F *coll_loss5=new TH1F("coll_loss5","coll loss map IP5-IP6",(16661.73-13329.29)/0.1,13329/29,16661.73);
  coll_loss5->SetFillColor(12);
  coll_loss5->SetLineColor(12);


  for(j=0;j<10;j++){
    for(i=0;i<dim-nhead;i++){
      for(k=0;k<n_warm;k+=2){

	if(losses[i] >= warm[k] && losses[i] <= warm[k+1])
	  warm_loss5->Fill(losses[i]);
	if(k<n_warm-1 && losses[i] >= warm[k+1] && losses[i] <= warm[k+2])
	  cold_loss5->Fill(losses[i]);
      }
    }
  }
  
  for(i=0;i<dim_c_s-nhead_c_s;i++){
    for(j=0;j<dim_c_p-nhead_c_p;j++){

      if(strcmp(names_c_s[i],names_c_p[j])==0){

	for(k=0;k<(Int_t)(nabs[i]/length[i]);k++)
	  //for(k=0;k<nabs[i];k++)
	  coll_loss5->Fill(pos[j]);

      }

    }
  }

  pad_ld->cd(5)->SetLogy(1);
  pad_ld->cd(5)->SetGridy(1);
  
  coll_loss5->Scale(1.0/max);
  coll_loss5->GetXaxis()->SetLabelFont(132);
  coll_loss5->GetYaxis()->SetLabelFont(132);
  coll_loss5->GetYaxis()->SetRangeUser(1.0e-7,5.0);
  coll_loss5->GetXaxis()->SetTitleFont(132);
  coll_loss5->GetYaxis()->SetTitleFont(132);
  coll_loss5->GetXaxis()->SetTitle("s [m]");
  coll_loss5->GetYaxis()->SetTitle("losses (#frac{n}{n_{T} length}) [1/m]");
  coll_loss5->Draw();


  warm_loss5->Scale(1.0/max);
  warm_loss5->Draw("same");


  cold_loss5->Scale(1.0/max);
  cold_loss5->Draw("same");

  TLegend *leg5 = new TLegend(0.8,0.8,0.95,0.95);
  leg5->SetHeader("LHC Loss Map IP5-IP6");
  leg5->AddEntry(coll_loss,"Collimator losses","l");
  leg5->AddEntry(warm_loss,"Warm losses","l");
  leg5->AddEntry(cold_loss,"Cold losses","l");

  leg5->SetFillColor(10);
  leg5->SetTextFont(132);

  leg5->Draw();
  /*---------------*/

  pad_ld->cd(6);  
  
  TH1F *warm_loss6=new TH1F("warm_loss6","warm loss map IP6-IP7",(19994.16-16661.73)/0.1,16661.73,19994.16);
  warm_loss6->SetFillColor(2);
  warm_loss6->SetLineColor(2);


  TH1F *cold_loss6=new TH1F("cold_loss6","cold loss map IP6-IP7",(19994.16-16661.73)/0.1,16661.73,19994.16);
  cold_loss6->SetFillColor(4);
  cold_loss6->SetLineColor(4);

  TH1F *coll_loss6=new TH1F("coll_loss6","coll loss map IP6-IP7",(19994.16-16661.73)/0.1,16661.73,19994.16);
  coll_loss6->SetFillColor(12);
  coll_loss6->SetLineColor(12);


  for(j=0;j<10;j++){
    for(i=0;i<dim-nhead;i++){
      for(k=0;k<n_warm;k+=2){

	if(losses[i] >= warm[k] && losses[i] <= warm[k+1])
	  warm_loss6->Fill(losses[i]);
	if(k<n_warm-1 && losses[i] >= warm[k+1] && losses[i] <= warm[k+2])
	  cold_loss6->Fill(losses[i]);
      }
    }
  }
  
  for(i=0;i<dim_c_s-nhead_c_s;i++){
    for(j=0;j<dim_c_p-nhead_c_p;j++){

      if(strcmp(names_c_s[i],names_c_p[j])==0){

	for(k=0;k<(Int_t)(nabs[i]/length[i]);k++)
	  //for(k=0;k<nabs[i];k++)
	  coll_loss6->Fill(pos[j]);

      }

    }
  }

  pad_ld->cd(6)->SetLogy(1);
  pad_ld->cd(6)->SetGridy(1);
  
  coll_loss6->Scale(1.0/max);
  coll_loss6->GetXaxis()->SetLabelFont(132);
  coll_loss6->GetYaxis()->SetLabelFont(132);
  coll_loss6->GetYaxis()->SetRangeUser(1.0e-7,5.0);
  coll_loss6->GetXaxis()->SetTitleFont(132);
  coll_loss6->GetYaxis()->SetTitleFont(132);
  coll_loss6->GetXaxis()->SetTitle("s [m]");
  coll_loss6->GetYaxis()->SetTitle("losses (#frac{n}{n_{T} length}) [1/m]");
  coll_loss6->Draw();


  warm_loss6->Scale(1.0/max);
  warm_loss6->Draw("same");


  cold_loss6->Scale(1.0/max);
  cold_loss6->Draw("same");

  TLegend *leg6 = new TLegend(0.8,0.8,0.95,0.95);
  leg6->SetHeader("LHC Loss Map IP6-IP7");
  leg6->AddEntry(coll_loss,"Collimator losses","l");
  leg6->AddEntry(warm_loss,"Warm losses","l");
  leg6->AddEntry(cold_loss,"Cold losses","l");

  leg6->SetFillColor(10);
  leg6->SetTextFont(132);

  leg6->Draw();
  /*---------------*/

  pad_ld->cd(7);  
  
  TH1F *warm_loss7=new TH1F("warm_loss7","warm loss map IP7-IP8",(23315.38-19994.16)/0.1,19994.16,23315.38);
  warm_loss7->SetFillColor(2);
  warm_loss7->SetLineColor(2);


  TH1F *cold_loss7=new TH1F("cold_loss7","cold loss map IP7-IP8",(23315.38-19994.16)/0.1,19994.16,23315.38);
  cold_loss7->SetFillColor(4);
  cold_loss7->SetLineColor(4);

  TH1F *coll_loss7=new TH1F("coll_loss1","coll loss map IP7-IP8",(23315.38-19994.16)/0.1,19994.16,23315.38);
  coll_loss7->SetFillColor(12);
  coll_loss7->SetLineColor(12);


  for(j=0;j<10;j++){
    for(i=0;i<dim-nhead;i++){
      for(k=0;k<n_warm;k+=2){

	if(losses[i] >= warm[k] && losses[i] <= warm[k+1])
	  warm_loss7->Fill(losses[i]);
	if(k<n_warm-1 && losses[i] >= warm[k+1] && losses[i] <= warm[k+2])
	  cold_loss7->Fill(losses[i]);
      }
    }
  }
  
  for(i=0;i<dim_c_s-nhead_c_s;i++){
    for(j=0;j<dim_c_p-nhead_c_p;j++){

      if(strcmp(names_c_s[i],names_c_p[j])==0){

	for(k=0;k<(Int_t)(nabs[i]/length[i]);k++)
	  //for(k=0;k<nabs[i];k++)
	  coll_loss7->Fill(pos[j]);

      }

    }
  }

  pad_ld->cd(7)->SetLogy(1);
  pad_ld->cd(7)->SetGridy(1);
  
  coll_loss7->Scale(1.0/max);
  coll_loss7->GetXaxis()->SetLabelFont(132);
  coll_loss7->GetYaxis()->SetLabelFont(132);
  coll_loss7->GetYaxis()->SetRangeUser(1.0e-7,5.0);
  coll_loss7->GetXaxis()->SetTitleFont(132);
  coll_loss7->GetYaxis()->SetTitleFont(132);
  coll_loss7->GetXaxis()->SetTitle("s [m]");
  coll_loss7->GetYaxis()->SetTitle("losses (#frac{n}{n_{T} length}) [1/m]");
  coll_loss7->Draw();


  warm_loss7->Scale(1.0/max);
  warm_loss7->Draw("same");


  cold_loss7->Scale(1.0/max);
  cold_loss7->Draw("same");

  TLegend *leg7 = new TLegend(0.8,0.8,0.95,0.95);
  leg7->SetHeader("LHC Loss Map IP7-IP8");
  leg7->AddEntry(coll_loss,"Collimator losses","l");
  leg7->AddEntry(warm_loss,"Warm losses","l");
  leg7->AddEntry(cold_loss,"Cold losses","l");

  leg7->SetFillColor(10);
  leg7->SetTextFont(132);

  leg7->Draw();
  /*---------------*/

  pad_ld->cd(8);  
  
  TH1F *warm_loss8=new TH1F("warm_loss1","warm loss map IP8-IP1",(26658.88-23315.38)/0.1,23315.38,26658.88);
  warm_loss8->SetFillColor(2);
  warm_loss8->SetLineColor(2);


  TH1F *cold_loss8=new TH1F("cold_loss8","cold loss map IP8-IP1",(26658.88-23315.38)/0.1,23315.38,26658.88);
  cold_loss8->SetFillColor(4);
  cold_loss8->SetLineColor(4);

  TH1F *coll_loss8=new TH1F("coll_loss1","coll loss map IP8-IP1",(26658.88-23315.38)/0.1,23315.38,26658.88);
  coll_loss8->SetFillColor(12);
  coll_loss8->SetLineColor(12);


  for(j=0;j<10;j++){
    for(i=0;i<dim-nhead;i++){
      for(k=0;k<n_warm;k+=2){

	if(losses[i] >= warm[k] && losses[i] <= warm[k+1])
	  warm_loss8->Fill(losses[i]);
	if(k<n_warm-1 && losses[i] >= warm[k+1] && losses[i] <= warm[k+2])
	  cold_loss8->Fill(losses[i]);
      }
    }
  }
  
  for(i=0;i<dim_c_s-nhead_c_s;i++){
    for(j=0;j<dim_c_p-nhead_c_p;j++){

      if(strcmp(names_c_s[i],names_c_p[j])==0){

	for(k=0;k<(Int_t)(nabs[i]/length[i]);k++)
	  //for(k=0;k<nabs[i];k++)
	  coll_loss8->Fill(pos[j]);

      }

    }
  }

  pad_ld->cd(8)->SetLogy(1);
  pad_ld->cd(8)->SetGridy(1);
  
  coll_loss8->Scale(1.0/max);
  coll_loss8->GetXaxis()->SetLabelFont(132);
  coll_loss8->GetYaxis()->SetLabelFont(132);
  coll_loss8->GetYaxis()->SetRangeUser(1.0e-7,5.0);
  coll_loss8->GetXaxis()->SetTitleFont(132);
  coll_loss8->GetYaxis()->SetTitleFont(132);
  coll_loss8->GetXaxis()->SetTitle("s [m]");
  coll_loss8->GetYaxis()->SetTitle("losses (#frac{n}{n_{T} length}) [1/m]");
  coll_loss8->Draw();


  warm_loss8->Scale(1.0/max);
  warm_loss8->Draw("same");


  cold_loss8->Scale(1.0/max);
  cold_loss8->Draw("same");

  TLegend *leg8 = new TLegend(0.8,0.8,0.95,0.95);
  leg8->SetHeader("LHC Loss Map IP8-IP1");
  leg8->AddEntry(coll_loss,"Collimator losses","l");
  leg8->AddEntry(warm_loss,"Warm losses","l");
  leg8->AddEntry(cold_loss,"Cold losses","l");

  leg8->SetFillColor(10);
  leg8->SetTextFont(132);

  leg8->Draw();
  pad_ld->cd();


  /*---------------*/


  /*---------------*/

  for(i=0;i<dim_c_s-nhead_c_s;i++)
    free(names_c_s[i]);

  free(names_c_s);

  for(i=0;i<dim_c_p-nhead_c_p;i++)
    free(names_c_p[i]);

  free(names_c_p);

  free(losses);
  free(nabs);
  free(pos);

}
