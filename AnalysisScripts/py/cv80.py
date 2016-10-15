#!/usr/bin/python
#
# reweights by pressure profile 6.5 TeV
# write rootfile with 2d histos flat and reweighted
# from 4 TeV version cv70

# Oct 16
#
# R Kwee, 2016
# 
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers
from ROOT import *
from array import array
from fillTTree import *
from fillTTree_dict import generate_sDict
from helpers import makeTGraph, mylabel, wwwpath
import cv79
from cv79 import pData
# --------------------------------------------------------------------------------
def resultFileBG(k,rel):
    n = os.path.join(os.path.dirname(k),"results_pressure2015_"+rel+k.split('/')[-1])
    return  n
# --------------------------------------------------------------------------------
def cv80():
    print pData
    pFile, xtitle,lText = pData[0]
    datafile = '/Users/rkwee/Documents/RHUL/work/HL-LHC/runs/TCT/ir1_BG_bs_6500GeV_b1_20MeV_nprim3198000_67'
    bbgFile = datafile + ".root"
    print "Opening", bbgFile
    tag = '_BG_6500GeV_flat_20MeV_bs' #!! MMMeV
    norm = float(bbgFile.split('nprim')[-1].split('_')[0])
    rfile = TFile.Open(bbgFile, "READ")
    tBBG = rfile.Get("particle")
    yrel = ''
    print tBBG
    sDict = generate_sDict(tag, norm, tBBG, yrel)

    # -- small version of fillTTree
    beamintensity = 2.29e14 ## https://acc-stats.web.cern.ch/acc-stats/#lhc/fill-details 4536, ring 1.
    Trev  = 1./11245
    kT = 1.38e-23*300

    # rootfile with results
    rfoutname = resultFileBG(bbgFile,'')
    
    print 'writing ','.'*33, rfoutname
    rfOUTile = TFile.Open(rfoutname, "RECREATE")

    rHists,hists_flat, hists_reweighted, cnt = [],[],[], 0
    sk = []
    for skey in sDict.keys():

        if skey.count("Sel"): continue
        elif skey.count("Neg"): continue
        elif skey.count("Pos"): continue
        elif skey.count("Z"): continue
        elif skey.count("Neu_"): continue
        elif skey.count("Char"): continue
        elif skey.count("Plus") or skey.count("Minus"): continue
        elif skey.split(tag)[0].endswith("0") or skey.count("XY"): continue
        elif skey.count("Pio") or skey.count("Kao"): continue

        # for testing!!
        # if not skey.startswith("Rad"): continue

        sk += [skey]
        
        print "histogram ", len(sk)+1, "."*33, skey

    for j,skey in enumerate(sk):
        print "Now on #",j,">"*5, skey
        cnt += 1

        # -- x axis, value
        particleTypes = sDict[skey][0]
        hname         = skey
        xnbins        = sDict[skey][2]
        xmin          = sDict[skey][3]
        xmax          = sDict[skey][4]
        mt            = tBBG

        var = ''
        energyweight = ''
        cuts = [' energy_ke > 0.02 ']
        if skey.startswith("Ekin"):
            xaxis = getXLogAxis(xnbins, xmin, xmax)
            var = "energy_ke"        

        elif hname.startswith("Rad"):
            binwidth = xmax/xnbins
            xaxis = [i*binwidth for i in range(xnbins+1)]
            var = '(TMath::Sqrt(x*x + y*y))'
            if skey.count("En"): energyweight = "energy_ke * "

        elif hname.startswith("Phi"):
            binwidth = (xmax-xmin)/xnbins
            xaxis = [xmin+i*binwidth for i in range(xnbins+1)]
            var = '(TMath::ATan2(y,x))'
            if skey.count("En"): energyweight = "energy_ke * "

        if not particleTypes[0].count('ll'):
            pcuts = [ 'particle ==' + p for p in particleTypes  ]
            pcut  = '||'.join(pcuts)
            cuts += ['('+ pcut + ')']

        # -- y axis, weigths
        ynbins, ymin, ymax =  523, 22.5, 550
        twoDhist = TH2F(skey, skey, xnbins, array('d', xaxis), ynbins, ymin, ymax)

        hname_flat = skey + '_flat'
        twoDhist_flat = twoDhist.Clone(hname_flat)
        twoDhist_flat.Sumw2()

        hname_reweighted = skey + '_reweighted'
        twoDhist_reweighted = twoDhist.Clone(hname_reweighted)

        var = '0.01*z_interact:' + var
        cuts = "weight * "+energyweight+"("+" && ".join(cuts) + ") "
        print "INFO: applying", cuts, "to", var, "in", hname_flat
        mt.Project(hname_flat, var, cuts)

        print "entries  ", twoDhist_flat.GetEntries()
        hist_flat = twoDhist_flat.ProjectionX("makeit1d_flat" + skey)
        hist_flat.SetLineColor(kTeal-2)

        # -- create histogram with same axis for pint 
        if cnt == 1:
            hist_pint = twoDhist.ProjectionY("pint")
            data = cv79.getdata5c(pFile)
            rho_H2, rho_CH4, rho_CO, rho_CO2 = cv79.getrho(data['H2_Eq']),cv79.getrho(data['CH4_Eq']),cv79.getrho(data['CO_Eq']),cv79.getrho(data['CO2_Eq'])
            rho_H, rho_C, rho_O = cv79.getAtomicRho(rho_H2, rho_CH4, rho_CO, rho_CO2)
            pint_H, pint_C, pint_O, pint_tot = cv79.getpint(rho_H, rho_C, rho_O)
            pint_incomingbeam = {}

            # incoming beam is left side of B1
            for i,spos in enumerate(data['s']):
                if float(spos)<0:
                    z = -float(spos)
                    pint_incomingbeam[z] = pint_tot[i]
                    zbin = hist_pint.FindBin(z)
                    hist_pint.SetBinContent(zbin, pint_incomingbeam[z])
                    #print z, zbin, pint_incomingbeam[z]

        # --
        # compute re-weights for each bin
        for w in range(1,ynbins+1):
            scale = beamintensity * hist_pint.GetBinContent(w)
            for v in range(1,xnbins+1):
                m = twoDhist_flat.GetBinContent(v,w)  
                #print "Weight", scale * m, "m", m, "scale",scale, "x,y", v,w
                twoDhist_reweighted.SetBinContent(v,w,scale * m)

        hists_flat += [twoDhist_flat]          
        hists_reweighted += [twoDhist_reweighted]
        rHists += [skey]
        
        # writing two d hists
        hists_flat[-1].Write()
        hists_reweighted[-1].Write()

    # for debugging
    hist_pint.Write()
        
    rfOUTile.Close()
    print 'wrote ','.'*20, rfoutname
    
    # --

