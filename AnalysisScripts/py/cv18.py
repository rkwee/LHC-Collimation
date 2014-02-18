#!/usr/bin/python
#
#
# Feb  2014, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
from helpers import workpath, wwwpath, mylabel
from createTTree import treeName
from fillTTree_dict import generate_sDict
## -------------------------------------------------------------------------------
def cv18():

    # compute how deep the TCT hits are inside the jaw
    # take the difference to the jaw edge
    # compare B1 and B2 hits to check why B2 induces more bbg than B1
    # B2 has only hits in the TCTV

    fB1 = '/Users/rkwee/Documents/RHUL/work/runs/TCT/rotate/4TeV/B1/oldFormat_final_hits_and_angles_TCTV.root'
    fB2 = '/Users/rkwee/Documents/RHUL/work/runs/TCT/rotate/4TeV/B2/oldFormat_final_hits_and_angles_72_TCTV.root'

    treeName = 'particle'
    tB1 = TFile.Open(fB1).Get(treeName)
    tB2 = TFile.Open(fB2).Get(treeName)

    y_jawTop =  0.830261
    y_jawBot = -0.415249 

    hB1, hB2, nbins, xmin, xmax = 'hB1', 'hB2', 100, -1., 1.2


    var  = 'y - ' + str(y_jawTop)
    cut  = 'y > 0.'
    rel  = '_topJaw'
    xtitle = 'y - y_{jaw}[cm]'

    # var  = str(y_jawBot) + ' - y'
    # cut  = 'y < 0.'
    # rel  = '_botJaw'
    # xtitle = 'y_{jaw} - y[cm]'

    # var  = 'y'
    # cut  = ''
    # rel  = ''
    # xtitle = 'y[cm]'


    hname = 'compB1B2'
    cv   = TCanvas( 'cv'+hname, 'cv'+hname, 1200, 900)
    hB1  = TH1F(hB1, hB1, nbins, xmin, xmax)
    hB2  = TH1F(hB2, hB2, nbins, xmin, xmax)
    ytitle = 'entries'
    hB1.GetXaxis().SetTitle(xtitle)
    hB2.GetXaxis().SetTitle(xtitle)
    hB1.GetYaxis().SetTitle(ytitle)
    hB2.GetYaxis().SetTitle(ytitle)

    hB1.SetLineWidth(2)
    hB2.SetLineWidth(2)

    cB1, cB2 = kBlue, kRed
    sB1, sB2 = 3004, 3005
    hB1.SetLineColor(cB1)
    hB2.SetLineColor(cB2)
    hB1.SetFillColor(cB1)
    hB2.SetFillColor(cB2)
    hB1.SetFillStyle(sB1)
    hB2.SetFillStyle(sB2)

    tB1.Project('hB1',var,cut)
    tB2.Project('hB2',var,cut)
    hB1.Draw('hist')
    gPad.Update()
    st1 = TPaveStats()
    st1 = gPad.GetPrimitive("stats")

    y1 = st1.GetY1NDC() # (lower) y start position of stats box
    y2 = st1.GetY2NDC() # (upper) y start position of stats box
    newy1 = 2 * y1 - y2   # new (lower) y start position of stats box
    newy2 = y1            # new (upper) y start position of stats box
    st1.SetY1NDC(newy1)    #set new y start position
    st1.SetLineColor(cB1)
    st1.SetTextColor(cB1)
    st1.SetY2NDC(newy2)    #set new y end position

    newx1 = 0.25* st1.GetX1NDC() # (left) x start position of stats box
    newx2 = 0.4* st1.GetX2NDC() # (right) x start position of stats box
    st1.SetX1NDC(newx1)  
    st1.SetX2NDC(newx2)  

    hB2.Draw('hists')
    gPad.Update()
    st2 = TPaveStats()
    st2 = gPad.GetPrimitive("stats")
    st2.SetLineColor(cB2)
    st2.SetTextColor(cB2)
    st2.SetX1NDC(newx1)  
    st2.SetX2NDC(newx2)  

    hB2.Draw('hist')
    hB1.Draw('histsames')

    pname = wwwpath + 'TCT/4TeV/' + hname + '/' + hname + rel + '.png' 
    print 'saving', pname
    cv.SaveAs(pname)
