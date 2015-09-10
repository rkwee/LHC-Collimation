#!/usr/bin/python
#
#
# R Kwee, April 2012

import os, math, time, ROOT
from ROOT import *
from optparse import OptionParser
from array import array as ar
# # # # # needs H4 folder # # # # # # # 
from helpers import mylabel, mean,gitpath, stddev

## -----------------------------------------------------------------------------------
parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", type="string",
                  help="Input file with TIMBER data")


(options, args) = parser.parse_args()
## -----------------------------------------------------------------------------------
debug  = 0

# dictionary of timber variables
vDictTCTs = {  
    "BLMTI.04L1.B1I10_TCTPH.4L1.B1:LOSS_RS09" : [kBlue,  33, ],
    "BLMTI.04L1.B1I10_TCTPV.4L1.B1:LOSS_RS09" : [kBlue-2,34, ],
    "BLMTI.04L5.B1I10_TCTPH.4L5.B1:LOSS_RS09" : [kRed+1, 22, ],
    "BLMTI.04L5.B1I10_TCTPV.4L5.B1:LOSS_RS09" : [kRed-2, 23, ],

    "BLMTI.04R1.B2I10_TCTPH.4R1.B2:LOSS_RS09" : [kGreen,  27, ],
    "BLMTI.04R1.B2I10_TCTPV.4R1.B2:LOSS_RS09" : [kGreen-2,28, ],
    "BLMTI.04R5.B2I10_TCTPH.4R5.B2:LOSS_RS09" : [kPink-3, 26, ],
    "BLMTI.04R5.B2I10_TCTPV.4R5.B2:LOSS_RS09" : [kPink+1, 28, ],
}

vDictTCPs = {  
    "BLMTI.06L3.B1I10_TCP.6L3.B1:LOSS_RS09"   : [kYellow-2, 33,],
    "BLMTI.06L7.B1E10_TCP.B6L7.B1:LOSS_RS09" : [kYellow-8,  34,],
    "BLMTI.06L7.B1E10_TCP.C6L7.B1:LOSS_RS09" : [kYellow+7,  22,],
    "BLMTI.06L7.B1E10_TCP.D6L7.B1:LOSS_RS09" : [kYellow+3,  23,],

    "BLMTI.06R3.B2E10_TCP.6R3.B2:LOSS_RS09" : [kOrange+1,  27,],
    "BLMTI.06R7.B2I10_TCP.B6R7.B2:LOSS_RS09" : [kOrange+2, 28,],
    "BLMTI.06R7.B2I10_TCP.C6R7.B2:LOSS_RS09" : [kOrange+3, 26,],
    "BLMTI.06R7.B2I10_TCP.D6R7.B2:LOSS_RS09" : [kOrange+4, 28,],

}

