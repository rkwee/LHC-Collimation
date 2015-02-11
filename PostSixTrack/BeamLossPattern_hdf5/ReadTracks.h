
#include <iostream>
#include <fstream>
#include <cstring>
#include <string>

#include <stdio.h>
#include <stdlib.h> 
#include <string.h> 
#include <ctype.h>

#include "config.h"

#ifdef HAVE_HDF5_H
#include "hdf5.h"

#define X     1024                        /* this is number of lines read per slab */
#define Y     9

#endif

#ifndef ReadTracks_h
#define ReadTracks_h 1

using namespace std;

class ReadTracks {
    private:
        ifstream in;
        char c_str[256];
        bool endoffile;
        bool USING_HDF5;
        int i, j,imin;
#ifdef HAVE_HDF5_H    
        hid_t file_id, filespace,memspace, dataset_id;  /* identifiers */
        herr_t status,status_n;
        hsize_t dims[2],count[2],offset[2]; /* dimensions of array, size of hyperslab, offset in hyperslab */ 
        int slabsize[2];
        float nextlines[X][Y];
#endif
#ifndef HAVE_HDF5_H
        int dims[2];
#endif
        
    public:
        ReadTracks(string tracksfile);
        ~ReadTracks();
        int getNextTrack(int& n_t, int& n_tu, double& s_t, double& x_t, double& xp_t, 
                         double& y_t, double& yp_t, double& en_t, int& n_h);

    
};

#endif
