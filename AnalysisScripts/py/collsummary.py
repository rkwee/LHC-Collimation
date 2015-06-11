#!/usr/bin/python
#
# Nov, 2014 rkwee
# -----------------------------------------------------------------------------------
import gzip, subprocess, os
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-c", dest="colls", type="string",
                  help="put list of coll families, 'TCP*7,TCSG*'")
parser.add_option("-f", dest="fname", type="string",
                  help="put unzipped coll_summary file")

(options, args) = parser.parse_args()

collsummaryfile = options.fname
Collfam = options.colls
collfam = Collfam.split(",")
# -----------------------------------------------------------------------------------

def getnprim():

    nprimfile = collsummaryfile.split('coll_s')[0] + 'nprim.txt'
    if os.path.exists(nprimfile):

        cmd = 'grep "for targetfile LPI" ' + nprimfile
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        myStdOut = process.stdout.read()
        nprim = float(myStdOut.split()[0]) * 6400.        
        print "nprim =", nprim, 'in', nprimfile
        return nprim
    else:
        return -9999

# -----------------------------------------------------------------------------------
def collsummary():
    # # # ## # # ## # # ## # # #
    # 
    # sums hits per collimator family (per bash grep)
    #
    #
    # # # ## # # ## # # ## # # #
    cList = []
    debug = 0

    nprim = getnprim()
    if debug: print "collfam", collfam

    # loop over all collimator familys
    for fam in collfam:

        # create a sub loop of pattern to grep for per family
        fampatt = []
        fampattern = fam.split("*") 

        # remove empty elements
        for fp in fampattern: 
            if fp: fampatt += [fp]

        if debug: print "looking at fampatt", fampatt

        # command is 
        cmd = 'grep "' + fampatt[0] + '" ' + collsummaryfile 

        # if there are more pattern to grep for, extend the comman
        if len(fampatt) > 1:
            for i in range(1,len(fampatt)):
                cmd += ' | grep ' + fampatt[i]

        # final command is 
        if debug: print cmd

        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        myStdOut = process.stdout.readlines() 
        
        if debug: print len(myStdOut)
        # convert list of lines to list of splitted lines (lists)
        lList = [line.split() for line in myStdOut]

        if debug: print lList
        # prepare a dictionary with fam as key
        cList += [[fam, lList]]

    cDict = dict(cList)
    if debug: print cDict

    for fam in cDict.keys():

        # 1=icoll 	 2=collname 	 3=nimp 	 4=nabs 	 5=imp_av 	 6=imp_sig 	

        print '-' * 99
        names = [lines[1] for lines in cDict[fam]]
        if debug: print "For collimator family", fam, " use hits of ", names

        # summed per family
        nimps = 0
        for lines in cDict[fam]: nimps += float(lines[2])
        nabss = 0
        for lines in cDict[fam]: nabss += float(lines[3])

        print 'family', names, 'absorbed ', nabss, 'protons. ratio nabss/nprim', nabss/nprim
    print '-' * 99

# -----------------------------------------------------------------------------------
if __name__ == "__main__":

    collsummary()

    
