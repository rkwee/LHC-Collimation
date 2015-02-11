/* 
 *   Writing and reading an existing dataset.
 */

#include "hdf5.h"
#include <iostream>
#include <stdlib.h>

using namespace std;

int changeMyVar(int &myvar) {
    myvar+=1;
    return 0;
}

int main(int argc, char* argv[]) {

    hid_t       file_id, filespace, dataset_id;  /* identifiers */
    herr_t      status,status_n;
    hsize_t     dims[2]; 
    int         i, j,imin;
    
    if (argc!=2) {
        cout << "ERROR, need to specify hdf5 file in input"<<endl;
        exit(1);
    }
    
    char* FILE = argv[1];
    cout << "reading file: "<<FILE<<endl;

    /* Open an existing file. */
    file_id = H5Fopen(FILE, H5F_ACC_RDWR, H5P_DEFAULT);

    /* Open an existing dataset. */
    dataset_id = H5Dopen(file_id, "/tracks", H5P_DEFAULT);
    
    filespace = H5Dget_space(dataset_id);
    status_n  = H5Sget_simple_extent_dims(filespace, dims, NULL);
    printf("dataset dimensions %lu x %lu\n",
            dims[0], dims[1]);
    float dset_data[dims[0]][dims[1]];
    status = H5Dread(dataset_id, H5T_NATIVE_FLOAT_g, H5S_ALL, H5S_ALL, H5P_DEFAULT, 
                        dset_data);
    imin=dims[0];
    if (dims[0]>3) imin=3;
    for (i=0;i<imin;i++) {
        for (j=0;j<dims[1];j++) {
                cout << dset_data[i][j] <<  " ";
        }
        cout << endl;
    }
   /* Close the dataset. */
   status = H5Dclose(dataset_id);

   /* Close the file. */
   status = H5Fclose(file_id);
   int myvar=5;
   cout << "init var: "<<myvar<< endl;
   changeMyVar(myvar);
   cout << "final var: "<< myvar<<endl;
}
