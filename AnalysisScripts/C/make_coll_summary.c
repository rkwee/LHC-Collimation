#include"func_sim.h"
#include"func_sim.c"

void make_coll_summary(){

  char* filename;
  Int_t nhead,dim,i,j,k,n_coll;
  char **names;
  Int_t *nimp,*nabs,*icoll;
  Float_t *imp_av,*imp_sig,*length;

  filename="coll_summary.dat_total.dat";
  nhead=1;
  n_coll=45;

  dim=count_line(filename);

  //cout<<dim<<endl;

  names=(char **)malloc((dim-nhead)*sizeof(char *));

  for(i=0;i<dim-nhead;i++)
    names[i]=(char *)malloc(100*sizeof(char));

  icoll=(Int_t *)malloc((dim-nhead)*sizeof(Int_t));
  nimp=(Int_t *)malloc((dim-nhead)*sizeof(Int_t));
  nabs=(Int_t *)malloc((dim-nhead)*sizeof(Int_t));
  imp_av=(Float_t *)malloc((dim-nhead)*sizeof(Float_t));
  imp_sig=(Float_t *)malloc((dim-nhead)*sizeof(Float_t));
  length=(Float_t *)malloc((dim-nhead)*sizeof(Float_t));

  extr_names(filename,dim,names,2,nhead);
  extr_var_int(filename,dim,icoll,1,nhead);
  extr_var_int(filename,dim,nimp,3,nhead);
  extr_var_int(filename,dim,nabs,4,nhead);
  extr_var_float(filename,dim,imp_av,5,nhead);
  extr_var_float(filename,dim,imp_sig,6,nhead);
  extr_var_float(filename,dim,length,7,nhead);

  /*------------*/

  FILE *out;

  Int_t icoll_tot,nimp_tot,nabs_tot;
  Float_t imp_av_tot,imp_sig_tot,length_tot;

  icoll_tot=0;
  nimp_tot=0;
  nabs_tot=0;
  imp_av_tot=0;
  imp_sig_tot=0;
  length_tot=0;

  out=fopen("coll_summary_final.dat","w");

  fprintf(out," # 1=icoll 2=nimp 3=nabs 4=imp_av 5=imp_sig 6=length\n");

  for(i=0;i<n_coll;i++){

    k=0;
    nimp_tot=0;
    nabs_tot=0;
    imp_av_tot=0;
    imp_sig_tot=0;

    for(j=0;j<dim-nhead;j++){

      //cout<<names[j]<<endl;

      //cout<<names[i]<<" "<<names[j]<<endl;

      //if(names[i]==names[j]){
      if(strcmp(names[i],names[j])==0){

	//cout<<"INNNNNNNNNN"<<endl;

	//cout<<i<<" "<<j<<" "<<names[i]<<endl;

	icoll_tot=icoll[j];
	nimp_tot+=nimp[j];
	nabs_tot+=nabs[j];
	imp_av_tot+=imp_av[j];
	imp_sig_tot+=imp_sig[j];
	length_tot=length[j];

	//cout<<length_tot<<" "<<length[j]<<endl;

	k+=1;

      }

    }

    //cout<<k<<endl;

    imp_av_tot/=k;
    imp_sig_tot/=k;

    fprintf(out," %d %s %d %d %e %e %f \n",icoll_tot,names[i],nimp_tot,nabs_tot,imp_av_tot,imp_sig_tot,length_tot);

  }

  /*-------------*/

  for(i=0;i<dim-nhead;i++)
    free(names[i]);

  free(icoll);
  free(names);
  free(nimp);
  free(nabs);
  free(imp_av);
  free(imp_sig);


  fclose(out);

}


