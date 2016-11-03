#!/usr/bin/python
#
# compare pressure profiles 6.5 TeV 2015
# compare incoming side only
# 
# Oct 2016, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, os, time, math
from ROOT import *
import helpers, array
from helpers import wwwpath, length_LHC, mylabel, gitpath, workpath, makeTGraph
from array import array
import cv79
## -------------------------------------------------------------------------------
pData = [
    ("/Users/rkwee/Downloads/Density_Fill4536_2041b_26158.8832-500_B1_withECLOUD.txt", "distance from IP1 [m]", "Fill 4536 B1"),
    ("/Users/rkwee/Downloads/Density_Fill4536_2041b_26158.8832-500_B2_withECLOUD.txt", "distance from IP1 [m]",  "Fill 4536 B2"),
    ("/Users/rkwee/Downloads/Density_Fill4532_1824b_26158.8832-500_B1_withECLOUD.txt", "distance from IP1 [m]",  "Fill 4532 B1"),
    ("/Users/rkwee/Downloads/Density_Fill4532_1824b_26158.8832-500_B2_withECLOUD.txt", "distance from IP1 [m]",  "Fill 4532 B2"),
]
# # -----------------------------------------------------------------------

def cv82():
    # ---------------------------------------------------
    rel = 'allpinttot'
    cv = TCanvas( 'cv'+ rel , 'cv'+rel , 2100, 900)
    cv.SetLogy(0)
    cv.SetGridy(0)
    x1, y1, x2, y2 = 0.75, 0.72, 0.88, 0.92
    mlegend = TLegend( x1, y1, x2, y2)
    mlegend.SetFillColor(0)
    mlegend.SetFillStyle(0)
    mlegend.SetLineColor(0)
    mlegend.SetTextSize(0.035)
    mlegend.SetShadowColor(0)
    mlegend.SetBorderSize(0)

    mg = TMultiGraph(rel,rel)
    lm = 'l'
    
    grs = []
    
    for i,( pFile, xTitle, lText) in enumerate(pData):

        print "Getting data from file", pFile
        fillnumber = pFile.split("Density_")[1].split('b_26')[0] + 'b'
        print  "."*33
        data = cv79.getdata5c(pFile)

        s_incoming = []
        
        # only one side, chose positive s
        s_positiveb1, s_positiveb2 = [],[]

        for cs in data['s']:
            s = float(cs)
            if s<0.:
                s_positiveb1 += [-s]
            else:
                s_positiveb2 += [s]
                
        print "len(s_positiveb1)",len(s_positiveb1)
        print "len(s_positiveb2)",len(s_positiveb2)


        rho_H2, rho_CH4, rho_CO, rho_CO2 = cv79.getrho(data['H2_Eq']),cv79.getrho(data['CH4_Eq']),cv79.getrho(data['CO_Eq']),cv79.getrho(data['CO2_Eq'])
        rho_H, rho_C, rho_O = cv79.getAtomicRho(rho_H2, rho_CH4, rho_CO, rho_CO2)
        pint_H, pint_C, pint_O, pint_tot = cv79.getpint(rho_H, rho_C, rho_O)

        pint_incoming, pint_tot_incomingbeam = [],[]
        if lText.count("B2"):
            pint_tot_incomingbeam = pint_tot[len(s_positiveb2):]
            s_incoming = s_positiveb2[:len(s_positiveb2)-1]
        else:
            pint_tot_incomingbeam = [p for p in pint_tot[:len(s_positiveb1)+1]]
            s_incoming = s_positiveb1

        print "len(pint_tot_incomingbeam)", len(pint_tot_incomingbeam)
        print "len(s_incoming)", len(s_incoming)
        xlist, ylist, col, mstyle, lg = s_incoming,pint_tot_incomingbeam , kBlack+i,20+i, lText
        grs += [ makeTGraph(xlist, ylist, col, mstyle)]
        mlegend.AddEntry(grs[-1], lg, lm)    
        mg.Add(grs[-1])

    mg.Draw("al")

    mg.SetTitle("pressure profiles")
    mg.GetXaxis().SetTitle(xTitle)
    mg.GetYaxis().SetTitle("total interaction probability")
    mg.GetYaxis().SetRangeUser(5e-18,4e-10)
    mlegend.Draw()
    lab = mylabel(42)
    lab.DrawLatex(0.42, 0.82, 'incoming beams 6.5 TeV') 

    pname = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/6500GeV'
    pname = "pint_"+rel+".pdf"
    print('Saving file as ' + pname )
    cv.Print(pname)

        
