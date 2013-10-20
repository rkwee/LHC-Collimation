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
cX,cY,cZ = 5,6,13
tag      = '4TeV'
csfile_H = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/TCT_4TeV_B2hHalo/coll_summary_TCT_4TeV_B2hHalo.dat'
csfile_V = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/TCT_4TeV_B2vHalo/coll_summary_TCT_4TeV_B2vHalo.dat'
Ntct_V   = 3 # wc -l TCT_4TeV_B2vHalo/impacts_real_on_71_TCTH.4R1.B2_B2vHalo.dat
Ntct_H   = 452 # wc -l TCT_4TeV_B2vHalo/impacts_real_on_72_TCTVA.4R1.B2_B2vHalo.dat
NtotBeam = 1.15e11*1404
nprim    = 1.57e7 # number of simulated primary interactions in fluka

if fname.endswith("30"): doHL = 1
if doHL:
    sometext = 'HL LHC'
    pID      = 1
    cEkin    = 9
    cX,cY,cZ = 4,5,13
    tag      = 'HL'
    csfile_H = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/ats-HL_LHC_1.0/nominal_settings/hor-B1/coll_summary_hor-B1.dat'
    csfile_V = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/ats-HL_LHC_1.0/nominal_settings/ver-B1/coll_summary_ver-B1.dat'
    Ntct_H   = 15793 # ats-HL_LHC_1.0/nominal_settings/impacts_real_on_52_TCTH.4L1.B1.dat
    Ntct_V   = 5817 # ats-HL_LHC_1.0/nominal_settings/impacts_real_on_53_TCTVA.4L1.B1.dat
    NtotBeam = 1.6e11*2808
    nprim    = 3e6
# ---------------------------------------------------------------------------------
# dict  key = hname  #0 particleTypes #1 colNumbers #2 nbins #3 xmin #4 xmax #5 drawOpt #6 prettyName 
                     #7 hcolor #8 ekinCut [GeV] #9 xtitle #10 ytitle
