#!/usr/bin/python
#
#
# R Kwee, April 2012

import os, math, time, ROOT
from ROOT import *
from optparse import OptionParser
from array import array as ar
# # # # # needs H4 folder # # # # # # # 
from helpers import mylabel, gitpath

## -----------------------------------------------------------------------------------
parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", type="string",
                  help="Input file with TIMBER data")


(options, args) = parser.parse_args()
#fname = options.filename
dpath = '/Users/rkwee/Documents/RHUL/work/beamgas/'
dpath = ''
path = dpath

foutname = 'bg'
doSave = 1
debug  = 1
## -----------------------------------------------------------------------------------
fills = [
#3819,
#3820,
#3824,
#3829,
# 3833,
# 3835,
#3846,
#3851,
3855,
#3857,
]

# dictionary of vacuum pressures and other timber variables
vDict    = {  ##position of vacuum pipe 0, YurMin 1, YurMax 2, beamcolor 3, lText 4, ytitle 5,

'VGI.220.1L1.X.PR' : ['at -22 m', 1, 1, kBlack, '', 'pressure [mbar]',  ],
'VGPB.220.1L1.X.PR' : ['at -22 m', 1, 1, kBlack, '', 'pressure [mbar]',  ],
'VGI.188.1R1.X.PR' : ['at 18.8 m', 1, 1, kBlack, '', 'pressure [mbar]',  ],
'VGPB.188.1R1.X.PR' : ['at 18.8 m', 1, 1, kBlack, '', 'pressure [mbar]',  ],
'VGI.188.1L1.X.PR' : ['at -18.8 m', 1, 1, kBlack, '', 'pressure [mbar]',  ],
'VGPB.188.1L1.X.PR' : ['at -18.8 m', 1, 1, kBlack, '', 'pressure [mbar]',  ],
'VGI.220.1R1.X.PR' : ['at 22 m', 1, 1, kBlack, '', 'pressure [mbar]',  ],
'VGPB.220.1R1.X.PR' : ['at 22 m', 1, 1, kBlack, '', 'pressure [mbar]',  ],
'VGPB.222.1R1.X.PR' : ['at 22.18 m', 1, 1, kBlack, '', 'pressure [mbar]',  ],
'VGPB.7.4R1.X.PR' : ['at 58.635 m', 1, 1, kBlack, '', 'pressure [mbar]',  ],
'VGPB.9.4R1.X.PR' : ['at 58.884 m', 1, 1, kBlack, '', 'pressure [mbar]',  ],

'LHC.BCTFR.A6R4.B1:BEAM_INTENSITY':['', 1e6, 2e12, kBlue, '', '#protons', '', ],
'LHC.BCTFR.A6R4.B2:BEAM_INTENSITY':['', 1e6, 2e12, kRed, '', '#protons', '', ],
#'LHC.STATS:ENERGY':['', 1e6, 2e12, kBlack, '', 'beam energy [GeV]', '', ],
'LHC.BOFSU:OFSU_ENERGY':['', 1e6, 2e12, kBlack, '', 'beam energy [GeV]', '', ],

'ATLAS:BKGD1':['', 1e6, 2e12, kCyan, '', 'ATLAS BKGD1', '', ],
'ATLAS:BKGD2':['', 1e6, 2e12, kCyan-1, '', 'ATLAS BKGD2', '', ],
'ATLAS:BKGD3':['', 1e6, 2e12, kCyan-2, '', 'ATLAS BKGD3', '', ],
'CMS:BKGD1':['', 1e6, 2e12, kMagenta, '', 'CMS BKGD1', '', ],
'CMS:BKGD2':['', 1e6, 2e12, kMagenta-1, '', 'CMS BKGD2', '', ],
'CMS:BKGD3':['', 1e6, 2e12, kMagenta-2, '', 'CMS BKGD3', '', ],
}

## -----------------------------------------------------------------------------------

def stringDateToTimeStamp(sDateTime):

    if sDateTime.startswith("2011"):
        pattern = "%Y-%m-%d %H:%M:%S"

    # 2015-06-07 17:10:45.604
    pattern = "%Y-%m-%d %H:%M:%S"
    sStruct = time.strptime(sDateTime, pattern)

    ts = time.mktime(sStruct)
    return ts

## -----------------------------------------------------------------------------------

