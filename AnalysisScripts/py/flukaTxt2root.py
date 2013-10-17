#!/usr/bin/python
#
# R Kwee-Hinzmann, 2013
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers
from ROOT import *
from helpers import *
from array import array
# ---------------------------------------------------------------------------------
import optparse
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", type="string",
                  help="put the path of the merged fort.66 file from fluka runs")

(options, args) = parser.parse_args()

fname  = options.filename
rfname = fname + '.root'
#######################################################################################
    # FORMAT RODERIK

    # http://bbgen.web.cern.ch/bbgen/bruce/fluka_beam_gas_arc_4TeV/flukaIR15.html
    # 1  FLUKA run number (between 1 and 3000)
    # 2  ID of primary particle (between 1 and 60 000 in each run)
    # 3  FLUKA particle type (an explanation of the numbers can be found at http://www.fluka.org/fluka.php?id=man_onl&sub=7)
    # 4  kinetic energy (GeV)
    # 5  statistical weight (should be 1 for all particles)
    # 6  X (cm)
    # 7  Y (cm)
    # 8  directional cosine w.r.t X-axis
    # 9  directional cosine w.r.t Y-axis
    # 10 time (s) since start of primary particle
    # 11 total energy (GeV)
    # 12 X_start (cm) : starting position of primary particle
    # 13 Y_start (cm)
    # 14 Z_start (cm)
    # 15 t_start (s) : starting time of primary particle where t=0 is at the entrance of the TCTH
#######################################################################################
    # FORMAT FLUKA GUYS

    # Scoring from Region No  1754 to  1753
    # Col  1: primary event number
    # -- Particle information --
    # Col  2: FLUKA particle type ID
    # Col  3: generation number
    # Col  4: statistical weight
    # -- Crossing at scoring plane --
    # Col  5: x coord (cm)
    # Col  6: y coord (cm)
    # Col  7: x dir cosine
    # Col  8: y dir cosine
    # Col  9: total energy (GeV)
    # Col 10: kinetic energy (GeV)
    # Col 11: particle age since primary event (sec)
    # -- Primary event --
    # Col 12: x coord TCT impact (cm)
    # Col 13: y coord TCT impact (cm)
    # Col 14: z coord TCT impact (cm)
#######################################################################################
doHL = 0
sometext = '4 TeV beam'
cEkin    = 3
pID      = 2
cX, cY   = 6,7
tag      = '4TeV'

if fname.endswith("30"): doHL = 1
if doHL:
    sometext = 'HL LHC'
    pID      = 1
    cEkin    = 9
    cX, cY   = 4,5
    tag      = 'HL'
# ---------------------------------------------------------------------------------
# dict  key = hname  #0 particleTypes #1 colNumbers #2 nbins #3 xmin #4 xmax #5 drawOpt #6 prettyName 
                     #7 hcolor #8 ekinCut [GeV] #9 xtitle #10 ytitle
sDict = { 

    "EkinAll"      : [ ['all'],      [cEkin],     100, 1e-3,  1e4, 'HIST',     'all',                        kAzure -10, -9999,'E [GeV]', '#frac{dN (counts)}{dlog E}', ],
    # "EkinMuons"    : [ ['10', '11'], [cEkin],     100, 1e-3,  1e4, 'SAMEHIST', '#mu^{#pm}',                  kAzure -9, -9999,'E [GeV]', '#frac{dN (counts)}{dlog E}', ],
    # "EkinProtons"  : [ ['1'],        [cEkin],     100, 1e-3,  1e4, 'SAMEHIST', 'protons',                    kAzure -8, -9999,'E [GeV]', '#frac{dN (counts)}{dlog E}', ],
    # "EkinNeutrons" : [ ['8'],        [cEkin],     100, 1e-3,  1e4, 'SAMEHIST', 'neutrons',                   kAzure -7, -9999,'E [GeV]', '#frac{dN (counts)}{dlog E}', ],
    # "EkinPhotons"  : [ ['7'],        [cEkin],     100, 1e-3,  1e4, 'SAMEHIST', '#gamma',                     kAzure -6, -9999,'E [GeV]', '#frac{dN (counts)}{dlog E}', ],
    # "EkinElecPosi" : [ ['3', '4'],   [cEkin],     100, 1e-3,  1e4, 'SAMEHIST', 'e^{#pm}',                    kAzure -5, -9999,'E [GeV]', '#frac{dN (counts)}{dlog E}', ],
    # "RadMuonsEAll" : [ ['10', '11'], [cX,cY,cEkin], 242,    0, 1210, 'HIST',     '#mu^{#pm}',                        kRed-10, -9999,'r [cm]', 'particles/cm^{2}'],
    # "RadMuonsE20"  : [ ['10', '11'], [cX,cY,cEkin], 242,    0, 1210, 'HISTSAME', '#mu^{#pm} with E_{kin} >  20 GeV', kRed-7,   20.,'r [cm]', 'particles/cm^{2}'],
    # "RadMuonsE100" : [ ['10', '11'], [cX,cY,cEkin], 242,    0, 1210, 'HISTSAME', '#mu^{#pm} with E_{kin} > 100 GeV', kRed-1,  100.,'r [cm]', 'particles/cm^{2}'],
    }
