#!/usr/bin/python
#
#
# R Kwee, April 2012

import os, math, time, ROOT, sys
from ROOT import *
from optparse import OptionParser
from array import array as ar
from helpers import mylabel, mean,gitpath, stddev
from MDAnalysis_dict import vDictTCTs, vDictTCPs
## -----------------------------------------------------------------------------------
parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", type="string",
                  help="Input file with TIMBER data")


(options, args) = parser.parse_args()
## -----------------------------------------------------------------------------------
debug  = 1

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

def doGraph( col, k, xarray, yarray):
  
    kname = getkname(k) 
    gr = TGraph( len(xarray), ar('d',xarray), ar('d',yarray) )
    gr.SetName('gr_' + kname )
    gr.GetXaxis().SetLabelSize(0.04)
    gr.GetYaxis().SetTitleOffset(0.8)
    gr.SetMarkerColor(1)
    gr.SetMarkerStyle(23)
    gr.SetMarkerSize(1.2)
  
    return gr
            
## -----------------------------------------------------------------------------------
def doHistoLabels(scnt, k, xLabels, yarray):
    print "Filling histogram with yarray", yarray

    kname = 'hist_' + getkname(k) + "_" + str(scnt)
    xmin, xmax = -0.5, 5.5
    hist = TH1F(kname, kname, len(xLabels), xmin, xmax)

    if debug: print "Creating histogram", kname
    cnt = 1
    for y in yarray:
        hist.SetBinContent(cnt,y)
        cnt += 1

    cnt = 1
    for xl in xLabels:
        hist.GetXaxis().SetBinLabel(cnt,xl)
        cnt += 1
        
    hist.GetXaxis().SetLabelSize(0.07)
    return hist
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
    if debug: print peaksList

    peaks = [pDict[det][2] for det in pDict.keys()]
    peak = max( peaks )
    for det, ts_dt_peak in pDict.iteritems():
        if debug: print "searching for peak", peak, "in ", det
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

            noise = pDict[det][0]
            stddev = pDict[det][1]
            if noise-stddev > val:
                if debug: print "No signal in",det, ". Found larger noise", noise-stddev,"than value", val
                noise = val
            # substract pedestral, leave maximal stddev of noise.
            pedSubData += [ [ts, dt, val-noise+stddev] ]

        if debug: print "adding data of ", det

        tpList += [[det, pedSubData]]

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

def createKey(l):

    #l = "TCTs at 8.3#sigma, TCLAs at 14#sigma, on-momentum, B2V "
    if debug: print l.split()
    TCTsett = l.split()[2].split("#")[0]
    TCLAsett = l.split()[5].split("#")[0]
    rfSett = l.split()[6].split("-mom")[0]
    try: 
        beamplane = "_" + l.split()[7]
    except:
        beamplane = ""

    k = TCTsett + "_" + TCLAsett + "_" + rfSett + beamplane
    return k
## -----------------------------------------------------------------------------------    
def getPedDicts(tDict, doTCPs):

    # return by default pDict for TCTs

    from MDAnalysis_dict import timeNoise 
    pedDictTCTs = []
    pedDictTCPs = []

    for timetupel in timeNoise:
        pedDictTCTs += [ getPedestral(tDict, vDictTCTs, timetupel ) ]
        if doTCPs: pedDictTCPs += [ getPedestral(tDict, vDictTCPs, timetupel ) ]


    if doTCPs:
        return pedDictTCTs, pedDictTCPs
    else:
        return pedDictTCTs
## -----------------------------------------------------------------------------------    
def plotLossesForTimeRange(tDict):
    # ............................................................ 
    #     
    # 
    #
    # ............................................................

    from MDAnalysis_dict import timeSignal 

    pedDictTCTs, pedDictTCPs = getPedDicts(tDict,1)
    if len(pedDictTCTs) != len(timeSignal): 
        print "Error!!! ", len(pedDictTCTs), len(timeSignal)
        sys.exit()

    for i,timetupel in enumerate(timeSignal):

        pDictTCTs = pedDictTCTs[i]
        pDictTCPs = pedDictTCPs[i]
        
        doLossesVsTime(tDict, vDictTCTs, pDictTCTs, timetupel, "BLM_TCTs", 5e-9,1e-4)
        doLossesVsTime(tDict, vDictTCPs, pDictTCPs, timetupel, "BLM_TCPs", 5e-9,3e-3)