otherDict = {
# "TCLA.6L3.B2:MEAS_MOTOR_LD" : [],
# "TCLA.6L3.B2:MEAS_MOTOR_RD" : [],
# "TCLA.6R3.B1:MEAS_MOTOR_LD" : [],
# "TCLA.6R3.B1:MEAS_MOTOR_RD" : [],
# "TCLA.7L3.B2:MEAS_MOTOR_LD" : [],
# "TCLA.7L3.B2:MEAS_MOTOR_RD" : [],
# "TCLA.7R3.B1:MEAS_MOTOR_LD" : [],
# "TCLA.7R3.B1:MEAS_MOTOR_RD" : [],
# "TCLA.A5L3.B2:MEAS_MOTOR_LD" : [],
# "TCLA.A5L3.B2:MEAS_MOTOR_RD" : [],
# "TCLA.A5R3.B1:MEAS_MOTOR_LD" : [],
# "TCLA.A5R3.B1:MEAS_MOTOR_RD" : [],
# "TCLA.A6L7.B2:MEAS_MOTOR_LD" : [],
# "TCLA.A6L7.B2:MEAS_MOTOR_RD" : [],
# "TCLA.A6R7.B1:MEAS_MOTOR_LD" : [],
# "TCLA.A6R7.B1:MEAS_MOTOR_RD" : [],
# "TCLA.A7L7.B2:MEAS_MOTOR_LD" : [],
# "TCLA.A7L7.B2:MEAS_MOTOR_RD" : [],
# "TCLA.A7R7.B1:MEAS_MOTOR_LD" : [],
# "TCLA.A7R7.B1:MEAS_MOTOR_RD" : [],
# "TCLA.B5L3.B2:MEAS_MOTOR_LD" : [],
# "TCLA.B5L3.B2:MEAS_MOTOR_RD" : [],
# "TCLA.B5R3.B1:MEAS_MOTOR_LD" : [],
# "TCLA.B5R3.B1:MEAS_MOTOR_RD" : [],
# "TCLA.B6L7.B2:MEAS_MOTOR_LD" : [],
# "TCLA.B6L7.B2:MEAS_MOTOR_RD" : [],
# "TCLA.B6R7.B1:MEAS_MOTOR_LD" : [],
# "TCLA.B6R7.B1:MEAS_MOTOR_RD" : [],
# "TCLA.C6L7.B2:MEAS_MOTOR_LD" : [],
# "TCLA.C6L7.B2:MEAS_MOTOR_RD" : [],
# "TCLA.C6R7.B1:MEAS_MOTOR_LD" : [],
# "TCLA.C6R7.B1:MEAS_MOTOR_RD" : [],
# "TCLA.D6L7.B2:MEAS_MOTOR_LD" : [],
# "TCLA.D6L7.B2:MEAS_MOTOR_RD" : [],
# "TCLA.D6R7.B1:MEAS_MOTOR_LD" : [],
# "TCLA.D6R7.B1:MEAS_MOTOR_RD" : [],
# "TCTPH.4L1.B1:MEAS_MOTOR_LD" : [],
# "TCTPH.4L1.B1:MEAS_MOTOR_RD" : [],
# "TCTPH.4L5.B1:MEAS_MOTOR_LD" : [],
# "TCTPH.4L5.B1:MEAS_MOTOR_RD" : [],
# "TCTPH.4R1.B2:MEAS_MOTOR_LD" : [],
# "TCTPH.4R1.B2:MEAS_MOTOR_RD" : [],
# "TCTPH.4R5.B2:MEAS_MOTOR_LD" : [],
# "TCTPH.4R5.B2:MEAS_MOTOR_RD" : [],
# "TCTPV.4L1.B1:MEAS_MOTOR_LD" : [],
# "TCTPV.4L1.B1:MEAS_MOTOR_RD" : [],
# "TCTPV.4L5.B1:MEAS_MOTOR_LD" : [],
# "TCTPV.4L5.B1:MEAS_MOTOR_RD" : [],
# "TCTPV.4R1.B2:MEAS_MOTOR_LD" : [],
# "TCTPV.4R1.B2:MEAS_MOTOR_RD" : [],
# "TCTPV.4R5.B2:MEAS_MOTOR_LD" : [],
# "TCTPV.4R5.B2:MEAS_MOTOR_RD" : [],

}

## -----------------------------------------------------------------------------------

def stringDateToTimeStamp(sDateTime):

    # 2015-06-07 17:10:45.604
    pattern = "%Y-%m-%d %H:%M:%S"
    sStruct = time.strptime(sDateTime, pattern)

    ts = time.mktime(sStruct)
    return ts

## -----------------------------------------------------------------------------------

def dictionizeData(fname):

    #  collect data in list (actually in tDict)
    tDict = {}


    print "Creating dictionary from file", fname
    with open(fname) as myfile:
        for i,line in enumerate(myfile):

            if line.count('VARIABLE'):

                key = line.split()[-1]

                # intialise
                if key not in tDict:
                    tDict[key] = []
                    if debug: 
                        print len(tDict)
                        print 'adding' , key

            elif line.count("Value") or line.startswith('#'):
                continue

            elif len(line.split()) == 2:

                # UTC date time, human readable
                dt = line.split(',')[0].split('.')[0]

                # UTC timestamp in seconds, add shift to convert to local cern time
                ts = stringDateToTimeStamp(dt) 

                # value
                val = float(line.split(',')[-1])

                # save into list
                tDict[key] += [[ts, dt, val]]


    # check if timestamps are about the same

    keys = tDict.keys()
 
    if debug: print 'have data from ',len(keys),' detectors'
    return tDict
