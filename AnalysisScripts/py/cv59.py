#!/usr/bin/python
#
# Nov 2015, rkwee
## -------------------------------------------------------------------------------
# plot data lossmap
## -------------------------------------------------------------------------------
import helpers, subprocess
from helpers import *
# -----------------------------------------------------------------------------------

def cv59():

    debug = 0

    thispath         = "/Users/rkwee/Documents/RHUL/work/" 
    thispath         = workpath 
    thispath         +=  "BLMDataAnalysis/lossmaps/"
    rawDataFileName1 = thispath + "20120402__LOSS_RS09__180500_1333382700__Data_Extract_BLMs_all.txt"
    rawDataFileName2 = thispath + "20120402__LOSS_RS09__181500_1333383300__Data_Extract_BLMs_all.txt"
    blmPositions     = thispath + "BLMs_all_with_s_coordinate.txt"
    
    blmPositionsDict = createDictFromRow(blmPositions)

    print "have",len(blmPositionsDict),"blm positions"

    def getBlmNames(fileName):

        blmNames = []
        with open(fileName) as mf:

                headerline = mf.readline()
                headerlist = headerline.split()

                for element in headerlist:
                    if element.count("BLM"):
                        blmNames += [element.split(":LOSS_RS09")[0]]
        return blmNames


    blmsPos = blmPositionsDict.keys()

    # .................................................................................................
    # -- get a specific line
    format = "%Y-%m-%d %H:%M:%S"
    lossmaps_dt = [
        ['B1H_afterSqueeze', '2012-04-02 18:17:38', rawDataFileName2],
        ['B1V_afterSqueeze', '2012-04-02 18:16:07', rawDataFileName2],
        # ['B2H_afterSqueeze', '2012-04-02 18:14:50', rawDataFileName1],
        # ['B2V_afterSqueeze', '2012-04-02 18:13:29', rawDataFileName1],
        ]

    # has as key B1H_xxx and as content a dict [blmName]: measurement
    dataList = []

    for lossmapType, dt, rawDataFileName in lossmaps_dt: 
        ts = int(stringDateToTimeStamp(dt,format))
        print "."*33, lossmapType, " lossmap took place at", dt, ' = ', ts

        cmd = 'grep ' + str(ts) + ' ' + rawDataFileName
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        myStdOut = process.stdout.read()
        dataline = myStdOut.split()
        dataline = [float(d) for d in dataline]

        blmsData = getBlmNames(rawDataFileName)
        print "have",len(blmsData),"blms in ", rawDataFileName

        # check for position of each blm with data
        missingData, missingPos = [], []
        for blm in blmsPos:

            if blm not in blmsData:
                missingData += [blm]

        for blm in blmsData:

            if blm not in blmsPos:
                missingPos += [blm]

        print "Missing data of ", len(missingData), "blms"#, missingData
        print "Missing position of ", len(missingPos), "blms",# missingPos

        # collect all info in new list->dict
        dataPerLossmap = []
        for i,blm in enumerate(blmsData):
            dataPerLossmap += [[blm, dataline[i] ]]

        dataList += [[lossmapType, [ dict(dataPerLossmap), missingData, missingPos] ]]
        maxloss = max(dataline)
        indexmax = dataline.index(maxloss)
        blmMaxloss = blmsData[indexmax]
        print "Maximum loss", maxloss, "in ", blmMaxloss

        if maxloss > 1: 
            # remove bad data, this changes dataline!
            dataline.pop(indexmax)
            # apply same change to the names
            blmsData.pop(indexmax)

            maxloss = max(dataline)
            indexmax = dataline.index(maxloss)
            blmMaxloss = blmsData[indexmax]
            print "Unreasonable data loss in that blm. Next maximum is", maxloss, "in ", blmMaxloss


    # make it a dict
    dataDict = dict(dataList)

    print "."*99
    for dKey in dataDict.keys():
        print "-"*44, dKey,'-'*44
        #print "length of ", dKey, "is", len(dataDict[dKey][0])

        missingPos = dataDict[dKey][2]
        dataPerLossmapDict = dataDict[dKey][0]
        for i,blm in enumerate(missingPos):
            print "Missing position of blm #",i, blm, ". Data is", dataPerLossmapDict[blm]




            
