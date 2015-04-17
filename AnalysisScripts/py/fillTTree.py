#!/usr/bin/python
#
# R Kwee-Hinzmann, 2013
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers
from ROOT import *
from helpers import *
from array import array
from fillTTree_dict import generate_sDict
from createTTree import treeName
# ---------------------------------------------------------------------------------
# helper functions first, then main local function //
# global variables
# ---------------------------------------------------------------------------------
zmin, zmax = 2260., 14960.
# to disable the zcut have zOn > zmax
zOn = 2e4
# for all use energy cut at 20 MeV
encut = 'energy_ke > ' + EnCut
debug = 1
# ---------------------------------------------------------------------------------
def getXLogAxis(nbins, xmin, xmax):

    # exponent width
    width = 1./nbins*(math.log10(xmax) - math.log10(xmin))
    # width = 1./nbins*(math.log(xmax) - math.log(xmin))

    # axis with exponents only 
    xtmp  = [math.log10(xmin) + i * width for i in range(nbins+1)]
    # xtmp  = [math.log(xmin) + i * width for i in range(nbins+1)]

    # real axis in power of 10
    xaxis = [math.pow(10, xExp) for xExp in xtmp]
    # xaxis = [math.exp(xExp) for xExp in xtmp]

    return xaxis
# ---------------------------------------------------------------------------------
def do1dLogHisto(sDict, mt, hname, xaxis, particleTypes):

    nbins = len(xaxis)-1
    hist  = TH1F(hname, hname, nbins, array('d', xaxis) )
    cuts  = []

    # cut on radius
    radius = 'TMath::Sqrt(x*x + y*y)'
    rcuts  = sDict[hname][8].split(':')

    if not rcuts[0].count('-9999'): 
        rcut  = ' '.join(rcuts)
        cuts += [radius + ' ' + rcut]

    # store sum of squares of weights 
    hist.Sumw2()

    var = 'energy_ke'

    if zOn < zmax: cuts += ['z_interact > ' + str(zmin) + ' && z_interact < ' + str(zmax)]
    cuts += [encut]

    if not particleTypes[0].count('ll'):
      pcuts = [ 'particle ==' + p for p in particleTypes  ]
      pcut  = '||'.join(pcuts)
      cuts += ['('+ pcut + ')']

    if cuts: cut = 'weight * (' + ' && '.join(cuts) + ')'
    else: cut = 'weight'

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
def do1dRadHisto(sDict, mt, hname, xaxis, particleTypes):

    ekinCut = sDict[hname][8]
    nbins   = len(xaxis)-1
    hist    = TH1F(hname, hname, nbins, array('d', xaxis))
    cuts    = []

    # store sum of squares of weights 
    hist.Sumw2()

    # EXPRESSION MUST BE IN ROOT not pyROOT!!
    var = 'TMath::Sqrt(x*x + y*y)'

    if zOn < zmax: cuts += ['z_interact > ' + str(zmin) + ' && z_interact < ' + str(zmax)]
    cuts += [encut]

    if not ekinCut.count('-9999'): cuts += ['energy_ke > ' + ekinCut]

    if not particleTypes[0].count('ll'):
      pcuts = [ 'particle ==' + p for p in particleTypes  ]
      pcut  = '||'.join(pcuts)
      cuts += ['('+ pcut + ')']

    if cuts: cut = 'weight * (' + ' && '.join(cuts) + ')'
    else: cut = 'weight'

    if debug: print 'INFO: will apply a cut of ', cut, 'to', hname
    mt.Project(hname, var, cut)
    if debug: print 'INFO: Have ', hist.GetEntries(), ' entries in', hname

    #    if debug: print 'INFO: Ignoring binarea!!!'
    for i in range(nbins):
        binArea = math.pi * (xaxis[i+1]**2 - xaxis[i]**2)
        content = hist.GetBinContent(i)
        hist.SetBinContent(i,content/binArea)

    return hist
