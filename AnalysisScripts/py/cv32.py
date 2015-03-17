#!/usr/bin/python
#
# Mar 2015, rkwee
## -------------------------------------------------------------------------------
## -------------------------------------------------------------------------------
import ROOT, sys, os, time, math
from ROOT import *
import lossmap, helpers, array
from helpers import wwwpath, length_LHC, mylabel, gitpath, workpath
from array import array
## -------------------------------------------------------------------------------
pressureData = 'beam-gas-sixtrack/pressure_profiles_2012/LSS4_IP4_2012_Roderik.csv'
#pressureData = 'beam-gas-sixtrack/pressure_profiles_2012/test.csv'
# -----------------------------------------------------------------------------------
def getdata():

    c = [ [] for i in range(14) ]
    with open(pressureData) as mf:
        for l,line in enumerate(mf):

            for i in range(14):
                
                if i != 13:
                    c[i] += [ line.split(',')[i] ]
                else:
                    c[i] += [ line.split(',')[i].rstrip('\r\n') ]

    data = dict(s=c[0], l_total=c[1], rho_H2=c[2], rho_CH4=c[3], rho_CO=c[4], rho_CO2=c[5], \
                H2_N2Eq=c[6], CH4_N2Eq=c[7], CO_N2Eq=c[8], CO2_N2Eq=c[9], avPress=c[10], avPressCorr=c[11], H2Eq=c[12], H2EqCorr=c[13])

    return data
# ----------------------------------------------------------------------------
def makeGraph(data, xKey, yKey, color, mStyle):

    """ returns TGraph of x, y """

    xarrayV = data[xKey]
    yarrayV = data[yKey]
    gr = TGraph()
    np = len(data[xKey]) - 1  # remove title element
    gr.Set(np)

    gr.SetMarkerStyle(mStyle)
    gr.SetLineWidth(1)
    gr.SetLineColor(color)
    gr.SetMarkerColor(color)

    for i in range(1,len(xarrayV)-1):
        x=float(xarrayV[i+1])
        y=float(yarrayV[i+1])
        gr.SetPoint(i+1, x, y)

    return gr
# ----------------------------------------------------------------------------
def cv32a():

    data = getdata()

    cv = TCanvas( 'cv', 'cv', 2100, 900)

    x1, y1, x2, y2 = 0.8, 0.65, 0.9, 0.9
    mlegend = TLegend( x1, y1, x2, y2)
    mlegend.SetFillColor(0)
    mlegend.SetFillStyle(0)
    mlegend.SetLineColor(0)
    mlegend.SetTextSize(0.035)
    mlegend.SetShadowColor(0)
    mlegend.SetBorderSize(0)

    mg = TMultiGraph()

    xKey, yKey, color, mStyle, lg = 's','rho_H2', kGreen, 22, '#rho_{H_2}'
    g0 = makeGraph(data, xKey, yKey, color, mStyle)
    mlegend.AddEntry(g0, lg, "p")    
    mg.Add(g0)

    xKey, yKey, color, mStyle, lg = 's','rho_CH4', kBlue, 23, '#rho_{CH_{4}}'
    g1 = makeGraph(data, xKey, yKey, color, mStyle)
    mlegend.AddEntry(g1, lg, "p") 
    mg.Add(g1)

    xKey, yKey, color, mStyle, lg = 's','rho_CO', kRed, 20, '#rho_{CO}'
    g2 = makeGraph(data, xKey, yKey, color, mStyle)
    mlegend.AddEntry(g2, lg, "p") 
    mg.Add(g2)

    xKey, yKey, color, mStyle, lg = 's','rho_CO2', kMagenta, 21, '#rho_{CO_2}'
    g3 = makeGraph(data, xKey, yKey, color, mStyle)
    mlegend.AddEntry(g3, lg, "p") 
    mg.Add(g3)

    mg.Draw("ap")

    gPad.SetLogy(1)
    gPad.RedrawAxis()

    mg.SetTitle("2012 pressure profiles")
    mg.GetXaxis().SetTitle("s ")
    mg.GetYaxis().SetTitle("density #rho [molecules/m^{3}]")

    mlegend.Draw()

    # pname  = wwwpath
    # subfolder = 'TCT/HL/relaxedColl/newScatt/'
    # pname += subfolder + hname + '_' + doZoom + '.png'

    pname = pressureData.split('.csv')[0] + "a_pressure_2012.png"    
    print('Saving file as ' + pname ) 
    cv.Print(pname)