## -----------------------------------------------------------------------------------

def getkname(k):
    if k.count('.'):
        kname = k.replace('.', '_')
    else:
        kname = k

    if kname.count(":"):
        kname = kname.replace(':', '_')
    else:
        kname = k

    if kname.endswith('.csv'): kname = kname.split('.')[0]
    return kname

def legendName(k):
    legname = ""

    #if k.count("BLM"): legname = "BLM_"
    if k.count("TC"): legname += "TC" + k.split("TC")[-1].split("_LOSS")[0]
    return legname.replace("_", ".")    

## -----------------------------------------------------------------------------------

def doGraph(vDict, k, xarray, yarray):
  
    kname = getkname(k) 
    gr = TGraph( len(xarray), ar('d',xarray), ar('d',yarray) )
    gr.SetName('gr_' + kname )

    gr.GetXaxis().SetTimeDisplay(1)
    gr.GetXaxis().SetTimeFormat("%H:%M:%S")
    gr.GetXaxis().SetLabelSize(0.04)
    gr.GetXaxis().SetTitle("local time")
    if k.count("BLM"): gr.GetYaxis().SetTitle("Gy/s")
    gr.GetYaxis().SetTitleOffset(0.8)
    gr.SetMarkerColor(vDict[k][0])
    gr.SetMarkerStyle(vDict[k][1])
    gr.SetMarkerSize(1.2)
  
    return gr
            
## -----------------------------------------------------------------------------------
def doHisto(vDict, k, xarray, yarray):

    kname = 'hist_' + getkname(k)
    col  =  vDict[k][0]

    print "Creating histogram", kname
    hist = TH1F(kname, kname, len(xarray), min(xarray), max(xarray) )

    cnt = 1
    for y in yarray:
        hist.SetBinContent(cnt,y)
        cnt += 1

    hist.GetXaxis().SetTimeDisplay(1)
    hist.GetXaxis().SetTimeFormat("%H:%M:%S")
    hist.GetXaxis().SetLabelSize(0.04)
    hist.GetXaxis().SetTitle("local time")
    if k.count("BLM"): hist.GetYaxis().SetTitle("Gy/s")
    hist.GetYaxis().SetTitleOffset(0.8)
    hist.SetMarkerColor(col)  
    
    return hist
## -----------------------------------------------------------------------------------
def getPedestral(tDict, vDict, timetupel):

    (dtStart, dtEnd, labText) = timetupel

    tsStart = stringDateToTimeStamp(dtStart)
    tsEnd   = stringDateToTimeStamp(dtEnd)

    pList = []

    print "Starting time", dtStart
    print "Ending time", dtEnd
    vars = vDict.keys()

    for det in vDict.keys():

        xarray, yarray = [], []
        print "timber var ", det
        detData = tDict[det]        

        for ts, dt, val in detData:
            if ts > tsEnd or ts <= tsStart: 
                continue
            yarray += [val]



        meanPedestral = mean(yarray)
        stddevPed = stddev(yarray)

        pList +=  [(det, [meanPedestral, stddevPed])]

    pDict = dict(pList)
    print pDict
    return pDict