# ---------------------------------------------------------------------------------
def do1dRadEnHisto(mt, hname, xaxis, particleTypes):

    nbins   = len(xaxis)-1
    hist    = TH1F(hname, hname, nbins, array('d', xaxis))
    cuts    = []

    # store sum of squares of weights 
    hist.Sumw2()

    # EXPRESSION MUST BE IN ROOT not pyROOT!!
    var = 'TMath::Sqrt(x*x + y*y)'

    if zOn < zmax: cuts += ['z_interact > ' + str(zmin) + ' && z_interact < ' + str(zmax)]
    cuts += [encut]

    if not particleTypes[0].count('ll'):
      pcuts = [ 'particle ==' + p for p in particleTypes  ]
      pcut  = '||'.join(pcuts)
      cuts += ['('+ pcut + ')']

    # weightening by multiplying the cut
    if cuts: cut = 'weight * energy_ke * (' + ' && '.join(cuts) + ')'
    else: cut = 'weight * energy_ke'

    if debug: print 'INFO: will apply a cut of ', cut, 'to', hname
    mt.Project(hname, var, cut)
    if debug: print 'INFO: Have ', hist.GetEntries(), ' entries in', hname

    for i in range(nbins):
        binArea = math.pi * (xaxis[i+1]**2 - xaxis[i]**2)
        content = hist.GetBinContent(i)
        hist.SetBinContent(i,content/binArea)

    return hist
# ---------------------------------------------------------------------------------
def do1dPhiHisto(sDict, mt, hname, xaxis, particleTypes):

    nbins   = len(xaxis)-1
    hist    = TH1F(hname, hname, nbins, array('d', xaxis))
    cuts    = []

    # store sum of squares of weights 
    hist.Sumw2()

    # EXPRESSION MUST BE IN ROOT not pyROOT!!
    var = 'TMath::ATan2(y,x)'

    # cut on radius 
    rcut = sDict[hname][8]
    if float(rcut) > 0.: cuts += ['TMath::Sqrt(x*x + y*y) > ' + rcut]

    if zOn < zmax: cuts += ['z_interact > ' + str(zmin) + ' && z_interact < ' + str(zmax)]
    cuts += [encut]

    if not particleTypes[0].count('ll'):
      pcuts = [ 'particle ==' + p for p in particleTypes  ]
      pcut  = '||'.join(pcuts)
      cuts += ['('+ pcut + ')']

    if cuts: cut = 'weight * (' + ' && '.join(cuts) + ')'
    else: cut = 'weight'

    if debug: print 'INFO: will apply a cut of ', cut, 'to', hname
    mt.Project(hname, var, cut)
    if debug: print 'INFO: Have ', hist.GetEntries(), ' entries in', hname

    for i in range(nbins):
        content = hist.GetBinContent(i)
        hist.SetBinContent(i,content/hist.GetBinWidth(i))

    return hist
# ---------------------------------------------------------------------------------
def do1dPhiEnHisto(sDict, mt, hname, xaxis, particleTypes):

    nbins   = len(xaxis)-1
    hist    = TH1F(hname, hname, nbins, array('d', xaxis))
    cuts    = []

    # store sum of squares of weights 
    hist.Sumw2()

    # EXPRESSION MUST BE IN ROOT not pyROOT!!
    var = 'TMath::ATan2(y,x)'

    if zOn < zmax: cuts += ['z_interact > ' + str(zmin) + ' && z_interact < ' + str(zmax)]
    cuts += [encut]

    # cut on radius
    rcut = sDict[hname][8]
    if float(rcut) > 0.: cuts += ['TMath::Sqrt(x*x + y*y) > ' + rcut]

    if not particleTypes[0].count('ll'):
      pcuts = [ 'particle ==' + p for p in particleTypes  ]
      pcut  = '||'.join(pcuts)
      cuts += ['('+ pcut + ')']

    # weightening by multiplying the cut
    if cuts: cut = 'weight * energy_ke * (' + ' && '.join(cuts) + ')'
    else: cut = 'weight * energy_ke'

    if debug: print 'INFO: will apply a cut of ', cut, 'to', hname
    mt.Project(hname, var, cut)
    if debug: print 'INFO: Have ', hist.GetEntries(), ' entries in', hname

    for i in range(nbins):
        content = hist.GetBinContent(i)
        hist.SetBinContent(i,content/hist.GetBinWidth(i))

    return hist
