#!/usr/bin/python
#
# cv25: plot lossmaps on top of each other to precisely compare 
#
# Jan. 2015, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os, time, math
from ROOT import *
import lossmap, helpers, array
from helpers import wwwpath, file_len, length_LHC, mylabel, addCol, gitpath, workpath
from array import array
## -------------------------------------------------------------------------------

def cv25():

    debug   = 1
    hnames  = [ 'coll_loss', 'warm_loss', 'cold_loss' ]
    color   = [ kBlack, kRed, kBlue]

    def getHists(tag, hnames):

        hists   = []
        rfname  = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/testHDF5_100Pack/lossmap'+tag+'.root'

        rfname  = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/'+tag.lstrip('_')+'/lossmap'+tag+'.root'

        print('Plotting lossmaps from ' + '.'*20 + ' '+ rfname)

        trname  = 'normtree' + tag
        rf = TFile.Open(rfname)            
        nt = rf.Get(trname)
        branchname = tag.replace('.','QQQ')

        norm = -9999
        for entry in nt: 
            norm = getattr(entry,branchname)
            print 'norm', norm

        for hname in hnames:  
            hists += [rf.Get(hname + tag)]
            print 'entries = ', hists[-1].GetEntries(), ' of ', hists[-1].GetName()

        return hists, norm

        
    # hists_ascii, n_ascii = getHists('_NewScatt_TCT_4TeV_B1hHaloTEST', hnames)
    # hists_hdf5 , n_hdf5  = getHists('_H5_NewScatt_TCT_4TeV_B1hHaloTEST',  hnames)


    # -- different random seeds

    # -- 9020 packs -> nprim 9020 x 64
    # hists_ascii, n_ascii = getHists('_NewScatt_TCT_4TeV_B1hHalo', hnames)
    # -- 9700 packs -> nprim = 9700 x 64
    # hists_hdf5 , n_hdf5  = getHists('_H5_NewScatt_TCT_4TeV_B1hHalo',  hnames)
    # ----

    # 9020 packs -> nprim 9020 x 64
    hists_ascii, n_ascii = getHists('_NewScatt_TCT_4TeV_B2hHalo', hnames)
    # 9700 packs -> nprim = 9700 x 64
    hists_hdf5 , n_hdf5  = getHists('_H5_NewScatt_TCT_4TeV_B2hHalo',  hnames)
    # --

    for k in ['_hdf5']:
#    for k in ['_ascii']:
#    for k in ['_both']:
        for h,hname in enumerate(hnames):

            cv = TCanvas( 'cv' + hname+k, 'cv' + hname+k, 1200, 700)

            hists_ascii[h].SetLineColor(color[h])
            hists_hdf5[h].SetLineColor(kOrange)
            hists_ascii[h].SetFillColor(color[h])
            hists_hdf5[h].SetFillColor(kOrange)

            hists_ascii[h].Scale(1.0/n_ascii)
            hists_hdf5[h].Scale(1.0/n_hdf5)

            x1, y1, x2, y2 = 0.18, 0.78, 0.42, 0.9
            YurMin, YurMax = 3.2e-9, 3.

            rel = '_fullring'
            XurMin, XurMax = 0., length_LHC

            rel = '_ir7' + k
            XurMin, XurMax = 19.7e3, 20.6e3

            # for B2
            XurMin, XurMax = 6.3e3, 8.0e3 

            if k.count('ascii'):  hists_ascii[h].Draw('hist')
            if k.count('hdf5'): hists_hdf5[h].Draw('hist')
            if k.count('both'):
                hists_ascii[h].Draw('hist')
                hists_hdf5[h].Draw('samehist')

            lh = []
            # YurMin = 3.2e-9
            lhRange  = [3e-9+i*1e-9 for i in range(3,7)]
            lhRange += [i*1.e-8 for i in range(1,11)]
            lhRange += [i*1.e-7 for i in range(1,11)]
            lhRange += [i*1.e-6 for i in range(1,11)]
            lhRange += [i*1.e-5 for i in range(1,11)]
            lhRange += [i*1.e-4 for i in range(1,11)]
            lhRange += [i*1.e-3 for i in range(1,11)]
            lhRange += [i*1.e-2 for i in range(1,11)]
            lhRange += [i*1.e-1 for i in range(1,11)]
            lhRange += [i*1. for i in range(1,int(YurMax))]

            for i in lhRange:
                lh += [TLine()]
                lh[-1].SetLineStyle(1)
                lh[-1].SetLineColor(kGray)
                lh[-1].DrawLine(XurMin,i,XurMax,i)

            lv = []
            lvRange = [1000*i for i in range(0,int(length_LHC*1e-3))]
            for s in lvRange:

                if s > XurMin and s < XurMax:
                    lv += [TLine()]
                    lv[-1].SetLineStyle(1)
                    lv[-1].SetLineColor(kGray)
                    lv[-1].DrawLine(s,YurMin,s,YurMax)

            if k.count('ascii'): hists_ascii[h].Draw('same')                
            if k.count('hdf5'): hists_hdf5[h].Draw('same')
            if k.count('both'):
                hists_ascii[h].Draw('same')
                hists_hdf5[h].Draw('same')

            hists_ascii[h].GetXaxis().SetRangeUser(XurMin, XurMax)
            hists_ascii[h].GetYaxis().SetRangeUser(YurMin, YurMax)
            hists_hdf5[h].GetXaxis().SetRangeUser(XurMin, XurMax)
            hists_hdf5[h].GetYaxis().SetRangeUser(YurMin, YurMax)

            thelegend = TLegend( x1, y1, x2, y2)
            thelegend.SetFillColor(0)
            thelegend.SetLineColor(0)
            thelegend.SetTextSize(0.035)
            thelegend.SetShadowColor(10)
            if k.count('ascii'): thelegend.AddEntry(hists_ascii[h], hname + ' from ascii file', 'L')
            if k.count('hdf5'): thelegend.AddEntry(hists_hdf5[h], hname + ' from hdf5 file', 'L')

            if k.count('both'):
                thelegend.AddEntry(hists_ascii[h], hname + ' from ascii file', 'L')
                thelegend.AddEntry(hists_hdf5[h], hname + ' from hdf5 file', 'L')

            thelegend.Draw()

            gPad.RedrawAxis()
            gPad.SetGrid(0,1)
            gPad.SetLogy(1)

            pname  = wwwpath
            subfolder = 'TCT/4TeV/hdf5/'
            pname += subfolder + hname + rel + '.png'

            print('Saving file as' + pname ) 
            cv.Print(pname)
