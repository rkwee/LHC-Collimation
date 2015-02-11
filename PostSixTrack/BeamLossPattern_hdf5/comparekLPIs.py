#!/usr/bin/python

import optparse
import numpy as np
import os,sys
import filecmp

totdist=0.

def compareDistance(l1,l2):
    global totdist
    if l1[1]!=l2[1]:
        print '# WARNING: Particle',int(l1[0]),'did not collide with aperture on same turn'
    else:
        dist=0
        for i in [2,3,5]:
            dist+=(l1[i]-l2[i])**2
        dist=np.sqrt(dist)
        print int(l1[0]),dist
        totdist+=dist

def main(args,options):
    global totdist
    if filecmp.cmp(args[0],args[1]):
        print '# Info: Perfect comparison, the result was identical'
        sys.exit(0)
    n1=np.loadtxt(args[0])
    n2=np.loadtxt(args[1])
    for l1 in n1:
        found=False
        for l2 in n2:
            if l1[0]==l2[0]:
                found=True
                compareDistance(l1,l2)
                break
        if not found:
            print '# Warning, particle',int(l1[0]),'not found'
    print '# Total dist',totdist

    if totdist/len(l1)>.2:
        print '# Warning: the average distance is',totdist/len(n1)
        exit(1)
    else:
        print '# Info: It looks like the losses were quite close, average was',totdist/len(l1)
        exit(0)


if __name__=="__main__":
    usage="%prog [options] file1 file2"
    usage+='\n\n\tThis script compares two LPI files.'
    parser = optparse.OptionParser(usage)
    (options,args) = parser.parse_args()
    if len(args)!=2:
        print '\n    **ERROR: wrong number of input arguments**\n'
        print usage
        exit(1)
    elif not (os.path.isfile(args[0]) and os.path.isfile(args[1])):
        print '\n    **ERROR: input arguments must be files**\n'
        print usage
        exit(1)

    main(args,options)
