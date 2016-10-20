#!/usr/bin/python
#
# reweights by pressure profile
# Sept 16
#
# R Kwee, 2016
# 
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers
from ROOT import *
from array import array
from fillTTree import *
from fillTTree_dict import generate_sDict
# get function to read the data if 14 columns are present 
from cv32 import getdata14c
from helpers import makeTGraph, mylabel, wwwpath
import cv65, cv66, cv79
# --------------------------------------------------------------------------------
def resultFileBG(k,rel):
    n = os.path.join(os.path.dirname(k),"results_pressure"+rel+"_"+k.split('/')[-1])
    return  n

def cv70():
# --------------------------------------------------------------------------------
# density profile is given in the following format:
# densities per molecule as function of s-coordinate
# x,y,z, cx, cy, cz as function of (different s-coordinate)
# merge densities with coordinates
# note, that the source routine needs fluka units, ie *cm*!
# --------------------------------------------------------------------------------
    debug  = 0
    do4TeV = 1 # 
    do6p5  = 0 #
    
    if do4TeV:
        year = "2012"
        energy = "4 TeV"
        pressFile = '/afs/cern.ch/work/r/rkwee/HL-LHC/beam-gas-sixtrack/pressure_profiles_2012/LSS1_B1_Fill2736_Final.csv'
        pressFile = '/Users/rkwee/Documents/RHUL/work/data/4TeV/LSS1_B1_Fill2736_Final.csv'

        bbgFile = '/afs/cern.ch/project/lhc_mib/valBG4TeV/ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67.root'
        bbgFile = thispath + 'ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67.root'
        beamintensity = 2e14    
        tag = '_BG_4TeV_20MeV_bs'
        data = getdata14c(pressFile)
        startarc = 260.
    elif do6p5:
        year = "2015"
        energy = "6.5 TeV"
        bbgFile = '/Users/rkwee/Documents/RHUL/work/HL-LHC/runs/TCT/ir1_BG_bs_6500GeV_b1_20MeV_nprim3198000_67.root'
        pressFile = "/Users/rkwee/Downloads/Density_Fill4536_2041b_26158.8832-500_B1_withECLOUD.txt"
        beamintensity = 2.29e14 ## https://acc-stats.web.cern.ch/acc-stats/#lhc/fill-details 4536, ring 1.
        tag = '_BG_6500GeV_flat_20MeV_bs' #!! MMMeV
        data = cv79.getdata5c(pressFile)
        startarc = 493.6
    else:
        year = "2011"
        energy = " 3.5 TeV "
        pressFile = "/Users/rkwee/Documents/RHUL/work/HL-LHC/runs/TCT/LSS1_B1_fill_2028-sync_rad_and_ecloud.csv"
        bbgFile = "/Users/rkwee/Documents/RHUL/work/HL-LHC/runs/TCT/beam_gas_3.5TeV_IR1_to_arc_20MeV_100M_nprim7660649_66.root"
        beamintensity = 1.66e14    
        tag = "_BG_3p5TeV_20MeV"
        data = getdata14c(pressFile)
        startarc = 260.

        
    print 'data keys are',data.keys()
    print "Opening", bbgFile
    
    nprim = float(bbgFile.split('nprim')[-1].split('_')[0])
    rfile = TFile.Open(bbgFile, "READ")
    tBBG = rfile.Get("particle")
    yrel = ''
    print tBBG
    sDict = generate_sDict(tag, nprim, tBBG, yrel)

    # -- small version of fillTTree
    Trev  = 1./11245
    kT = 1.38e-23*300

    # rootfile with results
    rfoutname = resultFileBG(bbgFile,year)
    
    print 'writing ','.'*33, rfoutname
    rfOUTile = TFile.Open(rfoutname, "RECREATE")

    rHists,hists_flat, hists_reweighted, cnt = [],[],[], 0
    sk = []
    for skey in sDict.keys():

        if skey.count("Sel"): continue
        elif skey.count("Neg"): continue
        elif skey.count("Pos"): continue
        elif skey.count("Z") and not skey.startswith("OrigZ"): continue
        elif skey.count("Neu_"): continue
        elif skey.count("Char"): continue
        elif skey.count("Plus") or skey.count("Minus"): continue
        elif skey.split(tag)[0].endswith("0") or skey.count("XY"): continue
        elif skey.count("Pio") or skey.count("Kao"): continue

        # for testing
        #if not skey.startswith("OrigZMuon"): continue

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

        #print xnbins, xmin, xmax, "xnbins, xmin, xmax"
        var = ''
        energyweight = ''
        cf = 0.01
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

        elif hname.startswith("OrigZ"):
            binwidth = cf*(xmax-xmin)/xnbins
            xaxis = [cf*xmin+i*binwidth for i in range(xnbins+1)]
            var = 'z_interact*0.01'
            xtitle = "s [m]"

        if not particleTypes[0].count('ll'):
            pcuts = [ 'particle ==' + p for p in particleTypes  ]
            pcut  = '||'.join(pcuts)
            cuts += ['('+ pcut + ')']

        # -- y axis = z-position
        ynbins, ymin, ymax = 524, 22.6, 546.6 # MUST TAKE FULL RANGE
        twoDhist = TH2F(skey, skey, xnbins, array('d', xaxis), ynbins, ymin, ymax)

        binw = (ymax-ymin)/ynbins
        if debug: print xaxis[:10], xaxis[-5:], len(xaxis), array('d', xaxis)[:10]
        
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
        #hist_flat = twoDhist_flat.Clone("some1dclone")
        hist_flat.SetLineColor(kTeal-2)
        print "hist_flat.GetEntries()", hist_flat.GetEntries()
        print "twoDhist_flat.GetEntries()", twoDhist_flat.GetEntries()
        
        #for i in range(xnbins+1): print "hist_flat.GetBinLowEdge(i)",hist_flat.GetBinLowEdge(i)
        # -- create pint histogram when at least 1 histogram is formed and do it only once
        if cnt == 1:
            hist_pint = twoDhist.ProjectionY("pint")
            #hist_pint = twoDhist.Clone("pint")## 1d test case

            if do6p5:
                data = cv79.getdata5c(pressFile)
                rho_H2, rho_CH4, rho_CO, rho_CO2 = cv79.getrho(data['H2_Eq']),cv79.getrho(data['CH4_Eq']),cv79.getrho(data['CO_Eq']),cv79.getrho(data['CO2_Eq'])
                rho_H, rho_C, rho_O = cv79.getAtomicRho(rho_H2, rho_CH4, rho_CO, rho_CO2)
                s = data['s']
            else:
                s, rho_C, rho_H, rho_O = cv65.getAtomicRho(data)
                
            pint_tot = cv66.calc_pint_tot(energy,rho_C, rho_H, rho_O)                
            pint_incomingbeam = {}

            for i,spoS in enumerate(s):
                spos = float(spoS)
                if spos < 0.: 
                    z = -spos
                    pint_incomingbeam[z] = pint_tot[i]
                    zbin = hist_pint.FindBin(z)
                    hist_pint.SetBinContent(zbin, pint_incomingbeam[z])

            # first value is for arc
            arcvalue = pint_tot[1]

            startarcBin = hist_pint.FindBin(startarc)
            print "setting arc pressure in bin", startarcBin, hist_pint.GetBinLowEdge(startarcBin),hist_pint.GetNbinsX()#, hist_pint.GetBinLowEgde(hist_pint.GetNbinsX()+1), 
            for i in range(startarcBin, ynbins+1): hist_pint.SetBinContent(i,arcvalue)    

            # --

        # compute re-weights for each bin
        Mk = nprim/ynbins # number of primary interactions per zbin on yaxis
        for j in range(1,ynbins+1):
            scale = 1e2 * beamintensity * hist_pint.GetBinContent(j) * binw/Mk            
            for i in range(1,xnbins+1):
                m = twoDhist_flat.GetBinContent(i,j)
                twoDhist_reweighted.SetBinContent(i,j,scale * m)

        hists_flat += [twoDhist_flat]          
        hists_reweighted += [twoDhist_reweighted]
        rHists += [skey]
        print hists_flat[-1].GetNbinsX()
        hists_flat[-1].Write() 
        hists_reweighted[-1].Write()
    hist_pint.GetXaxis().SetTitle("s [m]")
    hist_pint.GetYaxis().SetTitle("interaction probability [1/s/m]")
    hist_pint.Write()
    rfOUTile.Close()
    print 'wrote ','.'*20, rfoutname
    
    # --