## -----------------------------------------------------------------------------------    
def getTCTlosses(ts_dt_peak, tDict, pDict):

    (ts_peak, dt, peak) = ts_dt_peak
    print "Searching for ts ", ts_peak, dt
    tpDict = subPedestral(tDict, vDictTCTs, pDict)

    delta = 60.
    npList = []
    for det in vDictTCTs.keys():
        
        detData = tpDict[det]

        if debug: print "Checking data of ", det

        for ts, dt, val in detData:

            normVal = val
            if peak: normVal /= peak
                
            if ts == ts_peak:
                npList += [ [det,normVal] ]
                if debug: print "Found exact same timestamp of peak and tct loss", normVal
                break
            elif (ts <= ts_peak+delta) and ts > ts_peak:
                npList += [ [det,normVal] ]
                if debug: print "Look for ts ", delta,"sec. after peak happened. Found", dt, normVal
                break

    if len(vDictTCTs.keys()) != len(npList):
        print "Expected ", len(vDictTCTs.keys()), " entries and have", len(npList)
        print "Exiting.. not yet."
        #sys.exit()

    if debug: print npList
    return npList

## -----------------------------------------------------------------------------------    
def prepYarray(loss_at_thisTCT, xLabels):

    yarray = [ 1e-16 for i in range(len(xLabels)) ]
    for settID, loss in loss_at_thisTCT:
        
        for xl in xLabels:
            tctSett = settID.split("_")[0]
            if settID.count(xl): 
                t = xLabels.index(tctSett)
                break

        yarray[t] = loss
            
    return yarray

