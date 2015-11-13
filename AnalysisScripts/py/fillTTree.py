#!/usr/bin/python
#
# R Kwee-Hinzmann, 2013
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers
from ROOT import *
from helpers import *
from array import array
from fillTTree_dict import generate_sDict, sDict_HL_hybridComp
from createTTree import treeName
# ---------------------------------------------------------------------------------
# helper functions first, then main local function //
# global variables
# ---------------------------------------------------------------------------------
zmin, zmax = 2260., 55060.
#zmin, zmax = 2260., 14960.
#zmin, zmax = 2260., 21560.
# to disable the zcut have zOn > zmax
zOn = 9e4
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
        hist.SetBinError(i,hist.GetBinError(i)/binArea)

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
        hist.SetBinError(i,hist.GetBinError(i)/binArea)

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

    # cut on radius r or energy E
    rEcut  = sDict[hname][8]
    print "rEcut", rEcut
    if rEcut != '-9999':
        cutdir = rEcut.split()[1] 
        cutval = rEcut.split()[-1]
        if rEcut.startswith("r"): 
            cuton = 'TMath::Sqrt(x*x + y*y) '
        elif rEcut.startswith("E") : 
            cuton = "energy_ke "
        cuts += [ cuton + cutdir + ' ' + cutval]

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
        binWidth = hist.GetBinWidth(i)
        hist.SetBinContent(i,content/binWidth)
        hist.SetBinError(i,hist.GetBinError(i)/binWidth)

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

    # cut on radius r or energy E
    rEcut  = sDict[hname][8]
    print "rEcut", rEcut
    if rEcut != '-9999':
        cutdir = rEcut.split()[1] 
        cutval = rEcut.split()[-1]
        if rEcut.startswith("r"): 
            cuton = 'TMath::Sqrt(x*x + y*y) '
        elif rEcut.startswith("E") : 
            cuton = "energy_ke "
        cuts += [ cuton + cutdir + ' ' + cutval]

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
        binWidth = hist.GetBinWidth(i)
        hist.SetBinContent(i,content/binWidth)
        hist.SetBinError(i,hist.GetBinError(i)/binWidth)

    return hist
# ---------------------------------------------------------------------------------
def do1dTcoorHisto(var,sDict, mt, hname, xaxis, particleTypes):

    nbins   = len(xaxis)-1
    hist    = TH1F(hname, hname, nbins, array('d', xaxis))
    cuts    = []

    # store sum of squares of weights 
    hist.Sumw2()

    # cut on radius - not used
    rcut = sDict[hname][8]

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
        binWidth = hist.GetBinWidth(i)
        hist.SetBinContent(i,content/binWidth)
        hist.SetBinError(i,hist.GetBinError(i)/binWidth)

    return hist
# ---------------------------------------------------------------------------------
def do1dZcoorHisto(sDict, mt, hname, xaxis, particleTypes):

    nbins   = len(xaxis)-1
    hist    = TH1F(hname, hname, nbins, array('d', xaxis))
    cuts    = []

    # store sum of squares of weights 
    hist.Sumw2()

    # cut - not used
    rcut = sDict[hname][8]

    cuts += [encut]

    var = 'z_interact'

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
        binWidth = hist.GetBinWidth(i)
        hist.SetBinContent(i,content/binWidth)
        hist.SetBinError(i,hist.GetBinError(i)/binWidth)

    return hist
# ---------------------------------------------------------------------------------
def doOrigXYHisto(sDict, mt, hname, nbins, xmin, xmax, ynbins, ymin, ymax, particleTypes):
    print nbins, ynbins
    hist    = TH2F(hname, hname, nbins, xmin, xmax, ynbins, ymin, ymax)
    cuts    = []

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

    var = 'y_interact:x_interact'

    if not particleTypes[0].count('ll'):
      pcuts = [ 'particle ==' + p for p in particleTypes  ]
      pcut  = '||'.join(pcuts)
      cuts += ['('+ pcut + ')']

    if cuts: cut = 'weight * (' + ' && '.join(cuts) + ')'
    else: cut = 'weight'

    if debug: print 'INFO: will apply a cut of ', cut, 'to', hname
    mt.Project(hname, var, cut)
    if debug: print 'INFO: Have ', hist.GetEntries(), ' entries in', hname

    return hist
# ---------------------------------------------------------------------------------
def doOrigXZHisto(sDict, mt, hname, nbins, xmin, xmax, ynbins, ymin, ymax, particleTypes):

    hist    = TH2F(hname, hname, nbins, xmin, xmax, ynbins, ymin, ymax)
    cuts    = []

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


    var = 'x_interact:z_interact'

    if not particleTypes[0].count('ll'):
      pcuts = [ 'particle ==' + p for p in particleTypes  ]
      pcut  = '||'.join(pcuts)
      cuts += ['('+ pcut + ')']

    if cuts: cut = 'weight * (' + ' && '.join(cuts) + ')'
    else: cut = 'weight'

    if debug: print 'INFO: will apply a cut of ', cut, 'to', hname
    mt.Project(hname, var, cut)
    if debug: print 'INFO: Have ', hist.GetEntries(), ' entries in', hname

    return hist
# ---------------------------------------------------------------------------------
def doProfOrigHisto(var,sDict, mt, hname, nbins, xmin, xmax, ynbins, ymin, ymax, particleTypes):

    hist    = TProfile(hname, hname, nbins, xmin, xmax, ymin, ymax)
    cuts    = []

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

    if not particleTypes[0].count('ll'):
      pcuts = [ 'particle ==' + p for p in particleTypes  ]
      pcut  = '||'.join(pcuts)
      cuts += ['('+ pcut + ')']

    if cuts: cut = 'weight * (' + ' && '.join(cuts) + ')'
    else: cut = 'weight'

    if debug: print 'INFO: will apply a cut of ', cut, 'to', hname
    mt.Project(hname, var, cut)
    if debug: print 'INFO: Have ', hist.GetEntries(), ' entries in', hname

    return hist
