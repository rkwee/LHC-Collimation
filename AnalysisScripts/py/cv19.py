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
# Oct 2014, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os, time, math
from ROOT import *
import lossmap, helpers, array
from helpers import wwwpath, file_len, length_LHC, mylabel, addCol, gitpath
from array import array
## -------------------------------------------------------------------------------

def cv19():

    debug        = 1
    doWriteRFile = 0
    plotLossMaps = 1

    # subfolder in wwwpath for result plots
    subfolder = './' 
    
    colls = [

        ('hHalo', 'TCT_4TeV_B1hHalo'),
        ('vHalo', 'TCT_4TeV_B1vHalo'),
        ('hHalo', 'TCT_4TeV_B2hHalo'),
        ('vHalo', 'TCT_4TeV_B2vHalo'),

        ]

    for haloType,coll in colls:

        if not coll.startswith('_'): coll = '_'+coll

        beam   = 'b2'            
        beamn  = '2'        
        if coll.count('B1'):
            beam  = 'b1'
            beamn = '1'

        # my results 
        thispath  = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/TCT/4TeV/TCT_4TeV_B'+beamn+haloType+'/'

        rfname = thispath + 'lossmap'+ coll +'.root'
        trname = 'normtree' + coll
        colNumber = 4
            
        f3 = gitpath + 'SixTrackConfig/4TeV/TCThaloStudies/'+beam+'/CollPositions.'+beam+'.dat'

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
                warm_loss.SetLineColor(kRed)
                cold_loss.SetLineColor(kBlue)
                coll_loss.SetFillColor(kBlack)
                warm_loss.SetFillColor(kRed)
                cold_loss.SetFillColor(kBlue)

                coll_loss.Scale(1.0/norm)
                cold_loss.Scale(1.0/norm)
                warm_loss.Scale(1.0/norm)

                if beam.count('1') and not doZoom:
                    x1, y1, x2, y2 = 0.18, 0.78, 0.42, 0.9
                else:
                    x1, y1, x2, y2 = 0.6, 0.78, 0.91, 0.9

                XurMin, XurMax = 0., length_LHC
                if doZoom:
                    rel = '_zoom'
                    XurMin, XurMax = 6.3e3, 8.0e3 
                    if beam.count('1') : XurMin, XurMax = 19.7e3, 20.6e3
                coll_loss.Draw('hist')
                warm_loss.Draw('samehist')
                cold_loss.Draw('samehist')

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
                warm_loss.Draw('same')
                cold_loss.Draw('same')

                coll_loss.GetXaxis().SetRangeUser(XurMin, XurMax)
                coll_loss.GetYaxis().SetRangeUser(YurMin, YurMax)

                thelegend = TLegend( x1, y1, x2, y2)
                thelegend.SetFillColor(0)
                thelegend.SetLineColor(0)
                thelegend.SetTextSize(0.035)
                thelegend.SetShadowColor(10)
                thelegend.AddEntry(coll_loss,'losses on collimators', 'L')
                thelegend.AddEntry(warm_loss,'warm losses', 'L')
                thelegend.AddEntry(cold_loss,'cold losses', 'L')
                thelegend.Draw()

                lab = mylabel(60)
                lab.DrawLatex(x1, y1-0.1, coll.lstrip('_'))

                if not rel and beam.count('1'):

                    lab = mylabel(42)
                    lab.SetTextColor(kGreen+1)
                    lab.SetTextSize(0.04)
                    lab.DrawLatex(0.15, 0.43, 'IR1')
                    lab.DrawLatex(0.88, 0.43, 'IR1')
                    lab.DrawLatex(0.23, 0.55, 'IR2')
                    lab.DrawLatex(0.33, 0.58, 'IR3')
                    lab.DrawLatex(0.51, 0.47, 'IR5')
                    lab.DrawLatex(0.61, 0.54, 'IR6')
                    lab.DrawLatex(0.70, 0.92, 'IR7')
                    lab.DrawLatex(0.79, 0.55, 'IR8')
                
                elif not rel and beam.count('2'):

                    lab = mylabel(42)
                    lab.SetTextColor(kGreen+1)
                    lab.SetTextSize(0.04)
                    lab.DrawLatex(0.15, 0.43, 'IR1')
                    lab.DrawLatex(0.88, 0.47, 'IR1')
                    lab.DrawLatex(0.23, 0.30, 'IR8')
                    lab.DrawLatex(0.33, 0.92, 'IR7')
                    lab.DrawLatex(0.43, 0.56, 'IR6')
                    lab.DrawLatex(0.51, 0.48, 'IR5')
                    lab.DrawLatex(0.61, 0.34, 'IR4')
                    lab.DrawLatex(0.70, 0.60, 'IR3')
                    lab.DrawLatex(0.79, 0.30, 'IR2')

                gPad.RedrawAxis()
                gPad.SetGrid(0,1)
                gPad.SetLogy(1)

                pname  = wwwpath
                subfolder = 'TCT/4TeV/B'+beamn+'/'
                pname += subfolder + hname + rel + '.png'

                print('Saving file as' + pname ) 
                cv.Print(pname)