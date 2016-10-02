#!/usr/bin/python
#
# # compare all BKG types at 4 TeV
# compare with proper normalisation

#   Sep 16 rkwee
#   cv68->this
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
from helpers import *
from createTTree import treeName
from fillTTree_dict import generate_sDict
## -------------------------------------------------------------------------------
def cv78():
    # new halo (new scatt)
    norm4TeVB1newHalo = 1380 *1.4e11/360000 * 0.5*(622.0/50807535 + 930.0/53036514) 
    # IR5: (866+92 + 170.0+456 )/(60948098 + 64935501) = 1.26e-5,>>> (866+92)/60948098 + (170.0+456)/64935501 = 9.64e-06
    # norm4TeVB2Offmom = 1380*1.4e11/360000 * ()
    norm4TeVB2newHalo = 1380 * 1.4e11/360000 * (1179.0/49207325 +967/46222723.)/2.  
    # IR5: (1893.0 + 135)/(59198135 +56887051) = 1.75e-5, >>> 1893.0/59198135 +135/56887051. = 3.435e-05

    norm4TeVoffmomPLUS500 = 1380*1.4e11/360000 *0.5*(11919./995698)
    norm4TeVoffmomMINUS500 = 1380*1.4e11/360000 *0.5*(22278./3501844)
    norm6500GeVB1 = 2748 * 1.2e11/360000 *0.5*(739./53731448 +(312+273.)/52806720) # 2.1e-5
    norm6500GeVB2 = 2748 * 1.2e11/360000 *0.5*(779./43692659+773./52962459.) # 2.76e-5 take the average of H an V runs!

    # python /afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/AnalysisScripts/py/collsummary.py -f 6.5TeV_vHaloB2_h5/coll_summary_6.5TeV_vHaloB2_h5.dat -c TCT*R5
    # IR5 B1: h:( 53754939.0 protons on IR7 primaries, 346.0 protons on TCT*L5.B1), v(52838656.0 on primaries IR7,  408.0 protons on TCTL5)
    # .5*( 346.0/53754939.0 + 408.0/52838656.0 ) = 7.0791187088930279e-06
    # IR5 B2: h:( 43718962.0 IR7,  302.0 protons ), v(53000835.0, 106.0 protons. )
    # 0.5 * (302.0/43718962.0 + 106.0/53000835.0) = 4.4538612500709768e-06

    # ------------------------------------------------------------------------

    # all at 4 TeV
    f1 = '/afs/cern.ch/project/lhc_mib/valBG4TeV/results_pressure2012_ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67.root'
    f2 =  projectpath + 'bgChecks2/FL_NewHalo_4TeV_B1/results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b1_nprim6904000_30.root'
    f3 =  projectpath + 'bgChecks2/FL_NewHalo_4TeV_B2/results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b2_nprim6914000_30.root'
    f4 = '/afs/cern.ch/project/lhc_mib/offmom/FL_4TeVplusB2/results_ir1_offplus500Hz_4TeV_settings_from_TWISS_20MeV_b2_nprim3980000_30.root'
    f5 = '/afs/cern.ch/project/lhc_mib/offmom/FL_4TeVminusB2/results_ir1_offmin500Hz4TeV_settings_from_TWISS_20MeV_b2_nprim3987000_30.root'
    filenames = [f1,f2,f3,f4,f5]

    subfolder = wwwpath + 'TCT/4TeV/compAllBKG/normalised/'

    lTexts = ['beam-gas', 'Halo B1', 'Halo B2','+500 Hz', '-500 Hz']
    tags   = [ '_BG_4TeV_20MeV_bs_reweighted','_BH_4TeV_B1_20MeV', '_BH_4TeV_B2_20MeV' , '_offplus500Hz_4TeV_B2_20MeV', '_offmin500Hz_4TeV_B2_20MeV']
    cols   = [kOrange-3, kBlue, kRed,kMagenta+4, kTeal+4]
    mars   = [33, 20, 24, 22, 23 ]
    dOpt   = [ 'h', 'hsame', 'hsame', 'hsame', 'hsame']
    scalf  = [ 1., norm4TeVB1newHalo, norm4TeVB2newHalo, norm4TeVoffmomPLUS500, norm4TeVoffmomMINUS500]
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

    if not os.path.exists(subfolder):
        print 'making dir',  subfolder
        os.mkdir(subfolder)

    rfs = [  TFile.Open(f_i) for f_i in filenames ]

    msize = 0.05
    for skey in sDict.keys():

        if skey.count("Sel"): continue
        elif skey.count("Neg"): continue
        elif skey.count("Pos"): continue
        elif skey.count("Z"): continue
        elif skey.count("Neu_"): continue
        elif skey.count("Char"): continue
        elif skey.count("Plus") or skey.count("Minus"): continue
        elif skey.split(tag)[0].endswith("0") or skey.count("XY"): continue
        elif skey.count("Pio") or skey.count("Kao"): continue

        # # for testing
        #        elif not skey.count('Rad'): continue

        cv = TCanvas( 'cv'+skey, 'cv'+skey,  10, 10, 1200, 900 )     

        x1, y1, x2, y2 = 0.65,0.73,0.95,0.93 # right corner        

        if skey.count("PhiEnAll") or skey.count("PhiEnPhot") or skey.count("PhiNAllE") or skey.count("PhiNP") or skey.count("EnPro"):
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
        print 'plotting ', hnames

        xtitle, ytitle = sDict[skey][9], sDict[skey][10]

        # per rf file 1 histogram
        hists = []
        Ymax, Ymin = [], []
        for i,rf  in enumerate(rfs):

            print "trying to get", hnames[i], "from ", rf
            hists += [ rf.Get(hnames[i]) ]

            if not hists[-1]:
                print "WARNING : Didn't find ", hnames[i]
                continue

        if debug: print "Have in hists", hists
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

                if isLogy:
                    Ymax += [ hists[i].GetMaximum() ]
                    Ymin += [ hists[i].GetBinContent(10) ]
                # if debug: print Ymin, " for", hname


            except AttributeError:
                print "WARNING : histogram", hnames[i], "doesn't exist in", filenames[i]
                break

        # skip all histograms when one is missing        
        if not hists[0]: continue
       
        cv.cd()
        if isLogx:  cv.SetLogx()
        if isLogy:  cv.SetLogy()

        if debug: print len(hists), hists
        for i in range(len(hists)):
            hists[i].Scale(scalf[i])


            print "Setting y axes", YurMin, YurMax, dOpt[i]

            if hnames[i].count("Phi"):
                XurMin, XurMax = -3.14, 3.01
                YurMin, YurMax = 1e-5*max(Ymax), max(Ymax)*1e2
                if hnames[i].count("En"):
                    YurMin, YurMax = 1e-7*max(Ymax), max(Ymax)*5e4
                    
            elif hnames[i].count("Ekin"):
                YurMin, YurMax = 1e-8*max(Ymax), max(Ymax)*1e3


            elif hnames[i].count("Rad"):
                XurMin, XurMax = 0.,600.
                YurMin, YurMax = 1e-5,1e9
                if  hnames[i].count("All"):
                    YurMin, YurMax = 1e-5,1e12

            if XurMin != -1:
                hists[i].GetXaxis().SetRangeUser(XurMin,XurMax)

            print "Setting y axes", YurMin, YurMax, dOpt[i]
            if YurMin != -1:
                print "Setting y axes", YurMin, YurMax, dOpt[i]
                hists[i].GetYaxis().SetRangeUser(YurMin,YurMax)

            if hists[i].GetName().endswith("reweighted"):
                hists[i].ProjectionX().GetYaxis().SetRangeUser(YurMin,YurMax)
                hists[i].ProjectionX().GetXaxis().SetTitle(xtitle)
                hists[i].ProjectionX().GetYaxis().SetTitle(ytitle)
                hists[i].ProjectionX().Draw(dOpt[i])
            else:
                hists[i].GetXaxis().SetTitle(xtitle)
                hists[i].Draw(dOpt[i])
            mlegend.AddEntry(hists[i], lTexts[i], "lp")

        mlegend.Draw()

        lab = mylabel(42)
        lab.DrawLatex(0.356, 0.955, sDict[skey][6])
        lab = mylabel(62)
        lab.SetTextSize(0.055)
        lab.DrawLatex(.8,y1-0.07,'')

        lab = mylabel(42)
        lab.SetTextSize(0.1)
#        lab.SetTextColor(col)

        # if hnames[i].count('Ekin'):


            #            YurMin, YurMax = ymin, 4*max(Ymax)
        #     if hnames[i].count("All"):
        #         YurMin, YurMax = ymin, 10*max(Ymax)
        #     elif hnames[i].count("EnPro"):
        #         YurMin, YurMax = 0.1, 10*max(Ymax)
        #     elif hnames[i].count("EnMuE"):
        #         YurMin, YurMax = 1e-3, 10*max(Ymax)

        #gPad.RedrawAxis()

        pname = subfolder+hnames[i].split('_')[0]+'.pdf'

        print pname
        cv.SaveAs(pname)