def makeRootFile(fname, doHistos, doGraphs):
    kB = 1.3806503e-23 # J/K
    T  = 293        # K

    # shift UTC to local time (adding two hours)
    shift = 432000

    #  collect data in list (actually in tDict)
    tDict = {}

    fill = fname.split('fill')[-1]
    fill = fill.split('.')[0]
    
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

            elif len(line.split()) == 2 and not key.count('INTENSITY'):

                # UTC date time, human readable
                dt = line.split(',')[0].split('.')[0]

                # UTC timestamp in seconds, add shift to convert to local cern time
                ts = stringDateToTimeStamp(dt) 

                # pressure in mbar
                pr = float(line.split(',')[-1])

                # number of particles convert mbar->Pa 10^-3 x 10^5 = 100.
                np = pr*100./(kB*T)

                # save into list
                tDict[key] += [[ts, dt, pr]]

            elif len(line.split()) == 2 and key.count('INTENSITY'):

                # UTC date time, human readable
                dt = line.split(',')[0].split('.')[0]

                # UTC timestamp in seconds
                ts = stringDateToTimeStamp(dt) 

                # beam intensity
                bi = float(line.split(',')[-1])

                # zero suppressed
                if bi:
                # save into list
                    tDict[key] += [[ts, dt, bi]]

    # check if timestamps are about the same

    keys = tDict.keys()

    if debug: print 'have data from ',len(keys),' detectors'

    foutname = 'bg_' + str(fill) + '.root'
    rfile = TFile.Open(foutname, "RECREATE")
    print 'writing............', foutname

    goodHistos = []               
    for k in keys:
        nval = len(tDict[k])
        if debug: print 'detector',k, 'has', len(tDict[k]), 'entries'

        if not nval:
            print 'skipping detector ', k, tDict[k]
            continue        

        xarray, labels, yarray = [],[],[]

        for i in range(len(tDict[k])):

            x,l,y = tDict[k][i][0], tDict[k][i][1], tDict[k][i][2]
            xarray += [x]
            yarray += [y] #Scale here!
            labels += [l]


        if k in vDict.keys():

            if doHistos: 
                obj = doHisto(k, xarray, yarray)
                obj.Write()

            if doGraphs: 
                obj = doGraph(k, xarray, yarray)
                obj.Write()

            goodHistos += [k]
        else:
            print k, ' is not defined in vDict?', nval
        
    rfile.Close()
    return goodHistos

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

## -----------------------------------------------------------------------------------

def doGraph(k, xarray, yarray):
  
    kname = getkname(k)        
    gr = TGraph( len(xarray), ar('d',xarray), ar('d',yarray) )
    gr.SetName('gr_' + kname )

    gr.GetXaxis().SetTimeDisplay(1)
    gr.GetXaxis().SetTimeFormat("%d.%m. %H:%M")
    gr.GetXaxis().SetLabelSize(0.04)
    gr.GetXaxis().SetTitle("UTC time")
    gr.GetYaxis().SetTitleOffset(0.8)
    gr.SetMarkerStyle(20)
    gr.SetMarkerSize(0.9)
  
    return gr
            
## -----------------------------------------------------------------------------------
def doHisto( k, xarray, yarray):

    position, YurMin,YurMax = vDict[k][0], vDict[k][1], vDict[k][2]
    col  =  vDict[k][3]
    kname = 'hist_' + getkname(k)        
       
    hist = TH1F(kname, kname, len(xarray), min(xarray), max(xarray) )

    cnt = 1
    for y in yarray:
        hist.SetBinContent(cnt,y)
        cnt += 1

    hist.GetXaxis().SetTimeDisplay(1)
    hist.GetXaxis().SetTimeFormat("%d.%m. %H:%M")
    hist.GetXaxis().SetLabelSize(0.04)
    hist.GetXaxis().SetTitle("UTC time")
    hist.GetYaxis().SetTitleOffset(0.8)
    hist.SetMarkerColor(col)  
    hist.Draw("histpe")
    
    return hist

## -----------------------------------------------------------------------------------

