import numpy as np
import h5py
import re

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", dest="file", type="string",
                  help="tracks2.h5 file")

(options, args) = parser.parse_args()
f = options.file

imax = 0
tracks2 = h5py.File(f,'r')
tracks2ascii = open(f + '-to-txt','w')
tracks2ascii.write(" # 1=name 2=turn 3=s 4=x 5=xp 6=y 7=yp 8=DE/E 9=type\n")


i = 0
for t in tracks2['tracks']:
    #Alignment doesn't fully match FORTRAN
    tracks2ascii.write(" %8i %4i %8.2f %11.5e %11.5e %11.5e %11.5e %11.3e %4i\n" % tuple(t))

    #Matches fortran, sloooow...
    #tracks2ascii.write(" {0:8d} {1:4d} {2:8.2f}{3:s}{4:s}{5:s}{6:s}{7:s} {8:4d}\n".format(
    #    int(t[0]),int(t[1]),t[2], fixexp1(t[3]),fixexp1(t[4]),fixexp1(t[5]),fixexp1(t[6]), fixexp2(t[7]), int(t[8])
    #))
    
    #Stop halfway for debugging
    i = i+1
    if (i%100000==0):
        print i, " rows converted"
    if imax > 0 and i >= imax:
        break
    

tracks2ascii.close()
tracks2.close()
