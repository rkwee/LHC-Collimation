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
import cv66 
# --------------------------------------------------------------------------------
# calc total interaction probability


def resultFileBG(k,rel):
    n = os.path.join(os.path.dirname(k),"results_pressure2011_"+rel+k.split('/')[-1])
    return  n

def cv70():
# --------------------------------------------------------------------------------
# density profile is given in the following format:
# densities per molecule as function of s-coordinate
# x,y,z, cx, cy, cz as function of (different s-coordinate)
# merge densities with coordinates
# note, that the source routine needs fluka units, ie *cm*!
# --------------------------------------------------------------------------------
    bgfile    = '/afs/cern.ch/work/r/rkwee/HL-LHC/beam-gas-sixtrack/pressure_profiles_2012/LSS1_B1_Fill2736_Final.csv'

    energy = " 3.5 TeV "
    bgfile = "/Users/rkwee/Documents/RHUL/work/HL-LHC/runs/TCT/LSS1_B1_fill_2028-sync_rad_and_ecloud.csv"

    debug = 0

    data = getdata14c(bgfile)
    print 'data keys are',data.keys()
    nb_s = len(data['s'])
    print 'number of s values', nb_s

    # atomic densities
    rho_C, rho_H, rho_O = [0 for i in range(nb_s)],[0 for i in range(nb_s)],[0 for i in range(nb_s)]
    s = [-9999 for i in range(nb_s)]

    cf = 1.

    for i in range(1,nb_s):
        # get the data
        try:
            if debug:
                print 'i = ', i
                print "data['rho_H2'][i]", data['rho_H2'][i]
                print "data['rho_CH4'][i]", data['rho_CH4'][i]
                print "data['rho_CO'][i]", data['rho_CO'][i]
                print "data['rho_CO2'][i]", data['rho_CO2'][i]

            rho_H2   = cf * float(data['rho_H2'][i])
            rho_CH4  = cf * float(data['rho_CH4'][i])
            rho_CO   = cf * float(data['rho_CO'][i])
            rho_CO2  = cf * float(data['rho_CO2'][i])

            # compute atomic rhos

            rho_H[i]  = 2.0*rho_H2
            rho_H[i] += 4.0*rho_CH4

            rho_C[i]  = 1.0*rho_CH4
            rho_C[i] += 1.0*rho_CO
            rho_C[i] += 1.0*rho_CO2

            rho_O[i]  = 1.0*rho_CO
            rho_O[i] += 2.0*rho_CO2

            s[i] = float(data['s'][i])

        except ValueError:
            continue

    # --

    datafile = '/afs/cern.ch/project/lhc_mib/valBG4TeV/ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67'
    beamintensity = 2e14    
    tag = '_BG_4TeV_20MeV_bs'

    datafile = "/Users/rkwee/Documents/RHUL/work/HL-LHC/runs/TCT/beam_gas_3.5TeV_IR1_to_arc_20MeV_100M_nprim7660649_66"
    beamintensity = 1.66e14    
    tag = "_BG_3p5TeV_20MeV"

    bbgFile = datafile + ".root"    
    print "Opening", bbgFile
    
    nprim = float(bbgFile.split('nprim')[-1].split('_')[0])
    rfile = TFile.Open(bbgFile, "READ")
    tBBG = rfile.Get("particle")
    yrel = ''
    print tBBG
    sDict = generate_sDict(tag, nprim, tBBG, yrel)

    # -- small version of fillTTree
    Trev  = 2*math.pi/112450
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
        #elif skey.count("Z"): continue
        elif skey.count("Neu_"): continue
        elif skey.count("Char"): continue
        elif skey.count("Plus") or skey.count("Minus"): continue
        elif skey.split(tag)[0].endswith("0") or skey.count("XY"): continue
        elif skey.count("Pio") or skey.count("Kao"): continue

        # for testing
        if not skey.startswith("OrigZMuon"): continue

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
        elif hname.startswith("OrigZ"):
            binwidth = (xmax-xmin)/xnbins
            xaxis = [xmin+i*binwidth for i in range(xnbins+1)]
            var = 'z_interact*0.01'
            xtitle = "s [m]"

        if not particleTypes[0].count('ll'):
            pcuts = [ 'particle ==' + p for p in particleTypes  ]
            pcut  = '||'.join(pcuts)
            cuts += ['('+ pcut + ')']

        # -- y axis, weigths
        ynbins, ymin, ymax =  546,0,546.
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
            pint_tot = cv66.calc_pint_tot(rho_C, rho_H, rho_O)
            pint_incomingbeam = {}

            for i,spos in enumerate(s):
                if spos < 0.: 
                    z = -spos
                    pint_incomingbeam[z] = pint_tot[i]
                    zbin = hist_pint.FindBin(z)
                    hist_pint.SetBinContent(zbin, pint_incomingbeam[z])

            # first value is for arc
            arcvalue = pint_tot[1]

            startarc = 260.
            startarcBin = hist_pint.FindBin(startarc)
            for i in range(startarcBin, ynbins-1): hist_pint.SetBinContent(i,arcvalue)    
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

    #     hcolor = sDict[skey][7]
    #     hists[-1].SetLineColor(hcolor)
    #     hists[-1].SetLineWidth(3)

    #     if not i: 
    #         if   type(hists[-1]) == TH1F: hists[-1].Draw("HIST")
    #         hists[-1].SetMarkerColor(hcolor)
    #         hists[-1].Draw("P")
    #     else:
    #         if   type(hists[-1]) == TH1F: hists[-1].Draw("HISTSAME")
        
        # writing two d hists
        hists_flat[-1].Write()
        hists_reweighted[-1].Write()

    rfOUTile.Close()
    print 'wrote ','.'*20, rfoutname
    
    # --