# ---------------------------------------------------------------------------------
def getColContent(colNumbers, particleTypes):

    cols, col = [], []

    for colNumber in colNumbers:

        with open(fname) as myfile:

            for line in myfile:       

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
def doTGraph(hist):

    nbins   = hist.GetNbinsX()
    bcenter = [ hist.GetXaxis().GetBinCenterLog(i) for i in range(1,nbins+1) ]
    content = [ hist.GetBinContent(i) for i in range(1,nbins+1) ]
    gr      = TGraph(hist)
    npoints = gr.GetN()

    for i in range(npoints):
        x, y = ROOT.Double(), ROOT.Double()
        x, y = bincenter[i], bincenter[i]*content[i]
        gr.SetPoint(1+i, x, y)

    return gr
# ---------------------------------------------------------------------------------
def do1dRadHisto(hname, colNumbers, xaxis, particleTypes):

    # expect 2 lists for radially-binned histograms
    [xcol, ycol, ekin] = getColContent(colNumbers, particleTypes) 

    ekinCut = sDict[hname][8]
    nbins   = len(xaxis)-1
    hist    = TH1F(hname, hname, nbins, array('d', xaxis))

    for i in range(len(xcol)): 
        if ekin[i] > ekinCut:
            hist.Fill(math.sqrt(xcol[i]**2 + ycol[i]**2))

    for i in range(nbins):
        binArea = math.pi * (xaxis[i+1]**2 - xaxis[i]**2)
        content = hist.GetBinContent(i)
        hist.SetBinContent(i,content/binArea)
 
    return hist
# ---------------------------------------------------------------------------------
def saveRootFile():

    print 'writing ','.'*20, rfname
    rfile = TFile.Open(rfname, "RECREATE")

    for skey in sDict.keys():

        particleTypes = sDict[skey][0]
        hname         = skey
        colNumber     = sDict[skey][1]
        nbins         = sDict[skey][2]
        xmin          = sDict[skey][3]
        xmax          = sDict[skey][4]

        if hname.startswith("Ekin"):
            xaxis = getXLogAxis(nbins, xmin, xmax)
            hist  = do1dLogHisto(hname, colNumber, xaxis, particleTypes) 
        elif hname.startswith("Rad"):
            binwidth = xmax/nbins
            xaxis = [i*binwidth for i in range(nbins+1)]
            hist  = do1dRadHisto(hname, colNumber, xaxis, particleTypes) 

        hist.Write()

    rfile.Close()

    return rfname
# ---------------------------------------------------------------------------------
def plotSpectra():

    rfname  = saveRootFile()    
    rfile   = TFile.Open(rfname)
    cv      = TCanvas( 'cv' , 'cv', 1200, 900)

    hists  = []
    # ....................................
    if True:
        var    = ['EkinAll', 
                  # 'EkinElecPosi', 
                  # 'EkinProtons', 
                  # 'EkinNeutrons',
                  # 'EkinPhotons', 
                  # 'EkinMuons', 
                  ]
        x1, y1, x2, y2 = 0.72, 0.75, 0.98, 0.9
        doLogx, doLogy = 1,1
        pname  = wwwpath + 'TCT/Ekin_TCT_'+tag
    # ....................................

    if 0:
        var    = ['RadMuonsEAll', 'RadMuonsE20', 'RadMuonsE100']
        x1, y1, x2, y2 = 0.6, 0.75, 0.9, 0.9
        doLogx, doLogy = 0,1
        pname  = wwwpath + 'TCT/RadialDist_TCT_'+tag
    # ....................................

    # ONCE: print all keys to order them
    # print sDict.keys()

    mlegend = TLegend( x1, y1, x2, y2)
    mlegend.SetFillColor(0)
    mlegend.SetLineColor(0)
    mlegend.SetTextSize(0.035)
    mlegend.SetShadowColor(10)

    for i,skey in enumerate(var):
        
        hists += [rfile.Get(skey)]

        print "Histogram ....", skey, "has ", hists[-1].GetEntries() - hists[-1].GetNbinsX(), "entries."
        hcolor = sDict[skey][7]
        hists[-1].SetLineColor(hcolor)
        hists[-1].SetLineWidth(2)
        #hists[-1].SetFillColor(hcolor)

        drawOpt = sDict[skey][5]
        hists[-1].Draw(drawOpt)

        prettyName = sDict[skey][6]
        mlegend.AddEntry(hists[-1],prettyName, "lf")
    
        xtitle = sDict[skey][9]
        ytitle = sDict[skey][10]

    hists[0].GetYaxis().SetTitleSize(0.04)
    hists[0].GetYaxis().SetLabelSize(0.035)
    hists[0].GetXaxis().SetTitle(xtitle)
    hists[0].GetYaxis().SetTitle(ytitle)
    
    mlegend.Draw()
    lab = mylabel(60)
    lab.DrawLatex(x1, y1-0.1, sometext)

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

    plotSpectra()
