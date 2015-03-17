#!/usr/bin/python
#
# plot pressure profiles 4 TeV (2011/12)
#
# Mar 2015, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, os, time, math
from ROOT import *
import lossmap, helpers, array
from helpers import wwwpath, length_LHC, mylabel, gitpath, workpath
from array import array
## -------------------------------------------------------------------------------
# 14 colum format
pData = [ 
    ('beam-gas-sixtrack/pressure_profiles_2012/LSS4_IP4_2012_Roderik.csv',  "distance from IP4 [m]"),
    ('beam-gas-sixtrack/pressure_profiles_2012/LSS1_B1_Fill2736_Final.csv', "distance from IP1 [m]"),
    ('beam-gas-sixtrack/pressure_profiles_2012/LSS2_B1_Fill2736_Roderik.csv', "distance from IP2 [m]"),
    ('beam-gas-sixtrack/pressure_profiles_2012/LSS7_B1_Fill2736_Roderik.csv', "distance from IP7 [m]"),
    ('beam-gas-sixtrack/pressure_profiles_2011/LSS1_B1_fill_2028-sync_rad_and_ecloud.csv', "distance from IP1 [m]"),
    ('beam-gas-sixtrack/pressure_profiles_2011/LSS7_Fill2028_Roderick.csv', "distance from IP7 [m]"),
]

# 7 colum format
pData2 = [ 
    ('beam-gas-sixtrack/pressure_profiles_2011/LSS8_Fill_2028_B1_Roderik.csv', "distance from IP8 [m]"),
    ('beam-gas-sixtrack/pressure_profiles_2011/LSS2_B1_Blue_Fill2028_Roderick.csv',"distance from IP2 [m]"),
]

# comparison
pData3 = [
    ('beam-gas-sixtrack/pressure_profiles_2011/LSS1_B1_fill_2028-sync_rad_and_ecloud.csv', \
     'beam-gas-sixtrack/pressure_profiles_2012/LSS1_B1_Fill2736_Final.csv' ,"distance from IP1 [m]"),
    ('beam-gas-sixtrack/pressure_profiles_2011/LSS2_B1_Blue_Fill2028_Roderick.csv', \
     'beam-gas-sixtrack/pressure_profiles_2012/LSS2_B1_Fill2736_Roderik.csv', "distance from IP2 [m]"),
#    ('beam-gas-sixtrack/pressure_profiles_2011/LSS7_Fill2028_Roderick.csv', \
#     'beam-gas-sixtrack/pressure_profiles_2012/LSS7_B1_Fill2736_Roderik.csv', "distance from IP7 [m]"),
]
# -----------------------------------------------------------------------------------
def getdata14c(pFile):

    c = [ [] for i in range(14) ]
    with open(pFile) as mf:
        for l,line in enumerate(mf):

            for i in range(14):
                
                if i != 13:
                    c[i] += [ line.split(',')[i] ]
                else:
                    c[i] += [ line.split(',')[i].rstrip('\r\n') ]

    data = dict(s=c[0], l_total=c[1], rho_H2=c[2], rho_CH4=c[3], rho_CO=c[4], rho_CO2=c[5], \
                H2_N2Eq=c[6], CH4_N2Eq=c[7], CO_N2Eq=c[8], CO2_N2Eq=c[9], avPress=c[10], avPressCorr=c[11], H2Eq=c[12], H2EqCorr=c[13])

    return data
# -----------------------------------------------------------------------------------
def getdata7c(pFile):

    c = [ [] for i in range(7) ]
    with open(pFile) as mf:
        for l,line in enumerate(mf):

            for i in range(7):
                
                if i != 6:
                    c[i] += [ line.split(',')[i] ]
                else:
                    c[i] += [ line.split(',')[i].rstrip('\r\n') ]

    data = dict(s=c[0], rho_H2=c[1], rho_CH4=c[2], rho_CO=c[3], rho_CO2=c[4], \
                avPress=c[5], H2Eq=c[6])

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
        #print x, y
        gr.SetPoint(i+1, x, y)

    return gr
# ----------------------------------------------------------------------------
def cv32a(pFile,xTitle,data):

    lText = '2012'
    if pFile.count('2011'): lText = '2011'

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

    lab = mylabel(42)
    lab.DrawLatex(0.45, 0.9, lText)

    mg.SetTitle("pressure profiles")
    mg.GetXaxis().SetTitle(xTitle)
    mg.GetYaxis().SetTitle("density #rho [molecules/m^{3}]")
    mg.GetYaxis().SetRangeUser(1e7,1e17)
    mlegend.Draw()

    # pname  = wwwpath
    # subfolder = 'TCT/HL/relaxedColl/newScatt/'
    # pname += subfolder + hname + '_' + doZoom + '.png'

    pname = pFile.split('.csv')[0] + "a_pressure.png"    
    print('Saving file as ' + pname ) 
    cv.Print(pname)

# ----------------------------------------------------------------------------
def cv32b(pFile,xTitle,data):

    lText = '2012'
    if pFile.count('2011'): lText = '2011'

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

    lab = mylabel(42)
    lab.DrawLatex(0.45, 0.9, lText)

    mg.SetTitle("pressure profiles")
    mg.GetXaxis().SetTitle(xTitle)
    mg.GetYaxis().SetTitle("N_{2} Eq")
    mg.GetYaxis().SetRangeUser(1e-16,1e-7)

    mlegend.Draw()

    # pname  = wwwpath
    # subfolder = 'TCT/HL/relaxedColl/newScatt/'
    # pname += subfolder + hname + '_' + doZoom + '.png'

    pname = pFile.split('.csv')[0] + "b_pressure.png"    
    print('Saving file as ' + pname ) 
    cv.Print(pname)


