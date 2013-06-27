#include"func_sim.h"
#include"func_sim.c"

void clean_coll_summary(){

  char* filename;
  Int_t nhead,dim,i,j,k;
  char **names;
  Int_t *nimp,*nabs,*icoll;
  Float_t *imp_av,*imp_sig,*length;

  filename="coll_summary_final.dat";
  nhead=1;

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

  cout<<"letto coll"<<endl;

  /*------------*/

  char* filename2;

  filename2="impacts_fake.dat_total.dat";

  Int_t dim2;  

  dim2=count_line(filename2);

  cout<<dim2<<endl;

  Int_t *ic;

  ic=(Int_t *)malloc((dim2-nhead)*sizeof(Int_t));

  extr_var_int(filename2,dim2,ic,1,nhead);

  cout<<"letto"<<endl;

  /*-------------*/

  FILE *out;

  out=fopen("coll_summary_cleaned.dat","w");

  fprintf(out," # 1=icoll 2=nimp 3=nabs 4=imp_av 5=imp_sig 6=length\n");

  for(i=0;i<dim-nhead;i++){
    for(j=0;j<dim2-nhead;j++){

      if(icoll[i]==ic[j])
	nabs[i]-=1;

    }

    fprintf(out," %d %s %d %d %e %e %f \n",icoll[i],names[i],nimp[i],nabs[i],imp_av[i],imp_sig[i],length[i]);

  }
  for(i=0;i<dim-nhead;i++)
    free(names[i]);

  free(icoll);
  free(names);
  free(nimp);
  free(nabs);
  free(imp_av);
  free(imp_sig);
  free(ic);

  fclose(out);

}
