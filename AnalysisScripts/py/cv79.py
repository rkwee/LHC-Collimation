#!/usr/bin/python
#
# plot pressure profiles 6.5 TeV 2015
#
# Oct 2016, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, os, time, math
from ROOT import *
import helpers, array
from helpers import wwwpath, length_LHC, mylabel, gitpath, workpath, makeTGraph
from array import array
## -------------------------------------------------------------------------------
pData = [("/Users/rkwee/Downloads/Density_Fill4536_2041b_26158.8832-500_B1_withECLOUD.txt", "distance from IP1 [m]", "Fill 4536 B1"),
         ("/Users/rkwee/Downloads/Density_Fill4536_2041b_26158.8832-500_B2_withECLOUD.txt", "distance from IP1 [m]",  "Fill 4536 B2"),
         ("/Users/rkwee/Downloads/Density_Fill4532_1824b_26158.8832-500_B1_withECLOUD.txt", "distance from IP1 [m]",  "Fill 4532 B1"),
         ("/Users/rkwee/Downloads/Density_Fill4532_1824b_26158.8832-500_B2_withECLOUD.txt", "distance from IP1 [m]",  "Fill 4532 B2"),
]
# -----------------------------------------------------------------------
def getrho(pressEq):

    kBT = 1.38e-23*300
    rho = [float(p)/kBT for p in pressEq]
    return rho
# -----------------------------------------------------------------------
def getTotalPressure(data):

    dkeys = ['H2_Eq','CH4_Eq', 'CO_Eq', 'CO2_Eq']
    totalPress = []

    for i in range(len(data['s'])):    
        totalpressure = 0.        
        for dk in dkeys:
            
            totalpressure += float(data[dk][i])
        totalPress += [totalpressure]

    return totalPress
    
# -----------------------------------------------------------------------
def getdata5c(pFile):
    # fixed to 5 data columns
    # each column in a dict

    
    c = [ [] for i in range(5)]
    with open(pFile) as mf:
        for line in mf:
            
            #print line.split()
            
            for j in range(5):
                # first line
                if len(line.split()) != 5:
                    continue
                else:

                    c[j] += [ line.split()[j] ] 

    # creates automatic keynames
    data = dict(s=c[0], H2_Eq=c[1], CH4_Eq=c[2], CO_Eq=c[3], CO2_Eq=c[4])

    return data
