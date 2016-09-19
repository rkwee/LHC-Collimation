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
from fillTTree import getXLogAxis
from fillTTree_dict import generate_sDict
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

    pint_C = [sigma_C*j/Trev for j in rho_C[1:]]
    pint_H = [sigma_H*j/Trev for j in rho_H[1:]]
    pint_O = [sigma_O*j/Trev for j in rho_O[1:]]

    pint_tot = [pint_H[i] + pint_O[i] + pint_C[i] for i in range(len(pint_O))]
    return pint_tot

def cv70():
# --------------------------------------------------------------------------------
# density profile is given in the following format:
# densities per molecule as function of s-coordinate
# x,y,z, cx, cy, cz as function of (different s-coordinate)
# merge densities with coordinates
# note, that the source routine needs fluka units, ie *cm*!
# --------------------------------------------------------------------------------
    bgfile    = '/afs/cern.ch/work/r/rkwee/HL-LHC/beam-gas-sixtrack/pressure_profiles_2012/LSS1_B1_Fill2736_Final.csv'

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

            s[i] = float(data['s'][i])

        except ValueError:
            continue

    # --
    # x axis, value
    nbins, xmin, xmax = 60, 1e-2, 1.e4
    xaxis = getXLogAxis(nbins, xmin, xmax)
    xnbins = len(xaxis)-1

    # y axis, weigths
    hname, ynbins, ymin, ymax = 'all', 523, 22.5, 550
    twoDhist = TH2F(hname, hname, xnbins, array('d', xaxis), ynbins, ymin, ymax)
    # -- create histogram with same axis for pint 
    hist_pint = twoDhist.ProjectionY("pint")
    pint_tot = calc_pint_tot(rho_C, rho_H, rho_O)
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


    datafile = '/afs/cern.ch/project/lhc_mib/valBG4TeV/ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67'
    bbgFile = datafile + ".root"
    print "Opening", bbgFile
    norm = float(bbgFile.split('nprim')[-1].split('_')[0])
    rfile = TFile.Open(bbgFile, "READ")

    hists = []
    cnt = 0

    mt  = rfile.Get('particle')

    particleTypes = [10, 11]

    # -- fill 2d histo
    hname_flat = 'EkinAll_flatpressure'
    twoDhist_flat = twoDhist.Clone(hname_flat)
    twoDhist_flat.Sumw2()

    hname_reweighted = 'EkinAll_reweighted'
    twoDhist_reweighted = twoDhist.Clone(hname_reweighted)

    # y is on y-axis, x on x-axis
    # var = "y:x"

    var = '0.01*z_interact:energy_ke'
    cuts = "weight * ( energy_ke > 0.2 )"
    print "INFO: applying", cuts, "to", var, "in", hname_flat
    mt.Project(hname_flat, var, cuts)

    print "entries  ", twoDhist_flat.GetEntries()
    hist_flat = twoDhist_flat.ProjectionX("makeit1d_flat")
    hist_flat.SetLineColor(kGreen-2)

    beamintensity = 2e14
    nprim = float(bbgFile.split('nprim')[-1].split('_')[0]) 
    Trev  = 2*math.pi/112450
    kT = 1.38e-23*300

    # compute normalisation fct for each bin

    for w in range(1,ynbins+1):
        scale = beamintensity * hist_pint.GetBinContent(w)
        for v in range(1,xnbins+1):
            m = twoDhist_flat.GetBinContent(v,w)  
            print "Weight", scale * m, "m", m, "scale",scale, "x,y", v,w
            twoDhist_reweighted.SetBinContent(v,w,scale * m)

    cv = TCanvas( 'cv', 'cv', 1500, 900)

    x1, y1, x2, y2 = 0.7, 0.65, 0.9, 0.88
    mlegend = TLegend( x1, y1, x2, y2)
    mlegend.SetFillColor(0)
    mlegend.SetFillStyle(0)
    mlegend.SetLineColor(0)
    mlegend.SetTextSize(0.035)
    mlegend.SetShadowColor(0)
    mlegend.SetBorderSize(0)

    # YurMin, YurMax = 2e2, 9e6
    # hist.GetYaxis().SetRangeUser(YurMin,YurMax)
    # XurMin,XurMax = 0.,545.
    # hist.GetXaxis().SetRangeUser(XurMin,XurMax)
    ytitle = "GeV/m/BG int."
    hist_flat.Scale(1./hist_flat.Integral())
    hist_flat.GetYaxis().SetTitle(ytitle)
    hist_flat.Draw("h")
    lg, lm = "flat", 'l'
    mlegend.AddEntry(hist_flat, lg, lm)

    hist_reweighted = twoDhist_reweighted.ProjectionX("makeit1d_reweighted")
    hist_reweighted.SetLineColor(kPink-3)
    hist_reweighted.Scale(1./hist_reweighted.Integral())
    hist_reweighted.GetYaxis().SetTitle(ytitle)
    hist_reweighted.Draw("hsame")
    lg, lm = "reweighted", 'l'
    mlegend.AddEntry(hist_reweighted, lg, lm)
    #twoDhist_reweighted.Draw("colz")
#    hist_pint.Draw("hist")
    cv.SetLogx(1)
    cv.SetLogy(1)
    gPad.RedrawAxis()

    lab = mylabel(42)
    lab.DrawLatex(0.45, 0.9, '4 TeV beam-gas' )
#    lab.DrawLatex(0.7, 0.82, '#mu^{#pm}' )

    mlegend.Draw()

    pname = wwwpath + 'TCT/4TeV/beamgas/fluka/bs/reweighted/Ekin.pdf'
    print('Saving file as ' + pname ) 
    cv.Print(pname)

