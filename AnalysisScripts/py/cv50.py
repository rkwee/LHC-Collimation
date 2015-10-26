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

        (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_hHaloB1_roundthin', 'round B1H'),
        (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_vHaloB1_roundthin', 'round B1V'),
        (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5LOUT_relaxColl_hHaloB1_roundthin', 'round B1H'),
        (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5LOUT_relaxColl_vHaloB1_roundthin', 'round B1V'),
        (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_hHaloB1_flatthin', 'flat B1H'),
        (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_vHaloB1_flatthin', 'flat B1V'),
        (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5LOUT_relaxColl_hHaloB1_flatthin', 'flat B1H'),
        (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5LOUT_relaxColl_vHaloB1_flatthin', 'flat B1V'),

        (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_hHaloB2_roundthin', 'round B2H'),
        (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_vHaloB2_roundthin', 'round B2V'),
        (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5LOUT_relaxColl_hHaloB2_roundthin', 'round B2H'),
        (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5LOUT_relaxColl_vHaloB2_roundthin', 'round B2V'),
        # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_hHaloB2_flatthin', 'fl B2H'),
        # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_vHaloB2_flatthin', 'fl B2V'),
        # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5LOUT_relaxColl_hHaloB2_flatthin', 'fl B2H'),
        # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5LOUT_relaxColl_vHaloB2_flatthin', 'fl B2V'),


        #(projectpath + 'HL1.0/H5_HL_nomSett_hHalo_b1', 'rd B1H nom. sett'),
        #(projectpath + 'HL1.0/H5_HL_nomSett_vHalo_b1', 'rd B1V nom. sett'),
        # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_hHaloB1_roundthin', 'rd B1H 2#sigma-retract. sett'),
        # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_vHaloB1_roundthin', 'rd B1V 2#sigma-retract. sett'),
        # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_hHaloB1_flatthin',  'fl B1H 2#sigma-retract. sett'),
        # (workpath  + 'runs/HL_TCT5INOUT_relSett/H5_HL_TCT5IN_relaxColl_vHaloB1_flatthin',  'fl B1V 2#sigma-retract. sett'),

        ]


    lossPointsB1 = [#('cold_loss', 20290., 20340., "Q8"),
                    #('cold_loss', 20380., 20430., "Q10"),
                    ('cold_loss', 2029., 20430., "both"),
                    ]
    lossPointsB2 = [#('cold_loss', 6950., 7010., "Q7"),
                    #('cold_loss', 7050., 7110., "Q9"),
                    ('cold_loss', 6950., 7110., "both"),
                    ]

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

        # ................................................
        for h,loss_start,loss_end,pointName in lossPoints:
            
            # structure: summed loss, loss in bin range, statistical error, maximal loss in bin range, its statistical error
            losses += [avLosses(rfname, tag, 1., h+tag, loss_start, loss_end, pointName)]
    

    # ------------------------------------------------
    # plot 

    print "plotting ",len(losses), "loss points. Expect to have same amount of dirs", len(dirs)
    #    print losses
    cv = TCanvas( 'cv', 'cv', 1000, 600)
    cv.SetGridx(1)
    cv.SetGridy(1)
    x1, y1, x2, y2 = 0.56, 0.8, 0.9, 0.9
    mlegend = TLegend( x1, y1, x2, y2)
    mlegend.SetFillColor(0)
    mlegend.SetFillStyle(0)
    mlegend.SetLineColor(0)
    mlegend.SetTextSize(0.035)
    mlegend.SetShadowColor(0)
    mlegend.SetBorderSize(0)

    hname, nbins, xmin, xmax = "summary", len(losses), -0.5, len(losses)-0.5
    hx = TH1F(hname,hname,nbins, xmin, xmax) 
    hm = TH1F(hname,hname,nbins, xmin, xmax) 

    hs = TH1F(hname,hname,nbins, xmin, xmax) 
    hn = TH1F(hname,hname,nbins, xmin, xmax) 

    hx.SetMarkerStyle(34)
    hx.SetMarkerSize(2)
    hx.SetMarkerColor(kBlue-2)

    hm.SetMarkerSize(2)
    hm.SetMarkerStyle(33)
    hm.SetMarkerColor(kGreen+1)

    hs.SetMarkerStyle(23)
    hs.SetMarkerColor(kPink-2)

    hn.SetMarkerStyle(34)
    hn.SetMarkerColor(kBlue)

    ytitle = "local cleaning inefficiency #eta [1/m]"

    hx.GetXaxis().SetLabelSize(0.05)
    hx.GetYaxis().SetLabelSize(0.05)
    hx.GetYaxis().SetTitleOffset(0.8)
    hx.GetYaxis().SetTitle(ytitle)

    YurMin, YurMax = 3e-6,1.2e-5
    #YurMin, YurMax = 3e-6,1.3e-3
    hx.GetYaxis().SetRangeUser(YurMin, YurMax)
    hs.GetYaxis().SetRangeUser(YurMin, YurMax)

    for bin, losslist in enumerate(losses):
        sumLoss, avLoss, avLossErr, maxColdLoss, maxColdLossErr = losslist
        hx.SetBinContent(bin+1,avLoss)
        hx.GetXaxis().SetBinLabel(bin+1,dirs[bin][1])
        hs.SetBinContent(bin+1, sumLoss)
        hm.SetBinContent(bin+1, maxColdLoss*0.1)
        hn.SetBinContent(bin+1, maxColdLoss)

    mlegend.AddEntry(hx, 'average #eta in Q8+Q10', 'p')
    mlegend.AddEntry(hm, '10% of max #eta in Q8+Q10', 'p')
    #mlegend.AddEntry(hs, 'integrated #eta in Q8+Q10', 'p')
    #mlegend.AddEntry(hn, 'max #eta in Q8+Q10', 'p')

    hx.Draw("p")
    hm.Draw("psame")
    mlegend.Draw()
    x1, y1, x2, y2 = 0.35, 1.1, 0.9, 1.3
    lab = mylabel(42)
    lab.DrawLatex(x1, y2-0.05, 'HL 2#sigma-retracted setting')
    pname  = wwwpath
    pname += subfolder + 'comparison_avloss_retracted_HL.png'

    print('Saving file as ' + pname ) 
    cv.SaveAs(pname)


