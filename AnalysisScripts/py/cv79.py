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
         # ("/Users/rkwee/Downloads/Density_Fill4536_2041b_26158.8832-500_B2_withECLOUD.txt", "distance from IP1 [m]",  "Fill 4536 B2"),
         # ("/Users/rkwee/Downloads/Density_Fill4532_1824b_26158.8832-500_B1_withECLOUD.txt", "distance from IP1 [m]",  "Fill 4532 B1"),
         # ("/Users/rkwee/Downloads/Density_Fill4532_1824b_26158.8832-500_B2_withECLOUD.txt", "distance from IP1 [m]",  "Fill 4532 B2"),
]
# -----------------------------------------------------------------------
def getpint(rho_H,rho_C,rho_O):

    # 6.5 TeV inel cross-sections scaled from paper
    sigma_O = 329.e-31
    sigma_C = 269.e-31
    sigma_H = 38.4e-31
    Trev = 1./11245

    pint_C = [sigma_C*j/Trev for j in rho_C]
    pint_H = [sigma_H*j/Trev for j in rho_H]
    pint_O = [sigma_O*j/Trev for j in rho_O]

    pint_tot = [pint_H[i] + pint_O[i] + pint_C[i] for i in range(len(pint_O))]
    return pint_H, pint_C,pint_O,  pint_tot


