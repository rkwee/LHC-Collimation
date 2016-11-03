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
    # updated to 4 TeV 
    sigma_O = 318.e-31
    sigma_C = 260.e-31
    sigma_H =  37.1e-31
    Trev = 1./11245

    pint_C = [sigma_C*j/Trev for j in rho_C[1:]]
    pint_H = [sigma_H*j/Trev for j in rho_H[1:]]
    pint_O = [sigma_O*j/Trev for j in rho_O[1:]]

    pint_tot = [pint_H[i] + pint_O[i] + pint_C[i] for i in range(len(pint_O))]
    return pint_C, pint_H, pint_O, pint_tot

def getAtomicRho(data):
    debug = 0

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

    return s, rho_C, rho_H, rho_O
def cv65():
# --------------------------------------------------------------------------------
# density profile is given in the following format:
# densities per molecule as function of s-coordinate
# x,y,z, cx, cy, cz as function of (different s-coordinate)
# merge densities with coordinates
# note, that the source routine needs fluka units, ie *cm*!
# --------------------------------------------------------------------------------
    bgfile    = '/afs/cern.ch/work/r/rkwee/HL-LHC/beam-gas-sixtrack/pressure_profiles_2012/LSS1_B1_Fill2736_Final.csv'
    bgfile    = '/Users/rkwee/Documents/RHUL/work/data/4TeV/LSS1_B1_Fill2736_Final.csv'

    data = getdata14c(bgfile)
    print 'data keys are',data.keys()

    # --
    s, rho_C, rho_H, rho_O = getAtomicRho(data)

    # plot atomic densities

    cv = TCanvas( 'cv', 'cv', 2100, 900)

    x1, y1, x2, y2 = 0.8, 0.7, 0.9, 0.92
    mlegend = TLegend( x1, y1, x2, y2)
    mlegend.SetFillColor(0)
    mlegend.SetFillStyle(0)
    mlegend.SetLineColor(0)
    mlegend.SetTextSize(0.035)
    mlegend.SetShadowColor(0)
    mlegend.SetBorderSize(0)

    mg = TMultiGraph()
    lm = 'pl'

    pint_C, pint_H, pint_O, pint_tot = calc_pint_tot(rho_C, rho_H, rho_O)

    xlist, ylist, col, mstyle, lg = s[1:], pint_tot, kBlack, 28, 'total'
    g3 = makeTGraph(xlist, ylist, col, mstyle)
    mlegend.AddEntry(g3, lg, lm)    
    mg.Add(g3)

    xlist, ylist, col, mstyle, lg = s[1:], pint_O, kGreen, 22, 'O'
    g0 = makeTGraph(xlist, ylist, col, mstyle)
    mlegend.AddEntry(g0, lg, lm)    
    mg.Add(g0)

    xlist, ylist, col, mstyle, lg = s[1:], pint_C, kGreen-1, 20, 'C'
    g1 = makeTGraph(xlist, ylist, col, mstyle)
    mlegend.AddEntry(g1, lg, lm)    
    mg.Add(g1)


    xlist, ylist, col, mstyle, lg = s[1:], pint_H, kBlue-2, 23, 'H'
    g2 = makeTGraph(xlist, ylist, col, mstyle)
    mlegend.AddEntry(g2, lg, lm)    
    mg.Add(g2)

    mg.Draw("alp")

    gPad.SetLogy(1)
    gPad.RedrawAxis()

    lab = mylabel(42)
    lab.DrawLatex(0.45, 0.88, 'interaction probability' )

    mg.SetTitle("pressure profiles")
    mg.GetXaxis().SetTitle('distance to IP1 [m]')
    mg.GetYaxis().SetTitle('interaction probability [1/proton/m/s]')#"density #rho [atoms/m^{3}]")
    mg.GetYaxis().SetRangeUser(7e-17,9e-11)
    mlegend.Draw()

    pname = wwwpath + 'TCT/beamgas/pressure_profiles_2012/pint.pdf'
    pname = "/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/4TeV/reweighted/cv65_pint.pdf"
    print('Saving file as ' + pname ) 
    cv.Print(pname)