# ---------------------------------------------------------------------------------
def do1dXcoorHisto(sDict, mt, hname, xaxis, particleTypes):

    nbins   = len(xaxis)-1
    hist    = TH1F(hname, hname, nbins, array('d', xaxis))
    cuts    = []

    # store sum of squares of weights 
    hist.Sumw2()

    # cut on radius - not used
    rcut = sDict[hname][8]

    if zOn < zmax: cuts += ['z_interact > ' + str(zmin) + ' && z_interact < ' + str(zmax)]
    cuts += [encut]

    var = 'x'

    if not particleTypes[0].count('ll'):
      pcuts = [ 'particle ==' + p for p in particleTypes  ]
      pcut  = '||'.join(pcuts)
      cuts += ['('+ pcut + ')']

    if cuts: cut = 'weight * (' + ' && '.join(cuts) + ')'
    else: cut = 'weight'

    if debug: print 'INFO: will apply a cut of ', cut, 'to', hname
    mt.Project(hname, var, cut)
    if debug: print 'INFO: Have ', hist.GetEntries(), ' entries in', hname

    for i in range(nbins):
        content = hist.GetBinContent(i)
        hist.SetBinContent(i,content/hist.GetBinWidth(i))

    return hist
# ---------------------------------------------------------------------------------
def do1dYcoorHisto(sDict, mt, hname, xaxis, particleTypes):

    nbins   = len(xaxis)-1
    hist    = TH1F(hname, hname, nbins, array('d', xaxis))
    cuts    = []

    # store sum of squares of weights 
    hist.Sumw2()

    # cut - not used
    rcut = sDict[hname][8]

    if zOn < zmax: cuts += ['z_interact > ' + str(zmin) + ' && z_interact < ' + str(zmax)]
    cuts += [encut]

    var = 'y'

    if not particleTypes[0].count('ll'):
      pcuts = [ 'particle ==' + p for p in particleTypes  ]
      pcut  = '||'.join(pcuts)
      cuts += ['('+ pcut + ')']

    if cuts: cut = 'weight * (' + ' && '.join(cuts) + ')'
    else: cut = 'weight'

    if debug: print 'INFO: will apply a cut of ', cut, 'to', hname
    mt.Project(hname, var, cut)
    if debug: print 'INFO: Have ', hist.GetEntries(), ' entries in', hname

    for i in range(nbins):
        content = hist.GetBinContent(i)
        hist.SetBinContent(i,content/hist.GetBinWidth(i))

    return hist

# ---------------------------------------------------------------------------------
def do2dScatHisto(var, sDict, mt, hname, nbins, xmin, xmax, ynbins, ymin, ymax, particleTypes):

    hist = TH2F(hname, hname, nbins, xmin, xmax, ynbins, ymin, ymax)
    cuts = []

    # store sum of squares of weights 
    hist.Sumw2()

    # cut on energy
    ecuts = sDict[hname][8]
    if not ecuts.split(':')[0].count('-9999'):
        if len(ecuts.split(':')) > 1:
            emin = ecuts.split(':')[0]
            emax = ecuts.split(':')[1]
            cuts += [emax + ' > energy_ke && ' + emin + ' < energy_ke']
        else:
            cuts += ['energy_ke > ' + ecuts.split(':')[0]]
    else:
        cuts += [encut]

    if zOn < zmax: cuts += ['z_interact > ' + str(zmin) + ' && z_interact < ' + str(zmax)]


    # y is on y-axis, x on x-axis
    # var = "y:x"

    if debug: print 'INFO: will fill these variables ', var, 'into', hname

    if not particleTypes[0].count('ll'):
      pcuts = [ 'particle ==' + p for p in particleTypes  ]
      pcut  = '||'.join(pcuts)
      cuts += ['('+ pcut + ')']

    if cuts: cut = 'weight * (' + ' && '.join(cuts) + ')'
    else: cut = 'weight'

    if debug: print 'INFO: will apply a cut of ', cut, 'to', hname
    mt.Project(hname, var, cut)
    if debug: print 'INFO: Have ', hist.GetEntries(), ' entries in', hname

    # for i in range(nbins):
    #     content = hist.GetBinContent(i)
    #     hist.SetBinContent(i,content/hist.GetBinWidth(i))

    return hist