## -----------------------------------------------------------------------------------    
def plotPeaks(tDict):
    # ............................................................ 
    #     
    # plot losses vs BLM for a certain time
    #
    # ............................................................
    from MDAnalysis_dict import timeNoise 

    pedDictTCTs = getPedDicts(tDict,0)
    timeRanges = [
        [ ('2015-08-28 05:54:00','2015-08-28 05:55:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, on-momentum, B1H "),
          ('2015-08-28 06:01:00','2015-08-28 06:02:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, on-momentum, B1V "),
          ('2015-08-28 06:03:00','2015-08-28 06:04:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, on-momentum, B2H "),
          ('2015-08-28 06:05:00','2015-08-28 06:06:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, on-momentum, B2V "),
      ],
        [ ('2015-08-28 05:54:00','2015-08-28 05:55:00', "TCTs at 8.3#sigma, TCLAs at 14#sigma, on-momentum, B1H "),
          ('2015-08-28 06:01:00','2015-08-28 06:02:00', "TCTs at 8.3#sigma, TCLAs at 14#sigma, on-momentum, B1V "),
          ('2015-08-28 06:03:00','2015-08-28 06:04:00', "TCTs at 8.3#sigma, TCLAs at 14#sigma, on-momentum, B2H "),
          ('2015-08-28 06:05:00','2015-08-28 06:06:00', "TCTs at 8.3#sigma, TCLAs at 14#sigma, on-momentum, B2V "),
      ],
        [ ('2015-08-28 06:16:00','2015-08-28 06:17:00', "TCTs at 8.8#sigma, TCLAs at 14#sigma, on-momentum, B1H "),
          ('2015-08-28 06:17:01','2015-08-28 06:18:00', "TCTs at 8.8#sigma, TCLAs at 14#sigma, on-momentum, B1V "),
          ('2015-08-28 06:20:01','2015-08-28 06:21:00', "TCTs at 8.8#sigma, TCLAs at 14#sigma, on-momentum, B2H "),
          ('2015-08-28 06:21:01','2015-08-28 06:22:00', "TCTs at 8.8#sigma, TCLAs at 14#sigma, on-momentum, B2V "),
      ],
        [ ('2015-08-28 06:24:01','2015-08-28 06:25:00', "TCTs at 9.3#sigma, TCLAs at 14#sigma, on-momentum, B1H "),
          ('2015-08-28 06:25:31','2015-08-28 06:26:30', "TCTs at 9.3#sigma, TCLAs at 14#sigma, on-momentum, B1V "),
          ('2015-08-28 06:26:51','2015-08-28 06:28:00', "TCTs at 9.3#sigma, TCLAs at 14#sigma, on-momentum, B2H "),
          ('2015-08-28 06:28:01','2015-08-28 06:29:00', "TCTs at 9.3#sigma, TCLAs at 14#sigma, on-momentum, B2V "),
      ],
        [ ('2015-08-28 06:30:31','2015-08-28 06:31:30', "TCTs at 9.8#sigma, TCLAs at 14#sigma, on-momentum, B1H "),
          ('2015-08-28 06:32:01','2015-08-28 06:33:00', "TCTs at 9.8#sigma, TCLAs at 14#sigma, on-momentum, B1V "),
          ('2015-08-28 06:36:01','2015-08-28 06:37:00', "TCTs at 9.8#sigma, TCLAs at 14#sigma, on-momentum, B2H "),
          ('2015-08-28 06:37:31','2015-08-28 06:38:20', "TCTs at 9.8#sigma, TCLAs at 14#sigma, on-momentum, B2V "),
      ],
        [ ('2015-08-28 06:40:11','2015-08-28 06:41:10', "TCTs at 10.3#sigma, TCLAs at 14#sigma, on-momentum, B1H "),
          ('2015-08-28 06:47:21','2015-08-28 06:48:20', "TCTs at 10.3#sigma, TCLAs at 14#sigma, on-momentum, B1V "),
          ('2015-08-28 06:52:01','2015-08-28 06:53:00', "TCTs at 10.3#sigma, TCLAs at 14#sigma, on-momentum, B2H "),
          ('2015-08-28 06:50:01','2015-08-28 06:51:00', "TCTs at 10.3#sigma, TCLAs at 14#sigma, on-momentum, B2V "),
      ],
        [ ('2015-08-28 07:32:00','2015-08-28 07:33:00', "TCTs at 8.3#sigma, TCLAs at 10#sigma, on-momentum, B1H "),
          ('2015-08-28 07:34:00','2015-08-28 07:35:00', "TCTs at 8.3#sigma, TCLAs at 10#sigma, on-momentum, B1V "),
          ('2015-08-28 07:35:00','2015-08-28 07:36:00', "TCTs at 8.3#sigma, TCLAs at 10#sigma, on-momentum, B2H "),
          ('2015-08-28 07:36:00','2015-08-28 07:37:00', "TCTs at 8.3#sigma, TCLAs at 10#sigma, on-momentum, B2V "),
      ],
        [ ('2015-08-28 07:40:00','2015-08-28 07:41:00', "TCTs at 8.8#sigma, TCLAs at 10#sigma, on-momentum, B1H "),
          ('2015-08-28 07:41:50','2015-08-28 07:42:50', "TCTs at 8.8#sigma, TCLAs at 10#sigma, on-momentum, B1V "),
          ('2015-08-28 07:43:00','2015-08-28 07:44:00', "TCTs at 8.8#sigma, TCLAs at 10#sigma, on-momentum, B2H "),
          ('2015-08-28 07:44:01','2015-08-28 07:45:00', "TCTs at 8.8#sigma, TCLAs at 10#sigma, on-momentum, B2V "),
      ],
        [ ('2015-08-28 07:46:00','2015-08-28 07:47:00', "TCTs at 9.8#sigma, TCLAs at 10#sigma, on-momentum, B1H "),
          ('2015-08-28 07:47:01','2015-08-28 07:48:00', "TCTs at 9.8#sigma, TCLAs at 10#sigma, on-momentum, B1V "),
          ('2015-08-28 07:48:01','2015-08-28 07:49:00', "TCTs at 9.8#sigma, TCLAs at 10#sigma, on-momentum, B2H "),
          ('2015-08-28 07:49:01','2015-08-28 07:50:00', "TCTs at 9.8#sigma, TCLAs at 10#sigma, on-momentum, B2V "),
      ],
        [ ('2015-08-28 07:51:00','2015-08-28 07:52:00', "TCTs at 7.8#sigma, TCLAs at 10#sigma, on-momentum, B1H "),
          ('2015-08-28 07:52:01','2015-08-28 07:53:00', "TCTs at 7.8#sigma, TCLAs at 10#sigma, on-momentum, B1V "),
          ('2015-08-28 07:53:01','2015-08-28 07:54:00', "TCTs at 7.8#sigma, TCLAs at 10#sigma, on-momentum, B2H "),
          ('2015-08-28 07:54:01','2015-08-28 07:55:00', "TCTs at 7.8#sigma, TCLAs at 10#sigma, on-momentum, B2V "),
      ],
        [ ('2015-08-28 08:08:00','2015-08-28 08:09:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, neg-off-momentum, B1H "),
          ('2015-08-28 08:10:00','2015-08-28 08:11:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, neg-off-momentum, B1V "),
          ('2015-08-28 08:11:51','2015-08-28 08:12:50', "TCTs at 7.8#sigma, TCLAs at 14#sigma, neg-off-momentum, B2H "),
          ('2015-08-28 08:13:00','2015-08-28 08:14:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, neg-off-momentum, B2V "),
      ],
        [ ('2015-08-28 08:18:00','2015-08-28 08:19:00', "TCTs at 8.8#sigma, TCLAs at 14#sigma, neg-off-momentum, B1H "),
          ('2015-08-28 08:19:01','2015-08-28 08:19:50', "TCTs at 8.8#sigma, TCLAs at 14#sigma, neg-off-momentum, B1V "),
          ('2015-08-28 08:20:51','2015-08-28 08:21:50', "TCTs at 8.8#sigma, TCLAs at 14#sigma, neg-off-momentum, B2H "),
          ('2015-08-28 08:21:00','2015-08-28 08:22:00', "TCTs at 8.8#sigma, TCLAs at 14#sigma, neg-off-momentum, B2V "),
      ],
        [ ('2015-08-28 08:25:20','2015-08-28 08:26:10', "TCTs at 9.8#sigma, TCLAs at 14#sigma, neg-off-momentum, B1H "),
          ('2015-08-28 08:26:11','2015-08-28 08:27:00', "TCTs at 9.8#sigma, TCLAs at 14#sigma, neg-off-momentum, B1V "),
          ('2015-08-28 08:27:51','2015-08-28 08:28:50', "TCTs at 9.8#sigma, TCLAs at 14#sigma, neg-off-momentum, B2H "),
          ('2015-08-28 08:29:00','2015-08-28 08:30:00', "TCTs at 9.8#sigma, TCLAs at 14#sigma, neg-off-momentum, B2V "),
      ],
        [ ('2015-08-28 08:31:20','2015-08-28 08:32:20', "TCTs at 9.8#sigma, TCLAs at 14#sigma, pos-off-momentum, B1H "),
          ('2015-08-28 08:32:41','2015-08-28 08:33:30', "TCTs at 9.8#sigma, TCLAs at 14#sigma, pos-off-momentum, B1V "),
          ('2015-08-28 08:33:40','2015-08-28 08:34:40', "TCTs at 9.8#sigma, TCLAs at 14#sigma, pos-off-momentum, B2H "),
          ('2015-08-28 08:35:00','2015-08-28 08:36:00', "TCTs at 9.8#sigma, TCLAs at 14#sigma, pos-off-momentum, B2V "),
      ],
        [ ('2015-08-28 08:36:50','2015-08-28 08:37:50', "TCTs at 8.8#sigma, TCLAs at 14#sigma, pos-off-momentum, B1H "),
          ('2015-08-28 08:38:00','2015-08-28 08:39:00', "TCTs at 8.8#sigma, TCLAs at 14#sigma, pos-off-momentum, B1V "),
          ('2015-08-28 08:40:00','2015-08-28 08:41:10', "TCTs at 8.8#sigma, TCLAs at 14#sigma, pos-off-momentum, B2H "),
          ('2015-08-28 08:41:30','2015-08-28 08:42:50', "TCTs at 8.8#sigma, TCLAs at 14#sigma, pos-off-momentum, B2V "),
      ],
        [ ('2015-08-28 08:44:00','2015-08-28 08:45:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, pos-off-momentum, B1H "),
          ('2015-08-28 08:45:01','2015-08-28 08:46:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, pos-off-momentum, B1V "),
          ('2015-08-28 08:46:01','2015-08-28 08:47:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, pos-off-momentum, B2H "),
          ('2015-08-28 08:47:01','2015-08-28 08:48:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, pos-off-momentum, B2V "),
      ],

    ]

    tctLossList = []

    for i,sett in enumerate(timeRanges):

        for timetupel in sett:
            print "-" * 80
            det, ts_dt_peak = getPeak( getPeaks(tDict, vDictTCPs, timetupel) )
            print "Found peak in ", det, ts_dt_peak, timetupel

            # create key from timeRange
            tR_key = createKey(timetupel[-1])

            tctLosses = getTCTlosses(ts_dt_peak, tDict, pedDictTCTs[i])
            tctLossList += [ (tR_key, tctLosses)]


    tctLossDict = dict(tctLossList)
    tkeys = tctLossDict.keys()
    tkeys.sort()
    print tkeys

    ## ...................................................................................
    
    # scan identifier
    scans = ["14_on", "10_on", "14_neg-off", "14_pos-off"]
    smark = [20 , 34 , 24, 23]

    xLabels = ["7.8", "8.3", "8.8", "9.3", "9.8", "10.3"]
    for det in vDictTCTs.keys():
        print "Preparing plot for ", det

        hists = []
        graphs = []
        mg = TMultiGraph()

        Beam = "B1"
        if det.count("B2"): Beam = "B2"

        Plane = "H"
        if det.count("TCTPV"): Plane = "V"

        IP = "IP1"
        if det.count("L5") or det.count("R5"): IP = "IP5"

        colcnt = 0
        for s,scan in enumerate(scans):
            print "In scan",  scan

            # get settings per scan
            keys_per_scan = []

            for tk in tkeys:
                if tk.count(scan) and tk.count(Beam+Plane): keys_per_scan += [tk]

            if 1: 
                print "Found these keys identifying the settings per scan", keys_per_scan

            # collect losses on this tct per setting

            loss_at_thisTCT = []
            for tk in keys_per_scan:

                tctLosses = tctLossDict[tk]

                for tct,loss in tctLosses:
                    if tct == det: 
                        loss_at_thisTCT += [ [tk, loss] ]
                        # dont really need other losses...
                        break

            if debug: print "loss_at_thisTCT", loss_at_thisTCT
            yarray = prepYarray(loss_at_thisTCT, xLabels)
            if debug: print "yarray", yarray
            hists += [doHistoLabels(s, det, xLabels, yarray)]

        cv = TCanvas( 'cv', 'cv' , 10, 10, 900, 600 )
        cv.SetLogy(1)
        pname = getkname(det)
        YurMin, YurMax = 1e-6, 1e-1

        thelegend = TLegend(0.72,0.72,0.88,0.88)
        thelegend.SetFillColor(ROOT.kWhite)
        thelegend.SetShadowColor(ROOT.kWhite)
        thelegend.SetLineColor(ROOT.kWhite)
        thelegend.SetLineStyle(0)
        thelegend.SetTextSize(0.03)

        for h,hist in enumerate(hists):            
            if not h: hist.Draw("P")
            hist.Draw("PSAME")
            hist.GetYaxis().SetRangeUser(YurMin, YurMax)
            hist.GetXaxis().SetTitle("[#sigma]")
            hist.GetYaxis().SetTitle("normalised loss")
            hist.SetMarkerColor(vDictTCTs[det][0]+h)  
            hist.SetMarkerStyle(smark[h])        
            lText = scans[h]
            thelegend.AddEntry(hist,lText, 'p')

        thelegend.Draw()
        ml = mylabel(42)
        ml.SetTextSize(0.04)
        X1, Y1 = 0.23, 0.96
        ml.DrawLatex(X1, Y1, det)

        print "Saving", pname 
        cv.Print(pname + ".png" )

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
    fname = "TIMBER_DATA_BLMs_20152808_default_MDB.csv"
    fname = "TIMBER_DATA_BLMs_20152808_default_MDB.csv"

    tDict = dictionizeData(fname)
    #plotLossesForTimeRange(tDict)
    plotPeaks(tDict)
    