sDict = { 
    
    "EkinAll"           : [ ['all'],      [cEkin],      60, 1e-2,  1e4, 'HIST',     'all',      kBlack, -9999,'E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    "EkinMuons"         : [ ['10', '11'], [cEkin],      60, 1e-2,  1e4, 'SAMEHIST', '#mu^{#pm}',kAzure -7, -9999,'E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    "EkinProtons"       : [ ['1'],        [cEkin],      60, 1e-2,  1e4, 'SAMEHIST', 'protons',  kAzure -2, -9999,'E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    "EkinNeutrons"      : [ ['8'],        [cEkin],      60, 1e-2,  1e4, 'SAMEHIST', 'neutrons', kAzure -9, -9999,'E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    "EkinPhotons"       : [ ['7'],        [cEkin],      60, 1e-2,  1e4, 'SAMEHIST', '#gamma',   kAzure +1, -9999,'E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    "EkinElecPosi"      : [ ['3', '4'],   [cEkin],      60, 1e-2,  1e4, 'SAMEHIST', 'e^{#pm}',  kBlue,+4   -9999,'E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],

    "RadNMuonsEAll"      : [ ['10', '11'], [cX,cY,cZ,cEkin], 242,    0, 1210, 'HIST',     '#mu^{#pm}',                        kRed-10, -9999,'r [cm]', 'particles/cm^{2}/TCT hit'],
    "RadNMuonsE20"       : [ ['10', '11'], [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', '#mu^{#pm} with E_{kin} >  20 GeV', kRed-7,   20.,'r [cm]',  'particles/cm^{2}/TCT hit'],
    "RadNMuonsE100"      : [ ['10', '11'], [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', '#mu^{#pm} with E_{kin} > 100 GeV', kRed-1,  100.,'r [cm]',  'particles/cm^{2}/TCT hit'],
    
    "RadEnAll"          : [ ['all'],      [cX,cY,cZ,cEkin], 242,    0, 1210, 'HIST',     'all',        kBlack, -9999,'r [cm]', 'GeV/cm^{2}/TCT hit'],
    "RadEnMuons"        : [ ['10', '11'], [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', '#mu^{#pm} ', kGreen+7,  -9999,'r [cm]', 'GeV/cm^{2}/TCT hit'],
    "RadEnNeutrons"     : [ ['8'],        [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', 'neutrons',   kGreen+1,  -9999,'r [cm]', 'GeV/cm^{2}/TCT hit'],
    "RadEnProtons"      : [ ['1'],        [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', 'protons',    kGreen,    -9999,'r [cm]', 'GeV/cm^{2}/TCT hit'],
    "RadEnPhotons"      : [ ['7'],        [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', '#gamma',     kGreen-7,  -9999,'r [cm]', 'GeV/cm^{2}/TCT hit'],
    "RadEnElecPosi"     : [ ['3','4'],    [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', 'e^{#pm}',    kGreen-10, -9999,'r [cm]', 'GeV/cm^{2}/TCT hit'],

    "PhiNAll"           : [ ['all'],      [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HIST',     'all',          kBlack,    -9999,'#phi [rad]', 'particles/rad/TCT hit'],
    "PhiNMuons"         : [ ['10', '11'], [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HISTSAME', '#mu^{#pm} ',   kOrange+4,  -9999,'#phi [rad]', 'particles/rad/TCT hit'],
    "PhiNNeutrons"      : [ ['8'],        [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HISTSAME', 'neutrons',     kOrange+3,  -9999,'#phi [rad]', 'particles/rad/TCT hit'], 
    "PhiNProtons"       : [ ['1'],        [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HISTSAME', 'protons',      kOrange-3,  -9999,'#phi [rad]', 'particles/rad/TCT hit'],
    "PhiNPhotons"       : [ ['7'],        [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HISTSAME', '#gamma',       kOrange-1,  -9999,'#phi [rad]', 'particles/rad/TCT hit'],
    "PhiNElecPosi"      : [ ['3', '4'],   [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HISTSAME', 'e^{#pm}',      kOrange-4,  -9999,'#phi [rad]', 'particles/rad/TCT hit'],

    "PhiEnAll"         : [ ['all'],      [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HIST',     'all',          kBlack, -9999,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnMuons"       : [ ['10', '11'], [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HISTSAME', '#mu^{#pm} ',   kPink+10,  -9999,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnNeutrons"    : [ ['8'],        [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HISTSAME', 'neutrons',     kPink+4,  -9999,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnProtons"     : [ ['1'],        [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HISTSAME', 'protons',      kPink-1,  -9999,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnPhotons"     : [ ['7'],        [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HISTSAME', '#gamma',       kPink-4,  -9999,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnElecPosi"    : [ ['3','4'],    [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HISTSAME', 'e^{#pm}',      kPink-7,  -9999,'#phi [rad]', 'GeV/rad/TCT hit'],

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
def doNormR():
    # normlise by loss rate

    # lifetime
    tau_1   = 12*60 # loose beam in 12 minutes
    tau_2   = 100*60*60 # in 100 h

    Ntot_H  = addCol(csfile_H, 4-1)
    R1det_H = Ntct_H/Ntot_H * NtotBeam/tau_1
    R2det_H = Ntct_H/Ntot_H * NtotBeam/tau_2

    print "total #p lost in 200 turns _H", Ntot_H

    Ntot_V  = addCol(csfile_V, 4-1)
    R1det_V = Ntct_V/Ntot_V * NtotBeam/tau_1
    R2det_V = Ntct_V/Ntot_V * NtotBeam/tau_2

    print "total #p lost in 200 turns _V", Ntot_V

    R1det = int(0.5*( R1det_H + R1det_V ))
    R2det = int(0.5*( R2det_H + R2det_V ))

    return R1det, R2det
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

    #   rfname  = saveRootFile()    
    rfile   = TFile.Open(rfname)

    # dict for variables
    vDict   = { # vkey = pname; #0 list of hists #1 legend x1 #2 y1 #3 x2 #4 y2 #5 doLogx #6 doLogy #7 XurMin #8 XurMax #9 YurMin #10 YurMax #11 doFill
        'Ekin_TCT' : [["EkinAll", "EkinMuons", "EkinPhotons", "EkinElecPosi","EkinNeutrons", "EkinProtons" ],0.72, 0.75, 0.98, 0.9, 1,1, 2e-2,1e4,-1,-1, 0],
        'RadNMuons_TCT': [ ["RadNMuonsEAll", "RadNMuonsE20", "RadNMuonsE100" ],0.52, 0.75, 0.98, 0.9, 0,1, 0.,1200.,-1,-1, 1,],
        'RadialEnDist_TCT':[ ["RadEnAll", "RadEnMuons", "RadEnNeutrons", "RadEnProtons", "RadEnPhotons", "RadEnElecPosi" ],0.72, 0.75, 0.98, 0.9, 0,1, -1,-1,-1,-1, 1,],
        'PhiNDist_TCT': [ ["PhiNAll", "PhiNMuons", "PhiNPhotons", "PhiNNeutrons","PhiNElecPosi","PhiNProtons", ],0.72, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-5,9e-3, 0,],
        'PhiEnDist_TCT':[ [ "PhiEnAll", "PhiEnMuons", "PhiEnNeutrons", "PhiEnProtons", "PhiEnPhotons", "PhiEnElecPosi" ],0.72, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-6,4, 0,],
        }
    
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

    #print doNormR(), 'Hz'
    plotSpectra()