# ----------------------------------------------------------------------------
def cv32b():

    data = getdata()

    cv = TCanvas( 'cv', 'cv', 2100, 900)

    x1, y1, x2, y2 = 0.8, 0.65, 0.9, 0.9
    mlegend = TLegend( x1, y1, x2, y2)
    mlegend.SetFillColor(0)
    mlegend.SetFillStyle(0)
    mlegend.SetLineColor(0)
    mlegend.SetTextSize(0.035)
    mlegend.SetShadowColor(0)
    mlegend.SetBorderSize(0)

    mg = TMultiGraph()

    xKey, yKey, color, mStyle, lg = 's','H2_N2Eq', kGreen, 22, 'H_{2} N_{2} Eq'
    g0 = makeGraph(data, xKey, yKey, color, mStyle)
    mlegend.AddEntry(g0, lg, "p")    
    mg.Add(g0)

    xKey, yKey, color, mStyle, lg = 's','CH4_N2Eq', kBlue, 23, 'CH_{4} N_{2} Eq'
    g1 = makeGraph(data, xKey, yKey, color, mStyle)
    mlegend.AddEntry(g1, lg, "p") 
    mg.Add(g1)

    xKey, yKey, color, mStyle, lg = 's','CO_N2Eq', kRed, 20, 'CO N_{2} Eq'
    g2 = makeGraph(data, xKey, yKey, color, mStyle)
    mlegend.AddEntry(g2, lg, "p") 
    mg.Add(g2)

    xKey, yKey, color, mStyle, lg = 's','CO2_N2Eq', kMagenta, 21, 'CO_{2} N_{2} Eq'
    g3 = makeGraph(data, xKey, yKey, color, mStyle)
    mlegend.AddEntry(g3, lg, "p") 
    mg.Add(g3)

    mg.Draw("ap")

    gPad.SetLogy(1)
    gPad.RedrawAxis()

    mg.SetTitle("2012 pressure profiles")
    mg.GetXaxis().SetTitle("s ")
    mg.GetYaxis().SetTitle("N_{2} Eq")
    #    mgclone.GetYaxis().SetRangeUser(-3,0)

    mlegend.Draw()

    # pname  = wwwpath
    # subfolder = 'TCT/HL/relaxedColl/newScatt/'
    # pname += subfolder + hname + '_' + doZoom + '.png'

    pname = pressureData.split('.csv')[0] + "b_pressure_2012.png"    
    print('Saving file as ' + pname ) 
    cv.Print(pname)


# ----------------------------------------------------------------------------
def cv32c():

    data = getdata()
    a,b = 1,2
    cv = TCanvas( 'cv', 'cv', a*2100, b*900)
    cv.Divide(a,b)

    cv.cd(1)
    x1, y1, x2, y2 = 0.8, 0.65, 0.9, 0.9
    mylegend = TLegend( x1, y1, x2, y2)
    mylegend.SetFillColor(0)
    mylegend.SetFillStyle(0)
    mylegend.SetLineColor(0)
    mylegend.SetTextSize(0.035)
    mylegend.SetShadowColor(0)
    mylegend.SetBorderSize(0)

    mgr = TMultiGraph()

    xKey, yKey, color, mStyle, lg = 's','avPress', kGreen, 22, 'aver. pressure'
    g0 = makeGraph(data, xKey, yKey, color, mStyle)
    mylegend.AddEntry(g0, lg, "p")    
    mgr.Add(g0)

    xKey, yKey, color, mStyle, lg = 's','avPressCorr', kBlue, 23, 'aver. pressure corr.'
    g1 = makeGraph(data, xKey, yKey, color, mStyle)
    mylegend.AddEntry(g1, lg, "p") 
    mgr.Add(g1)

    mgr.Draw("ap")

    gPad.SetLogy(1)
    gPad.RedrawAxis()

    mgr.SetTitle("2012 pressure profiles")
    mgr.GetXaxis().SetTitle("s ")
    mgr.GetYaxis().SetTitle("av. pressure")

    mylegend.Draw()

    # ....................................................................................................

    cv.cd(2)
    x1, y1, x2, y2 = 0.8, 0.65, 0.9, 0.9
    mlegend = TLegend( x1, y1, x2, y2)
    mlegend.SetFillColor(0)
    mlegend.SetFillStyle(0)
    mlegend.SetLineColor(0)
    mlegend.SetTextSize(0.035)
    mlegend.SetShadowColor(0)
    mlegend.SetBorderSize(0)

    mg = TMultiGraph()

    xKey, yKey, color, mStyle, lg = 's','H2Eq', kRed, 20, 'H_{2} Eq'
    g2 = makeGraph(data, xKey, yKey, color, mStyle)
    mlegend.AddEntry(g2, lg, "p") 
    mg.Add(g2)

    xKey, yKey, color, mStyle, lg = 's','H2EqCorr', kMagenta, 21, 'H_{2} Eq corr.'
    g3 = makeGraph(data, xKey, yKey, color, mStyle)
    mlegend.AddEntry(g3, lg, "p") 
    mg.Add(g3)

    mg.Draw("ap")

    gPad.SetLogy(1)
    gPad.RedrawAxis()

    mg.SetTitle("2012 pressure profiles")
    mg.GetXaxis().SetTitle("s ")
    mg.GetYaxis().SetTitle("H_{2} Eq")
    
    mlegend.Draw()

    # pname  = wwwpath
    # subfolder = 'TCT/HL/relaxedColl/newScatt/'
    # pname += subfolder + hname + '_' + doZoom + '.png'

    pname = pressureData.split('.csv')[0] + "c_pressure_2012.png"    
    print('Saving file as ' + pname ) 
    cv.Print(pname)

# ----------------------------------------------------------------------------

def cv32():
    cv32a()
    cv32b()
    cv32c()

# ----------------------------------------------------------------------------
