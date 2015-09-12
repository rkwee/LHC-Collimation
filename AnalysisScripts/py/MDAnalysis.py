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
import sys
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

    "BLMTI.04R1.B2I10_TCTPH.4R1.B2:LOSS_RS09" : [kCyan+2, 27, ],
    "BLMTI.04R1.B2I10_TCTPV.4R1.B2:LOSS_RS09" : [kGreen-2,28, ],
    "BLMTI.04R5.B2I10_TCTPH.4R5.B2:LOSS_RS09" : [kPink-3, 26, ],
    "BLMTI.04R5.B2I10_TCTPV.4R5.B2:LOSS_RS09" : [kPink+1, 28, ],
}

# not only primaries....
vDictTCPs = {  

    "BLMEI.06L7.B1E10_TCHSV.6L7.B1:LOSS_RS09" : [kYellow+2, 20], 
    "BLMEI.06L7.B1E10_TCP.A6L7.B1:LOSS_RS09" : [kOrange+6, 24,], 
    "BLMEI.06L7.B1E10_TCSM.A6L7.B1:LOSS_RS09" : [kOrange+4, 28,], 
    "BLMEI.06R7.B2I10_TCHSV.6R7.B2:LOSS_RS09" : [kOrange+3, 26,], 
    "BLMEI.06R7.B2I10_TCP.A6R7.B2:LOSS_RS09" : [kOrange+2, 28,],
    "BLMEI.06R7.B2I10_TCSM.A6R7.B2:LOSS_RS09" : [kOrange+1, 27,],
    "BLMTI.06L7.B2I10_TCLA.A6L7.B2:LOSS_RS09" : [kYellow-2, 33,],
    "BLMTI.06L7.B2I10_TCLA.B6L7.B2:LOSS_RS09" : [kYellow-8,  34,], 
    "BLMTI.06R7.B1E10_TCLA.A6R7.B1:LOSS_RS09" : [kYellow+7,  22,], 
    "BLMTI.06R7.B1E10_TCLA.B6R7.B1:LOSS_RS09" : [kYellow+3,  23,],

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
    legname = k.split("_")[1]

    #if k.count("BLM"): legname = "BLM_"
    if k.count("TC"): legname += ".TC" + k.split("TC")[-1].split("_LOSS")[0]
    return legname.replace("_", ".")    

## -----------------------------------------------------------------------------------

def doGraphTimeAxis(vDict, k, xarray, yarray):
  
    kname = getkname(k) 
    gr = TGraph( len(xarray), ar('d',xarray), ar('d',yarray) )
    gr.SetName('gr_' + kname )

    gr.GetXaxis().SetTimeDisplay(1)
    gr.GetXaxis().GetTimeFormatOnly() 
    gr.GetXaxis().SetTimeFormat("%H:%M:%S")
    gr.GetXaxis().SetLabelSize(0.04)
    gr.GetXaxis().SetTitle("local time")
    if k.count("BLM"): gr.GetYaxis().SetTitle("Gy/s")
    gr.GetYaxis().SetTitleOffset(0.9)
    gr.SetMarkerColor(vDict[k][0])
    gr.SetMarkerStyle(vDict[k][1])
    gr.SetMarkerSize(1.2)
  
    return gr
## -----------------------------------------------------------------------------------

def doGraphDetAxis(vDict, k, xarray, yarray):
  
    kname = getkname(k) 
    gr = TGraph( len(xarray), ar('d',xarray), ar('d',yarray) )
    gr.SetName('gr_' + kname )
    for i,det in enumerate(detLabels):
        gr.GetXaxis().SetBinLabel(i+1, det)

    gr.GetXaxis().SetLabelSize(0.04)

    if k.count("BLM"): gr.GetYaxis().SetTitle("Gy/s")
    gr.GetYaxis().SetTitleOffset(0.8)
    gr.SetMarkerColor(vDict[k][0])
    gr.SetMarkerStyle(vDict[k][1])
    gr.SetMarkerSize(1.2)
  
    return gr
            
## -----------------------------------------------------------------------------------
#def doHistoPeak(pDict):

    # pDict has structure key: [ts, dt, peakval]

    #kname = 'peakhisto_' + str(ts)
    #hist = TH1F(kname, kname, len(xarray), min(xarray), max(xarray) )
    #for det in pDict.keys():


    # 
    # col  =  vDict[k][0]

    # print "Creating histogram", kname


    # cnt = 1
    # for y in yarray:
    #     hist.SetBinContent(cnt,y)
    #     cnt += 1

    # hist.GetXaxis().SetTimeDisplay(1)
    # hist.GetXaxis().SetTimeFormat("%H:%M:%S")
    # hist.GetXaxis().SetLabelSize(0.04)
    # hist.GetXaxis().SetTitle("local time")
    # if k.count("BLM"): hist.GetYaxis().SetTitle("Gy/s")
    # hist.GetYaxis().SetTitleOffset(0.8)
    # hist.SetMarkerColor(col)  
    
    # return hist
## -----------------------------------------------------------------------------------
def getPedestral(tDict, vDict, timetupel):
    #
    # returns dict with timber var as keys and corresponding 
    # averaged pedestral for time period
    # 
    #

    (dtStart, dtEnd, labText) = timetupel

    tsStart = stringDateToTimeStamp(dtStart)
    tsEnd   = stringDateToTimeStamp(dtEnd)

    pedList = []

    if debug: 
        print "Starting time", dtStart
        print "Ending time", dtEnd
    vars = vDict.keys()

    for det in vDict.keys():

        xarray, yarray = [], []
        if debug: print "timber var ", det
        detData = tDict[det]        

        for ts, dt, val in detData:
            if ts > tsEnd or ts <= tsStart: 
                continue
            yarray += [val]

        meanPedestral = mean(yarray)
        stddevPed = stddev(yarray)

        pedList  +=  [(det, [meanPedestral, stddevPed])]

    pedDict  = dict(pedList)
    if debug: print "pedDict", pedDict
    return pedDict
## -----------------------------------------------------------------------------------
def getPeaks(tDict, vDict, timetupel):
    #
    # return dict with timber var as keys and 
    # corresponding maximum value and time stamps (ts, dt, max)
    # within given time interval
    #
    #
    (dtStart, dtEnd, labText) = timetupel

    tsStart = stringDateToTimeStamp(dtStart)
    tsEnd   = stringDateToTimeStamp(dtEnd)

    peakList, peakListAll = [],[]

    if debug: 
        print "Starting time", dtStart
        print "Ending time", dtEnd
    vars = vDict.keys()

    for det in vDict.keys():

        x_ts, x_dt, yarray = [],[],[]
        if debug: print "in getPeaks:timber var ", det
        detData = tDict[det]        

        for ts, dt, val in detData:
            if ts > tsEnd or ts <= tsStart: 
                continue
            yarray += [val]
            x_ts += [ts]
            x_dt += [dt]

        maxval = max(yarray)
        indexmax = yarray.index(maxval)
        peakList +=  [(  det,[x_ts[indexmax], x_dt[indexmax], maxval]  )]

    peakDict = dict(peakList)
    if debug: print "peakDict", peakDict

    return peakDict

## -----------------------------------------------------------------------------------
def getPeak(pDict):

    peaksList = [(det,pDict[det][2]) for det in pDict.keys()]
    print peaksList

    peaks = [pDict[det][2] for det in pDict.keys()]
    peak = max( peaks )
    for det, ts_dt_peak in pDict.iteritems():
        print "searching for peak", peak, "in ", det
        if peak in ts_dt_peak:
            return det, ts_dt_peak

## -----------------------------------------------------------------------------------
def subPedestral(tDict, vDict, pDict):

    # 
    # return dictionary with same structure as tDict but with pedestral substracted data
    # det: [ts, dt, val-ped]
    #
    # should only be applied to vDictTCTs and vDictTCPs
    tpList = []
    for det in vDict.keys():
        
        if debug: print "timber var ", det
        detData = tDict[det]        

        # pedestral substracted data
        pedSubData = []
        for ts, dt, val in detData:

            # substract pedestral
            pedSubData += [ [ts, dt, val-pDict[det][0]] ]

        print "adding data of ", det
        tpList += [(det, pedSubData)]

    return dict(tpList)
## -----------------------------------------------------------------------------------    
def doLossesVsTime(tDict, vDict, pDict, timetupel, pname, YurMin, YurMax):

    tpDict = subPedestral(tDict, vDict, pDict)

    hists = []
    graphs, graphsPed = [],[]

    ml = mylabel(42)
    ml.SetTextSize(0.06)
    X1, Y1 = 0.12, 0.88

    (dtStart, dtEnd, labText) = timetupel

    tsStart = stringDateToTimeStamp(dtStart)
    tsEnd   = stringDateToTimeStamp(dtEnd)

    if debug: 
        print "Starting time", dtStart
        print "Ending time", dtEnd

    # ............................................................ 
    # first graph : no noise substraction

    vars = vDict.keys()

    for det in vars:
        xarray, yarray, yarrayPed = [],[],[]
        if debug: print "timber var ", det
        detData = tDict[det]        

        for ts, dt, val in detData:

            if ts > tsEnd or ts <= tsStart: 
                continue

            if debug: print "at", dt, "have", val

            yarray += [val]
            xarray += [ts]
        
        if debug: print "Counted", len(xarray), "time points"
        graphs   += [doGraphTimeAxis(vDict, det, xarray, yarray)]

    # ............................................................ 
    # second graph : with noise substraction

    for det in vars:
        xarray, yarrayPed = [],[]

        # use noise substracted data
        detData = tpDict[det]        
        
        for ts, dt, val in detData:

            if ts > tsEnd or ts <= tsStart: 
                continue

            yarrayPed += [val]
            xarray += [ts]
        
        if debug: print "Counted", len(xarray), "time points"
        graphsPed+= [doGraphTimeAxis(vDict, det, xarray, yarrayPed)]
    # ............................................................ 
    # actual plots

    a,b,doLogy = 1,2,1
    cv = TCanvas( 'cv', 'cv' , 10, 10, a*1200, b*500 )

    # great root needs some Timeoffset
    da = TDatime(2002,01,01,02,00,00)
    cv.Divide(a,b)

    thelegend = TLegend(0.865,0.53,0.94,0.95)
    thelegend.SetFillColor(ROOT.kWhite)
    thelegend.SetShadowColor(ROOT.kWhite)
    thelegend.SetLineColor(ROOT.kWhite)
    thelegend.SetLineStyle(0)
    thelegend.SetTextSize(0.03)

    mg    = TMultiGraph(pname, pname)
    mgPed = TMultiGraph(pname+"Ped", pname+"Ped")
    for gr in graphs:

        kname = gr.GetName()
        lText = legendName(kname)
        thelegend.AddEntry(gr,lText, 'p')
        mg.Add(gr)

    for gr in graphsPed:
        mgPed.Add(gr)

    cv.cd(1)
    gStyle.SetTimeOffset(da.Convert())
    gPad.SetLogy(doLogy)
    gPad.SetLeftMargin(-0.09)
    gPad.SetRightMargin(0.14)
    gPad.SetGridx(1)

    mg.Draw('ap')
    mg.GetXaxis().SetTimeDisplay(1)
    mg.GetXaxis().SetTimeFormat("%H:%M:%S")
    mg.GetXaxis().SetLabelSize(0.04)
    mg.GetXaxis().SetTitle("local time")
    mg.GetYaxis().SetRangeUser(YurMin, YurMax)
    mg.GetYaxis().SetTitle("Gy/s")
    mg.GetYaxis().SetTitleOffset(0.98)
    ml.DrawLatex(X1, Y1, "with pedestral")
    ml.DrawLatex(X1, Y1+0.075, labText)
    thelegend.Draw()

    cv.cd(2)
    gStyle.SetTimeOffset(da.Convert())
    gPad.SetLogy(doLogy)
    gPad.SetLeftMargin(-0.09)
    gPad.SetRightMargin(0.14)
    gPad.SetGridx(1)

    mgPed.Draw('ap')
    mgPed.GetXaxis().SetTimeDisplay(1)
    mgPed.GetXaxis().SetTimeFormat("%H:%M:%S")
    mgPed.GetXaxis().SetLabelSize(0.04)
    mgPed.GetXaxis().SetTitle("local time")
    mgPed.GetYaxis().SetRangeUser(YurMin, YurMax)
    mgPed.GetYaxis().SetTitle("Gy/s")
    mgPed.GetYaxis().SetTitleOffset(0.8)

    thelegend.Draw()

    ml.DrawLatex(X1, Y1, "noise substracted")
    ml.DrawLatex(X1, Y1+0.075, labText)

    TCTsett = labText.split()[2].split("#")[0]
    TCLAsett = labText.split()[5].split("#")[0]
    rfSett = labText.split()[6].split("-mom")[0]
    pname += "_TCT" + TCTsett + "_TCLA" + TCLAsett + "_" + rfSett
    print "Saving", pname
    cv.Print(pname + ".png" )
## -----------------------------------------------------------------------------------    
def plotLossesForTimeRange(tDict):
    # ............................................................ 
    #     
    # 
    #
    # ............................................................

    timeNoise  = [
        ('2015-08-28 05:50:00','2015-08-28 05:54:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, on-momentum"),       # 1
        ('2015-08-28 06:06:00','2015-08-28 06:08:20', "TCTs at 8.3#sigma, TCLAs at 14#sigma, on-momentum"),       # 2
        ('2015-08-28 06:13:01','2015-08-28 06:15:59', "TCTs at 8.8#sigma, TCLAs at 14#sigma, on-momentum"),       # 3
        ('2015-08-28 06:23:00','2015-08-28 06:24:10', "TCTs at 9.3#sigma, TCLAs at 14#sigma, on-momentum"),       # 4
        ('2015-08-28 06:29:01','2015-08-28 06:30:10', "TCTs at 9.8#sigma, TCLAs at 14#sigma, on-momentum"),       # 5
        ('2015-08-28 06:39:01','2015-08-28 06:40:20', "TCTs at 10.3#sigma, TCLAs at 14#sigma, on-momentum"),      # 6

        ('2015-08-28 07:28:00','2015-08-28 07:31:00', "TCTs at 8.3#sigma, TCLAs at 10#sigma, on-momentum"),       # 7
        ('2015-08-28 07:38:00','2015-08-28 07:40:00', "TCTs at 8.8#sigma, TCLAs at 10#sigma, on-momentum"),       # 8
        ('2015-08-28 07:45:30','2015-08-28 07:46:20', "TCTs at 9.8#sigma, TCLAs at 10#sigma, on-momentum"),       # 9
        ('2015-08-28 07:50:00','2015-08-28 07:51:30', "TCTs at 7.8#sigma, TCLAs at 10#sigma, on-momentum"),      # 10

        ('2015-08-28 08:02:00','2015-08-28 08:05:20', "TCTs at 7.8#sigma, TCLAs at 14#sigma, neg-off-momentum"), # 11
        ('2015-08-28 08:15:00','2015-08-28 08:17:20', "TCTs at 8.8#sigma, TCLAs at 14#sigma, neg-off-momentum"), # 12
        ('2015-08-28 08:23:00','2015-08-28 08:25:00', "TCTs at 9.8#sigma, TCLAs at 14#sigma, neg-off-momentum"), # 13

        ('2015-08-28 08:31:00','2015-08-28 08:31:20', "TCTs at 9.8#sigma, TCLAs at 14#sigma, pos-off-momentum"), # 14
        ('2015-08-28 08:39:00','2015-08-28 08:40:00', "TCTs at 8.8#sigma, TCLAs at 14#sigma, pos-off-momentum"), # 15
        ('2015-08-28 08:43:00','2015-08-28 08:44:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, pos-off-momentum"), # 16

    ]

    pedDictTCTs = []
    pedDictTCPs = []

    for timetupel in timeNoise:
        pedDictTCTs += [ getPedestral(tDict, vDictTCTs, timetupel ) ]
        pedDictTCPs += [ getPedestral(tDict, vDictTCPs, timetupel ) ]



    timeSignal = [

        ('2015-08-28 05:50:00','2015-08-28 06:06:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, on-momentum"),       # 1
        ('2015-08-28 06:06:01','2015-08-28 06:13:00', "TCTs at 8.3#sigma, TCLAs at 14#sigma, on-momentum"),       # 2
        ('2015-08-28 06:13:01','2015-08-28 06:23:00', "TCTs at 8.8#sigma, TCLAs at 14#sigma, on-momentum"),       # 3
        ('2015-08-28 06:23:01','2015-08-28 06:29:00', "TCTs at 9.3#sigma, TCLAs at 14#sigma, on-momentum"),       # 4
        ('2015-08-28 06:29:01','2015-08-28 06:39:00', "TCTs at 9.8#sigma, TCLAs at 14#sigma, on-momentum"),       # 5
        ('2015-08-28 06:39:01','2015-08-28 06:53:00', "TCTs at 10.3#sigma, TCLAs at 14#sigma, on-momentum"),      # 6
        ('2015-08-28 07:20:01','2015-08-28 07:38:00', "TCTs at 8.3#sigma, TCLAs at 10#sigma, on-momentum"),       # 7
        ('2015-08-28 07:38:01','2015-08-28 07:45:30', "TCTs at 8.8#sigma, TCLAs at 10#sigma, on-momentum"),       # 8
        ('2015-08-28 07:45:31','2015-08-28 07:50:00', "TCTs at 9.8#sigma, TCLAs at 10#sigma, on-momentum"),       # 9
        ('2015-08-28 07:50:01','2015-08-28 07:55:00', "TCTs at 7.8#sigma, TCLAs at 10#sigma, on-momentum"),      # 10
        ('2015-08-28 07:58:01','2015-08-28 08:14:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, neg-off-momentum"), # 11
        ('2015-08-28 08:14:01','2015-08-28 08:22:00', "TCTs at 8.8#sigma, TCLAs at 14#sigma, neg-off-momentum"), # 12
        ('2015-08-28 08:22:01','2015-08-28 08:30:00', "TCTs at 9.8#sigma, TCLAs at 14#sigma, neg-off-momentum"), # 13
        ('2015-08-28 08:30:01','2015-08-28 08:36:00', "TCTs at 9.8#sigma, TCLAs at 14#sigma, pos-off-momentum"), # 14
        ('2015-08-28 08:36:01','2015-08-28 08:43:00', "TCTs at 8.8#sigma, TCLAs at 14#sigma, pos-off-momentum"), # 15
        ('2015-08-28 08:43:01','2015-08-28 08:48:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, pos-off-momentum"), # 16
    ]


    if len(timeNoise) != len(timeSignal): 
        print "Error!!! ", len(timeNoise), len(timeSignal)
        sys.exit()

    for i,timetupel in enumerate(timeSignal):

        pDictTCTs = pedDictTCTs[i]
        pDictTCPs = pedDictTCPs[i]
        
        doLossesVsTime(tDict, vDictTCTs, pDictTCTs, timetupel, "BLM_TCTs", 5e-9,1e-4)
        doLossesVsTime(tDict, vDictTCPs, pDictTCPs, timetupel, "BLM_TCPs", 5e-9,3e-3)

## -----------------------------------------------------------------------------------    
def plotPeaks(tDict):
    # ............................................................ 
    #     
    # plot losses vs BLM for a certain time
    #
    # ............................................................


    timeRanges = [
        ('2015-08-28 05:54:00','2015-08-28 05:55:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, on-momentum, B1H "),
        ('2015-08-28 06:01:00','2015-08-28 06:02:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, on-momentum, B1V "),
        ('2015-08-28 06:03:00','2015-08-28 06:04:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, on-momentum, B2H "),
        ('2015-08-28 06:05:00','2015-08-28 06:06:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, on-momentum, B2V "),

        ('2015-08-28 05:54:00','2015-08-28 05:55:00', "TCTs at 8.3#sigma, TCLAs at 14#sigma, on-momentum, B1H "),
        ('2015-08-28 06:01:00','2015-08-28 06:02:00', "TCTs at 8.3#sigma, TCLAs at 14#sigma, on-momentum, B1V "),
        ('2015-08-28 06:03:00','2015-08-28 06:04:00', "TCTs at 8.3#sigma, TCLAs at 14#sigma, on-momentum, B2H "),
        ('2015-08-28 06:05:00','2015-08-28 06:06:00', "TCTs at 8.3#sigma, TCLAs at 14#sigma, on-momentum, B2V "),

    ]
    for timetupel in timeRanges:
        print "-" * 80
        det, ts_dt_peak = getPeak( getPeaks(tDict, vDictTCPs, timetupel) )
        print "Found peak in ", det, ts_dt_peak, timetupel

        #doHistoPeak(pDict)
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

    #print "time.ctime(1) = ", time.ctime(1.) 
    fname = "TIMBER_DATA_BLMs_20152808_default.csv"

    tDict = dictionizeData(fname)
    plotLossesForTimeRange(tDict)
    #plotPeaks(tDict)
    