# -----------------------------------------------------------------------
def getAtomicRho(rho_H2, rho_CH4, rho_CO, rho_CO2):

    nb_s = len(rho_H2)
    rho_C, rho_H, rho_O = [0 for i in range(nb_s)],[0 for i in range(nb_s)],[0 for i in range(nb_s)]

    for i in range(nb_s):

        try:
            # compute atomic rhos
            rho_H[i]  = 2.0*rho_H2[i]
            rho_H[i] += 4.0*rho_CH4[i]

            rho_C[i]  = 1.0*rho_CH4[i]
            rho_C[i] += 1.0*rho_CO[i]
            rho_C[i] += 1.0*rho_CO2[i]

            rho_O[i]  = 1.0*rho_CO[i]
            rho_O[i] += 2.0*rho_CO2[i]

        except ValueError:
            continue
    return rho_H, rho_C, rho_O
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
        #cv.SetGridy(1)
        x1, y1, x2, y2 = 0.8, 0.65, 0.9, 0.9
        mlegend = TLegend( x1, y1, x2, y2)
        mlegend.SetFillColor(0)
        mlegend.SetFillStyle(0)
        mlegend.SetLineColor(0)
        mlegend.SetTextSize(0.035)
        mlegend.SetShadowColor(0)
        mlegend.SetBorderSize(0)

        mg = TMultiGraph(rel,rel)
        lm = 'l'

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
        mg.GetYaxis().SetTitle("pressure equivalent [mbar]")
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
        #cv.SetGridy(1)
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
        mg.GetYaxis().SetTitle("density [molecules/m^{3}]")
        mg.GetYaxis().SetRangeUser(5e5,1e16)
        mlegend.Draw()
        lab = mylabel(42)
        lab.DrawLatex(0.45, 0.88, lText)
        
        
        pname = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/6500GeV'
        pname = pFile.split('.txt')[0] + "_"+rel+".pdf"
        print('Saving file as ' + pname )
        cv.Print(pname)

        # ---------------------------------------------------
        # plot data as rho
        rel = 'rho'
        cv = TCanvas( 'cvrho'+ lText , 'cvrho'+ lText , 2100, 900)
        cv.SetLogy(1)
        #cv.SetGridy(1)
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

        rho_H2 = getrho(data['H2_Eq'])
        xlist, ylist, col, mstyle, lg = data['s'], rho_H2, kTeal-3, 22, 'H_{2}'
        g0 = makeTGraph(xlist, ylist, col, mstyle)
        mlegend.AddEntry(g0, lg, lm)    
        mg.Add(g0)

        rho_CH4 = getrho(data['CH4_Eq'])
        xlist, ylist, col, mstyle, lg = data['s'], rho_CH4, kMagenta+1, 24, 'CH_{4}'
        g1 = makeTGraph(xlist, ylist, col, mstyle)
        mlegend.AddEntry(g1, lg, lm)    
        mg.Add(g1)

        rho_CO2 =getrho(data['CO2_Eq'])
        xlist, ylist, col, mstyle, lg = data['s'], rho_CO2, kAzure+4, 33, 'CO_{2}'
        g2 = makeTGraph(xlist, ylist, col, mstyle)
        mlegend.AddEntry(g2, lg, lm)    
        mg.Add(g2)

        rho_CO = getrho( data['CO_Eq'] )
        xlist, ylist, col, mstyle, lg = data['s'],rho_CO, kRed-2, 21, 'CO'
        g3 = makeTGraph(xlist, ylist, col, mstyle)
        mlegend.AddEntry(g3, lg, lm)    
        mg.Add(g3)

        mg.Draw("al")

        mg.SetTitle("pressure profiles")
        mg.GetXaxis().SetTitle(xTitle)
        mg.GetYaxis().SetTitle("density [molecules/m^{3}]")
        mg.GetYaxis().SetRangeUser(5e5,1e16)
        mlegend.Draw()
        lab = mylabel(42)
        lab.DrawLatex(0.45, 0.88, lText)
        
        
        pname = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/6500GeV'
        pname = pFile.split('.txt')[0] + "_"+rel+".pdf"
        print('Saving file as ' + pname )
        cv.Print(pname)

        # ---------------------------------------------------
        # plot atomic rho
        rel = 'atomicrho'
        cv = TCanvas( 'cv'+ rel+lText , 'cv'+rel+ lText , 2100, 900)
        cv.SetLogy(1)
        #cv.SetGridy(1)
        x1, y1, x2, y2 = 0.8, 0.7, 0.9, 0.9
        mlegend = TLegend( x1, y1, x2, y2)
        mlegend.SetFillColor(0)
        mlegend.SetFillStyle(0)
        mlegend.SetLineColor(0)
        mlegend.SetTextSize(0.035)
        mlegend.SetShadowColor(0)
        mlegend.SetBorderSize(0)

        mg = TMultiGraph(rel,rel)
        lm = 'pl'

        rho_H, rho_C, rho_O = getAtomicRho(rho_H2, rho_CH4, rho_CO, rho_CO2)

        rho_total_atomic = [ rho_H[i] + rho_C[i] + rho_O[i] for i in range(len(rho_O)) ]
        xlist, ylist, col, mstyle, lg = data['s'],rho_total_atomic , kBlack, 20, 'total'
        g3 = makeTGraph(xlist, ylist, col, mstyle)
        mlegend.AddEntry(g3, lg, lm)    
        mg.Add(g3)

        xlist, ylist, col, mstyle, lg = data['s'],rho_H , kTeal+3, 22, 'H'
        g0 = makeTGraph(xlist, ylist, col, mstyle)
        mlegend.AddEntry(g0, lg, lm)    
        mg.Add(g0)

        xlist, ylist, col, mstyle, lg = data['s'], rho_O, kAzure-4, 33, 'O'
        g2 = makeTGraph(xlist, ylist, col, mstyle)
        mlegend.AddEntry(g2, lg, lm)    
        mg.Add(g2)

        xlist, ylist, col, mstyle, lg = data['s'], rho_C, kMagenta-1, 24, 'C'
        g1 = makeTGraph(xlist, ylist, col, mstyle)
        mlegend.AddEntry(g1, lg, lm)    
        mg.Add(g1)

        mg.Draw("al")

        mg.SetTitle("pressure profiles")
        mg.GetXaxis().SetTitle(xTitle)
        mg.GetYaxis().SetTitle("density [atoms/m^{3}]")
        mg.GetYaxis().SetRangeUser(5e5,1e16)
        mlegend.Draw()
        lab = mylabel(42)
        lab.DrawLatex(0.45, 0.88, lText)
        
        
        pname = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/6500GeV'
        pname = pFile.split('.txt')[0] + "_"+rel+".pdf"
        print('Saving file as ' + pname )
        cv.Print(pname)
        
        # ---------------------------------------------------
        # plot pint
        rel = 'pint'
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
        pint_H, pint_C,pint_O, pint_tot = getpint(rho_H,rho_C,rho_O)

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
        mg.GetYaxis().SetTitle("interaction probability")
        mg.GetYaxis().SetRangeUser(5e-19,1e-10)
        mlegend.Draw()
        lab = mylabel(42)
        lab.DrawLatex(0.45, 0.88, lText)        
        
        pname = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/6500GeV/'
        pname = pFile.split('.txt')[0].split("/")[-1] + "_"+rel+".pdf"
        print('Saving file as ' + pname )
        cv.Print(pname)

        
