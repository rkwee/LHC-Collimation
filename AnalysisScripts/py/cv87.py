#!/usr/bin/python
#
# # compare all BKG types at 4 TeV and 6.5TeV
# compare with proper normalisation

#   Sep 16 rkwee
#   cv68->this
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
from helpers import *
import cv81
from createTTree import treeName
from fillTTree_dict import generate_sDict
## -------------------------------------------------------------------------------
def cv87():

    f1 = thispath + 'results_pressure2011_beam_gas_3.5TeV_IR1_to_arc_20MeV_100M_nprim7660649_66.root'
    f2 = thispath + 'results_pressure2012_ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67.root'
    f3 = thispath + 'results_pressure2015_ir1_BG_bs_6500GeV_b1_20MeV_nprim3198000_67.root'

    filenames = [f1, f2,f3]

    lTexts = ['3.5 TeV', '4 TeV', '6.5 TeV']
    tags   = ['_BG_3p5TeV_20MeV_reweighted', '_BG_4TeV_20MeV_bs_reweighted','_BG_6500GeV_flat_20MeV_bs_reweighted']
    cols   = [kAzure-2, kPink-3, kYellow-2]
    mars   = [ 33, 20, 22 ]
    dOpt   = [ 'h', 'hsame', 'hsame']

    # ------------------------------------------------------------------------
    debug = 0
    # need one file to generate sDict
    bbgFile = f1
    print "Opening for sDict generation ...", bbgFile
    tag = tags[0]
    yrel = '/s' 
    norm = float(bbgFile.split('nprim')[-1].split('_')[0])
    tBBG = TFile.Open(bbgFile).Get(treeName)
    sDict = generate_sDict(tag, norm, tBBG, yrel)
    try:
        if not os.path.exists(subfolder):
            print 'making dir',  subfolder
            os.mkdir(subfolder)
    except:
        pass
    
    rfs = [  TFile.Open(f_i) for f_i in filenames ]

    msize = 0.05
    for skey in sDict.keys():

        if skey.count("Sel"): continue
        elif skey.count("Neg"): continue
        elif skey.count("Pos"): continue
        elif skey.count("Z") and not skey.startswith("OrigZ") : continue
        elif skey.count("Neu_"): continue
        elif skey.count("Char"): continue
        elif skey.count("Plus") or skey.count("Minus"): continue
        elif skey.split(tag)[0].endswith("0") or skey.count("XY"): continue
        elif skey.count("Pio") or skey.count("Kao"): continue

        # # for testing
        elif not skey.count('OrigZMuon'): continue
               
        cv = TCanvas( 'cv'+skey, 'cv'+skey,  10, 10, 1200, 900 )     

        x1, y1, x2, y2 = 0.65,0.73,0.95,0.93 # right corner        

        if 0:# skey.count("PhiEnAll") or skey.count("PhiEnPhot") or skey.count("PhiNAllE") or skey.count("PhiNP") or skey.count("EnPro"):
            x1, y1, x2, y2 = 0.2,0.75,0.44,0.93 # left corner

        mlegend = TLegend( x1, y1, x2, y2)
        mlegend.SetFillColor(0)
        mlegend.SetFillStyle(0)
        mlegend.SetLineColor(0)
        mlegend.SetTextSize(0.04)
        mlegend.SetShadowColor(0)
        mlegend.SetBorderSize(0)

        XurMin, XurMax = -1, -1
        YurMin, YurMax = -1, -1

        hname = skey # contains tag
        hnames = [ hname.replace(tag, tg) for tg in tags ] 
        if debug: print 'plotting ', hnames

        xtitle, ytitle = sDict[skey][9], sDict[skey][10]

        # per rf file 1 histogram
        hists = []
        Ymax, Ymin = [], []
        for i,rf  in enumerate(rfs):

            if debug: print "trying to get", hnames[i], "from ", rf
            hists += [ rf.Get(hnames[i]) ]

            if not hists[-1]:
                print "WARNING : Didn't find ", hnames[i]
                continue

            print "Have in hists", hists
        for i in range(len(hists)):

            isLogx, isLogy = 0, 0

            try:
                hname  =  hnames[i]

                if hname.count('Ekin') or hname.count("En") or hname.startswith("Rad") or hname.startswith("Phi"):
                    isLogy = 1
                    if hname.count("Ekin"): 
                        isLogx = 1

                hists[i].SetLineWidth(2)
                hists[i].SetLineStyle(1)
                hists[i].SetLineColor(cols[i])
                hists[i].SetMarkerStyle(mars[i])
                hists[i].SetMarkerSize(1.03)
                hists[i].SetMarkerColor(cols[i])
                #hists[i].GetXaxis().SetLabelSize(0.2))
                # To scale get min max value from all histograms first before drawing

            except AttributeError:
                print "WARNING : histogram", hnames[i], "doesn't exist in", filenames[i]
                break

        # skip all histograms when one is missing        
        if not hists[0]: continue
        
        
        print len(hists), hists
        for i in range(len(hists)):

            hist_reweighted = hists[i].ProjectionX()
            
            
            #     XurMin, XurMax = -3.14, 3.01
            #     YurMin, YurMax = 1e-1*max(Ymax), max(Ymax)*1e4
            #     if hnames[i].count("En"):
            #         YurMin, YurMax = 1e-5*max(Ymax), max(Ymax)*5e4
                    
            # elif hnames[i].count("Ekin"):
            #     YurMin, YurMax = 1e-2,8e10


            # elif hnames[i].count("Rad"):
            #     XurMin, XurMax = 0.,600.
            #     YurMin, YurMax = 1e-3,1e10
            #     if  hnames[i].count("All"):
            #         YurMin, YurMax = 1e-4,1e12


            legendunit = "/m"
                                              
            nbins = hist_reweighted.GetNbinsX()
            hist_reweighted.GetYaxis().SetRangeUser(YurMin,YurMax)
            rbf = 4
            hist_reweighted = cv81.doNormalBinw(hist_reweighted,nbins)
            hist_reweighted.Rebin(rbf)
            hist_reweighted.Scale(1./rbf)
            hist_reweighted.GetYaxis().SetTitle(ytitle)
            hist_reweighted.Draw(dOpt[i])
            doLogx, doLogy = 0,1
            xtitle = "s [m]"
            hist_reweighted.GetXaxis().SetTitle(xtitle)
            cv.SetLogy(doLogy)
            mlegend.AddEntry(hists[i], lTexts[i], "lp")

            YurMin, YurMax = 1e-2,1e7
            if XurMin != -1:
                hist_reweighted.GetXaxis().SetRangeUser(XurMin,XurMax)

            if YurMin != -1:                
                hist_reweighted.GetYaxis().SetRangeUser(YurMin,YurMax)
            print "Setting y axes", YurMin, YurMax, dOpt[i]

        mlegend.Draw()

        lab = mylabel(42)
        lab.SetTextSize(0.06)
        lab.DrawLatex(0.39, 0.855, sDict[skey][6])
        nlab = mylabel(42)
        nlab.DrawLatex(0.45,0.955,"")

        lab = mylabel(42)
        lab.SetTextSize(0.1)
#        lab.SetTextColor(col)

#        pname = subfolder+hnames[i].split('_')[0]+'.pdf'

        pname = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/cv87_allenergies_' + hnames[i].split('_')[0]+'.pdf'
        print pname
        cv.SaveAs(pname)
