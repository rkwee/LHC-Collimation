#!/usr/bin/python
#
# if doWriteRFile == 1
#    writes out root file : histograms for lossmaps and 1 ttree with normalisation factor
#    
# if plotLossMaps == 1
#    uses rootfile
#    plots lossmap for every tcs
#    plots zoomed version
#
#
# Sept 2013, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os, time, math
from ROOT import *
import lossmap, helpers, array
from helpers import wwwpath, file_len, length_LHC, mylabel, addCol
from array import array
## -------------------------------------------------------------------------------

def cv10():

    debug        = 1
    doWriteRFile = 0
    plotLossMaps = 0
    doSelectRange= 1
    doAvLoss     = 0


    collsHB1 = [
        # hHaloB1
        ('hHalo', '_sel1.B1'),
        ('hHalo', '_nominal.B1'),
        ('hHalo', '_TCSG.A6L7.B1'),
        ('hHalo', '_TCSG.B5L7.B1'),
        ('hHalo', '_TCSG.A5L7.B1'),
        ('hHalo', '_TCSG.D4L7.B1'),
        ('hHalo', '_TCSG.B4L7.B1'),
        ('hHalo', '_TCSG.A4L7.B1'),
        ('hHalo', '_TCSG.A4R7.B1'),
        ('hHalo', '_TCSG.B5R7.B1'),
        ('hHalo', '_TCSG.D5R7.B1'),
        ('hHalo', '_TCSG.E5R7.B1'),
        ('hHalo', '_TCSG.6R7.B1'),
        ]

    collsVB1 = [
        # vHaloB1
        ('vHalo', '_sel1.B1'),
        ('vHalo', '_nominal.B1'),
        ('vHalo', '_TCSG.A6L7.B1'),
        ('vHalo', '_TCSG.B5L7.B1'),
        ('vHalo', '_TCSG.A5L7.B1'),
        ('vHalo', '_TCSG.D4L7.B1'),
        ('vHalo', '_TCSG.B4L7.B1'),
        ('vHalo', '_TCSG.A4L7.B1'),
        ('vHalo', '_TCSG.A4R7.B1'),
        ('vHalo', '_TCSG.B5R7.B1'),
        ('vHalo', '_TCSG.D5R7.B1'),
        ('vHalo', '_TCSG.E5R7.B1'),
        ('vHalo', '_TCSG.6R7.B1'),
        ]

    collsHB2 = [
	('hHalo', '_nominal_B2'),
	('hHalo', '_nominal.B2'),
	('hHalo', '_TCSG.6L7.B2'),
	('hHalo', '_TCSG.A4L7.B2'),
	('hHalo', '_TCSG.A4R7.B2'),
	('hHalo', '_TCSG.A5R7.B2'),
	('hHalo', '_TCSG.A6R7.B2'),
	('hHalo', '_TCSG.B4R7.B2'),
	('hHalo', '_TCSG.B5L7.B2'),
	('hHalo', '_TCSG.B5R7.B2'),
	('hHalo', '_TCSG.D4R7.B2'),
	('hHalo', '_TCSG.D5L7.B2'),
	('hHalo', '_TCSG.E5L7.B2'),
        ]

    # tcs 
    colls = collsHB2
    # subfolder in wwwpath for result plots
    subfolder = 'scan/' 
    
    for haloType,coll in colls:

        beam   = 'b2'            
        beamn  = '2'        
        if coll.count('B1'):
            beam  = 'b1'
            beamn = '1'

        # my results (tight coll settings)
        thispath  = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/scan/B'+beamn+'/'+haloType+'/' 

        rfname = thispath + 'scan_lossmaps_'+ haloType+'B'+beamn+coll+'.root'
        trname = 'normtree' + coll
        colNumber = 4
            
        f3 = helpers.source_dir + 'HL_TCT_7TeV/' + beam +'/CollPositions.'+beam+'.dat'
        f3 = helpers.source_dir + 'TCT_4TeV_60cm/'+beam+'/CollPositions.'+beam+'.dat'
        f3 = helpers.source_dir + 'NewColl7TeVB'+beamn+'/CollPositions.'+beam+'.dat'

        # use for normalisation the sum of nabs (col 4)
        f4 = thispath + 'coll_summary' + coll + '.dat'

        # ------------------------------------------------

        if doWriteRFile:

            print 'Writing ' + '.'* 25 +' ' + rfname        

            # create a root file
            rf = TFile(rfname, 'recreate')
    
            nt  = TTree(trname,'norm for each coll') 

            if not os.path.exists(f4): 
                print f4,' does not exist?!'
                continue

            t0 = time.time()
            h_tot_loss, h_cold, h_warm = lossmap.lossmap(beam,thispath,coll, f3) 
            t1 = time.time()
            print(str(t1-t0)+' for returning lossmap histograms of ' + coll )

            if debug:
                if h_cold.GetEntries() < 1.:
                    print 'Empty histogram! Binary characters in LPI file?'
                    sys.exit()

            h_tot_loss.Write()
            h_cold.Write()
            h_warm.Write()            

            # -- write the for each norm value a branch into ttree
            t0 = time.time()

            # setting branch name 
            branchname = coll.replace('.','QQQ')

            if debug and 0: print globals()

            # use globals dict to convert strings to variable names
            globals()[branchname] = array('i',[0])

            # create branch
            nt.Branch(branchname, globals()[branchname], branchname+'/i')

            # get value
            maxval = int(addCol(f4, colNumber-1))

            # assigning value
            globals()[branchname][0] = maxval

            # write to tree
            nt.Fill()

            t1 = time.time()

            nt.Write()
            rf.Close()

        # ------------------------------------------------

        if plotLossMaps:
            
            if not os.path.exists(rfname): 
                print rfname,' does not exist?!'
                continue

            print('Plotting lossmaps from ' + '.'*20 + ' '+ rfname)
            trname = 'normtree' + coll

            doZooms = [0,1]
            rel = ''
            for doZoom in doZooms: 

                rf = TFile.Open(rfname)            
                nt = rf.Get(trname)
                branchname = coll.replace('.','QQQ')

                norm = -9999
                for entry in nt: 
                    norm = getattr(entry,branchname)
                    print 'norm', norm

                cv = TCanvas( 'cv' + coll + str(doZoom), 'cv' + coll + str(doZoom), 1200, 700)

                YurMin, YurMax = 3.2e-9, 3.

                hname = 'coll_loss' +coll

                if debug: print('Get histograms for coll ' + coll + ', starting with ' + hname)

                coll_loss = rf.Get(hname)
                cold_loss = rf.Get('cold_loss' +coll)
                warm_loss = rf.Get('warm_loss' +coll)

                coll_loss.SetLineColor(kBlack)
                warm_loss.SetLineColor(kOrange)
                cold_loss.SetLineColor(kBlue)
                coll_loss.SetFillColor(kBlack)
                warm_loss.SetFillColor(kOrange)
                cold_loss.SetFillColor(kBlue)

                coll_loss.Scale(1.0/norm)
                cold_loss.Scale(1.0/norm)
                warm_loss.Scale(1.0/norm)

                if beam.count('1') and not doZoom:
                    x1, y1, x2, y2 = 0.18, 0.78, 0.42, 0.9
                else:
                    x1, y1, x2, y2 = 0.68, 0.78, 0.91, 0.9

                XurMin, XurMax = 0., length_LHC
                if doZoom and beam.count('1'):
                    XurMin, XurMax = 19.7e3, 20.6e3
                    rel = '_zoom'

                coll_loss.Draw('hist')
                cold_loss.Draw('samehist')
                warm_loss.Draw('samehist')

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

                coll_loss.Draw('same')
                cold_loss.Draw('same')
                warm_loss.Draw('same')

                coll_loss.GetXaxis().SetRangeUser(XurMin, XurMax)
                coll_loss.GetYaxis().SetRangeUser(YurMin, YurMax)

                thelegend = TLegend( x1, y1, x2, y2)
                thelegend.SetFillColor(0)
                thelegend.SetLineColor(0)
                thelegend.SetTextSize(0.035)
                thelegend.SetShadowColor(10)
                thelegend.AddEntry(coll_loss,'losses on collimators', 'L')
                thelegend.AddEntry(cold_loss,'cold losses', 'L')
                thelegend.AddEntry(warm_loss,'warm losses', 'L')
                thelegend.Draw()

                lab = mylabel(60)
                lab.DrawLatex(x1, y1-0.1, coll.lstrip('_'))
                lab = mylabel(42)
                lab.DrawLatex(.5, y1+0.08, haloType)

                gPad.RedrawAxis()
                gPad.SetGrid(0,1)
                gPad.SetLogy(1)

                pname  = wwwpath
                pname += subfolder + hname + '_' + haloType+ rel+'.png'

                print('Saving file as' + pname ) 
                cv.Print(pname)

        # ------------------------------------------------
        if doSelectRange:

            rf = TFile.Open(rfname)            
            trname = 'normtree' + coll
            branchname = coll.replace('.','QQQ')
            nt = rf.Get(trname)
            norm = -9999
            for entry in nt: norm = getattr(entry,branchname)

            hist = rf.Get('cold_loss' + coll)
            hist.Scale(1./norm)

            cv = TCanvas( 'cv'+coll , 'cv'+coll , 2000, 700)
            gPad.SetLogy(1)

            s_startQ8, s_stopQ8   = 6940., 7020.
            s_startQ10, s_stopQ10 = 7050., 7110.

            if coll.count('B1'):
                s_startQ8, s_stopQ8   = 20270., 20340.
                s_startQ10, s_stopQ10 = 20370., 20435.

            XurMin, XurMax = s_startQ8, s_stopQ10
            hist.GetXaxis().SetRangeUser(XurMin*.995, XurMax*1.005)

            YurMin, YurMax = 1e-8,5e-5
            hist.GetYaxis().SetRangeUser(YurMin, YurMax)

            hist.GetYaxis().SetTitle('#eta [m^{-1}]')
            hist.GetYaxis().SetTitle('s [m]')
            hist.Draw()

            lv = TLine()
            lv.SetLineStyle(1)
            lv.SetLineWidth(2)
            lv.SetLineColor(kBlue)
            xval = s_startQ8
            lv.DrawLine(xval,YurMin,xval,YurMax)
            xval = s_stopQ8
            lv.DrawLine(xval,YurMin,xval,YurMax)

            lv.SetLineStyle(1)
            lv.SetLineWidth(2)
            lv.SetLineColor(kOrange)
            xval = s_startQ10
            lv.DrawLine(xval,YurMin,xval,YurMax)
            xval = s_stopQ10
            lv.DrawLine(xval,YurMin,xval,YurMax)

            subfolder = 'scan/benchmarkLosses/'
            resulthist = 'bm' + coll + '_' + haloType + 'B'+ beamn

            pname  = wwwpath
            pname += subfolder + resulthist+'.png'

            print('Saving file as' + pname ) 
            cv.Print(pname)

    # ------------------------------------------------
    
    if doAvLoss:

        maxLosses, lossesQ8, lossesQ10 = [],[],[]
        fraction = 0.1
        for haloType,coll in colls:

            beam   = 'b2'            
            beamn  = '2'        
            if coll.count('B1'):
                beam  = 'b1'
                beamn = '1'

            rfname = thispath + 'scan_lossmaps_'+ haloType+'B'+beamn+coll+'.root'
            trname = 'normtree' + coll

            branchname = coll.replace('.','QQQ')

            print 'Opening.....', rfname
            rf = TFile.Open(rfname)
            nt = rf.Get(trname)
            norm = -9999
            for entry in nt: 
                norm = getattr(entry,branchname)
                print 'norm', norm

            histname = 'cold_loss' + coll
            hist = rf.Get(histname)

            # max loss in cold magnets, get also poisson error
            maxLoss = hist.GetMaximum()
            maxLosses += [(fraction*maxLoss/norm,fraction*math.sqrt(maxLoss)/norm)]

            s_startQ8, s_stopQ8   = 6940., 7020.
            s_startQ10, s_stopQ10 = 7050., 7110.

            if coll.count('B1'):
                s_startQ8, s_stopQ8   = 20270., 20340.
                s_startQ10, s_stopQ10 = 20370., 20435.

            bin_startQ8, bin_stopQ8   = hist.FindBin(s_startQ8), hist.FindBin(s_stopQ8)
            bin_startQ10, bin_stopQ10 = hist.FindBin(s_startQ10), hist.FindBin(s_stopQ10)

            lQ8, lErrQ8, lQ10, lErrQ10 = 0.,0.,0.,0.

            for bin in range(bin_startQ8, bin_stopQ8):   lQ8 += hist.GetBinContent(bin)
            for bin in range(bin_startQ10, bin_stopQ10): lQ10 += hist.GetBinContent(bin)

            nbinsQ8, nbinsQ10 = bin_stopQ8-bin_startQ8, bin_stopQ10-bin_startQ10 
            vQ8, vQ10 = lQ8/nbinsQ8, lQ10/nbinsQ10

            lossesQ8 += [( vQ8/norm,math.sqrt(lQ8)/nbinsQ8/norm )]
            lossesQ10 += [( vQ10/norm,math.sqrt(lQ10)/nbinsQ10/norm )]



        hname, nbins, xmin, xmax = 'hmaxLoss', len(colls), 0, len(colls)
        hist_maxLoss = TH1F(hname, hname, nbins, xmin, xmax)
        hist_maxLoss.GetYaxis().SetTitle('#eta [m^{-1}]')
        hist_maxLoss.SetMarkerStyle(20)
        hist_maxLoss.SetMarkerColor(kBlue)
        hist_maxLoss.SetLineColor(kBlue)

        hist_Q8 = hist_maxLoss.Clone('lossesQ8')
        hist_Q8.SetMarkerStyle(22)
        hist_Q8.SetMarkerColor(kPink-9)
        hist_Q8.SetLineColor(kPink-9)

        hist_Q10 = hist_maxLoss.Clone('lossesQ10')
        hist_Q10.SetMarkerStyle(23)
        hist_Q10.SetMarkerColor(kGreen-3)
        hist_Q10.SetLineColor(kGreen-3)

        for i in range(len(colls)):
            hist_maxLoss.SetBinContent(i+1, maxLosses[i][0])
            hist_maxLoss.SetBinError(i+1, maxLosses[i][1])
            hist_maxLoss.GetXaxis().SetBinLabel(i+1, colls[i][1].lstrip('_'))

            hist_Q8.SetBinContent(i+1, lossesQ8[i][0])
            hist_Q8.SetBinError(i+1,   lossesQ8[i][1])
            hist_Q10.SetBinContent(i+1,lossesQ10[i][0])
            hist_Q10.SetBinError(i+1,  lossesQ10[i][1])

        cv = TCanvas( 'cv' , 'cv' , 2000, 700)
        gPad.SetGridx(1)
        gPad.SetGridy(1)

        YurMin, YurMax = 1.5e-6,5e-6
        hist_maxLoss.GetYaxis().SetRangeUser(YurMin,YurMax)
        hist_maxLoss.GetXaxis().SetNdivisions(len(colls))
        hist_maxLoss.Draw('pe')
        hist_Q8.Draw('pesame')
        hist_Q10.Draw('pesame')

        x1, y1, x2, y2 = 0.2, 0.7, 0.4, 0.9
        mlegend = TLegend( x1, y1, x2, y2)
        mlegend.SetFillColor(0)
        mlegend.SetFillStyle(0)
        mlegend.SetLineColor(0)
        mlegend.SetTextSize(0.035)
        mlegend.SetShadowColor(0)
        mlegend.SetBorderSize(0)

        mlegend.AddEntry(hist_maxLoss, '10% of max cold loss', 'lpe')
        mlegend.AddEntry(hist_Q8, 'loss in Q8', 'lpe')
        mlegend.AddEntry(hist_Q10, 'loss in Q10', 'lpe')
        mlegend.Draw()

        lv = TLine()
        lv.SetLineStyle(1)
        lv.SetLineWidth(2)
        lv.SetLineColor(1)
        xval = len(collsHB2)
        lv.DrawLine(xval,YurMin,xval,YurMax)

        lab = mylabel(42)
        lab.DrawLatex(.48, y1+0.15, 'hHalo')
        if beamn == '1':
            lab.DrawLatex(.59, y1+0.15, 'vHalo')

        resulthist = 'complossesB'+beamn
        pname  = wwwpath
        pname += subfolder + resulthist+'.png'

        print('Saving file as' + pname ) 
        cv.Print(pname)

