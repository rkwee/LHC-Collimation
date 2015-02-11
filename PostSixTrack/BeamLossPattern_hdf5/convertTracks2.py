#!/usr/bin/python

import numpy as np
import h5py
import optparse


if __name__=="__main__":
    usage="%prog [options] ascii-file hdf-file"
    usage+='\n\n\tThis script converts an ascii file to a hdf5 file.'
    parser = optparse.OptionParser(usage)
    (options,args) = parser.parse_args()
    if len(args)!=2:
        print "ERROR: wrong number of input arguments"
        print usage
        exit(1)

    hf = h5py.File(args[1], 'w')
    infile = open(args[0],'r')
    
    outarray=[]
    for l in infile:
        if l.strip()[0]!='#':
            outarray.append(l.split())
        else:
            attrs=l.strip()[1:].split()
    outarray=np.array(outarray,dtype=np.float)
    
    print np.shape(outarray)
    hf['tracks']=outarray
    hf['tracks'].attrs["header"]=attrs