def makeSeparatePlot(f,goodHistos):
    # ------------------------------------------------------------ 
    #     
    #  correlates beam intensity with pressure/beamgas density    
    #
    # ------------------------------------------------------------

    goodHistos.sort()
    fill = str(f)

    foutname = 'bg_' + str(f) + '.root'
    print 'opening ......', foutname
    rfile = TFile.Open(foutname)
    gr = []
    cnt = 0
    print rfile
    a,b  = 1, len(goodHistos)
    cv = TCanvas( 'cv' + str(f), 'cv' + str(f), 10, 10, a*1200, b*500 )
    cv.Divide(a,b)

    thelegend = TLegend(0.6,0.82,0.92,0.92)
    thelegend.SetFillColor(ROOT.kWhite)
    thelegend.SetShadowColor(ROOT.kWhite)
    thelegend.SetLineColor(ROOT.kWhite)
    thelegend.SetLineStyle(0)
    thelegend.SetTextSize(0.04)        

    xtitle = 'UTC time'
    xtitle = 'local CERN time'

    for k in goodHistos:
        cnt += 1
        # -- plot with vacuum values
        kname    = 'hist_' + getkname(k)
        thisgr = rfile.Get(kname)
        if not thisgr:
            print 'skipping graph for', k
            continue

        gr      += [thisgr]

        print 'retrieved......', kname, gr[-1]

        position = vDict[k][0]
        ytitle = vDict[k][5]

        cv.cd(cnt)            
        gr[-1].SetLineColor(vDict[k][3])
        gr[-1].GetYaxis().SetTitleOffset(0.8)
        gr[-1].SetMarkerSize(0.3)
        gr[-1].GetXaxis().SetTimeFormat("%d.%m. %Hh")
        gr[-1].GetYaxis().SetTitle(ytitle)
        gr[-1].GetXaxis().SetTitle(xtitle)
        lText = k + ' ' + vDict[k][4] + position
        X1, Y1 = 0.34, 0.98
        drawOpt = 'lp'
        gr[-1].Draw(drawOpt)
        ml = mylabel(42)
        ml.SetTextSize(0.06)
        ml.DrawLatex(X1, Y1, lText)

    pname = path + 'fill' + fill + '.png'
    print "Saving", pname
    cv.Print(pname)

## -----------------------------------------------------------------------------------    

def makeCommonPlot(fname):
    # ------------------------------------------------------------ 
    #     
    #  correlates beam intensity with pressure/beamgas density
    #  use TGraphs
    #
    # ------------------------------------------------------------

    print 'opening ......', fname
    rfile = TFile.Open(fname)
    vkeys = vDict.keys()
    vkeys.sort()
    for f in fills:

        gr = []
        cnt = 0

        a,b  = 1, 1
        cv = TCanvas( 'cv', 'cv', 10, 10, a*1000, b*400 )
        cv.Divide(a,b)

        thelegend = TLegend(0.6,0.82,0.92,0.92)
        thelegend.SetFillColor(ROOT.kWhite)
        thelegend.SetShadowColor(ROOT.kWhite)
        thelegend.SetLineColor(ROOT.kWhite)
        thelegend.SetLineStyle(0)
        thelegend.SetTextSize(0.04)        

        fill = str(f) 

        mg = TMultiGraph()

        for k in vkeys:

            cnt += 1
            if k.count('INTENSITY'): continue
            # -- plot with vacuum values
            kname    = getkname(k)
            gr      += [ rfile.Get(kname) ]
            print 'retrieved......', kname, gr[-1]
            
            position = vDict[k][0]
            ytitle = vDict[k][5]

            gr[-1].SetLineColor(vDict[k][3])
            gr[-1].GetYaxis().SetTitleOffset(0.8)
            gr[-1].SetMarkerSize(0.3)
            gr[-1].GetXaxis().SetTimeFormat("%d.%m. %Hh")
            gr[-1].GetYaxis().SetTitle(ytitle)
            lText = k + ' ' + vDict[k][4] + position
            thelegend.AddEntry(gr[-1],lText, 'p')

            mg.Add(gr[-1])

    mg.Draw('ap')

    ml = mylabel(42)
    ml.SetTextSize(0.06)
    X1, Y1 = 0.34, 0.98
    ml.DrawLatex(X1, Y1, 'LHC fill ' + fill)

    pname = path + 'fill' + fill + '.png'
    print "Saving", pname
    cv.Print(pname)

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

    for fill in fills:
        fname = 'TIMBER_DATA_localtime_fill'+str(fill)+'.csv'
        print 'reading file', fname

        goodHistos = makeRootFile(fname,1,1)
        makeSeparatePlot(fill,goodHistos)

    #calcInt()
