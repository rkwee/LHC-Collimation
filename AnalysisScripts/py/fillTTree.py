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

# setting variables

debug        = 1
treeName     = "particle"
fortformat66 = "event/I:generation/I:particle/I:energy_ke/F:weight/F:x/F:y/F:xp/F:yp/F:age/F:energy_tot/F:x_interact/F:y_interact/F:z_interact/F:t_interact/F"
fortformat30 = "event/I:particle/I:generation/I:weight/F:x/F:y/F:xp/F:yp/F:energy_tot/F:energy_ke/F:age/F:x_interact/F:y_interact/F:z_interact/F"

if fname.endswith("30"): 
    fortformat = fortformat30
    varList = varList_HL
    hDict = hDict_HL_halo

    if debug: print "Using HL format", '.'*10
else: 
    fortformat = fortformat66
    varList = varList_4TeV
    hDict = hDict_4TeV
    if debug: print "Using 4 TeV format", '.'*10
# ---------------------------------------------------------------------------------
sometext,pID,cEkin,cX,cY,cZ,tag,csfile_H,csfile_V,Ntct_H,Ntct_V, NtotBeam,nprim = [v for v in varList]
rfoutName = fname +".root"
# ---------------------------------------------------------------------------------
def createTTree(fname):
  print "writing ", rfoutName

  mytree = TTree(treeName,treeName)
  mytree.ReadFile(fname,fortformat)
  mytree.SaveAs(rfoutName)

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
def do1dLogHisto(mt, colNumbers, hname, xaxis, particleTypes):

    nbins = len(xaxis)-1
    hist  = TH1F(hname, hname, nbins, array('d', xaxis) )

    # store sum of squares of weights 
    hist.Sumw2()

    var = colNumbers[0]

    # this cut doesnt change anything. it may only for beamgas
    zmin, zmax = 2260., 14960.

    if debug: print "INFO: Using these variables", colNumbers
    cut  = 'z_interact > ' + str(zmin) + ' && z_interact < ' + str(zmax)

    if not particleTypes[0].count('ll'):
      cuts  = [ 'particle ==' + p for p in particleTypes  ]
      cut   = '||'.join(cuts)

    if debug: print 'will apply a cut of ', cut, 'to', hname
    mt.Project(hname, var, cut)
    if debug: print 'INFO: Have ', hist.GetEntries(), ' entries in', hname
   
    # This second loop changes the Get.Entries() value by number of bins!!
    for bin in range(1,nbins+1):
        content = hist.GetBinContent(bin)
        width   = hist.GetBinWidth(bin)
        bcenter = hist.GetXaxis().GetBinCenterLog(bin)
        hist.SetBinContent(bin,bcenter*content/width)
 
    return hist
# ---------------------------------------------------------------------------------
def do1dRadHisto(mt, hname, colNumbers, xaxis, particleTypes):

    ekinCut = sDict[hname][8]
    nbins   = len(xaxis)-1
    hist    = TH1F(hname, hname, nbins, array('d', xaxis))

    # store sum of squares of weights 
    hist.Sumw2()

    # this cut doesnt change anything. it may only for beamgas
    zmin, zmax = 2260., 14960.

    if debug: print "INFO: Using these variables", colNumbers

    cut  = 'z_interact > ' + str(zmin) + ' && z_interact < ' + str(zmax)
    cut += ' && energy_ke > ' + str(ekinCut)

    # EXPRESSION MUST BE IN ROOT not pyROOT!!
    var = 'TMath::Sqrt(TMath::Power(x,2) + TMath::Power(y,2))'

    if not particleTypes[0].count('ll'):
      pcuts = [ 'particle ==' + p for p in particleTypes  ]
      pcut  = '||'.join(pcuts)
      cut   = '('+ pcut + ') && ' + cut 

    if debug: print 'INFO: will apply a cut of ', cut, 'to', hname
    mt.Project(hname, var, cut)
    if debug: print 'INFO: Have ', hist.GetEntries(), ' entries in', hname

    for i in range(nbins):
        binArea = math.pi * (xaxis[i+1]**2 - xaxis[i]**2)
        content = hist.GetBinContent(i)
        hist.SetBinContent(i,content/binArea)
 
    return hist
