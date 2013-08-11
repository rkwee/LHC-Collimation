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
# if doAvLoss = 1
#    uses rootfile 
#    plots losses at Q8 and Q10 
# 
#
# May 2013, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os, time, math, gzip
from ROOT import *
import lossmap, helpers, array
from helpers import wwwpath, file_len, length_LHC, mylabel
from array import array
## -------------------------------------------------------------------------------

# already merged the new files??

# -- order of appearance according s-coor
#   ('nominal_B1    # 1e4),       
# ('TCSG.A6L7.B1    # 19832.68),  
# ('TCSG.B15L7.B1   # 19891.91),  
# ('TCSG.A5L7.B1    # 19895.91),  
# ('TCSG.D4L7.B1    # 19917.24),  
# ('TCSG.B14L7.B1   # 19987.16),  
# ('TCSG.A4L7.B1    # 19991.16),  
# ('TCSG.A4R7.B1    # 19995.16),  
# ('TCSG.B15R7.B1   # 20086.42),  
# ('TCSG.D5R7.B1    # 20102.42),  
# ('TCSG.E5R7.B1    # 20106.42),  
# ('TCSG.6R7.B1     # 20141.02),  
                                   
# ('TCSG.A6R7.B2',  # 6503.24),
# ('TCSG.B5R7.B2',  # 6562.46),
# ('TCSG.A5R7.B2',  # 6566.46),
# ('TCSG.D4R7.B2',  # 6587.79),
# ('TCSG.B4R7.B2',  # 6653.72),
# ('TCSG.A4R7.B2',  # 6657.72),
# ('TCSG.A4L7.B2',  # 6673.72),
# ('TCSG.B5L7.B2',  # 6756.98),
# ('TCSG.D5L7.B2',  # 6772.98),
# ('TCSG.E5L7.B2',  # 6776.98),
# ('TCSG.6L7.B2',   # 6811.58),

TCS = [

'nominal_B1', 
'TCSG.A6L7.B1', 
'TCSG.B5L7.B1', 
'TCSG.A5L7.B1', 
'TCSG.D4L7.B1', 
'TCSG.B4L7.B1', 
'TCSG.A4L7.B1', 
'TCSG.A4R7.B1', 
'TCSG.B5R7.B1', 
'TCSG.D5R7.B1', 
'TCSG.E5R7.B1', 
'TCSG.6R7.B1', 
'nominal_B2', 
'TCSG.A6R7.B2', 
'TCSG.B5R7.B2', 
'TCSG.A5R7.B2', 
'TCSG.D4R7.B2', 
'TCSG.B4R7.B2', 
'TCSG.A4R7.B2', 
'TCSG.A4L7.B2', 
'TCSG.B5L7.B2', 
'TCSG.D5L7.B2', 
'TCSG.E5L7.B2', 
'TCSG.6L7.B2', 
#     'testB1',
]               