# ----------------------------------------------------------------------------
def cv32c(pFile, xTitle, data, doCorr):

    lText = '2012'
    if pFile.count('2011'): lText = '2011'

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

    xKey, yKey, color, mStyle, lg = 's','avPress', kGreen, 23, 'aver. pressure'
    g0 = makeGraph(data, xKey, yKey, color, mStyle)
    mylegend.AddEntry(g0, lg, "p")    
    mgr.Add(g0)

    if doCorr:
        xKey, yKey, color, mStyle, lg = 's','avPressCorr', kBlue, 24, 'aver. pressure corr.'
        g1 = makeGraph(data, xKey, yKey, color, mStyle)
        mylegend.AddEntry(g1, lg, "p") 
        mgr.Add(g1)

    mgr.Draw("ap")

    gPad.SetLogy(1)
    gPad.RedrawAxis()

    lab = mylabel(42)
    lab.DrawLatex(0.45, 0.9, lText)

    mgr.SetTitle("pressure profiles")
    mgr.GetXaxis().SetTitle(xTitle)
    mgr.GetYaxis().SetTitle("av. pressure")
    mgr.GetYaxis().SetRangeUser(1e-12,1e-6)

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

    xKey, yKey, color, mStyle, lg = 's','H2Eq', kBlue, 23, 'H_{2} Eq'
    g2 = makeGraph(data, xKey, yKey, color, mStyle)
    mlegend.AddEntry(g2, lg, "p") 
    mg.Add(g2)

    if doCorr:
        xKey, yKey, color, mStyle, lg = 's','H2EqCorr', kMagenta, 24, 'H_{2} Eq corr.'
        g3 = makeGraph(data, xKey, yKey, color, mStyle)
        mlegend.AddEntry(g3, lg, "p") 
        mg.Add(g3)

    mg.Draw("ap")

    gPad.SetLogy(1)
    gPad.RedrawAxis()
    lab = mylabel(42)
    lab.DrawLatex(0.45, 0.9, lText)

    mg.SetTitle("pressure profiles")
    mg.GetXaxis().SetTitle(xTitle)
    mg.GetYaxis().SetTitle("H_{2} Eq")
    mg.GetYaxis().SetRangeUser(2e10,9e17)

    mlegend.Draw()

    # pname  = wwwpath
    # subfolder = 'TCT/HL/relaxedColl/newScatt/'
    # pname += subfolder + hname + '_' + doZoom + '.png'

    pname = pFile.split('.csv')[0] + "c_pressure.png"    
    print('Saving file as ' + pname ) 
    cv.Print(pname)

# ----------------------------------------------------------------------------
def cv32d( data2011, data2012, xTitle):

    LSS = 'LSS' + xTitle.split('IP')[1][0]
    cv = TCanvas( 'cv', 'cv', 2100, 900)

    x1, y1, x2, y2 = 0.7, 0.65, 0.9, 0.9
    mlegend = TLegend( x1, y1, x2, y2)
    mlegend.SetFillColor(0)
    mlegend.SetFillStyle(0)
    mlegend.SetLineColor(0)
    mlegend.SetTextSize(0.035)
    mlegend.SetShadowColor(0)
    mlegend.SetBorderSize(0)

    mg = TMultiGraph()

    xKey, yKey, color, mStyle, lg = 's','H2Eq', kBlue, 23, 'H_{2} Eq 2011'
    g0 = makeGraph(data2011, xKey, yKey, color, mStyle)
    mlegend.AddEntry(g0, lg, "p") 
    mg.Add(g0)


    xKey, yKey, color, mStyle, lg = 's','H2Eq', kMagenta, 24, 'H_{2} Eq 2012'
    g1 = makeGraph(data2012, xKey, yKey, color, mStyle)
    mlegend.AddEntry(g1, lg, "p") 
    mg.Add(g1)

    mg.Draw("ap")

    gPad.SetLogy(1)
    gPad.RedrawAxis()

    mg.SetTitle("pressure profiles")
    mg.GetXaxis().SetTitle(xTitle)
    mg.GetYaxis().SetTitle("H_{2} Eq")
    mg.GetYaxis().SetRangeUser(2e10,9e17)

    mlegend.Draw()

    # pname  = wwwpath
    # subfolder = 'TCT/HL/relaxedColl/newScatt/'
    # pname += subfolder + hname + '_' + doZoom + '.png'

    pname = "comparison_"+ LSS +".png"
    print('Saving file as ' + pname ) 
    cv.Print(pname)
# ----------------------------------------------------------------------------

def cv32():

    data2011, data2012 = {}, {}

    pDataFiles  = [p[0] for p in pData]
    pData2Files = [p[0] for p in pData2]

    for p2011, p2012, xTitle in pData3:
        if p2011 in pDataFiles:
            data2011 = getdata14c(p2011)
        elif p2011 in pData2Files:
            data2011 = getdata7c(p2011)

        if p2012 in pDataFiles:
            data2012 = getdata14c(p2012)
        elif p2012 in pData2Files:
            data2012 = getdata7c(p2012)

        if data2011 and data2012:
            cv32d( data2011, data2012, xTitle)


    if 0:
        for pFile,xTitle in pData:
            print '.'*22,pFile,'.'*22
            data = getdata14c(pFile)
            cv32a(pFile,xTitle,data)
            cv32b(pFile,xTitle,data)
            cv32c(pFile,xTitle,data,1)


        for pFile,xTitle in pData2:
            print '.'*22,pFile,'.'*22
            data = getdata7c(pFile)
            cv32a(pFile,xTitle,data)
            cv32c(pFile,xTitle,data,0)

# ----------------------------------------------------------------------------
