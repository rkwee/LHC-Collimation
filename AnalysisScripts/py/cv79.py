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
#         ("/Users/rkwee/Downloads/Density_Fill4536_2041b_26158.8832-500_B2_withECLOUD.txt", "distance from IP1 [m]",  "Fill 4536 B2"),
]


def getdata5c(pFile):
    # fixed to 5 data columns
    # each column in a dict

    
    c = [ [] for i in range(5)]
    with open(pFile) as mf:
        for line in mf:
            #
            print line.split()
            

            for j in range(5):
                # first line
                if len(line.split()) != 5:
                    continue
                else:

                    c[j] += [ line.split()[j] ] 

    # creates automatic keynames
    data = dict(s=c[0], H2_Eq=c[1], CH4_Eq=c[2], CO_Eq=c[3], CO2_Eq=c[4])

    return data
def cv79():

    for pFile, xTitle, lText in pData:
        # get data
        data = getdata5c(pFile)
        print data.keys()

        # plot data
        cv = TCanvas( 'cv', 'cv', 2100, 900)
        cv.SetLogy(1)
        x1, y1, x2, y2 = 0.8, 0.65, 0.9, 0.9
        mlegend = TLegend( x1, y1, x2, y2)
        mlegend.SetFillColor(0)
        mlegend.SetFillStyle(0)
        mlegend.SetLineColor(0)
        mlegend.SetTextSize(0.035)
        mlegend.SetShadowColor(0)
        mlegend.SetBorderSize(0)

        mg = TMultiGraph()
        lm = 'pl'

        xlist, ylist, col, mstyle, lg = data['s'][1:], data['H2_Eq'][1:], kTeal-3, 22, 'H_{2}'
        g0 = makeTGraph(xlist, ylist, col, mstyle)
        mlegend.AddEntry(g0, lg, lm)    
        mg.Add(g0)

        xlist, ylist, col, mstyle, lg = data['s'][1:], data['CH4_Eq'][1:], kMagenta+1, 24, 'CH_{4}'
        g1 = makeTGraph(xlist, ylist, col, mstyle)
        mlegend.AddEntry(g1, lg, lm)    
        mg.Add(g1)

        xlist, ylist, col, mstyle, lg = data['s'][1:], data['CO2_Eq'][1:], kBlue+4, 33, 'CO_{2}'
        g2 = makeTGraph(xlist, ylist, col, mstyle)
        mlegend.AddEntry(g2, lg, lm)    
        mg.Add(g2)

        xlist, ylist, col, mstyle, lg = data['s'][1:], data['CO_Eq'][1:], kRed-2, 21, 'CO'
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
        pname = pFile.split('.txt')[0] + "_pressure.pdf"
        print('Saving file as ' + pname )
        cv.Print(pname)

                                                    