def cv03():

    debug        = 1
    doWriteRFile = 0
    plotLossMaps = 1
    doAvLoss     = 0

    rfname = "7TeVPostLS1_scan.root"
    #    rfname = "7TeVPostLS1_DEBUG_scan.root"
    trname = 'normtree'
    tA = time.time()

    if doWriteRFile:
        print "Writing " + rfname

        # create a root file
        rf = TFile(rfname, 'recreate')
        nt = TTree(trname,"norm for each tcs")        

        for tcs in TCS:
            
            tag      = '_' + tcs
            thispath = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/7TeVPostLS1' + tag + '/'
            beam     = 'b2'
            if tag.count("B1"):
                beam = 'b1'

            t0 = time.time()
            f4 = thispath + 'FirstImpacts'+tag+'.dat'
            h_tot_loss, h_cold, h_warm = lossmap.lossmap(beam,thispath,tag) 
            t1 = time.time()
            print(str(t1-t0)+" for returning lossmap histograms of " + tcs )
            h_tot_loss.Write()
            h_cold.Write()
            h_warm.Write()            

            # -- write the for each norm value a branch into ttree
            t0 = time.time()

            # setting branch name 
            branchname = 'norm' + tag

            # use globals dict to convert strings to variable names
            globals()[branchname] = array('i',[0])

            # create branch
            nt.Branch(branchname, globals()[branchname], branchname+'/i')

            # get value
            maxval = int(open(f4).read())
            if debug: print "('"+tcs+"', " + str(maxval) + "),"

            # assigning value
            globals()[branchname][0] = maxval

            # write to tree
            nt.Fill()

            t1 = time.time()
            print(str(t1-t0)+" for checking file_len of " + f4 + " =  " + str(maxval))
        
        nt.Write()
        rf.Close()

    tB = time.time()

    print(str(tB-tA)+" for producing " + rfname)
    # ------------------------------------------------

    if plotLossMaps:
        print("Plotting lossmaps from " + "."*20 + rfname)

        doZooms = [0,1]

        for doZoom in doZooms: 
           
            rf = TFile.Open(rfname)
            nt = rf.Get(trname)

            for tcs in TCS:

                tag        = '_' + tcs
                rel        = tag 
                thispath   = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/7TeVPostLS1' + tag + '/'
                beam       = 'b2'
                branchname = 'norm'+tag

                nt.SetBranchAddress(branchname, globals()[branchname])
                nt.GetEntry(0)
                norm       = globals()[branchname][0]
                if debug: print "('"+tcs+"', " + str(norm) + "),"

                if tag.count("B1"):
                    beam = 'b1'

                cv = TCanvas( 'cv' + tag + str(doZoom), 'cv' + tag + str(doZoom), 1200, 700)

                YurMin, YurMax = 3.2e-9, 3.

                if debug: print("Get histograms for tcs " + tcs )

                coll_loss = rf.Get('coll_loss' +tag)
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

                XurMin, XurMax = 0., length_LHC
                if doZoom and beam.count('1'):
                    XurMin, XurMax = 19.7e3, 20.6e3
                    rel = tag + '_zoom'
                if doZoom and beam.count("2"):
                    XurMin, XurMax = 6.4e3, 7.3e3
                    rel = tag + '_zoom'

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
                lab.DrawLatex(x1, y1-0.1, tcs)

                gPad.RedrawAxis()
                gPad.SetGrid(0,1)
                gPad.SetLogy(1)

                pname  = wwwpath
                pname += 'scan/losses'+rel+'.png'

                print('Saving file as' + pname ) 
                cv.Print(pname)

    # ------------------------------------------------
    tC = time.time()
    print(str(tC-tB)+" for plotting lossmaps.")

    if doAvLoss:
        print "Calculating losses at Q8 and Q10 for B1 and QA and QB for B2"

        print "Opening ", rfname
        rf = TFile.Open(rfname)
        max_cold_losses, Q8_losses, Q10_losses = [],[],[]

        # for better visibility 
        scaleFactor = 10.

        for tcs in TCS:

            tag  = '_'+ tcs
            cold_loss = rf.Get('cold_loss' + tag)
            cold_loss.Scale(1./norm)
            print "-"*20, tcs, "-"*20

            if tag.count("B1"):
                p1_cold_loss_start, p1_cold_loss_end  = 20290., 20340.
                p2_cold_loss_start, p2_cold_loss_end  = 20380., 20430.
            else:
                p1_cold_loss_start, p1_cold_loss_end  = 6950., 7010.
                p2_cold_loss_start, p2_cold_loss_end  = 7050., 7110.

            #norm = 1.
            p1_bin_start = cold_loss.FindBin(p1_cold_loss_start)
            p1_bin_end   = cold_loss.FindBin(p1_cold_loss_end)
            p1_cold_loss = cold_loss.Integral(p1_bin_start,p1_bin_end)
            p1_nbins     = p1_bin_end - p1_bin_start

            p2_bin_start = cold_loss.FindBin(p2_cold_loss_start)
            p2_bin_end   = cold_loss.FindBin(p2_cold_loss_end)
            p2_cold_loss = cold_loss.Integral(p2_bin_start,p2_bin_end)
            p2_nbins     = p2_bin_end - p2_bin_start

            # statistical uncertainty
            p1_stat, p2_stat = 0.,0.

            if debug:
                print('Q8: averaging from bin ' + str(p1_bin_start) + ' to bin ' + str(p1_bin_end))

            Q8_losses  += [(tcs, p1_cold_loss/p1_nbins, math.sqrt(p1_cold_loss/norm)/p1_nbins)]
            Q10_losses += [(tcs, p2_cold_loss/p2_nbins, math.sqrt(p2_cold_loss/norm)/p2_nbins)]

            max_cold_loss = cold_loss.GetMaximum()/scaleFactor
            max_cold_losses += [( max_cold_loss, math.sqrt(max_cold_loss/norm) )]
            print "Maximum loss in bin", cold_loss.GetMaximumBin(), \
                " from ", cold_loss.GetBinLowEdge(cold_loss.GetMaximumBin()), " to ", cold_loss.GetBinLowEdge(cold_loss.GetMaximumBin() + 1)

        # plot the benchmark plots
        bmPlot(Q8_losses,Q10_losses,max_cold_losses,'complossesErr_' + rfname.split('.')[0])


