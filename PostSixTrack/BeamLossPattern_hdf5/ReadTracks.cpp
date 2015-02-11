#include "ReadTracks.h"


ReadTracks::ReadTracks(string tracksfile) {
    USING_HDF5=false;
    string filesuffix = tracksfile.substr(tracksfile.find_last_of(".") + 1);
    if (filesuffix != "hd5" and filesuffix != "h5") {
        ReadTracks::in.open(tracksfile.c_str(), ios::in);
        if (!ReadTracks::in){
        cout<<"Impossible to open the file !"<<endl;
        cout<<"Error status: "<<in<<endl;
        exit(1);
        }
        ReadTracks::in.getline(c_str,256); // Skip the first line with the header
    }
    else {

#ifndef HAVE_HDF5_H
        cout << "HDF5 library not included in BeamLossPattern" << endl;
        exit(5);
#else
    USING_HDF5=true;

    /* Open an existing file. */
    file_id = H5Fopen(tracksfile.c_str(), H5F_ACC_RDWR, H5P_DEFAULT);

    /* Open an existing dataset. */
    dataset_id = H5Dopen(file_id, "/tracks", H5P_DEFAULT);
    
    filespace = H5Dget_space(dataset_id);
    status_n  = H5Sget_simple_extent_dims(filespace, dims, NULL);
    printf("dataset dimensions %lu x %lu\n",
            dims[0], dims[1]);
    
    // Set up sizes. (HEIGHT x WIDTH)
    // checks...
    H5T_class_t hclass;                 /* datatype class */
    H5T_order_t horder;                 /* data order */
    hid_t       hdatatype;
    hdatatype  = H5Dget_type(dataset_id);     /* datatype handle */ 
    hclass     = H5Tget_class(hdatatype);
    horder     = H5Tget_order(hdatatype);
    if (hclass == H5T_FLOAT) printf("Float type data\n");
    if (horder == H5T_ORDER_LE) printf("Little endian order \n");
    
    count[0]=X;
    count[1]=Y;
    offset[0]=0;
    offset[1]=0;
    ReadTracks::i=0;

    /* 
     * Define memory hyperslab. 
     */
    memspace = H5Screate_simple(2,count,NULL); 
    status = H5Sselect_hyperslab(memspace, H5S_SELECT_SET, offset, NULL, 
                                 count, NULL);
        
#endif
  }
  ReadTracks::endoffile=false;
    
}

ReadTracks::~ReadTracks()
{
#ifndef HAVE_HDF5_H
  ReadTracks::in.close();    
#else
    /*
     * Close and release resources.
     */
    H5Dclose (dataset_id);
    H5Sclose (filespace);
    H5Sclose (memspace);
    H5Fclose (file_id);
#endif

}


int ReadTracks::getNextTrack(int& n_t, int& n_tu, double& s_t, double& x_t, double& xp_t, 
                         double& y_t, double& yp_t, double& en_t, int& n_h) {
    if (ReadTracks::endoffile) return 1;
    if(USING_HDF5) {
        if (i%X==0) {
        /* select offset and read into memory */
        offset[0]=i;
        if (dims[0]-i<count[0]) {
            count[0]=dims[0]-i; // last slab might be smaller..
            memspace = H5Screate_simple(2,count,NULL); 
            status = H5Sselect_hyperslab(memspace, H5S_SELECT_SET, offset, NULL, 
                                        count, NULL);
        }
        status = H5Sselect_hyperslab(filespace, H5S_SELECT_SET, offset, NULL, 
                                     count, NULL);
        /*
        * Read data from hyperslab in the file into the hyperslab in 
        * memory and display.
        */
        status = H5Dread(dataset_id, H5T_NATIVE_FLOAT_g, memspace, filespace,
                        H5P_DEFAULT, nextlines); 
        }  
        n_t   = nextlines[i%count[0]][0];
        n_tu  = nextlines[i%count[0]][1];
        s_t   = nextlines[i%count[0]][2];
        x_t   = nextlines[i%count[0]][3];
        xp_t  = nextlines[i%count[0]][4];
        y_t   = nextlines[i%count[0]][5];
        yp_t  = nextlines[i%count[0]][6];
        en_t  = nextlines[i%count[0]][7];
        n_h   = nextlines[i%count[0]][8];
        if (nextlines[i%count[0]][0]==0.) { ReadTracks::endoffile = true; cout << "DBG "<< i <<" "<<count[0] << endl;return 1; }
        i++;
        if (ReadTracks::i>=ReadTracks::dims[0]) ReadTracks::endoffile = true;
        return 0;
    } else {
    in>>n_t>>n_tu>>s_t>>x_t>>xp_t>>y_t>>yp_t>>en_t>>n_h;
    if(ReadTracks::in.eof()) ReadTracks::endoffile=true;
    }
    return 0;
}
