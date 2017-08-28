#!/usr/bin/python
#
# plot pint for HL LHC
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
from helpers import *
import cv79
## -------------------------------------------------------------------------------

def getdata14cHL(pFile):

    print ("Opening", pFile)
    with open(pFile) as gf:

        for alldatainoneline in gf:

            alllines=alldatainoneline.split("^M")

    # alllines is a list with 1 element consisting of 1 string
    alll=alllines[0].split("\r")

    # alll: list with strings, each string is one data line. should be 14 values per line
    nlines = len(alll)

    c = [ [] for i in range(14) ]
    for ii, dline in enumerate(alll):
        # nval = list with strings: each string is 1 value

        vals  = dline.split(",")
        ncols = len(vals)  # == 14
        if ii==0: print "title", ii, vals

        # fill each column with values
        else:

            # vals is list of strings, list of nvals==14 values
            for v in range(14): c[v] += [ vals[v] ]

        # produces no printout , all have ncols == 14
        # if ncols!=14: print "not 14 lines, but?",i, len(dline)

    data = dict(s=c[0], l_total=c[1], rho_H2=c[2], rho_CH4=c[3], rho_CO=c[4], rho_CO2=c[5], \
                H2_N2Eq=c[6], CH4_N2Eq=c[7], CO_N2Eq=c[8], CO2_N2Eq=c[9], avPress=c[10], avPressCorr=c[11], H2Eq=c[12], H2EqCorr=c[13])

    return data

def cv95():

    # HL gas file
    pFile = "/Users/rkwee/Documents/RHUL/work/HL-LHC/HL_LHC_D2_IP_LSS1_After_Conditioning_Anton_onlydata.csv"
    xTitle= "distance from IP1 [m]"
    lText="HL-LHC after conditioning high "

    data = getdata14cHL(pFile)
    
    # plot pint
    rel = 'pintHL'
    cv = TCanvas( 'cv'+ rel+lText , 'cv'+rel+ lText , 2100, 900)
    cv.SetLogy(1)
    #cv.SetGridy(1)
    x1, y1, x2, y2 = 0.8, 0.72, 0.9, 0.92
    mlegend = TLegend( x1, y1, x2, y2)
    mlegend.SetFillColor(0)
    mlegend.SetFillStyle(0)
    mlegend.SetLineColor(0)
    mlegend.SetTextSize(0.035)
    mlegend.SetShadowColor(0)
    mlegend.SetBorderSize(0)

    mg = TMultiGraph(rel,rel)
    lm = 'l'

    rho_H2 = cv79.getrho(data['H2_N2Eq'])
    rho_CH4 = cv79.getrho(data['CH4_N2Eq'])
    rho_CO2 =cv79.getrho(data['CO2_N2Eq'])
    rho_CO = cv79.getrho(data['CO_N2Eq'])
    rho_H, rho_C, rho_O = cv79.getAtomicRho(rho_H2, rho_CH4, rho_CO, rho_CO2)

    pint_H, pint_C,pint_O, pint_tot = cv79.getpint(rho_H,rho_C,rho_O)

    
    xlist, ylist, col, mstyle, lg = data['s'],pint_tot , kBlack, 20, 'total'
    g3 = makeTGraph(xlist, ylist, col, mstyle)
    mlegend.AddEntry(g3, lg, lm)    
    mg.Add(g3)

    xlist, ylist, col, mstyle, lg = data['s'],pint_H , kTeal+3, 22, 'H'
    g0 = makeTGraph(xlist, ylist, col, mstyle)
    mlegend.AddEntry(g0, lg, lm)    
    mg.Add(g0)

    xlist, ylist, col, mstyle, lg = data['s'], pint_O, kAzure-4, 33, 'O'
    g2 = makeTGraph(xlist, ylist, col, mstyle)
    mlegend.AddEntry(g2, lg, lm)    
    mg.Add(g2)

    xlist, ylist, col, mstyle, lg = data['s'], pint_C, kMagenta-1, 24, 'C'
    g1 = makeTGraph(xlist, ylist, col, mstyle)
    mlegend.AddEntry(g1, lg, lm)    
    mg.Add(g1)

    mg.Draw("al")

    mg.SetTitle("pressure profiles")
    mg.GetXaxis().SetTitle(xTitle)
    mg.GetYaxis().SetTitle("interaction probability density")
    mg.GetYaxis().SetRangeUser(5e-19,1e-10)
    mlegend.Draw()
    lab = mylabel(42)
    lab.DrawLatex(0.45, 0.88, lText)        

    pname = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/HLRunII/'
    pname += pFile.split('.')[0].split("/")[-1] + "_"+rel+".pdf"
    print('Saving file as ' + pname )
    cv.Print(pname)