def bmPlot(Q8_losses,Q10_losses,max_cold_losses,hname):

    nbins = len(Q8_losses)

    cv = TCanvas( 'cv' + hname, 'cv' + hname, 2000, 800)
    cv.SetLeftMargin(0.15)
    cv.SetRightMargin(0.15)
    cv.SetTopMargin(0.15)

    hist1 = TH1F(hname, hname, nbins, 1, nbins+1)
    hist1.SetMarkerStyle(22)
    hist1.SetMarkerColor(kMagenta-3)
    hist1.SetLineColor(kMagenta-3)
    hist1.GetYaxis().SetTitle('Cleaning Inefficiency #eta')

    hist2 = TH1F(hname+'d', hname+'d', nbins, 1, nbins+1)
    hist2.SetMarkerStyle(23)
    hist2.SetMarkerColor(kGreen-3)
    hist2.SetLineColor(kGreen-3)

    hist3 = TH1F(hname+'m', hname+'m', nbins, 1, nbins+1)
    hist3.SetMarkerStyle(20)
    hist3.SetMarkerColor(kAzure-3)
    hist3.SetLineColor(kAzure-3)

    vals = []

    cnt = 0

    for tcs,val,err in Q8_losses:
        cnt +=1 
        hist1.GetXaxis().SetBinLabel(cnt, tcs)
        hist1.SetBinContent(cnt, val)
        hist1.SetBinError(cnt, err)
        vals += [val]

    cnt = 0

    for tcs,val,err in Q10_losses:
        cnt +=1 
        hist2.SetBinContent(cnt, val)
        hist2.SetBinError(cnt, err)
        vals += [val]

    cnt = 0

    for val,err in max_cold_losses:
        cnt +=1 
        hist3.SetBinContent(cnt, val)
        hist3.SetBinError(cnt, err)
        vals += [val]

    minval = min(vals)
    maxval = max(vals)

    hist1.GetYaxis().SetRangeUser(minval*.75, maxval*1.23)
    hist1.Draw('P')
    hist2.Draw('PSAME')
    hist3.Draw('PSAME')

    # x1, y1, x2, y2a
    thelegend = TLegend(0.16, 0.7, 0.42, 0.82) 
    thelegend.SetFillColor(0)
    thelegend.SetLineColor(0)
    thelegend.SetTextSize(0.035)
    thelegend.SetShadowColor(10)
    thelegend.AddEntry(hist1,'at Q8', "P")
    thelegend.AddEntry(hist2,'at Q10', "P")
    thelegend.AddEntry(hist3,'10% of maximum cold loss', "P")
    thelegend.Draw()

    pname  = wwwpath
    pname += 'scan/'+hname+'.png'

    cv.Print(pname)
