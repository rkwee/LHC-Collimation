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
    doWriteRFile = 1
    plotLossMaps = 0
    doAvLoss     = 0

    tct    = 'ver-B1'

    tcts   = ['HL_TCT_vHaloB1_TCT5OFF', 
              'HL_TCT_hHaloB1_TCT5OFF',
              ]
    tcts = ['TCT_4TeV_B2vHalo', 'TCT_4TeV_B2hHalo']

    tct = tcts[1]

    # is tcs again
    tcts = [
'hHalo/7TeVPostLS1_TCSG.6R7.B1',
'hHalo/7TeVPostLS1_TCSG.A4L7.B1',
'hHalo/7TeVPostLS1_TCSG.A4R7.B1',
'hHalo/7TeVPostLS1_TCSG.A5L7.B1',
'hHalo/7TeVPostLS1_TCSG.A6L7.B1',
'hHalo/7TeVPostLS1_TCSG.B4L7.B1',
'hHalo/7TeVPostLS1_TCSG.B5L7.B1',
'hHalo/7TeVPostLS1_TCSG.B5R7.B1',
'hHalo/7TeVPostLS1_TCSG.D4L7.B1',
'hHalo/7TeVPostLS1_TCSG.D5R7.B1',
'hHalo/7TeVPostLS1_TCSG.E5R7.B1',
'hHalo/7TeVPostLS1_nominal_B1',
'hHalo/7TeVPostLS1_sel1.B1',
        ]

    rfname = "tct" + tag + ".root"
    trname = 'normtree'

    if doWriteRFile:
        print "Writing " + '.'* 25 +' ' + rfname
        
        # create a root file
        rf = TFile(rfname, 'recreate')
        nt = TTree(trname,"norm for each tct")        
    
        for tct in tcts:

            tag    = '_' + tct
            tA = time.time()
            
            # subfolder in wwwpath for result plots
            subfolder = 'scan/'
            
            # roderiks results
            thispath  = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/ats-HL_LHC_1.0/nominal_settings/' + tct + '/'

            # my results (thight coll settings)
            thispath  = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/' + tct

            # my results (thight coll settings)
            thispath  = '/Users/rkwee/Documents/RHUL/work/HL-LHC/runs/scan/' + tct

            if not thispath.endswith('/'): thispath += '/'

            # use for normalisation the sum of nabs (col 4)
            fileName  = thispath + 'coll_summary' + tag + '.dat'
            colNumber = 4
            beam     = 'b2'            
            beamn    = '2'

            if tag.count("B1"):
                beam = 'b1'
                beamn = '1'
            f3 = helpers.source_dir + 'HL_TCT_7TeV/' + beam +'/CollPositions.'+beam+'.dat'
            f3 = helpers.source_dir + 'TCT_4TeV_60cm/'+beam+'/CollPositions.'+beam+'.dat'
            f3 = helpers.source_dir + 'sourcedirs/NewColl7TeVB'+beamn+'/CollPositions.'+beam+'.dat'

            t0 = time.time()
            h_tot_loss, h_cold, h_warm = lossmap.lossmap(beam,thispath,tag, f3) 
            t1 = time.time()
            print(str(t1-t0)+" for returning lossmap histograms of " + tct )
            h_tot_loss.Write()
            h_cold.Write()
            h_warm.Write()            

            # -- write the for each norm value a branch into ttree
            t0 = time.time()

            # setting branch name 
            branchname = 'norm' + tag
            branchname = tct.replace('.','QQQ')

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

        tB = time.time()

        print(str(tB-tA)+" for producing " + rfname)
        # ------------------------------------------------

    if plotLossMaps:
        print("Plotting lossmaps from " + "."*20 + ' '+ rfname)

        doZooms = [0,1]
        rel = ''
        for doZoom in doZooms: 

            rf = TFile.Open(rfname)
            nt = rf.Get(trname)

            beam       = 'b1'
            branchname = tct.replace('.','QQQ')

            norm = addCol(fileName, colNumber-1)

            if debug: print "('"+tct+"', " + str(norm) + "),"

            cv = TCanvas( 'cv' + tag + str(doZoom), 'cv' + tag + str(doZoom), 1200, 700)

            YurMin, YurMax = 3.2e-9, 3.

            hname = 'coll_loss' +tag

            if debug: print("Get histograms for tct " + tct + ", starting with " + hname)

            coll_loss = rf.Get(hname)
            cold_loss = rf.Get('cold_loss' +tag)
            warm_loss = rf.Get('warm_loss' +tag)

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
            lab.DrawLatex(x1, y1-0.1, tct)

            gPad.RedrawAxis()
            gPad.SetGrid(0,1)
            gPad.SetLogy(1)

            pname  = wwwpath
            pname += subfolder +'/'+hname+rel+'.png'

            print('Saving file as' + pname ) 
            cv.Print(pname)

    # ------------------------------------------------
    tC = time.time()
    print(str(tC-tB)+" for plotting lossmaps.")
