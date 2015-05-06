#!/usr/bin/python
#
# Nov 2014, rkwee
## -------------------------------------------------------------------------------
import helpers
from helpers import *

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", dest="file", type="string",
                  help="file with CPU time in it")

(options, args) = parser.parse_args()
f = options.file
# -----------------------------------------------------------------------------------

def getTimeSpent(f):

    with open(f) as mf:
        for line in mf:

    # example 
    # line = "Job finished at Wed Feb 11 10:02:28 CET 2015 on node"

    # dayNumber = line.split()[5]
    # monthName = line.split()[4]
    # timestring = line.split()[6]
    # year = line.split()[8]

    # print line
    # print dayNumber,monthName,timestring,year

    # ts = stringDateToTimeStamp( dayNumber +' '+ monthName + ' ' + year + ' ' + timestring, "%d %b %Y %H:%M:%S")

    # print ts

    with open(f) as mf:
        for line in mf:
            # line = NewScatt_TCT_4TeV_B1hHalo_bm_50packs/run_00001/LSFJOB_622145697/STDOUT:01:04:31 13.02.2015 CET

            line.split("T:")[-1].split()

# -----------------------------------------------------------------------------------

def getStats(f):
    nList, sList, jList, tList = [],[],[],[]
    with open(f) as mf:
        for line in mf:
            # job number 'LSF_932048'
            jn = line.split()[0].split('/')[-2]

            # corresponds file time
            if f.count("CPU"):
                tList += [ (int(line.split()[-3].lstrip('(')), jn) ]
            else:
                if line.count('tracks2.dat') and line.count('rkwee'):
                    size = int(line.split()[-5])
                    if size < 100: continue
                    else: sList += [(size, jn)]

                if line.count('tracks2.h5') and line.count('rkwee'):
                    sizeH5 = int(line.split()[-5])
                    if sizeH5 < 100: continue
                    else: nList += [(sizeH5, jn)]

    def printStats(sList):

        mean_s = mean([i[0] for i in sList])
        std_s = stddev([i[0] for i in sList])
        SList = [i[0] for i in sList]
        print 'sample of ',len(sList),' gives ', mean_s, '+-', std_s, 'which is ', std_s/mean_s
        maxV  = max(SList)
        minV  = min(SList)
        print 'max time', maxV, ' for job', sList[SList.index(maxV)][1]
        print 'min time', minV, ' for job', sList[SList.index(minV)][1]
        print '-'*44

    if tList:
        printStats(tList)
    if nList:
        print "="*22, 'tracks2.h5', "="*22
        printStats(nList)
    if sList:
        print "="*22, 'tracks2.dat', "="*22
        printStats(sList)

# ----------------------------------------------------------------------------
if __name__ == "__main__":

    #getTimeSpent()
    getStats(f)
