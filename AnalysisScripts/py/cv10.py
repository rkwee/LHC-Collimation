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
    doAvLoss     = 1

    coll    = 'ver-B1'

    colls   = ['HL_TCT_vHaloB1_TCT5OFF', 
              'HL_TCT_hHaloB1_TCT5OFF',
              ]
    colls = ['TCT_4TeV_B2vHalo', 'TCT_4TeV_B2hHalo']

    coll = colls[1]

    haloType = 'hHalo'
    # is tcs again
    colls = [
        '_sel1.B1',
        '_nominal_B1',
        '_TCSG.A6L7.B1',
        '_TCSG.B5L7.B1',
        '_TCSG.A5L7.B1',
        '_TCSG.D4L7.B1',
        '_TCSG.B4L7.B1',
        '_TCSG.A4L7.B1',
        '_TCSG.A4R7.B1',
        '_TCSG.B5R7.B1',
        '_TCSG.D5R7.B1',
        '_TCSG.E5R7.B1',
        '_TCSG.6R7.B1',
        ]
            
    # subfolder in wwwpath for result plots
    subfolder = 'scan/'
            
    # my results (thight coll settings)
    thispath  = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/hHaloB1/' 

    for coll in colls:

        rfname = "hHaloB1/scan_lossmaps_hHaloB1"+coll+".root"
        trname = 'normtree' + coll
        colNumber = 4

        beam   = 'b2'            
        beamn  = '2'        
        if coll.count("B1"):
            beam  = 'b1'
            beamn = '1'
            
        f3 = helpers.source_dir + 'HL_TCT_7TeV/' + beam +'/CollPositions.'+beam+'.dat'
        f3 = helpers.source_dir + 'TCT_4TeV_60cm/'+beam+'/CollPositions.'+beam+'.dat'
        f3 = helpers.source_dir + 'NewColl7TeVB'+beamn+'/CollPositions.'+beam+'.dat'

        # use for normalisation the sum of nabs (col 4)
        fileName  = thispath + 'coll_summary' + coll + '.dat'

        # ------------------------------------------------

        if doWriteRFile:

            print "Writing " + '.'* 25 +' ' + rfname        

            # create a root file
            rf = TFile(rfname, 'recreate')
    
            nt  = TTree(trname,"norm for each coll") 

            if not os.path.exists(fileName): 
                print fileName,' does not exist?!'
                continue

            t0 = time.time()
            h_tot_loss, h_cold, h_warm = lossmap.lossmap(beam,thispath,coll, f3) 
            t1 = time.time()
            print(str(t1-t0)+" for returning lossmap histograms of " + coll )
            h_tot_loss.Write()
            h_cold.Write()
            h_warm.Write()            

            # -- write the for each norm value a branch into ttree
            t0 = time.time()

            # setting branch name 
            branchname = 'norm' + coll
            branchname = coll.replace('.','QQQ')

            if debug and 0: print globals()

            # use globals dict to convert strings to variable names
            globals()[branchname] = array('i',[0])

            # create branch
            nt.Branch(branchname, globals()[branchname], branchname+'/i')

            # get value
            maxval = int(addCol(fileName, colNumber-1))

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

            print("Plotting lossmaps from " + "."*20 + ' '+ rfname)
            trname = 'normtree' + coll

            doZooms = [0,1]
            rel = ''
            for doZoom in doZooms: 

                rf = TFile.Open(rfname)
                nt = rf.Get(trname)

                beam       = 'b1'
                branchname = coll.replace('.','QQQ')

                norm = addCol(fileName, colNumber-1)

                if debug: print "('"+ coll + "', " + str(norm) + "),"

                cv = TCanvas( 'cv' + coll + str(doZoom), 'cv' + coll + str(doZoom), 1200, 700)

                YurMin, YurMax = 3.2e-9, 3.

                hname = 'coll_loss' +coll

                if debug: print("Get histograms for coll " + coll + ", starting with " + hname)

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
                thelegend.AddEntry(coll_loss,'losses on collimators', "L")
                thelegend.AddEntry(cold_loss,'cold losses', "L")
                thelegend.AddEntry(warm_loss,'warm losses', "L")
                thelegend.Draw()

                lab = mylabel(60)
                lab.DrawLatex(x1, y1-0.1, coll.lstrip('_'))
                lab = mylabel(42)
                lab.DrawLatex(.5, y1+0.08, haloType)

                gPad.RedrawAxis()
                gPad.SetGrid(0,1)
                gPad.SetLogy(1)

                pname  = wwwpath
                pname += subfolder +'/'+hname+rel+'.png'

                print('Saving file as' + pname ) 
                cv.Print(pname)

    # ------------------------------------------------
    
    if doAvLoss:

        maxLosses, lossesQ8, lossesQ10 = [],[],[]

        for coll in colls:

            rfname = "hHaloB1/scan_lossmaps_hHaloB1"+coll+".root"
            trname = 'normtree' + coll

            print 'Opening.....', rfname
            rf = TFile.Open(rfname)
            nt = rf.Get(trname)

            beam       = 'b1'
            branchname = coll.replace('.','QQQ')

            # too stupid to read the tree data
            norm = addCol(fileName, colNumber-1)

            histname = 'cold_loss' + coll
            hist = rf.Get(histname)

            # max loss in cold magnets
            maxLoss = hist.GetMaximum()
            maxLossErr = hist.GetBinError(hist.GetMaximumBin())
            maxLosses += [(maxLoss, maxLossErr)]

            s_startQ8, s_stopQ8 = 0,0


        hname, nbins, xmin, xmax = 'hmaxLoss', len(colls), -0.5, len(colls)+0.5
        hist_maxLoss = TH1F(hname, hname, nbins, xmin, xmax)
        hist_maxLoss.GetYaxis().SetTitle('#eta [m^{-1}]')
        hist_maxLoss.SetMarkerStyle(22)
        hist_maxLoss.SetMarkerColor(kBlue)
        hist_maxLoss.SetLineColor(kBlue)

        for i in range(len(colls)):
            hist_maxLoss.SetBinContent(i+1, maxLosses[i][1])
            hist_maxLoss.SetBinError(i+1, maxLosses[i][0])
            hist_maxLoss.GetXaxis().SetBinLabel(i+1, colls[i].lstrip('_'))

        coll = 'nothingSpecial'
        cv = TCanvas( 'cv' + coll, 'cv' + coll, 1200, 700)
        
        hist_maxLoss.Draw('pe')
        resulthist = 'complossTEST'
        pname  = wwwpath
        pname += subfolder + resulthist+'.png'

        print('Saving file as' + pname ) 
        cv.Print(pname)