## ---------------------------------------------------------------------------------
def doOrigYZHisto(sDict, mt, hname, nbins, xmin, xmax, ynbins, ymin, ymax, particleTypes):

    hist    = TH2F(hname, hname, nbins, xmin, xmax, ynbins, ymin, ymax)
    cuts    = []

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

    var = 'y_interact:z_interact'

    if not particleTypes[0].count('ll'):
      pcuts = [ 'particle ==' + p for p in particleTypes  ]
      pcut  = '||'.join(pcuts)
      cuts += ['('+ pcut + ')']

    if cuts: cut = 'weight * (' + ' && '.join(cuts) + ')'
    else: cut = 'weight'

    if debug: print 'INFO: will apply a cut of ', cut, 'to', hname
    mt.Project(hname, var, cut)
    if debug: print 'INFO: Have ', hist.GetEntries(), ' entries in', hname

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
        hist  = do1dTcoorHisto('x',sDict, mt, hname, xaxis, particleTypes) 

    elif hname.startswith("Ycoor"):
        binwidth = (xmax-xmin)/nbins
        xaxis = [xmin+i*binwidth for i in range(nbins+1)]
        hist  = do1dTcoorHisto('y',sDict, mt, hname, xaxis, particleTypes) 

    elif hname.startswith("Zcoor"):
        binwidth = (xmax-xmin)/nbins
        xaxis = [xmin+i*binwidth for i in range(nbins+1)]
        hist  = do1dZcoorHisto(sDict, mt, hname, xaxis, particleTypes) 

    elif hname.startswith("OrigXY"):
        binwidth = (xmax-xmin)/nbins
        xaxis = [xmin+i*binwidth for i in range(nbins+1)]
        hist  = doOrigXYHisto(sDict, mt, hname, nbins, xmin, xmax, ynbins, ymin, ymax, particleTypes)

    elif hname.startswith("OrigXZ"):
        binwidth = (xmax-xmin)/nbins
        xaxis = [xmin+i*binwidth for i in range(nbins+1)]
        hist  = doOrigXZHisto(sDict, mt, hname, nbins, xmin, xmax, ynbins, ymin, ymax, particleTypes)

    elif hname.startswith("OrigYZ"):
        binwidth = (xmax-xmin)/nbins
        xaxis = [xmin+i*binwidth for i in range(nbins+1)]
        hist  = doOrigYZHisto(sDict, mt, hname, nbins, xmin, xmax, ynbins, ymin, ymax, particleTypes)

    elif hname.startswith("ProfOrigXZ"):
        binwidth = (xmax-xmin)/nbins
        xaxis = [xmin+i*binwidth for i in range(nbins+1)]
        var = 'x_interact:z_interact'
        hist  = doProfOrigHisto(var, sDict, mt, hname, nbins, xmin, xmax, ynbins, ymin, ymax, particleTypes)

    elif hname.startswith("ProfOrigYZ"):
        binwidth = (xmax-xmin)/nbins
        xaxis = [xmin+i*binwidth for i in range(nbins+1)]
        var = 'y_interact:z_interact'
        hist  = doProfOrigHisto(var, sDict, mt, hname, nbins, xmin, xmax, ynbins, ymin, ymax, particleTypes)

    elif hname.startswith("XYN"):        
        var = 'y:x'
        hist  = do2dScatHisto(var,sDict, mt, hname, nbins, xmin, xmax, ynbins, ymin, ymax, particleTypes) 

    return hist
# ---------------------------------------------------------------------------------
def resultFile(k,rel):
    n = os.path.join(os.path.dirname(k),"results_"+rel+k.split('/')[-1])
    return  n
# ---------------------------------------------------------------------------------
# main local function
# ---------------------------------------------------------------------------------
def fillHistos(bbgFile, tag, doComp):
    
    # bbgFile is the rootfile with the TTree, use this to fill histograms
    # write out a rootfile with histograms

    print "Opening...", bbgFile
    norm = float(bbgFile.split('nprim')[-1].split('_')[0]) 

    rf = TFile.Open(bbgFile)
    tBBG = rf.Get(treeName)

    yrel = '/TCT hit'

    if doComp:
        # for comparisons plots, also edit rel
        sDict = sDict_HL_hybridComp
        rel = 'hybridComp_'
    else:
        sDict = generate_sDict(tag, norm, tBBG, yrel)
        rel = ''

    # histograms which should be written one to rootfile
    rHists = []

    # rootfile with results
    rfoutname = resultFile(bbgFile,rel)

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
       if norm != 1.: print 'scaling by ', 1./norm
       hists[-1].Scale(1./norm)

       hcolor = sDict[skey][7]
       hists[-1].SetLineColor(hcolor)
       hists[-1].SetLineWidth(3)

       if not i: 
           if   type(hists[-1]) == TH1F: hists[-1].Draw("HIST")
           elif type(hists[-1]) == TH2F: hists[-1].Draw("COLZ")
           elif type(hists[-1]) == TProfile: 
               hists[-1].SetMarkerColor(hcolor)
               hists[-1].Draw("P")
       else:
           if   type(hists[-1]) == TH1F: hists[-1].Draw("HISTSAME")

       hists[-1].Write()

    rfile.Close()
    print 'wrote ','.'*20, rfoutname

# ---------------------------------------------------------------------------------
