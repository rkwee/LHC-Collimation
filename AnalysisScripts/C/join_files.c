#include"func_sim.h"
#include"func_sim.c"

void join_files(){

  FILE *out;
  FILE *ptr;
  char filenames[50];
  Int_t n_runs,n_h,i,j;
  char line[10000];

  printf("Filename of the files to be joined:\n");
  scanf("%s",filenames);

  printf("\nNumber of runs:\n");
  scanf("%d",&n_runs);

  printf("\nNumber of header lines:\n");
  scanf("%d",&n_h);

  //cout<<filenames<<endl;

  out=fopen(Form("%s_total.dat",filenames),"w");

  for(i=1;i<=n_runs;i++){

    ptr=fopen(Form("run%.4d/%s",i,filenames),"r");
    if(ptr==NULL)
      cout<<"File "<<Form("run%.4d/%s",i,filenames)<<" not found!!"<<endl;
    else{

    cout<<Form("Opening: run%.4d/%s",i,filenames)<<endl;

    j=0;

    while(fgets(line,sizeof(line),ptr) != '\0'){

      if(i==1)
	fprintf(out,"%s",line);

      if(i>1 && j>=n_h)
	fprintf(out,"%s",line);

      j+=1;

    }  

    fclose(ptr);

    }

  }

  fclose(out);

}
