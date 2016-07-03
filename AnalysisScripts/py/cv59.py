#!/usr/bin/python
#
# Nov 2015, rkwee
## -------------------------------------------------------------------------------
# plot data lossmap
## -------------------------------------------------------------------------------
import helpers, subprocess, ROOT
from helpers import *
from ROOT import *
# -----------------------------------------------------------------------------------

def cv59():

    debug = 0

    thispath         = "/Users/rkwee/Documents/RHUL/work/" 
    thispath         = workpath 
    thispath         +=  "BLMDataAnalysis/lossmaps/"
    rawDataFileName1 = thispath + "20120402__LOSS_RS09__180500_1333382700__Data_Extract_BLMs_all.txt"
    rawDataFileName2 = thispath + "20120402__LOSS_RS09__181500_1333383300__Data_Extract_BLMs_all.txt"

    rawDataFileName3 = thispath + "20120701__LOSS_RS09__053500_1341113700__Data_Extract_BLMs_all.txt"
    rawDataFileName4 = thispath + "20120701__LOSS_RS09__054500_1341114300__Data_Extract_BLMs_all.txt"
    rawDataFileName5 = thispath + "20120701__LOSS_RS09__174500_1341157500__Data_Extract_BLMs_all.txt"
    rawDataFileName6 = thispath + "20120701__LOSS_RS09__175503_1341158103__Data_Extract_BLMs_all.txt"

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

    def getDataline(ts, rawDataFileName):
        cmd = 'grep ' + str(ts) + ' ' + rawDataFileName
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        myStdOut = process.stdout.read()
        dataline = myStdOut.split()
        return [float(d) for d in dataline]
 
    # .................................................................................................
    # -- get a specific line
    format = "%Y-%m-%d %H:%M:%S"
    lossmaps_dt = [
        # ['B1H_afterSqueeze_April', '2012-04-02 18:17:38', rawDataFileName2],
        # ['B1V_afterSqueeze_April', '2012-04-02 18:16:07', rawDataFileName2],
        # # ['B2H_afterSqueeze_April', '2012-04-02 18:14:50', rawDataFileName1],
        # # ['B2V_afterSqueeze_April', '2012-04-02 18:13:29', rawDataFileName1],

        # ['B1H_afterTS2', '2012-07-01 05:41:31', rawDataFileName3],
        # ['B1V_afterTS2', '2012-07-01 05:37:08', rawDataFileName3],
        # ['B2H_afterTS2', '2012-07-01 05:49:50', rawDataFileName4],
        # ['B2V_afterTS2', '2012-07-01 05:47:59', rawDataFileName4],

        ['B1H_afterSqueeze_July', '2012-07-01 18:00:26', rawDataFileName6, '2012-07-01 18:00:16', '2012-07-01 18:00:20'],
        # ['B1V_afterSqueeze_July', '2012-07-01 18:04:43', rawDataFileName6],
        # ['B2H_afterSqueeze_July', '2012-07-01 17:52:46', rawDataFileName5],
        # ['B2V_afterSqueeze_July', '2012-07-01 17:57:17', rawDataFileName6],

        ]

    # has as key B1H_xxx and as content a dict [blmName]: measurement
    dataList = []
    blmsPos  = blmPositionsDict.keys()

    for lossmapType, dt, rawDataFileName, noiseStart_dt, noiseEnd_dt in lossmaps_dt: 

        ## -- SIGNAL
        ts = int(stringDateToTimeStamp(dt,format))
        print "."*33, lossmapType, " lossmap took place at", dt, ' = ', ts

        blmsData = getBlmNames(rawDataFileName)
        #print "have",len(blmsData),"blms in ", rawDataFileName

        dataline = getDataline(ts, rawDataFileName)

        # check for position of each blm with data
        missingData, missingPos = [], []
        # for blm in blmsPos:
        #     if blm not in blmsData:
        #         missingData += [blm]

        # for blm in blmsData:
        #     if blm not in blmsPos:
        #         missingPos += [blm]

        # print "Missing data of ", len(missingData), "blms"#, missingData
        # print "Missing position of ", len(missingPos), "blms",# missingPos


        maxloss = max(dataline)
        indexmax = dataline.index(maxloss)
        blmMaxloss = blmsData[indexmax]
        print "Maximum loss", maxloss, "in ", blmMaxloss

        ## -- NOISE
        noiseStart_ts = int(stringDateToTimeStamp(noiseStart_dt,format))
        noiseEnd_ts   = int(stringDateToTimeStamp(noiseEnd_dt,format))

        datalineNoise = []
        for tsNoise in range(noiseStart_ts, noiseEnd_ts+1):
            datalineNoise += [ getDataline(tsNoise, rawDataFileName) ]


        if maxloss > 1.: 
            # remove bad data, this changes dataline
            dataline.pop(indexmax)
            # apply same change to the names, noise
            blmsData.pop(indexmax)
            datalineNoiseCleaned = []
            for dataNoise in datalineNoise:
                #print "dataNoise len before pop", len(dataNoise)
                dataNoise.pop(indexmax)
                #print "dataNoise len before pop", len(dataNoise)
                datalineNoiseCleaned += [dataNoise]


            maxloss = max(dataline)
            indexmax = dataline.index(maxloss)
            blmMaxloss = blmsData[indexmax]
            print "Unreasonable data loss in that blm. Next maximum is", maxloss, "in ", blmMaxloss
            datalineNoise = datalineNoiseCleaned


        # -- collect all info in new list->dict
        dataPerLossmap  = []
        noisePerLossmap = []
        for i,blm in enumerate(blmsData):
            dataPerLossmap += [ [blm, dataline[i] ]]
            noisePerLossmap += [ [blm, [dataNoise[i] for dataNoise in datalineNoise]] ]

        # save only good data
