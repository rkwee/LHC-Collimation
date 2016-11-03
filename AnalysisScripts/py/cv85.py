#!/usr/bin/python
#
# compare pressure profiles 6.5 TeV 2015
# compare incoming side only
# adding 4 TeV pressure
#
# Oct 2016, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, os, time, math
from ROOT import *
import helpers, array
from helpers import wwwpath, length_LHC, mylabel, gitpath, workpath, makeTGraph
from array import array
import cv79, cv32, cv65

## -------------------------------------------------------------------------------
pData = [
    ("/Users/rkwee/Downloads/Density_Fill4536_2041b_26158.8832-500_B1_withECLOUD.txt", "distance from IP1 [m]", "Fill 4536 B1"),
    ("/Users/rkwee/Downloads/Density_Fill4536_2041b_26158.8832-500_B2_withECLOUD.txt", "distance from IP1 [m]",  "Fill 4536 B2"),
    #("/Users/rkwee/Downloads/Density_Fill4532_1824b_26158.8832-500_B1_withECLOUD.txt", "distance from IP1 [m]",  "Fill 4532 B1"),
    #("/Users/rkwee/Downloads/Density_Fill4532_1824b_26158.8832-500_B2_withECLOUD.txt", "distance from IP1 [m]",  "Fill 4532 B2"),
#    ("/Users/rkwee/Documents/RHUL/work/data/4TeV/LSS1_B1_Fill2736_Final.csv", "distance from IP1 [m]",  "Fill 2736 B1"),
]
# # -----------------------------------------------------------------------
cols = [kBlue-2, kYellow+9, kAzure-1, kRed+1, kMagenta-5, kYellow-2]
def cv85():
    # ---------------------------------------------------
    rel = 'compallpint'
    # rel = 'compallpress'
    a,b = 1,1
    cv = TCanvas( 'cv'+ rel , 'cv'+rel , a*2100, b*900)
    cv.Divide(a,b)
    cv.SetLogy(0)
    cv.SetGridy(0)
    x1, y1, x2, y2 = 0.75, 0.6, 0.88, 0.94
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

        print  "."*33
        data = {}        
        if pFile.count("LSS1"):
            data = cv32.getdata14c(pFile)
            stmp, rho_C, rho_H, rho_O = cv65.getAtomicRho(data)
            stmp2 = stmp[1:]
            s_full = stmp2[::-1]
            totalPress = [ data['H2_N2Eq'][i] +  data['CH4_N2Eq'][i] + data['CO_N2Eq'][i] + data['CO2_N2Eq'][i] for i in range(len(data['H2_N2Eq'])) ]
        else:
            data = cv79.getdata5c(pFile)
            totalPress =  cv79.getTotalPressure(data)
            pressCO = data['CO_Eq']
            pressCO2 = data['CO2_Eq']
            pressCH4 = data['CH4_Eq']
            pressH2 = data['H2_Eq']

            s_full = data['s']
            
        s_incoming = []
        
        
        # only one side, chose positive s
        s_positiveb1, s_positiveb2 = [],[]

        #print s_full
        for cs in s_full:
            s = float(cs)
            if s<0.:
                s_positiveb1 += [-s]
            else:
                s_positiveb2 += [s]
                
        print "len(s_positiveb1)",len(s_positiveb1)
        print "len(s_positiveb2)",len(s_positiveb2)

        if lText.count("B2"):
            lenposb2 = len(s_positiveb2)
            press_tot_incomingbeam = totalPress[lenposb2:]
            pressH2_incoming = pressH2[lenposb2:]
            pressCO_incoming = pressCO[lenposb2:]
            pressCH4_incoming = pressCH4[lenposb2:]
            pressCO2_incoming = pressCO2[lenposb2:]
                        
            s_incoming = s_positiveb2[:len(s_positiveb2)-1]
        else:
            press_tot_incomingbeam = [p for p in totalPress[:len(s_positiveb1)+1]]
            pressH2_incoming = pressH2[:len(s_positiveb1)+1]
            pressCO_incoming = pressCO[:len(s_positiveb1)+1]
            pressCH4_incoming = pressCH4[:len(s_positiveb1)+1]
            pressCO2_incoming = pressCO2[:len(s_positiveb1)+1]
                        
            s_incoming = s_positiveb1
            if pFile.count("LSS"):
                press_tot_incomingbeam = totalPress[::-1]
            

        #        print s_incoming[:100],press_tot_incomingbeam[:100]

        xlist, ylist, col, mstyle, lg = s_incoming,press_tot_incomingbeam , cols[i],20+i, lText + 'total'
        grs += [ makeTGraph(xlist, ylist, col, mstyle)]
        mlegend.AddEntry(grs[-1], lg, lm)    
        mg.Add(grs[-1])

        # xlist, ylist, col, mstyle, lg = s_incoming,pressH2_incoming , cols[i]+1, 20,lText + 'H2'
        # grs += [ makeTGraph(xlist, ylist, col, mstyle)]
        # mlegend.AddEntry(grs[-1], lg, lm)    
        # mg.Add(grs[-1])

        # xlist, ylist, col, mstyle, lg = s_incoming,pressCH4_incoming , cols[i]+2, 20,lText + 'CH4'
        # grs += [ makeTGraph(xlist, ylist, col, mstyle)]
        # mlegend.AddEntry(grs[-1], lg, lm)    
        # mg.Add(grs[-1])

        # xlist, ylist, col, mstyle, lg = s_incoming,pressCO2_incoming , cols[i]+2, 20,lText + 'CO2'
        # grs += [ makeTGraph(xlist, ylist, col, mstyle)]
        # mlegend.AddEntry(grs[-1], lg, lm)    
        # mg.Add(grs[-1])

        xlist, ylist, col, mstyle, lg = s_incoming,pressCO_incoming , cols[i]+2, 20,lText + 'CO'
        grs += [ makeTGraph(xlist, ylist, col, mstyle)]
        mlegend.AddEntry(grs[-1], lg, lm)    
        mg.Add(grs[-1])

    mg.Draw("al")

    mg.SetTitle("pressure profiles")
    mg.GetXaxis().SetTitle(xTitle)
    #mg.GetYaxis().SetTitle("total interaction probability")
    mg.GetYaxis().SetTitle("total pressure [mbar]")
    #mg.GetYaxis().SetRangeUser(5e-18,4e-10)
    mg.GetYaxis().SetRangeUser(5e-15,4e-3)
    mlegend.Draw()
    lab = mylabel(42)
    lab.DrawLatex(0.42, 0.82, 'incoming beams') 

    pname = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/6500GeV'
    pname = rel+".pdf"
    print('Saving file as ' + pname )
    cv.Print(pname)

        