# ---------------------------------------------------------------------------------
def do1dRadEnHisto(mt, hname, colNumbers, xaxis, particleTypes):

    nbins   = len(xaxis)-1
    hist    = TH1F(hname, hname, nbins, array('d', xaxis))

    # store sum of squares of weights 
    hist.Sumw2()

    # this cut doesnt change anything. it may only for beamgas
    zmin, zmax = 2260., 14960.

    if debug: print "INFO: Using these variables", colNumbers
    cut  = 'z_interact > ' + str(zmin) + ' && z_interact < ' + str(zmax) 

    # EXPRESSION MUST BE IN ROOT not pyROOT!!
    var = 'TMath::Sqrt(TMath::Power(x,2) + TMath::Power(y,2))'

    if not particleTypes[0].count('ll'):
      pcuts = [ 'particle ==' + p for p in particleTypes  ]
      pcut  = '||'.join(pcuts)
      cut   = '('+ pcut + ') && ' + cut 

    # weightening by multiplying the cut
    cut = 'energy_ke * (' + cut + ')'
    if debug: print 'INFO: will apply a cut of ', cut, 'to', hname
    mt.Project(hname, var, cut)
    if debug: print 'INFO: Have ', hist.GetEntries(), ' entries in', hname

    for i in range(nbins):
        binArea = math.pi * (xaxis[i+1]**2 - xaxis[i]**2)
        content = hist.GetBinContent(i)
        hist.SetBinContent(i,content/binArea)
 
    return hist
# ---------------------------------------------------------------------------------
def do1dPhiHisto(mt, hname, colNumbers, xaxis, particleTypes):

    nbins   = len(xaxis)-1
    hist    = TH1F(hname, hname, nbins, array('d', xaxis))

    # store sum of squares of weights 
    hist.Sumw2()

    # this cut doesnt change anything. it may only for beamgas
    zmin, zmax = 2260., 14960.

    if debug: print "INFO: Using these variables", colNumbers
    cut  = 'z_interact > ' + str(zmin) + ' && z_interact < ' + str(zmax) 

    # EXPRESSION MUST BE IN ROOT not pyROOT!!
    var = 'TMath::ATan2(y,x)'

    if not particleTypes[0].count('ll'):
      pcuts = [ 'particle ==' + p for p in particleTypes  ]
      pcut  = '||'.join(pcuts)
      cut   = '('+ pcut + ') && ' + cut 

    if debug: print 'INFO: will apply a cut of ', cut, 'to', hname
    mt.Project(hname, var, cut)
    if debug: print 'INFO: Have ', hist.GetEntries(), ' entries in', hname

    for i in range(nbins):
        content = hist.GetBinContent(i)
        hist.SetBinContent(i,content/hist.GetBinWidth(i))

    return hist
# ---------------------------------------------------------------------------------
def do1dPhiEnHisto(mt, hname, colNumbers, xaxis, particleTypes):

    nbins   = len(xaxis)-1
    hist    = TH1F(hname, hname, nbins, array('d', xaxis))

    # store sum of squares of weights 
    hist.Sumw2()

    # this cut doesnt change anything. it may only for beamgas
    zmin, zmax = 2260., 14960.

    if debug: print "INFO: Using these variables", colNumbers
    cut  = 'z_interact > ' + str(zmin) + ' && z_interact < ' + str(zmax) 

    # EXPRESSION MUST BE IN ROOT not pyROOT!!
    var = 'TMath::ATan2(y,x)'

    if not particleTypes[0].count('ll'):
      pcuts = [ 'particle ==' + p for p in particleTypes  ]
      pcut  = '||'.join(pcuts)
      cut   = '('+ pcut + ') && ' + cut 

    # weightening by multiplying the cut
    cut = 'energy_ke * (' + cut + ')'
    if debug: print 'INFO: will apply a cut of ', cut, 'to', hname
    mt.Project(hname, var, cut)
    if debug: print 'INFO: Have ', hist.GetEntries(), ' entries in', hname

    for i in range(nbins):
        content = hist.GetBinContent(i)
        hist.SetBinContent(i,content/hist.GetBinWidth(i))
 
    return hist
