#!/usr/bin/python
#
# R Kwee-Hinzmann, 2013
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers
from ROOT import *
from helpers import *
from array import array
from fillTTree_dict import varList_4TeV, varList_HL,sDict,hDict_4TeV,hDict_HL_halo
# ---------------------------------------------------------------------------------
import optparse
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", type="string",
                  help="put the path of the merged fort.66 file from fluka runs")

(options, args) = parser.parse_args()

fname  = options.filename
# ---------------------------------------------------------------------------------
# setting variables

if fname.endswith("30"): 
    hDict   = hDict_HL_halo
else: 
    hDict   = hDict_4TeV


rfname = fname + '.root'
# ---------------------------------------------------------------------------------
def getColContent(colNumbers, particleTypes):

    cols, col = [], []

    with open(fname) as myfile:

        for line in myfile:       
            for colNumber in colNumbers:

                cline = line.split()
                pType = cline[pID]

                if particleTypes[0].count('ll'):
                    col  += [float(cline[colNumber])]
                elif pType in particleTypes: 
                    col  += [float(cline[colNumber])]

        cols += [array('d',col)]
        col   = []
    
    return cols
# ---------------------------------------------------------------------------------
def getXLogAxis(nbins, xmin, xmax):

    # exponent width
    width = 1./nbins*(math.log10(xmax) - math.log10(xmin))
    
    # axis with exponents only 
    xtmp  = [math.log10(xmin) + i * width for i in range(nbins+1)]
    
    # real axis in power of 10
    xaxis = [math.pow(10, xExp) for xExp in xtmp]

    return xaxis
# ---------------------------------------------------------------------------------
def do1dLogHisto(hname, colNumbers, xaxis, particleTypes):

    # expect only 1 list for Ekin histograms
    [col] = getColContent(colNumbers, particleTypes) 

    nbins = len(xaxis)-1
    hist  = TH1F(hname, hname, nbins, array('d', xaxis) )

    # store sum of squares of weights 
    hist.Sumw2()

    for colVal in col: hist.Fill(colVal)
   
    # This second loop changes the Get.Entries() value by number of bins!!
    for bin in range(1,nbins+1):
        content = hist.GetBinContent(bin)
        width   = hist.GetBinWidth(bin)
        bcenter = hist.GetXaxis().GetBinCenterLog(bin)
        #mybince = math.sqrt(hist.GetBinLowEdge(bin+1) * hist.GetBinLowEdge(bin))
        #print "mybincenter", mybince, "roots bincenter", bcenter
        hist.SetBinContent(bin,bcenter*content/width)
 
    return hist
# ---------------------------------------------------------------------------------
def do1dRadHisto(hname, colNumbers, xaxis, particleTypes):

    # expect 2 lists for radially-binned histograms
    [xcol, ycol, zcol, ekin] = getColContent(colNumbers, particleTypes) 

    ekinCut = sDict[hname][8]
    nbins   = len(xaxis)-1
    hist    = TH1F(hname, hname, nbins, array('d', xaxis))

    # store sum of squares of weights 
    hist.Sumw2()

    # this cut doesnt change anything. it may only for beamgas
    zmin, zmax = 2260., 14960.

    for i in range(len(xcol)): 
        if ekin[i] > ekinCut and zcol[i] > zmin and zcol[i] < zmax:
            hist.Fill(math.sqrt(xcol[i]**2 + ycol[i]**2))

    for i in range(nbins):
        binArea = math.pi * (xaxis[i+1]**2 - xaxis[i]**2)
        content = hist.GetBinContent(i)
        hist.SetBinContent(i,content/binArea)
 
    return hist
# ---------------------------------------------------------------------------------
def do1dRadEnHisto(hname, colNumbers, xaxis, particleTypes):

    # expect lists for radially-binned histograms
    [xcol, ycol, zcol, ekin] = getColContent(colNumbers, particleTypes) 

    nbins   = len(xaxis)-1
    hist    = TH1F(hname, hname, nbins, array('d', xaxis))

    # store sum of squares of weights 
    hist.Sumw2()

    # this cut doesnt change anything. it may only for beamgas
    zmin, zmax = 2260., 14960.

    for i,e in enumerate(ekin):
        if zcol[i] > zmin and zcol[i] < zmax:
            radius = math.sqrt(xcol[i]**2 + ycol[i]**2)
            bin = hist.FindBin(radius)
            hist.AddBinContent(bin,e)

    for i in range(nbins):
        binArea = math.pi * (xaxis[i+1]**2 - xaxis[i]**2)
        content = hist.GetBinContent(i)
        hist.SetBinContent(i,content/binArea)
 
    return hist

# ---------------------------------------------------------------------------------                                                                                                                                                                                                          
def do1dPhiHisto(hname, colNumbers, xaxis, particleTypes):

    # expect list for-binned histograms                                                                                                                                                                                                                                            
    [xcol, ycol, zcol, ekin] = getColContent(colNumbers, particleTypes)

    nbins   = len(xaxis)-1
    hist    = TH1F(hname, hname, nbins, array('d', xaxis))

    # store sum of squares of weights                                                                                                                                             
    hist.Sumw2()

    # this cut doesnt change anything. it may only for beamgas                                                                                                                                                                                                                               
    zmin, zmax = 2260., 14960.

    for i,e in enumerate(xcol):
        if zcol[i] > zmin and zcol[i] < zmax:

            phi = math.atan2(ycol[i], xcol[i])
            hist.Fill(phi)

    for i in range(nbins):
        content = hist.GetBinContent(i)
        hist.SetBinContent(i,content/hist.GetBinWidth(i))

    return hist
