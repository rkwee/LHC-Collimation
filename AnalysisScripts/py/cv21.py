#!/usr/bin/python
#
#
# Nov 2014, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os, time, math
from ROOT import *
import lossmap, helpers, array
from helpers import wwwpath, file_len, length_LHC,  addCol, gitpath
from operator import add
## -------------------------------------------------------------------------------

def cv21():

    # histogram losses in TCT4 and TCT5
    # HL scenario

    normhHaloTCTIN = 993400*64.
    normvHaloTCTIN = 994200.*64
    normvHaloTCTOUT = 14742*50.*64 
    normhHaloTCTOUT = 17237.*50*64
    
    tcts = [
        '19_TCTH.4L5',
        '20_TCTVA.4L5',
        '52_TCTH.4L1',
        '53_TCTVA.4L1',
        '54_TCTH.5L1',
        '55_TCTVA.5L1',
        '56_TCTH.5L5',
        '57 TCTVA.5L5',
        ]
    
    losseshTCTin = [2,31,1177,56,7517,1030,13,1443]
    lossesvTCTin = [0,48,1238,103,333,1719,8,969]
    sum1 = map(add,losseshTCTin,lossesvTCTin)

    losseshTCTout= [21,1221,7085,676,0,0,0,0]
    lossesvTCTout= [6,721,1141,1162,0,0,0,0]
    sum2 = map(add,losseshTCTout,lossesvTCTout)

    # 0 hname #1 norm, #2 losses in order of tcts, #3 MarkerColor #4 MarkerStyle #5 drawOpt
    hDict = {
        1:  ('hHalo_TCT5LIN', normhHaloTCTIN, losseshTCTin,           kBlue-2, 23, 'p'),
        2:  ('vHalo_TCT5LIN', normvHaloTCTIN, lossesvTCTin,           kBlue-1, 22, 'psame'),
        12: ('h+v_TCT5LIN', normvHaloTCTIN+normhHaloTCTIN, sum1,      kBlue,   24, 'psame'),
        3:  ('hHalo_TCT5LOUT', normhHaloTCTOUT,losseshTCTout,         kPink-2, 20, 'psame'),
        4:  ('vHalo_TCT5LOUT', normvHaloTCTOUT,lossesvTCTout,         kPink-1, 21, 'psame'),
        34: ('h+v_TCT5LOUT', normhHaloTCTOUT+normvHaloTCTOUT, sum2,   kPink,   27, 'psame'),
        }
        
    hkeys = hDict.keys()
    hkeys.sort()

    nbins, xmin, xmax = len(tcts), -0.5, len(tcts)-0.5
    hists = []

    cv = TCanvas( 'cv', 'cv', 10, 10, 1200, 700 )     

    x1, y1, x2, y2 = 0.65, 0.67, 0.84, 0.9
    thelegend = TLegend( x1, y1, x2, y2)
    thelegend.SetFillColor(0)
    thelegend.SetLineColor(0)
    thelegend.SetTextSize(0.035)
    thelegend.SetShadowColor(10)

    YurMin, YurMax = 1.e-9,1.6e-4
    for h in hkeys:
        hname = hDict[h][0]
        print('plotting ', hname)
        hists += [ TH1F(hname, hname, nbins, xmin, xmax) ]
        for i,v in enumerate(hDict[h][2]):
            hists[-1].SetBinContent(i+1,v)
            hists[-1].GetXaxis().SetBinLabel(i+1,tcts[i])
            
        hists[-1].GetYaxis().SetTitle('loss per primary')
        hists[-1].Scale(1./hDict[h][1])

        hists[-1].SetMarkerColor(hDict[h][3])
        hists[-1].SetMarkerStyle(hDict[h][4])
        hists[-1].GetYaxis().SetRangeUser(YurMin, YurMax)
        hists[-1].Draw(hDict[h][5])
        thelegend.AddEntry(hists[-1],hname.replace('_', ' '), 'p')

    thelegend.Draw()

    pname  = wwwpath
    subfolder = 'TCT/HL/relaxedColl/'
    pname += subfolder + 'compTCT5INOUT.png'
    print('Saving', pname)
    cv.SaveAs(pname)

