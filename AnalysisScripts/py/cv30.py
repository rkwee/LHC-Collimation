#!/usr/bin/python
#
# from cv24
#     
# plot lossmaps for different HL optics
# 
#
#
# Mar 2015, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os, time, math
from ROOT import *
import lossmap, helpers, array
from helpers import wwwpath, file_len, length_LHC, mylabel, addCol, gitpath, workpath, projectpath
from array import array
## -------------------------------------------------------------------------------

def cv30():

    debug        = 1
    doWriteRFile = 1
    plotLossMaps = 1

    doIR1 = 0
    
    subfolder = 'TCT/HL/nominalColl/2015/lossmaps/'
    subfolder = 'TCT/6.5TeV/'
#    subfolder = 'TCT/4TeV/'

    colls = [

        ('6.5TeV_hHaloB1_h5'),
        ('6.5TeV_vHaloB1_h5'),
        ('6.5TeV_hHaloB2_h5'),
        ('6.5TeV_vHaloB2_h5'),
        #('H5_HL_TCT5LOUT_relaxColl_hHaloB2_roundthin'),
        #('H5_HL_TCT5LOUT_relaxColl_vHaloB2_roundthin'),
        # ('H5_HL_TCT5IN_relaxColl_hHaloB2_roundthin'),
        # ('H5_HL_TCT5IN_relaxColl_vHaloB2_roundthin'),
        # ('H5_HL_TCT5LOUT_relaxColl_hHaloB1_flatthin'),
        # ('H5_HL_TCT5LOUT_relaxColl_vHaloB1_flatthin'),
        # ('H5_HL_TCT5LOUT_relaxColl_hHaloB1_roundthin'),
        # ('H5_HL_TCT5LOUT_relaxColl_vHaloB1_roundthin'),
        # ('H5_HL_TCT5IN_relaxColl_vHaloB1_roundthin'),
        # ('H5_HL_TCT5IN_relaxColl_vHaloB1_sroundthin'),
        # ('H5_HL_TCT5IN_relaxColl_vHaloB1_flatthin'),
        # ('H5_HL_TCT5IN_relaxColl_vHaloB1_sflatthin'),
        # ('H5_HL_TCT5IN_relaxColl_hHaloB1_roundthin'),
        # ('H5_HL_TCT5IN_relaxColl_hHaloB1_sroundthin'),
        # ('H5_HL_TCT5IN_relaxColl_hHaloB1_flatthin'),
        # ('H5_HL_TCT5IN_relaxColl_hHaloB1_sflatthin'),

        # ('H5_HL_nomSett_hHalo_b1'),
        # ('H5_HL_nomSett_vHalo_b1'),

        ]


    for coll in colls:

        if not coll.startswith('_'): 
            tag  = coll
            coll = '_'+coll

        thiscase = coll

        beam   = 'b2'            
        beamn  = '2'        
        beamColor = kRed
        if coll.count('B1') or coll.count('b1'):
            beam  = 'b1'
            beamn = '1'
            beamColor = kBlue

        # my results 
        thispath  = workpath + 'runs/' + tag +'/'
        #thispath  = projectpath + 'HL1.0/' + tag + '/'
        if doIR1: rfname = thispath + 'lossmap'+ coll +'_IR1.root'
        else:  rfname = thispath + 'lossmap'+ coll +'.root'

        trname = 'normtree' + coll
        colNumber = 4
            
        if coll.count("_HL"):
            f3 = gitpath + 'SixTrackConfig/7TeV/hilumiLHC/TCThaloStudies_relaxedCollSettings/'+beam+'/CollPositions.'+beam+'.dat'
        elif coll.count("6.5TeV"):
            f3 = gitpath + 'SixTrackConfig/6.5TeV/MED800/B'+beamn+'/CollPositions.'+beam+'.dat'
        else:
            print "No CollPosition file defined. Exitiing.... "
            sys.exit()

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

            if doIR1:  shiftVal = 10e3
            else: shiftVal = length_LHC

            h_tot_loss, h_cold, h_warm = lossmap.lossmap(beam,thispath,coll, f3, shiftVal) 
            t1 = time.time()
            print(str(t1-t0)+' for returning lossmap histograms of ' + coll )

            if debug:
                if h_tot_loss.GetEntries() < 1.:
                    print 'Empty collimator histogram!'
                    sys.exit()

            if debug:
                if h_cold.GetEntries() < 1.:
                    print 'Empty histogram! Binary characters in LPI file?'

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

            doZooms = ['fullring','IR7', 'IR5']
            if rfname.count("IR1"): doZooms = ['IR1']

            for doZoom in doZooms: 

                rf = TFile.Open(rfname)            
                nt = rf.Get(trname)
                branchname = coll.replace('.','QQQ')

                norm = -9999
                for entry in nt: 
                    norm = getattr(entry,branchname)
                    print 'norm', norm

                cv = TCanvas( 'cv' + coll + str(doZoom), 'cv' + coll + str(doZoom), 1200, 700)
                # x1,y1,x2,y2 = 0.2, 0.7,0.5,0.7
                # ar2 = TArrow(x1,y1,x2,y2,0.02,"-|>")
                # ar2.SetLineWidth(2)
                # ar2.SetLineColor(beamColor)
                # ar2.SetFillColor(beamColor)
                # ar2.Draw()
                # lBeam = mylabel(42)
                # lBeam.SetTextColor(beamColor)
                # lBeam.DrawLatex(0.3, 0.7, "B" + beamn)

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

                if doZoom == 'IR1': 
                    xmin  = coll_loss.GetXaxis().GetBinLowEdge(1)
                    xlab  = [ str(length_LHC+xmin + i*10) for i in range(int(-xmin)/10) ]
                    xlab += [ str(i*10) for i in range(int(length_LHC+xmin)/10) ]

                    # for i,xl in enumerate(xlab): coll_loss.GetXaxis().SetBinLabel(i+1, xl)
                # legend
                if beam.count('1') and doZoom == 'fullring':
                    x1, y1, x2, y2 = 0.18, 0.78, 0.42, 0.9
                elif doZoom == 'IR7' :
                    x1, y1, x2, y2 = 0.6, 0.78, 0.91, 0.9
                else:
                    x1, y1, x2, y2 = 0.6, 0.78, 0.91, 0.9

                # x-axis
                XurMin, XurMax = 0., length_LHC
                
                if beam.count('2'):
                    if   doZoom == 'IR5':  XurMin, XurMax = 13.e3,14e3
                    elif doZoom == 'IR7':  XurMin, XurMax = 6.3e3,  8.0e3 
                    elif doZoom == 'IR1':  XurMin, XurMax = -2.5e3,  2.0e3 
                else:
                    if   doZoom == 'IR5':  XurMin, XurMax = 13.e3,14e3
                    elif doZoom == 'IR7':  XurMin, XurMax = 19.7e3, 20.6e3
                    elif doZoom == 'IR1':  XurMin, XurMax = -2.5e3,  2.0e3 

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

                case = coll.split('_60')[0].replace('_',' ')
                lab = mylabel(60)
                lab.SetTextSize(0.035)
                lab.DrawLatex(0.28, y2+0.055, case)

                if doZoom == 'fullring' and beam.count('1'):

                    lab = mylabel(42)
                    lab.SetTextColor(kGreen+1)
                    lab.SetTextSize(0.04)
                    lab.DrawLatex(0.15, 0.62, 'IR1')
                    lab.DrawLatex(0.88, 0.62, 'IR1')
                    lab.DrawLatex(0.23, 0.62, 'IR2')
                    lab.DrawLatex(0.33, 0.62, 'IR3')
                    lab.DrawLatex(0.51, 0.62, 'IR5')
                    lab.DrawLatex(0.61, 0.62, 'IR6')
                    lab.DrawLatex(0.70, 0.92, 'IR7')
                    lab.DrawLatex(0.79, 0.62, 'IR8')
                
                elif doZoom == 'fullring' and beam.count('2'):

                    lab = mylabel(42)
                    lab.SetTextColor(kGreen+1)
                    lab.SetTextSize(0.04)
                    lab.DrawLatex(0.15, 0.6, 'IR1')
                    lab.DrawLatex(0.88, 0.6, 'IR1')
                    lab.DrawLatex(0.23, 0.6, 'IR8')
                    lab.DrawLatex(0.33, 0.92, 'IR7')
                    lab.DrawLatex(0.43, 0.6, 'IR6')
                    lab.DrawLatex(0.52, 0.6, 'IR5')
                    lab.DrawLatex(0.61, 0.6, 'IR4')
                    lab.DrawLatex(0.70, 0.6, 'IR3')
                    lab.DrawLatex(0.79, 0.6, 'IR2')

                elif doZoom.count("IR"):

                    lab = mylabel(42)
                    lab.SetTextColor(kGreen+1)
                    lab.SetTextSize(0.04)
                    lab.DrawLatex(0.5, 0.83, doZoom)

                gPad.RedrawAxis()
                gPad.SetGrid(0,1)
                gPad.SetLogy(1)

                pname  = wwwpath
                pname += subfolder + hname + '_' + doZoom + '.png'

                print('Saving file as' + pname ) 
                cv.Print(pname)
