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
import cv79, cv32, cv65, cv95

## -------------------------------------------------------------------------------
pData = [
    ("/Users/rkwee/Documents/RHUL/work/HL-LHC/runs/TCT/Density_Fill4536_2041b_26158.8832-500_B1_withECLOUD.txt", "distance from IP1 [m]", "Fill 4536"),
   # ("/Users/rkwee/Documents/RHUL/work/HL-LHC/runs/TCT/Density_Fill4536_2041b_26158.8832-500_B2_withECLOUD.txt", "distance from IP1 [m]",  "Fill 4536 B2"),
   # ("/Users/rkwee/Documents/RHUL/work/HL-LHC/runs/TCT/Density_Fill4532_1824b_26158.8832-500_B1_withECLOUD.txt", "distance from IP1 [m]",  "Fill 4532 B1"),
   # ("/Users/rkwee/Documents/RHUL/work/HL-LHC/runs/TCT/Density_Fill4532_1824b_26158.8832-500_B2_withECLOUD.txt", "distance from IP1 [m]",  "Fill 4532 B2"),
    ("/Users/rkwee/Documents/RHUL/work/data/4TeV/LSS1_B1_Fill2736_Final.csv", "distance from IP1 [m]",  "Fill 2736"),
    ( "/Users/rkwee/Documents/RHUL/work/HL-LHC/HL_LHC_D2_IP_LSS1_After_Conditioning_Anton_onlydata.csv", "distance from IP1 [m]","HL-LHC a.c. high"),
    ( "/Users/rkwee/Documents/RHUL/work/HL-LHC/HL_LHC_D2_IP_LSS1_After_ConditioningLowLevel_Anton_onlydata.csv", "distance from IP1 [m]","HL-LHC a.c. low"),
]
# # -----------------------------------------------------------------------
cols = [kBlue-2, kOrange+2, kRed-1, kAzure+1, kMagenta-5]
cols = [kGreen-8, kAzure+2, kRed-4, kMagenta]
def cv83():
    # ---------------------------------------------------
    rel = 'compallpint'
    #rel = 'compallpress'
    cv = TCanvas( 'cv'+ rel , 'cv'+rel , 1500, 900)
    cv.SetLogy(1)
    cv.SetGridy(0)
    x1, y1, x2, y2 = 0.67, 0.72, 0.88, 0.92
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

        print  "."*33
        print "Getting data from file", pFile
        
        data = {}        
        if pFile.count("2736"):
            data = cv32.getdata14c(pFile)
            stmp, rho_C, rho_H, rho_O = cv65.getAtomicRho(data)
            stmp2 = stmp[1:]
            s_full = stmp2[::-1]
            pint_C, pint_H, pint_O, pint_tot = cv65.calc_pint_tot(rho_C, rho_H, rho_O)
            totalPress = [ data['H2_N2Eq'][j] +  data['CH4_N2Eq'][j] + data['CO_N2Eq'][j] + data['CO2_N2Eq'][j] for j in range(len(data['H2_N2Eq'])) ]
        elif pFile.count("Density_Fill4"):
            data = cv79.getdata5c(pFile)
            totalPress =  cv79.getTotalPressure(data)
            rho_H2, rho_CH4, rho_CO, rho_CO2 = cv79.getrho(data['H2_Eq']),cv79.getrho(data['CH4_Eq']),cv79.getrho(data['CO_Eq']),cv79.getrho(data['CO2_Eq'])
            rho_H, rho_C, rho_O = cv79.getAtomicRho(rho_H2, rho_CH4, rho_CO, rho_CO2)
            pint_H, pint_C, pint_O, pint_tot = cv79.getpint(rho_H, rho_C, rho_O)
            s_full = data['s']
        elif pFile.count("HL_LHC"):
            # will only work for pint
            data = cv95.getdata14cHL(pFile)

            rho_H2 = cv79.getrho(data['H2_N2Eq'])
            rho_CH4 = cv79.getrho(data['CH4_N2Eq'])
            rho_CO2 =cv79.getrho(data['CO2_N2Eq'])
            rho_CO = cv79.getrho(data['CO_N2Eq'])

            rho_H, rho_C, rho_O = cv79.getAtomicRho(rho_H2, rho_CH4, rho_CO, rho_CO2)
            pint_H, pint_C, pint_O, pint_tot = cv79.getpint(rho_H, rho_C, rho_O)
            stmp =data["s"]
            s_full=stmp[::-1] # invert order ?
            
        s_incoming = []
        
        pint_incoming, pint_tot_incomingbeam = [],[]
        
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
            pint_tot_incomingbeam = pint_tot[len(s_positiveb2):]
            press_tot_incomingbeam = totalPress[len(s_positiveb2):]
            s_incoming = s_positiveb2[:len(s_positiveb2)-1]
        else:
            pint_tot_incomingbeam = [p for p in pint_tot[:len(s_positiveb1)+1]]
            if not pFile.count("HL_LHC"): press_tot_incomingbeam = [p for p in totalPress[:len(s_positiveb1)+1]]
            s_incoming = s_positiveb1
            if pFile.count("2736"):
                pint_tot_incomingbeam = pint_tot_incomingbeam[::-1]
                press_tot_incomingbeam = totalPress[::-1]
            
        print "len(pint_tot_incomingbeam)", len(pint_tot_incomingbeam)
        print "len(s_incoming)", len(s_incoming)

        print i, cols
        #        print s_incoming[:100],press_tot_incomingbeam[:100]
        xlist, ylist, col, mstyle, lg = s_incoming,pint_tot_incomingbeam , cols[i],20+i, lText
        #xlist, ylist, col, mstyle, lg = s_incoming,press_tot_incomingbeam , cols[i],20+i, lText
        grs += [ makeTGraph(xlist, ylist, col, mstyle)]
        mlegend.AddEntry(grs[-1], lg, lm)    
        mg.Add(grs[-1])

    mg.Draw("al")
    Tt = TLatex()
    Tt = "#splitline{interaction probability density}{[1/proton/m/s]}"
    #mg.SetTitle("pressure profiles")
    mg.GetXaxis().SetTitle(xTitle)
    mg.GetYaxis().SetTitle(Tt)
    #mg.GetYaxis().SetTitle("total pressure [mbar]")
    mg.GetYaxis().SetRangeUser(5e-18,4e-10)
    #mg.GetYaxis().SetRangeUser(5e-13,4e-6)
    mg.GetXaxis().SetRangeUser(0,260)
    mlegend.Draw()
    lab = mylabel(42)
    lab.DrawLatex(0.42, 0.82, 'incoming beams') 

    s = 22.6
    lInterface = TLine()
    lInterface.SetLineStyle(2)
    lInterface.SetLineColor(kGray+3)
    YurMin, YurMax = 5e-18,4e-10
    lInterface.DrawLine(s,YurMin,s,YurMax)
    pname = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/6500GeV/reweighted/'
    pname = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/HLRunII/'

    pname = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLLHCBackgroundPaper/figures/'
    pname += rel+".pdf"
    print('Saving file as ' + pname )
    cv.Print(pname)

        
