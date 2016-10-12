#!/usr/bin/python
#
#
#
# R Kwee, 2016
# 
# ---------------------------------------------------------------------------------
import ROOT, sys, glob, os, math, helpers
from ROOT import *
# get function to read the data if 14 columns are present 
from cv32 import getdata14c
from helpers import makeTGraph, mylabel, wwwpath
# --------------------------------------------------------------------------------
# calc total interaction probability

def calc_pint_tot(rho_C, rho_H, rho_O):
    # 3.5 TeV inel cross-sections proton-atom from paper
    sigma_O = 316.e-31
    sigma_C = 258.e-31
    sigma_H =  37.e-31
    Trev = 2*math.pi/112450
    sigma_N = 286.e-31
    
    pint_C = [sigma_N*rho/Trev for rho in rho_C[1:]]
    pint_H = [sigma_N*rho/Trev for rho in rho_H[1:]]
    pint_O = [sigma_N*rho/Trev for rho in rho_O[1:]]

    pint_tot = [pint_H[i] + pint_O[i] + pint_C[i] for i in range(len(pint_O))]
    return pint_tot

def cv66():
# --------------------------------------------------------------------------------
# density profile is given in the following format:
# densities per molecule as function of s-coordinate
# x,y,z, cx, cy, cz as function of (different s-coordinate)
# merge densities with coordinates
# note, that the source routine needs fluka units, ie *cm*!
# --------------------------------------------------------------------------------
    energy = '4 TeV beam-gas' 
    bgfile    = '/afs/cern.ch/work/r/rkwee/HL-LHC/beam-gas-sixtrack/pressure_profiles_2012/LSS1_B1_Fill2736_Final.csv'
    beamintensity = 2e14
    
    energy = " 3.5 TeV "
    bgfile = "/Users/rkwee/Documents/RHUL/work/HL-LHC/runs/TCT/LSS1_B1_fill_2028-sync_rad_and_ecloud.csv"
    beamintensity = 1.66e14

    print "Using", bgfile
    
    debug = 0

    data = getdata14c(bgfile)
    print 'data keys are',data.keys()
    nb_s = len(data['s'])
    print 'number of s values', nb_s

    # atomic densities
    rho_C, rho_H, rho_O = [0 for i in range(nb_s)],[0 for i in range(nb_s)],[0 for i in range(nb_s)]
    s = [-9999 for i in range(nb_s)]

    cf = 1.
    #for i in [1, 100, 300,500]:
    for i in range(1,nb_s):
        # get the data, convert to cm3
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

            rho_H[i]=0
            rho_C[i]=0
            rho_O[i]=(rho_H2*2.+rho_CH4*16.+rho_CO*28.+rho_CO2*44.)*4./(2.+16.+28.+44.)
            
            s[i] = float(data['s'][i])

        except ValueError:
            continue

    # --
    # calculate the scaled number

    # unscaled inf
    hname, nbins, xmin, xmax = 'muons', 546, 0., 546.
    binw = (xmax-xmin)/nbins
    hist = TH1F(hname, hname, nbins, xmin, xmax)
    hist.Sumw2()
    hist.GetXaxis().SetTitle('s [m]')
    datafile = '/afs/cern.ch/project/lhc_mib/valBG4TeV/ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67'
    datafile = '/Users/rkwee/Documents/RHUL/work/HL-LHC/runs/TCT/ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67'
    datafile = "/Users/rkwee/Documents/RHUL/work/HL-LHC/runs/TCT/beam_gas_3.5TeV_IR1_to_arc_20MeV_100M_nprim7660649_66"

    bbgFile = datafile + ".root"


    rfile = TFile.Open(bbgFile, "READ")

    hists = []
    cnt = 0

    mt  = rfile.Get('particle')

    particleTypes = [10, 11]

    hname = 'muons_flatpressure'
    hist_flat = hist.Clone(hname)
    hist_pint = hist.Clone("pint")
    var = "z_interact*0.01"
    cuts = "(particle == 10 || particle == 11) && energy_ke > 0.02"
    print "INFO: applying", cuts, "to", var, "in", hname
    mt.Project(hname, var, cuts)

    # create histogram with same axis for pint 
    pint_tot = calc_pint_tot(rho_C, rho_H, rho_O)
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

    startarc = 260.
    startarcBin = hist_pint.FindBin(startarc)
    for i in range(startarcBin, nbins-1): hist_pint.SetBinContent(i,arcvalue)
    
    nprim = float(bbgFile.split('nprim')[-1].split('_')[0]) 
    Trev  = 2*math.pi/112450
    kT = 1.38e-23*300

    # compute normalisation fct for each bin
    for i in range(nbins):
        m = hist_flat.GetBinContent(i)
        scale = beamintensity * hist_pint.GetBinContent(i)
        hist.SetBinContent(i,scale * m)

    cv = TCanvas( 'cv', 'cv', 2100, 900)

    x1, y1, x2, y2 = 0.57, 0.65, 0.9, 0.88
    mlegend = TLegend( x1, y1, x2, y2)
    mlegend.SetFillColor(0)
    mlegend.SetFillStyle(0)
    mlegend.SetLineColor(0)
    mlegend.SetTextSize(0.035)
    mlegend.SetShadowColor(0)
    mlegend.SetBorderSize(0)

    ytitle = "arbitrary units"
    YurMin, YurMax = 2e2, 9e6
    hist.GetYaxis().SetRangeUser(YurMin,YurMax)
    hist.SetMarkerColor(kRed)
    hist.SetLineColor(kRed)
    hist.GetYaxis().SetTitle(ytitle)
    XurMin,XurMax = 0.,545.
    hist.GetXaxis().SetRangeUser(XurMin,XurMax)
    YurMin, YurMax = 2e2, 9e6
    hist.GetYaxis().SetRangeUser(YurMin,YurMax)
    hist.Draw("hist")
    hist_flat.Scale(1e2)
    hist_flat.Draw("histsame")

    hist_pint.SetLineColor(kGreen-3)
    hist_pint.Scale(1e16)
    hist_pint.Draw("histsame")

    lg, lm = "interaction probability", 'l'
    mlegend.AddEntry(hist_pint, lg, lm)

    lg, lm = "interaction probability x10^{16}", 'l'
    mlegend.AddEntry(hist_pint, lg, lm)

    lg, lm = "#mu^{#pm} normalised to pressure profile", 'l'
    mlegend.AddEntry(hist, lg, lm)

    # lg, lm = "#mu^{#pm} rates/BG int. flat pressure", 'l'
    # mlegend.AddEntry(hist_flat, lg, lm)

    gPad.SetLogy(1)
    gPad.RedrawAxis()

    lab = mylabel(42)
    lab.DrawLatex(0.45, 0.9, energy)

    mlegend.Draw()

    pname = wwwpath + 'TCT/beamgas/pressure_profiles_2012/flatvsprofile.pdf'
    pname = "/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/4TeV/reweighted/atomicrho2011.pdf"
    pname = "/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/4TeV/reweighted/pressure2011.pdf"
    print('Saving file as ' + pname ) 
    cv.Print(pname)

