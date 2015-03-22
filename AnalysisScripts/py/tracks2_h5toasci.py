import numpy as np
import h5py
import re

tracks2 = h5py.File("tracks2.h5",'r')
tracks2ascii = open("tracks2.h5.dat",'w')
tracks2ascii.write(" # 1=name 2=turn 3=s 4=x 5=xp 6=y 7=yp 8=DE/E 9=type\n")

print "You may give an integer, indicating how many rows to convert from the h5 file"
imax = 0
import sys
if len(sys.argv) == 2:
    imax = int(sys.argv[1])
    print "\t Converting ",imax, "rows!"

def fixexp1(x):
    #Fixing fortran formatting
    #Adapted from
    #http://stackoverflow.com/questions/13031636/string-format-start-scientific-notation-with-0-for-positive-number-with-fo
    
    foo = (" {0:11.4E}").format(x)

    # shift the decimal point
    foo = re.sub(r"(\d)\.", r".\1", foo)
    # add 0 for positive numbers
    foo = re.sub(r" \.",    r"0.",  foo)
    # increase exponent by 1
    exp = re.search(r"E([+-]\d+)", foo)
    newexp = "E{:+03}".format(int(exp.group(1))+1)
    foo = re.sub(r"E([+-]\d+)", newexp, foo)
    return foo

def fixexp2(x):
    #Slightly different format
    foo = (" {0:11.2E}").format(x)

    # shift the decimal point
    foo = re.sub(r"(\d)\.", r".\1", foo)
    # add 0 for positive numbers
    foo = re.sub(r" \.",    r"0.",  foo)
    #add 0 for negative numbers
    foo = re.sub(r" -\.",    r"-0.",  foo)
    # increase exponent by 1
    exp = re.search(r"E([+-]\d+)", foo)
    newexp = "E{:+03}".format(int(exp.group(1))+1)
    foo = re.sub(r"E([+-]\d+)", newexp, foo)
    return foo

i = 0
for t in tracks2['tracks']:
    #Alignment doesn't fully match FORTRAN
    #tracks2ascii.write(" %8i %4i %8.2f %11.5e %11.5e %11.5e %11.5e %11.3e %4i\n" % tuple(t))

    #Matches fortran, sloooow...
    tracks2ascii.write(" {0:8d} {1:4d} {2:8.2f}{3:s}{4:s}{5:s}{6:s}{7:s} {8:4d}\n".format(
        int(t[0]),int(t[1]),t[2], fixexp1(t[3]),fixexp1(t[4]),fixexp1(t[5]),fixexp1(t[6]), fixexp2(t[7]), int(t[8])
    ))
    
    #Stop halfway for debugging
    i = i+1
    if (i%1000000==0):
        print "i = ",i, " rows converted"
    if imax > 0 and i >= imax:
        break
    

tracks2ascii.close()
tracks2.close()
