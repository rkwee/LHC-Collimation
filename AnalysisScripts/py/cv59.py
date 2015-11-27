#!/usr/bin/python
#
# Nov 2015, rkwee
## -------------------------------------------------------------------------------
# plot data lossmap
## -------------------------------------------------------------------------------
import helpers
from helpers import *
# -----------------------------------------------------------------------------------

debug =  0
def cv59():
    thispath         = "/Users/rkwee/Documents/RHUL/work/BLMDataAnalysis/lossmaps/"
    rawDataFileName  = thispath + "20120402__LOSS_RS09__180500_1333382700__Data_Extract_BLMs_all.txt"
    blmPositions     = thispath + "BLMs_all_with_s_coordinate.txt"
    
    def createDict(file):


        dList = []
        with open(file) as mf:

            for line in mf:
                
                dictkey = line.split()[0]

                restofline = line.split(dictkey)[-1]
                print "will have", len(restofline.split()), "elements for each key"
                dList += [(dictkey, restofline)]

        return dict(dList)


        blmPositionDict = createDict(blmPositions)
