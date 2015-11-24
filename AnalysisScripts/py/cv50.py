#!/usr/bin/python
#
# get average losses
# re-use cv22: compare cleaning efficiency of HL scenarios 
# oct 2015, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os, time, math
from ROOT import *
import avLosses
from avLosses import avLosses
from helpers import wwwpath, projectpath, length_LHC, mylabel, addCol, gitpath, workpath, getBeam
## -------------------------------------------------------------------------------

def cv50():

    debug = 1

    # subfolder in wwwpath for result plots
    subfolder = 'TCT/HL/' 
    

    # dont end the first element with a "/"
    dirs = [

        # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_hHaloB1_roundthin', 'rd B1H, TCT5 in'),
        # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_vHaloB1_roundthin', 'rd B1V, TCT5 in'),
        # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5LOUT_relaxColl_hHaloB1_roundthin', 'rd B1H, TCT5 out'),
        # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5LOUT_relaxColl_vHaloB1_roundthin', 'rd B1V, TCT5 out'),
        # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_hHaloB1_flatthin', 'fl B1H, TCT5 in'),
        # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_vHaloB1_flatthin', 'fl B1V, TCT5 in'),
        # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5LOUT_relaxColl_hHaloB1_flatthin', 'fl B1H, TCT5 out'),
        # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5LOUT_relaxColl_vHaloB1_flatthin', 'fl B1V, TCT5 out'),

        # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_hHaloB2_roundthin', 'rd B2H, TCT5 in'),
        # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_vHaloB2_roundthin', 'rd B2V, TCT5 in'),
        # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5LOUT_relaxColl_hHaloB2_roundthin', 'rd B2H, TCT5 out'),
        # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5LOUT_relaxColl_vHaloB2_roundthin', 'rd B2V, TCT5 out'),

        # # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_hHaloB2_flatthin', 'fl B2H'),
        # # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_vHaloB2_flatthin', 'fl B2V'),
        # # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5LOUT_relaxColl_hHaloB2_flatthin', 'fl B2H'),
        # # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5LOUT_relaxColl_vHaloB2_flatthin', 'fl B2V'),


        (projectpath + 'HL1.0/H5_HL_nomSett_hHalo_b1', 'rd B1H nom. sett'),
        (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_hHaloB1_roundthin', 'rd B1H 2#sigma-retract. sett'),
        (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_hHaloB1_flatthin',  'fl B1H 2#sigma-retract. sett'),
        (projectpath + 'HL1.0/H5_HL_nomSett_vHalo_b1', 'rd B1V nom. sett'),
        (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_vHaloB1_roundthin', 'rd B1V 2#sigma-retract. sett'),
        (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_vHaloB1_flatthin',  'fl B1V 2#sigma-retract. sett'),

        ]


    lossPointsB1 = [('cold_loss', 20300., 20335., "cluster 1", kBlue-2, 34),
                    ('cold_loss', 20390., 20400., "cluster 2", kCyan+1, 20),
                    #('cold_loss', 20290., 20430., "both"),
                    ]
    lossPointsB2 = [('cold_loss', 6967., 7000., "cluster 1", kMagenta-2, 34),
                    ('cold_loss', 7060., 7095., "cluster 2", kBlue-4, 33),
                    #('cold_loss', 6950., 7110., "both", kGreen-5, 30),
                    ]

    lossPoints = lossPointsB2
    lossesAllPoints = []
    cnt = 0
    for h,loss_start,loss_end,pointName, hxCol, hxMar in lossPoints:

        losses = []
        for case, lab in dirs:

            print '.'*50

            tag  = '_'+ case.split('/')[-1]

            print "extracted tag", tag
            Beam, beam, beamn = getBeam(tag)


            rfname = case + '/lossmap'+ tag +'.root'
            trname = 'normtree' + tag

            if not os.path.exists(rfname): 
                print rfname,' does not exist?!'
                continue

            lossPoints = lossPointsB2
            if beamn == "1": lossPoints = lossPointsB1

            h,loss_start,loss_end,pointName, hxCol, hxMar = lossPoints[cnt]
            # ................................................

            # structure: summed loss, loss in bin range, statistical error, maximal loss in bin range, its statistical error
            losses += [avLosses(rfname, tag, 1., h+tag, loss_start, loss_end, pointName)]

        lossesAllPoints += [losses]    
        cnt += 1 
    # ------------------------------------------------
    # plot 

    print "plotting ",len(lossesAllPoints), "loss points"
    print "len(lossesAllPoints[0])", len(lossesAllPoints[0]), "Expect to have same amount of dirs", len(dirs)

    cv = TCanvas( 'cv', 'cv', 1000, 600)
    cv.SetGridx(1)
    cv.SetGridy(1)
    x1, y1, x2, y2 = 0.56, 0.8, 0.9, 0.93
    mlegend = TLegend( x1, y1, x2, y2)
    mlegend.SetFillColor(0)
    mlegend.SetFillStyle(0)
    mlegend.SetLineColor(0)
    mlegend.SetTextSize(0.035)
    mlegend.SetShadowColor(0)
    mlegend.SetBorderSize(0)

    hx = []
    for i,losstuple in enumerate(lossPoints):

        histname, binStart, binEnd, pointName, hxCol, hxMar = losstuple
        hname, nbins, xmin, xmax = "summary" + pointName, len(dirs), -0.5, len(dirs)-0.5
        hx += [ TH1F(hname,hname,nbins, xmin, xmax) ]
        hm =  TH1F(hname,hname,nbins, xmin, xmax) 

        hx[-1].SetMarkerStyle(hxMar)
        hx[-1].SetMarkerSize(2)
        hx[-1].SetMarkerColor(hxCol)

        hmCol,hmMar = kGreen+1, 33
        hmCol,hmMar = kOrange+6, 22
        hm.SetMarkerSize(2)
        hm.SetMarkerStyle(hmMar)
        hm.SetMarkerColor(hmCol)


        ytitle = "local cleaning inefficiency #eta [1/m]"

        hx[-1].GetXaxis().SetLabelSize(0.05)
        hx[-1].GetYaxis().SetLabelSize(0.05)
        hx[-1].GetYaxis().SetTitleOffset(0.8)
        hx[-1].GetYaxis().SetTitle(ytitle)
        
        YurMin, YurMax = 3e-6,2.e-5
        hx[-1].GetYaxis().SetRangeUser(YurMin, YurMax)

        losses = lossesAllPoints[i]

        for bin, losslist in enumerate(losses):
            sumLoss, avLoss, avLossErr, maxColdLoss, maxColdLossErr = losslist
            hx[-1].SetBinContent(bin+1,avLoss)
            hx[-1].GetXaxis().SetBinLabel(bin+1,dirs[bin][1])
            hm.SetBinContent(bin+1, 0.1*maxColdLoss)

        rel = pointName
        mlegend.AddEntry(hx[-1], 'average #eta in ' + rel, 'p')


        if i == 0: drawOpt = ''
        else: drawOpt = 'same'
        hx[-1].Draw("p"+drawOpt)
        
        hm.Draw("psame")   

    mlegend.AddEntry(hm, '10% of max cold #eta', 'p')
    mlegend.Draw()
    x1, y1, x2, y2 = 0.35, 1.1, 0.9, 1.3
    lab = mylabel(42)
    lab.DrawLatex(x1, y2-0.05, 'HL 2#sigma-retracted setting')
    pname  = wwwpath
    pname += subfolder + 'comparison_avloss_HL.pdf'

    print('Saving file as ' + pname ) 
    cv.SaveAs(pname)


