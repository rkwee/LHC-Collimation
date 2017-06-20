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
    norm6500GeVB1OLD = 2748 * 1.2e11/360000 *0.5*(739./53731448 +(312+273.)/52806720) # 2.1e-5
    norm6500GeVB2OLD = 2748 * 1.2e11/360000 *0.5*(779./43692659+773./52962459.) # 2.76e-5 take the average of H an V runs!

    norm6500GeVB1 = 2041 * 1.12e11/360000 *0.5*(739./53731448 +(312+273.)/52806720) 
    norm6500GeVB2 = 2041 * 1.12e11/360000 *0.5*(779./43692659+773./52962459.) 
    # ---- HL -
    HLinitialFlux = 2736*2.2e11/360000 # 1.7e9

    # retracted settings
    normTCT5LOUTb1 = HLinitialFlux * 0.5*(9024.0/54609869.0 + 3071.0/52175081.0)# 0.00011205218641475149 #12091./(63828643+61405975) # 9.7e-5
    normTCT5LOUTb2 = HLinitialFlux * 0.5*(9936.0/40392116.0 + 11898.0/53157089.0)# 0.0002349078766943835 ### 21822/(47196776+63051589) # 2e-4
    normTCT5INb1 = HLinitialFlux * 0.5*(9712.0/54532193.0 + 3366.0/52154816.0) # 0.00012131762826402283
    normTCT5INb2 = HLinitialFlux * 0.5 * (9948.0/40401333.0 + 12028.0/53199970.0)# 0.0002361599262 # 11172./(47203328+63096910) # 1e-4 sum of all tcts over protons lost on primary for h and v separately

    # python /afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/AnalysisScripts/py/collsummary.py -f 6.5TeV_vHaloB2_h5/coll_summary_6.5TeV_vHaloB2_h5.dat -c TCT*R5
    # IR5 B1: h:( 53754939.0 protons on IR7 primaries, 346.0 protons on TCT*L5.B1), v(52838656.0 on primaries IR7,  408.0 protons on TCTL5)
    # .5*( 346.0/53754939.0 + 408.0/52838656.0 ) = 7.0791187088930279e-06
    # IR5 B2: h:( 43718962.0 IR7,  302.0 protons ), v(53000835.0, 106.0 protons. )
    # 0.5 * (302.0/43718962.0 + 106.0/53000835.0) = 4.4538612500709768e-06

    # steer
    do4TeV,do6500GeV = 1,0
    doHLcomp = 0
    doNumbers = 0
    # ------------------------------------------------------------------------
    if do4TeV:

        energy = "4 TeV"
        # all at 4 TeV
        f1 = '/afs/cern.ch/project/lhc_mib/valBG4TeV/results_pressure2012_ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67.root'
        f2 =  projectpath + 'bgChecks2/FL_NewHalo_4TeV_B1/results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b1_nprim6904000_30.root'
        f3 =  projectpath + 'bgChecks2/FL_NewHalo_4TeV_B2/results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b2_nprim6914000_30.root'
        # f4 = '/afs/cern.ch/project/lhc_mib/offmom/FL_4TeVplusB2/results_ir1_offplus500Hz_4TeV_settings_from_TWISS_20MeV_b2_nprim3980000_30.root'
        #f5 = '/afs/cern.ch/project/lhc_mib/offmom/FL_4TeVminusB2/results_ir1_offmin500Hz4TeV_settings_from_TWISS_20MeV_b2_nprim3987000_30.root'

        # local
        f1 = thispath + 'results_pressure2012_ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67.root'
        f2 = thispath + 'results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b1_nprim6904000_30.root'
        f3 = thispath + 'results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b2_nprim6914000_30.root'
        #f4 = thispath + 'results_ir1_offplus500Hz_4TeV_settings_from_TWISS_20MeV_b2_nprim3980000_30.root'
        #f5 = thispath + 'results_ir1_offmin500Hz4TeV_settings_from_TWISS_20MeV_b2_nprim3987000_30.root'

        filenames = [f1,f2,f3]

        subfolder = wwwpath + 'TCT/4TeV/compAllBKG/'

        lTexts = ['beam-gas', 'halo B1', 'halo B2','dp/p<0 (+500 Hz)', 'dp/p>0 (-500 Hz)']
        tags   = [ '_BG_4TeV_20MeV_bs_reweighted','_BH_4TeV_B1_20MeV', '_BH_4TeV_B2_20MeV' , '_offplus500Hz_4TeV_B2_20MeV', '_offmin500Hz_4TeV_B2_20MeV']
        cols   = [kOrange-3, kBlue, kRed,kMagenta+4, kTeal+4]
        mars   = [33, 20, 24, 22, 23 ]
        dOpt   = [ 'hp', 'hsame', 'hsame', 'hsame', 'hsame']
        scalf  = [ 1., norm4TeVB1newHalo, norm4TeVB2newHalo, norm4TeVoffmomPLUS500, norm4TeVoffmomMINUS500]
        roundingDigit = 3
    elif do6500GeV:

        energy = "6.5 TeV"
        # all at 6.5 TeV # from cv69
        f1 = thispath + 'results_ir1_BH_6500GeV_b1_20MeV_nprim4752000_30.root'
        f2 = thispath + 'results_ir1_BH_6500GeV_b2_20MeV_nprim3646000_30.root'
        f3 = thispath + 'results_pressure2015_ir1_BG_bs_6500GeV_b1_20MeV_nprim3198000_67.root'
        filenames = [f3, f1,f2]

        lTexts = ['beam-gas', 'Halo B1', 'Halo B2']
        tags   = ['_BG_6500GeV_flat_20MeV_bs_reweighted','_BH_6500GeV_haloB1_20MeV','_BH_6500GeV_haloB2_20MeV']
        cols   = [kYellow-2, kAzure+9, kPink-8]
        mars   = [ 33, 20, 24 ]
        dOpt   = [ 'hist', 'histsame', 'histsame']
        scalf  = [1., norm6500GeVB1, norm6500GeVB2]
        roundingDigit = 2

    elif doHLcomp:
        roundingDigit = 2
        energy = ""
        f1 = thispath + 'results_pressure2015_ir1_BG_bs_6500GeV_b1_20MeV_nprim3198000_67.root'
        f2 = thispath + "results_hilumi_ir1_hybrid_b1_exp_20MeV_nprim5550000_30.root"
        f2 = thispath + "results_ir1_BH_6500GeV_b2_20MeV_nprim3646000_30.root"
        f3 = thispath + "results_hilumi_ir1_hybrid_b2_exp_20MeV_nprim5924500_30.root"
        f4 = thispath + "results_hilumi_ir1_fort_scaled_afterconditioning_max_nprim1_30.root"


        filenames = [f4,f3,f1,f2]
        tags = [
                "_BG_HL_ac_20MeV",
                "_BH_HL_tct5inrdB2_20MeV",
            "_BG_6500GeV_flat_20MeV_bs_reweighted",
            "_BH_6500GeV_haloB2_20MeV",

        ]        

        lTexts = ['HL BG a.c.', 'HL Halo B2', 'Run II BG', 'Run II Halo B2', ]
        cols   = [kAzure+2, kGreen-3, kYellow-2, kRed-4]
        mars   = [ 23, 20, 22, 24 ]
        dOpt   = [ 'hp', 'hpsame', 'hpsame', 'hpsame']
        scalf  = [1.,normTCT5INb2,1.,norm6500GeVB2 ]


        
    # ------------------------------------------------------------------------
    debug = 1
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
        elif skey.count("Z") : continue
        elif skey.count("Neu_"): continue
        elif skey.count("Char"): continue
        elif skey.count("Plus") or skey.count("Minus"): continue
        elif skey.split(tag)[0].endswith("0") or skey.count("XY"): continue
        elif skey.count("Pio") or skey.count("Kao"): continue

        # # for testing
        #if not skey.count('Muons'): continue
               
        cv = TCanvas( 'cv'+skey, 'cv'+skey,  10, 10, 1200, 900 )     
        xpos = 0.65
        if doNumbers: xpos = 0.5
        x1, y1, x2, y2 = xpos,0.73,0.95,0.93 # right corner        

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

        if debug: print "Have in hists", hists

        intvals, ratios = [],[]
        for i in range(len(hists)):

            isLogx, isLogy = 0, 0

            try:
                hname  =  hnames[i]

                if hname.count('Ekin') or hname.count("En") or hname.startswith("Rad") or hname.startswith("Phi"):
                    isLogy = 1
                    if hname.count("Ekin"): 
                        isLogx = 1
                        #XurMin,XurMax = 0.02,8e3
                    

                hists[i].SetLineWidth(2)
                hists[i].SetLineStyle(1)
                hists[i].SetLineColor(cols[i])
                hists[i].SetMarkerStyle(mars[i])
                hists[i].SetMarkerSize(1.03)
                hists[i].SetMarkerColor(cols[i])
                #hists[i].GetXaxis().SetLabelSize(0.2))
                # To scale get min max value from all histograms first before drawing
                print ".."*22,hists[i].GetEntries(), "."*22, hists[i].GetName()
                if isLogy:
                    Ymax += [ hists[i].GetMaximum() ]
                    Ymin += [ hists[i].GetBinContent(10) ]
                # if debug: print Ymin, " for", hname


            except AttributeError:
                print "WARNING : histogram", hnames[i], "doesn't exist in", filenames[i]
                break

        # skip all histograms when one is missing        
        if not hists[0]: continue

        
        hists[0].GetXaxis().SetTitle(xtitle)
        
        cv.cd()
        if isLogx:  cv.SetLogx()
        if isLogy:  cv.SetLogy()

        if debug: print len(hists), hists
        for i in range(len(hists)):
            hists[i].Scale(scalf[i])


            if debug: print "Setting y axes", YurMin, YurMax, dOpt[i]

            if hnames[i].count("Phi"):
                XurMin, XurMax = -3.14, 3.01
                YurMin, YurMax = 1e-1*max(Ymax), max(Ymax)*1e4
                if hnames[i].count("En"):
                    YurMin, YurMax = 1e2,2e11


                    #if not hnames[i].count("All") and not hnames[i].count("Prot"):
                    #    YurMin, YurMax = 1e2,9e8
                        
            elif hnames[i].count("Ekin"):
                YurMin, YurMax = 1e-3,2e8


            elif hnames[i].count("Rad"):
                XurMin, XurMax = 0.,600.
                YurMin, YurMax = 1e-3,1e10
                if  hnames[i].count("All"):
                    YurMin, YurMax = 1e-4,1e12

            if hists[i].GetName().endswith("reweighted"):
                hists[i].ProjectionX().GetYaxis().SetRangeUser(YurMin,YurMax)
                hists[i].ProjectionX().GetYaxis().SetTitle(ytitle)
                intvals += [hists[i].ProjectionX().Integral()]
                hists[i].ProjectionX().Draw(dOpt[i])
                if XurMin != -1:                    
                    hists[i].ProjectionX().GetXaxis().SetRangeUser(XurMin,XurMax)
            else:
                intvals += [hists[i].Integral()]
                hists[i].GetXaxis().SetTitle(xtitle)
                hists[i].GetYaxis().SetTitle(ytitle)
                if XurMin != -1:
                    hists[i].GetXaxis().SetRangeUser(XurMin,XurMax)

                if YurMin != -1:                
                    hists[i].GetYaxis().SetRangeUser(YurMin,YurMax)


                hists[i].Draw(dOpt[i])

            ratios += [round(intvals[-1]/intvals[0], roundingDigit)]
            print " intergral of ", hists[i].GetName(), "=", intvals[-1], ratios[-1]
            numbers = ""
            if doNumbers: numbers = " ("+str(ratios[i])+")"
            mlegend.AddEntry(hists[i], lTexts[i] + numbers, "lp")
            
        mlegend.Draw()

        print "  ", hname, "=", intvals[-1]
        lab = mylabel(42)
        lab.SetTextSize(0.06)
        lab.DrawLatex(0.35, 0.855, sDict[skey][6])
        nlab = mylabel(42)
        nlab.DrawLatex(0.45,0.955,energy)

        lab = mylabel(42)
        lab.SetTextSize(0.1)
#        lab.SetTextColor(col)

# add new folder to separate from main note
        pname = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/6500GeV/reweighted/app/cv78_' + hnames[i].split('_')[0]+'.pdf'
        if do4TeV:
            pname = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/4TeV/reweighted/app/cv78_' + hnames[i].split('_')[0]+'.pdf'
        elif doHLcomp:

            pname = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/HLRunII/cv78_' + hnames[i].split('_')[0]+'.pdf'
            #subfolder = wwwpath + "TCT/HL/compHLRun2/"
            #pname = subfolder + "cv78_" + hnames[i].split("_")[0]+".pdf"
            print pname
        cv.SaveAs(pname)
