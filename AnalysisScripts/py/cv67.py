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
# get function to read the data if 14 columns are present 
from cv32 import getdata14c
from helpers import makeTGraph, mylabel, wwwpath
# --------------------------------------------------------------------------------
# calc total interaction probability
sigma_N = 286.e-31
Trev = 2*math.pi/112450
def calc_pint_tot(rho_C, rho_H, rho_O):
    # 3.5 TeV inel cross-sections proton-atom from paper
    sigma_O = 316.e-31
    sigma_C = 258.e-31
    sigma_H =  37.e-31

    # # 4 TeV inel cross sections scaled up
    # sigma_O = 318.e-31
    # sigma_C = 260.e-31
    # sigma_H = 37.1e-31

    
    pint_C = [sigma_N*j/Trev for j in rho_C[1:]]
    pint_H = [sigma_N*j/Trev for j in rho_H[1:]]
    pint_O = [sigma_N*j/Trev for j in rho_O[1:]]

    pint_tot = [pint_H[i] + pint_O[i] + pint_C[i] for i in range(len(pint_O))]
    return pint_tot

def cv67():
# --------------------------------------------------------------------------------
# density profile is given in the following format:
# densities per molecule as function of s-coordinate
# x,y,z, cx, cy, cz as function of (different s-coordinate)
# merge densities with coordinates
# note, that the source routine needs fluka units, ie *cm*!
# --------------------------------------------------------------------------------

    energy = "4 TeV"
    bgfile    = '/afs/cern.ch/work/r/rkwee/HL-LHC/beam-gas-sixtrack/pressure_profiles_2012/LSS1_B1_Fill2736_Final.csv'
    bgfile = "/Users/rkwee/Documents/RHUL/work/data/4TeV/LSS1_B1_Fill2736_Final.csv"
    beamintensity = 2e14

    energy = " 3.5 TeV "
    bgfile = "/Users/rkwee/Documents/RHUL/work/HL-LHC/runs/TCT/LSS1_B1_fill_2028-sync_rad_and_ecloud.csv"
    beamintensity = 1.66e14 # https://acc-stats.web.cern.ch/acc-stats/#lhc/fill-details 2028
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

            # compute atomic rhos and translate nitrogen equivalent density 

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
    # calculate the scaled number

    # unscaled inf
    hname, nbins, xmin, xmax = 'muons', 523, 22.5, 550
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
    hist_e100  = hist.Clone("e100")
    hist_e100p = hist.Clone("e100p")

    cuts = "(particle == 10 || particle == 11) && energy_ke > 100.0"
    var  = 'z_interact * 0.01'
    print "INFO: applying", cuts, "to", var, "in", "e100"
    mt.Project("e100", var, cuts)

    cuts = "(particle == 10 || particle == 11) && energy_ke > 0.02"
    print "INFO: applying", cuts, "to", var, "in", hname
    mt.Project(hname, var, cuts)


    sigma_N = 286.e-31
    sigma_N_4TeV = 289.e-31
    Trev = 2*math.pi/112450

    # create histogram with same axis for pint 
    pint_tot_atomic = calc_pint_tot(rho_C, rho_H, rho_O)
    # N2Eq_tot = [ float(data['CO_N2Eq'][i]) + float(data['CO2_N2Eq'][i]) + float(data['CH4_N2Eq'][i]) + float(data['H2_N2Eq'][i]) for i in range(1,len(data['s'])) ]
    # pint_tot = [sigma_N*j/Trev for j in range(len(N2Eq_tot))]

    rho_tot = [ float(data['rho_CO'][i]) + float(data['rho_CO2'][i]) + float(data['rho_CH4'][i]) + float(data['rho_H2'][i]) for i in range(1,len(data['s'])) ]
    pint_tot = [sigma_N*rho/Trev for rho in rho_tot]
    pint_incomingbeam = {}

    for i,sPos in enumerate(s):
        spos = float(sPos)
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
    for i in range(1,nbins+1):
        m = hist_flat.GetBinContent(i)
        scale = beamintensity * hist_pint.GetBinContent(i)
        hist.SetBinContent(i,scale * m)
        hist_e100p.SetBinContent(i, scale * hist_e100.GetBinContent(i))
        if i<11:
            print "pint in bin", i, "is", hist_pint.GetBinContent(i)
            print "pint * beamintensity is", scale
            print "pint * beamintensity * m is", scale*m

    cv = TCanvas( 'cv', 'cv', 2100, 900)
    cv.SetGridy(1)
    cv.SetGridx(1)
    x1, y1, x2, y2 = 0.7, 0.65, 0.9, 0.88
    mlegend = TLegend( x1, y1, x2, y2)
    mlegend.SetFillColor(0)
    mlegend.SetFillStyle(0)
    mlegend.SetLineColor(0)
    mlegend.SetTextSize(0.035)
    mlegend.SetShadowColor(0)
    mlegend.SetBorderSize(0)

    ytitle = "particles/m/BG int."

    YurMin, YurMax = 2e2, 9e6
    hist.GetYaxis().SetRangeUser(YurMin,YurMax)
    XurMin,XurMax = 0.,545.
    hist.GetXaxis().SetRangeUser(XurMin,XurMax)
    hist_flat.SetLineColor(kRed)
    hist_flat.GetYaxis().SetTitle(ytitle)
    hist.GetYaxis().SetTitle(ytitle)
    hist_e100p.SetFillColor(kRed-3)
    hist_e100p.SetLineColor(kRed-3)
#    hist_flat.Draw("hist")
    hist.Draw("hist")
    hist_e100p.Draw("histsame")
    #hist_pint.GetXaxis().SetRangeUser(1.e-13,2.5e-11)
    #hist_pint.Draw("l")
    lg, lm = "#mu^{#pm}", 'l'
    mlegend.AddEntry(hist_flat, lg, lm)

    lg, lm = "#mu^{#pm} E > 100 GeV", 'f'
    mlegend.AddEntry(hist_e100p, lg, lm)

    gPad.SetLogy(1)
    gPad.RedrawAxis()

    lab = mylabel(42)
    #    lab.DrawLatex(0.45, 0.9, energy+'beam-gas' )
    lab.DrawLatex(0.4, 0.82, energy )

    #mlegend.Draw()

    pname = wwwpath + 'TCT/beamgas/pressure_profiles_2012/muonrates.pdf'
    pname = "/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/4TeV/reweighted/muonrates.pdf"
    pname = "/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/4TeV/reweighted/muonrates2011.pdf"
    #   pname = "/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/4TeV/reweighted/pint2011.pdf"
    print('Saving file as ' + pname ) 
    cv.Print(pname)