## -----------------------------------------------------------------------------------
def plotVarGroup(tDict, vDict, timetupel, pname):
    hists = []
    graphs = []

    ml = mylabel(42)
    ml.SetTextSize(0.06)
    X1, Y1 = 0.2, 0.88

    (dtStart, dtEnd, labText) = timetupel

    tsStart = stringDateToTimeStamp(dtStart)
    tsEnd   = stringDateToTimeStamp(dtEnd)

    print "Starting time", dtStart
    print "Ending time", dtEnd
    vars = vDict.keys()

    for det in vDict.keys():
        xarray, yarray = [], []
        print "timber var ", det
        detData = tDict[det]        

        for ts, dt, val in detData:

            if ts > tsEnd or ts <= tsStart: 
                continue

            print "at", dt, "have", val

            yarray += [val]
            xarray += [ts]

        print "Counted", len(xarray), "time points"
        hists += [doHisto(vDict, det, xarray, yarray)]
        graphs+= [doGraph(vDict, det, xarray, yarray)]


    a,b,doLogy = 1,1,1
    cv = TCanvas( 'cv', 'cv' , 10, 10, a*1200, b*500 )
    cv.Divide(a,b)
    cv.SetLogy(doLogy)
    cv.SetGridy(1)

    thelegend = TLegend(0.91,0.58,0.92,0.95)
    thelegend.SetFillColor(ROOT.kWhite)
    thelegend.SetShadowColor(ROOT.kWhite)
    thelegend.SetLineColor(ROOT.kWhite)
    thelegend.SetLineStyle(0)
    thelegend.SetTextSize(0.03)

    mg = TMultiGraph(pname, pname)
    for gr in graphs:

        kname = gr.GetName()
        lText = legendName(kname)
        thelegend.AddEntry(gr,lText, 'p')
        mg.Add(gr)


    mg.Draw('ap')
    mg.GetXaxis().SetTimeDisplay(1)
    mg.GetXaxis().SetTimeFormat("%H:%M:%S")
    mg.GetXaxis().SetLabelSize(0.04)
    mg.GetXaxis().SetTitle("local time")
    mg.GetYaxis().SetTitle("Gy/s")
    mg.GetYaxis().SetTitleOffset(0.8)

    thelegend.Draw()

    ml.DrawLatex(X1, Y1, labText.split(",")[0])
    ml.DrawLatex(X1-0.005, Y1-0.08, labText.split(",")[1])

    TCTsett = labText.split(",")[0].split("#")[0].split()[-1]
    TCLAsett = labText.split(",")[-1].split("#")[0].split()[-1]
    pname += "_TCT" + TCTsett + "_TCLA" + TCLAsett
    print "Saving", pname
    cv.Print(pname + ".png" )

def plotLossesForTimeRange():
    # ------------------------------------------------------------ 
    #     
    # 
    #
    # ------------------------------------------------------------

    fname = "TIMBER_DATA_BLMs_Positions_default.csv"

    tDict = dictionizeData(fname)

    timeNoise  = [
        ('2015-08-28 05:50:00','2015-08-28 05:52:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma"),
    ]

    for timetupel in timeNoise:
        pDictTCTs = getPedestral(tDict, vDictTCTs, timetupel )
        pDictTCPs = getPedestral(tDict, vDictTCPs, timetupel )


    timeRanges = [
        # ('2015-08-28 05:50:00','2015-08-28 06:06:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma"),
        # ('2015-08-28 06:06:01','2015-08-28 06:13:00', "TCTs at 8.3#sigma, TCLAs at 14#sigma"),
    ]

    for timetupel in timeRanges:
        plotVarGroup(tDict, vDictTCTs, timetupel, "BLM_TCTs")
        plotVarGroup(tDict, vDictTCPs, timetupel, "BLM_TCPs")

## -----------------------------------------------------------------------------------    

## -----------------------------------------------------------------------------------    
if __name__ == "__main__":

    gROOT.SetBatch()
    gROOT.Reset()
    gROOT.SetStyle("Plain")
    gStyle.SetOptStat(0)
    gStyle.SetPalette(1)
    gROOT.LoadMacro(gitpath + "AnalysisScripts/C/AtlasStyle.C")
    gROOT.LoadMacro(gitpath + "AnalysisScripts/C/AtlasUtils.C")
    SetAtlasStyle()

    plotLossesForTimeRange()