# ---------------------------------------------------------------------------------
def getHistogram(sDict, skey, mt):

    if debug: print "INFO: filling histogram", '.'*20, skey, '.'*20

    particleTypes = sDict[skey][0]
    hname         = skey
    nbins         = sDict[skey][2]
    xmin          = sDict[skey][3]
    xmax          = sDict[skey][4]
    ynbins        = sDict[skey][11]
    ymin          = sDict[skey][12]
    ymax          = sDict[skey][13]


    if hname.startswith("Ekin"):
        xaxis = getXLogAxis(nbins, xmin, xmax)
        hist  = do1dLogHisto(sDict, mt, hname, xaxis, particleTypes)

    elif hname.startswith("RadN"):
        binwidth = xmax/nbins
        xaxis = [i*binwidth for i in range(nbins+1)]
        hist  = do1dRadHisto(sDict, mt, hname, xaxis, particleTypes) 

    elif hname.startswith("RadEn"):
        binwidth = xmax/nbins
        xaxis = [i*binwidth for i in range(nbins+1)]
        hist  = do1dRadEnHisto(mt, hname, xaxis, particleTypes) 

    elif hname.startswith("PhiN"):
        binwidth = (xmax-xmin)/nbins
        xaxis = [xmin+i*binwidth for i in range(nbins+1)]
        hist  = do1dPhiHisto(sDict, mt, hname, xaxis, particleTypes) 

    elif hname.startswith("PhiEn"):
        binwidth = (xmax-xmin)/nbins
        xaxis = [xmin+i*binwidth for i in range(nbins+1)]
        hist  = do1dPhiEnHisto(sDict, mt, hname, xaxis, particleTypes) 

    elif hname.startswith("Xcoor"):
        binwidth = (xmax-xmin)/nbins
        xaxis = [xmin+i*binwidth for i in range(nbins+1)]
        hist  = do1dXcoorHisto(sDict, mt, hname, xaxis, particleTypes) 

    elif hname.startswith("Ycoor"):
        binwidth = (xmax-xmin)/nbins
        xaxis = [xmin+i*binwidth for i in range(nbins+1)]
        hist  = do1dYcoorHisto(sDict, mt, hname, xaxis, particleTypes) 

    elif hname.startswith("XYN"):        
        var = 'y:x'
        hist  = do2dScatHisto(var,sDict, mt, hname, nbins, xmin, xmax, ynbins, ymin, ymax, particleTypes) 

    return hist
# ---------------------------------------------------------------------------------
def resultFile(bbgFile):
    k=bbgFile
    n='/'.join(k.split('/')[:-1]) + '/results_' + k.split('/')[-1]
    return  n
# ---------------------------------------------------------------------------------
# main local function
# ---------------------------------------------------------------------------------
def fillHistos(bbgFile, tag):
    
    # bbgFile is the rootfile with the TTree, use this to fill histograms
    # write out a rootfile with histograms

    print "Opening...", bbgFile
    norm = float(bbgFile.split('nprim')[-1].split('_')[0])

    rf = TFile.Open(bbgFile)
    tBBG = rf.Get(treeName)

    yrel = '/TCT hit'
    sDict = generate_sDict(tag, norm, tBBG, yrel)

    # histograms which should be written one to rootfile
    rHists = []

    # rootfile with results
    rfoutname = resultFile(bbgFile)

    print 'writing ','.'*20, rfoutname
    rfile = TFile.Open(rfoutname, "RECREATE")

    hists = []
    cnt = 0
    for i,skey in enumerate(sDict.keys()):

       if skey in rHists:
          continue

       cnt += 1
       print "Getting ...", skey, '... #', cnt

       mt     = sDict[skey][5]
       hists += [getHistogram(sDict, skey, mt)]          
       rHists += [skey]

       norm   = sDict[skey][1]
       if norm != 1.: print 'normalising by ', norm
       hists[-1].Scale(1./norm)

       hcolor = sDict[skey][7]
       hists[-1].SetLineColor(hcolor)
       hists[-1].SetLineWidth(3)

       if not i: 
           if   type(hists[-1]) == TH1F: hists[-1].Draw("HIST")
           elif type(hists[-1]) == TH2F: hists[-1].Draw("COLZ")
       else:
           if   type(hists[-1]) == TH1F: hists[-1].Draw("HISTSAME")

       hists[-1].Write()

    rfile.Close()
    print 'wrote ','.'*20, rfoutname

# ---------------------------------------------------------------------------------