noisePerLossmapDict = dict(noise)
        dataList += [[lossmapType, [ dict(dataPerLossmap), missingData, missingPos, maxloss, dt, noisePerLossmapDict] ]]

    # make it a dict
    dataDict = dict(dataList)
    # .................................................................................................

    cv = []
    subfolder = 'TCT/4TeV/datalossmaps/'
    for dKey in dataDict.keys():
        print "-"*44, dKey,'-'*44
        # print "length of ", dKey, "is", len(dataDict[dKey][0])

        # data dictionary
        dataPerLossmapDict = dataDict[dKey][0]
        maxloss = dataDict[dKey][3]
        dt = dataDict[dKey][4]
        noisePerLossmap = dataDict[dKey][5]
        print 'have ', len(noisePerLossmap), 'entries for noise'

        # check missing positions
        missingPos = dataDict[dKey][2]
        if missingPos:
            for i,blm in enumerate(missingPos):
                print "Missing position of blm #",i, blm, ". Data is", dataPerLossmapDict[blm]

        # plot now good data
        tag, nbins, xmin, xmax = dKey, 266590, 0.1, 26659.
        blm_loss = TH1F("blm_loss" + tag,"blm_loss" + tag,nbins, xmin, xmax)
        noise_loss = TH1F("noise_loss" + tag,"noise_loss" + tag,nbins, xmin, xmax)

        a,b = 1,1
        cv += [ TCanvas( 'cv'+tag, 'cv'+tag, a*1500, b*700) ]
        cv[-1].SetLogy(1)
        cv[-1].SetLeftMargin(0.2)
        cv[-1].SetTopMargin(0.15)        
        cv[-1].SetTopMargin(0.15)        
        gStyle.SetOptStat(0)
        cv[-1].cd(1)
        for blm in dataPerLossmapDict.keys():
            spos = float(blmPositionsDict[blm][0])
            val  = dataPerLossmapDict[blm]

            # noiseVal = noisePerLossmapDict[blm]

            cv[-1].cd(1)
            #print "spos ", spos, val
            blm_loss.Fill(spos,val)

            # cv[-1].cd(2)
            # noise_loss.Fill(spos,noiseVal)

            # pname  = wwwpath
            # pname += subfolder + tag +'.png'

        cv[-1].cd(1)
        blm_loss.Scale(1./maxloss)
        blm_loss.GetYaxis().SetRangeUser(1e-8,1.1)
        blm_loss.GetYaxis().SetTitle("local cleaning inefficiency")

        blm_loss.Draw("HIST")
        lab = mylabel(42)
        lab.DrawLatex(0.3, 0.92, 'betatron lossmap at 4 TeV ' + dt)

        # cv[-1].cd(2)
        # noise_loss.Draw("HIST")

        pname  = thispath + tag +'.png'

        print('Saving file as ' + pname ) 
        cv[-1].SaveAs(pname)