# ---------------------------------------------------------------------------------
def do1dPhiEnHisto(hname, colNumbers, xaxis, particleTypes):

    # expect list
    [xcol, ycol, zcol, ekin] = getColContent(colNumbers, particleTypes)

    nbins   = len(xaxis)-1
    hist    = TH1F(hname, hname, nbins, array('d', xaxis))

    # store sum of squares of weights
    hist.Sumw2()

    # this cut doesnt change anything. it may only for beamgas
    zmin, zmax = 2260., 14960.

    for i,e in enumerate(xcol):
        if zcol[i] > zmin and zcol[i] < zmax:

            phi = math.atan2(ycol[i], xcol[i])
            bin = hist.FindBin(phi)
            hist.AddBinContent(bin,ekin[i])

    for i in range(nbins):
        content = hist.GetBinContent(i)
        hist.SetBinContent(i,content/hist.GetBinWidth(i))

    return hist
# ---------------------------------------------------------------------------------
def saveRootFile():

    print 'writing ','.'*20, rfname
    rfile = TFile.Open(rfname, "RECREATE")

    for skey in sDict.keys():

        particleTypes = sDict[skey][0]
        hname         = skey
        colNumbers    = sDict[skey][1]
        nbins         = sDict[skey][2]
        xmin          = sDict[skey][3]
        xmax          = sDict[skey][4]

        if hname.startswith("Ekin"):
            xaxis = getXLogAxis(nbins, xmin, xmax)
            hist  = do1dLogHisto(hname, colNumbers, xaxis, particleTypes) 
        elif hname.startswith("RadN"):
            binwidth = xmax/nbins
            xaxis = [i*binwidth for i in range(nbins+1)]
            hist  = do1dRadHisto(hname, colNumbers, xaxis, particleTypes) 
        elif hname.startswith("RadEn"):
            binwidth = xmax/nbins
            xaxis = [i*binwidth for i in range(nbins+1)]
            hist  = do1dRadEnHisto(hname, colNumbers, xaxis, particleTypes) 
        elif hname.startswith("PhiN"):
            binwidth = (xmax-xmin)/nbins
            xaxis = [xmin+i*binwidth for i in range(nbins+1)]
            hist  = do1dPhiHisto(hname, colNumbers, xaxis, particleTypes) 
        elif hname.startswith("PhiEn"):
            binwidth = (xmax-xmin)/nbins
            xaxis = [xmin+i*binwidth for i in range(nbins+1)]
            hist  = do1dPhiEnHisto(hname, colNumbers, xaxis, particleTypes) 

        hist.Write()

    rfile.Close()
    print "writing file OK"
    return rfname
# ---------------------------------------------------------------------------------
def plotSpectra():

    # rfname  = saveRootFile()    
    rfile   = TFile.Open(rfname)
    
    vDict   = hDict_4TeV
    for vkey in vDict.keys():

        cv    = TCanvas( 'cv'+vkey, 'cv'+vkey, 1200, 900)
        hists = []        
        var   = vDict[vkey][0] 
        x1, y1, x2, y2 = vDict[vkey][1],vDict[vkey][2],vDict[vkey][3],vDict[vkey][4]
        doLogx, doLogy = vDict[vkey][5], vDict[vkey][6]
        pname = wwwpath + 'TCT/'+vkey+'_'+tag
        XurMin, XurMax = vDict[vkey][7],vDict[vkey][8]
        YurMin, YurMax = vDict[vkey][9],vDict[vkey][10]
        doFill = vDict[vkey][11]

        mlegend = TLegend( x1, y1, x2, y2)
        mlegend.SetFillColor(0)
        mlegend.SetLineColor(0)
        mlegend.SetTextSize(0.035)
        mlegend.SetShadowColor(10)
        # ....................................
        for i,skey in enumerate(var):

            hists += [rfile.Get(skey)]

            norm   = nprim
            hists[-1].Scale(1./norm)

            # print "Histogram ....", skey, "has ", hists[-1].GetEntries() - hists[-1].GetNbinsX(), "entries."
            hcolor = sDict[skey][7]
            hists[-1].SetLineColor(hcolor)
            hists[-1].SetLineWidth(3)
            if doFill:  hists[-1].SetFillColor(hcolor)

            drawOpt = sDict[skey][5]
            hists[-1].Draw(drawOpt)

            prettyName = sDict[skey][6]
            mlegend.AddEntry(hists[-1],prettyName, "lf")

            xtitle = sDict[skey][9]
            ytitle = sDict[skey][10]

        # ....................................
        if XurMin is not -1:                        
            hists[0].GetXaxis().SetRangeUser(XurMin, XurMax)
        if YurMin is not -1:         
            hists[0].GetYaxis().SetRangeUser(YurMin, YurMax)
        
        hists[0].GetYaxis().SetTitleSize(0.04)
        hists[0].GetYaxis().SetLabelSize(0.035)
        hists[0].GetXaxis().SetTitle(xtitle)
        hists[0].GetYaxis().SetTitle(ytitle)

        mlegend.Draw()
        lab = mylabel(60)
        lab.DrawLatex(x1-0.2, y2-0.05, sometext)

        gPad.RedrawAxis()
        gPad.SetLogx(doLogx)
        gPad.SetLogy(doLogy)

        print('Saving file as' + pname ) 
        cv.Print(pname + '.pdf')
        cv.Print(pname + '.png')

# ---------------------------------------------------------------------------------
if __name__ == "__main__":

    gROOT.SetBatch()
    gROOT.SetStyle("Plain")
    gROOT.LoadMacro("/afs/cern.ch/user/r/rkwee/scratch0/miScripts/py/AtlasStyle.C")
    gROOT.LoadMacro("/afs/cern.ch/user/r/rkwee/scratch0/miScripts/py/AtlasUtils.C")
    SetAtlasStyle()

    print doNormR(), 'Hz'
    #plotSpectra()