# -----------------------------------------------------------------------
def cv79():

    for pFile, xTitle, lText in pData:
        # get data
        data = getdata5c(pFile)

        
        # plot data as is
        rel = 'pressureEq'
        
        cv = TCanvas( 'cv' +rel+ lText, 'cv'+rel + lText, 2100, 900)
        cv.SetLogy(1)
        x1, y1, x2, y2 = 0.8, 0.65, 0.9, 0.9
        mlegend = TLegend( x1, y1, x2, y2)
        mlegend.SetFillColor(0)
        mlegend.SetFillStyle(0)
        mlegend.SetLineColor(0)
        mlegend.SetTextSize(0.035)
        mlegend.SetShadowColor(0)
        mlegend.SetBorderSize(0)

        mg = TMultiGraph(rel,rel)
        lm = 'pl'

        totalPress =  getTotalPressure(data)
        
        xlist, ylist, col, mstyle, lg = data['s'], totalPress, kBlack, 21, 'total'
        g4 = makeTGraph(xlist, ylist, col, mstyle)
        mlegend.AddEntry(g4, lg, lm)    
        mg.Add(g4)

        xlist, ylist, col, mstyle, lg = data['s'], data['H2_Eq'], kTeal-3, 22, 'H_{2}'
        g0 = makeTGraph(xlist, ylist, col, mstyle)
        mlegend.AddEntry(g0, lg, lm)    
        mg.Add(g0)

        xlist, ylist, col, mstyle, lg = data['s'], data['CH4_Eq'], kMagenta+1, 24, 'CH_{4}'
        g1 = makeTGraph(xlist, ylist, col, mstyle)
        mlegend.AddEntry(g1, lg, lm)    
        mg.Add(g1)

        xlist, ylist, col, mstyle, lg = data['s'], data['CO2_Eq'], kAzure+4, 33, 'CO_{2}'
        g2 = makeTGraph(xlist, ylist, col, mstyle)
        mlegend.AddEntry(g2, lg, lm)    
        mg.Add(g2)

        xlist, ylist, col, mstyle, lg = data['s'], data['CO_Eq'], kRed-2, 21, 'CO'
        g3 = makeTGraph(xlist, ylist, col, mstyle)
        mlegend.AddEntry(g3, lg, lm)    
        mg.Add(g3)
     

        mg.Draw("al")

        mg.SetTitle("pressure profiles")
        mg.GetXaxis().SetTitle(xTitle)
        mg.GetYaxis().SetTitle("pressure equivalent")
        mg.GetYaxis().SetRangeUser(5e-15,1e-5)
        mlegend.Draw()
        lab = mylabel(42)
        lab.DrawLatex(0.45, 0.88, lText)

        pname = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/6500GeV'
        pname = pFile.split('.txt')[0] + "_pressureEq.pdf"
        print('Saving file as ' + pname )
        cv.Print(pname)

        # ---------------------------------------------------
        # plot data as rho
        rel = 'rho'
        cv = TCanvas( 'cvrho'+ lText , 'cvrho'+ lText , 2100, 900)
        cv.SetLogy(1)
        x1, y1, x2, y2 = 0.8, 0.65, 0.9, 0.9
        mlegend = TLegend( x1, y1, x2, y2)
        mlegend.SetFillColor(0)
        mlegend.SetFillStyle(0)
        mlegend.SetLineColor(0)
        mlegend.SetTextSize(0.035)
        mlegend.SetShadowColor(0)
        mlegend.SetBorderSize(0)

        mg = TMultiGraph(rel,rel)
        lm = 'pl'

        
        xlist, ylist, col, mstyle, lg = data['s'], getrho(totalPress), kBlack, 21, 'total'
        g4 = makeTGraph(xlist, ylist, col, mstyle)
        mlegend.AddEntry(g4, lg, lm)    
        mg.Add(g4)

        xlist, ylist, col, mstyle, lg = data['s'], getrho(data['H2_Eq']), kTeal-3, 22, 'H_{2}'
        g0 = makeTGraph(xlist, ylist, col, mstyle)
        mlegend.AddEntry(g0, lg, lm)    
        mg.Add(g0)

        xlist, ylist, col, mstyle, lg = data['s'], getrho(data['CH4_Eq']), kMagenta+1, 24, 'CH_{4}'
        g1 = makeTGraph(xlist, ylist, col, mstyle)
        mlegend.AddEntry(g1, lg, lm)    
        mg.Add(g1)

        xlist, ylist, col, mstyle, lg = data['s'], getrho(data['CO2_Eq']), kAzure+4, 33, 'CO_{2}'
        g2 = makeTGraph(xlist, ylist, col, mstyle)
        mlegend.AddEntry(g2, lg, lm)    
        mg.Add(g2)

        xlist, ylist, col, mstyle, lg = data['s'],getrho( data['CO_Eq'] ), kRed-2, 21, 'CO'
        g3 = makeTGraph(xlist, ylist, col, mstyle)
        mlegend.AddEntry(g3, lg, lm)    
        mg.Add(g3)

        mg.Draw("al")

        mg.SetTitle("pressure profiles")
        mg.GetXaxis().SetTitle(xTitle)
        mg.GetYaxis().SetTitle("density [molecules/m^3]")
        mg.GetYaxis().SetRangeUser(5e5,1e16)
        mlegend.Draw()
        lab = mylabel(42)
        lab.DrawLatex(0.45, 0.88, lText)
        
        
        pname = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/6500GeV'
        pname = pFile.split('.txt')[0] + "_"+rel+".pdf"
        print('Saving file as ' + pname )
        cv.Print(pname)

                                                    