# ---------------------------------------------------------------------------------
def getHistogram(skey, mt):

    if debug: print "INFO: filling histogram ...", skey

    particleTypes = sDict[skey][0]
    hname         = skey
    colNumbers    = sDict[skey][1]
    nbins         = sDict[skey][2]
    xmin          = sDict[skey][3]
    xmax          = sDict[skey][4]

    if hname.startswith("Ekin"):
        xaxis = getXLogAxis(nbins, xmin, xmax)
        hist  = do1dLogHisto(mt, colNumbers, hname, xaxis, particleTypes)

    elif hname.startswith("RadN"):
        binwidth = xmax/nbins
        xaxis = [i*binwidth for i in range(nbins+1)]
        hist  = do1dRadHisto(mt, hname, colNumbers, xaxis, particleTypes) 

    elif hname.startswith("RadEn"):
        binwidth = xmax/nbins
        xaxis = [i*binwidth for i in range(nbins+1)]
        hist  = do1dRadEnHisto(mt, hname, colNumbers, xaxis, particleTypes) 

    elif hname.startswith("PhiN"):
        binwidth = (xmax-xmin)/nbins
        xaxis = [xmin+i*binwidth for i in range(nbins+1)]
        hist  = do1dPhiHisto(mt, hname, colNumbers, xaxis, particleTypes) 
        
    elif hname.startswith("PhiEn"):
        binwidth = (xmax-xmin)/nbins
        xaxis = [xmin+i*binwidth for i in range(nbins+1)]
        hist  = do1dPhiEnHisto(mt, hname, colNumbers, xaxis, particleTypes) 

    return hist
# ---------------------------------------------------------------------------------
def plotSpectra(fname):

    # branch names
    bnames = fortformat.split(':')
    bList  = [b.split('/')[0] for b in bnames]

    rf = TFile(fname + '.root')
    mt = rf.Get(treeName)

    for hkey in hDict.keys():

      cv = TCanvas( 'cv'+hkey, 'cv'+hkey, 1200, 900)
      hists = []

      hList = hDict[hkey][0] 
      x1, y1, x2, y2 = hDict[hkey][1],hDict[hkey][2],hDict[hkey][3],hDict[hkey][4]
      doLogx, doLogy = hDict[hkey][5], hDict[hkey][6]
      pname = wwwpath + 'TCT/'+hkey+'_'+tag
      XurMin, XurMax = hDict[hkey][7],hDict[hkey][8]
      YurMin, YurMax = hDict[hkey][9],hDict[hkey][10]
      doFill = hDict[hkey][11]

      mlegend = TLegend( x1, y1, x2, y2)
      mlegend.SetFillColor(0)
      mlegend.SetLineColor(0)
      mlegend.SetTextSize(0.035)
      mlegend.SetShadowColor(10)
      
      for hname in hList:
        
           hists += [getHistogram(hname, mt)]
           norm   = nprim
           hists[-1].Scale(1./norm)
           
           hcolor = sDict[hname][7]
           hists[-1].SetLineColor(hcolor)
           hists[-1].SetLineWidth(3)
           if doFill:  hists[-1].SetFillColor(hcolor)
           
           drawOpt = sDict[hname][5]
           hists[-1].Draw(drawOpt)
           
           prettyName = sDict[hname][6]
           mlegend.AddEntry(hists[-1],prettyName, "lf")
           
           xtitle = sDict[hname][9]
           ytitle = sDict[hname][10]
        
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

    #createTTree(fname)
    plotSpectra(fname)
