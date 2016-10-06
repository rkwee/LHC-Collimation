#!/usr/bin/python
#
# # compare all BKG types at 6.5 TeV
#   Sep 16 rkwee
#   cv16->cv68->cv69
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
from helpers import *
from createTTree import treeName
from fillTTree_dict import generate_sDict
## -------------------------------------------------------------------------------
def cv69():

    norm6500GeVB1 = 2748 * 1.2e11/360000 *0.5*(739./62515929 +(312+273.)/62692523) # 2.1e-5
    norm6500GeVB2 = 2748 * 1.2e11/360000 *0.5*(779./50890652+773./63119778.) # 2.76e-5 take the average of H an V runs!

    # python /afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/AnalysisScripts/py/collsummary.py -f 6.5TeV_vHaloB2_h5/coll_summary_6.5TeV_vHaloB2_h5.dat -c TCT*R5
    # IR5 B1: h:( 53754939.0 protons on IR7 primaries, 346.0 protons on TCT*L5.B1), v(52838656.0 on primaries IR7,  408.0 protons on TCTL5)
    # .5*( 346.0/53754939.0 + 408.0/52838656.0 ) = 7.0791187088930279e-06
    # IR5 B2: h:( 43718962.0 IR7,  302.0 protons ), v(53000835.0, 106.0 protons. )
    # 0.5 * (302.0/43718962.0 + 106.0/53000835.0) = 4.4538612500709768e-06

    run1iniFlux = 368 * 1.2e11/360000. # from Roderiks NIM paper: 2010: 368 up to 2011 1380
    norm3500GeVB1 = 1.02813e-5 # from http://bbgen.web.cern.ch/bbgen/bruce/fluka_beam-halo_3.5TeV/flukaIR15.html
    norm3500GeVB2 = 2.25625e-5 # from http://bbgen.web.cern.ch/bbgen/bruce/fluka_beam-halo_3.5TeV/flukaIR15.html

    # # ------------------------------------------------------------------------
    # 6.5 TeV

    # fNum = workpath + 'runs/FL_6500GeV_HaloB1_20MeV/results_ir1_6500GeV_b1_20MeV_nprim4752000_ntct1324_30.root'
    # fDenom = projectpath + 'valBG4TeV/results_beam_halo_6.5TeV_80cm_IR1B1_20MeV_nprim4702400_66.root'
    # # # old scattering routine
    # # fDenom = workpath + 'runs/4TeV_Halo/results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b1_nprim7964000_66.root'
    # lTextNum = 'old format'
    # lTextDenom = 'new format'
    # normDenom, normNum, yrel, addon = 1., 1., '/TCT hit', ''
    # tagNum, tagDenom = '_BH_6500GeV_haloB1_20MeV', '_BH_6500GeV_haloB1_20MeV'
    # nColor, dColor = kOrange-3, kPink-5
    # subfolder = wwwpath + 'TCT/6.5TeV/tctimpacts/validationBH/' 

    # fNum = workpath + 'runs/FL_6500GeV_HaloB1_20MeV/results_ir1_6500GeV_b1_20MeV_nprim4752000_ntct1324_30.root'
    # fDenom = 'bgChecks2/FL_NewHalo_4TeV_B1/results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b1_nprim6904000_30.root'
    # # # old scattering routine
    # # fDenom = workpath + 'runs/4TeV_Halo/results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b1_nprim7964000_66.root'
    # lTextNum = '6.5 TeV'
    # lTextDenom = '4 TeV'
    # #    normDenom, normNum, yrel, addon = 1./norm4TeVB1, 1./norm6500GeVB1, '/s', ''
    # normDenom, normNum, yrel, addon = 1., 1., '/TCT hit', 'perTCThit/'
    # tagNum, tagDenom = '_BH_6500GeV_haloB1_20MeV', '_BH_4TeV_B1_20MeV'
    # nColor, dColor = kOrange-3, kPink-5
    # subfolder = wwwpath + 'TCT/compBHB1_4TeV_vs_6.5TeVB1/' 


    # fNum = workpath + 'runs/FL_6500GeV_HaloB2_20MeV/results_ir1_6500GeV_b2_20MeV_nprim3646000_30.root'
    # fDenom = projectpath + 'bgChecks2/FL_NewHalo_4TeV_B2/results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b2_nprim6914000_30.root'
    # # ## -- fDenom = workpath + 'runs/4TeV_Halo/results_ir1_4TeV_settings_from_TWISS_20MeV_b2_nprim5356000_66.root'     # -- 4TeV are old fluka sim -- newer exist!
    # subfolder = wwwpath + 'TCT/compBHB2_4TeV_vs_6.5TeV/'
    # lTextNum = '6.5 TeV'
    # lTextDenom = '4 TeV'
    # normNum, normDenom = 1., 1.
    # tagNum, tagDenom = '_BH_6500GeV_haloB2_20MeV', '_BH_4TeV_B2_20MeV'
    # nColor, dColor = kOrange-3, kPink-4
    # yrel = '/TCT hit'

    # fNum = workpath + 'runs/4TeV_Halo/results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b1_nprim7964000_66.root'
    # fDenom = workpath + 'runs/4TeV_Halo/results_ir1_4TeV_settings_from_TWISS_20MeV_b2_nprim5356000_66.root'
    # subfolder = wwwpath + 'TCT/4TeV/comp4TeVB1B2/'
    # lTextNum = 'B1'
    # lTextDenom = 'B2'
    # normNum, normDenom = 1./norm4TeVB1, 1./norm4TeVB2
    # tagNum, tagDenom = '_BH_4TeV_B1_20MeV', '_BH_4TeV_B2_20MeV'
    # nColor, dColor = kOrange-3, kPink-3

#     fDenom = workpath + 'runs/FL_6500GeV_HaloB2_20MeV/results_ir1_6500GeV_b2_20MeV_nprim3646000_30.root'
#     fNum = workpath + 'runs/FL_6500GeV_HaloB1_20MeV/results_ir1_6500GeV_b1_20MeV_nprim4752000_30.root'
#     # fDenom = workpath + 'data/6p5TeV/results_ir1_BH_6500GeV_b2_20MeV_nprim3646000_30.root'
#     # fNum = workpath + 'data/6p5TeV/results_ir1_BH_6500GeV_b1_20MeV_nprim4752000_30.root'
#     subfolder = wwwpath + 'TCT/6.5TeV/tctimpacts/compB1B2/perTCThit/'
#     lTextNum = 'B1'
#     lTextDenom = 'B2'
# #    normDenom, normNum = 1./norm6500GeVB2, 1./norm6500GeVB1
#     normDenom, normNum = 1.,1.
#     tagNum, tagDenom = '_BH_6500GeV_haloB1_20MeV', '_BH_6500GeV_haloB2_20MeV'
#     nColor, dColor = kOrange+5, kGreen+2
#     yrel = "/TCT hit"

    # fNum =  '/afs/cern.ch/project/lhc_mib/tct_simulations/FlukaRuns/runs_usrbin/results_hilumi_ir1b1_exp_20MeV_nominalCollSett_nprim4269100_30.root'
    # fDenom = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/FL_TCT5IN_roundthin/results_hilumi_ir1_hybrid_b1_exp_20MeV_nprim5319000_30.root'
    # subfolder = wwwpath + 'TCT/HL/compB1CrabCFHalo/'
    # lTextNum = 'crabcf'
    # lTextDenom = 'halo'
    # normNum, normDenom, yrel = 1., 1., '/TCT hit'
    # tagDenom, tagNum =  '_BH_HL_tct5inrdB1_20MeV', '_crabcfb1'
    # dColor, nColor = kMagenta-2, kBlue-1

    # fNum = projectpath + 'HL1.0/FL_HL_TCT5IN_nomCollSett_haloB1/results_hilumi_BH_ir1b1_exp_20MeV_nominalCollSett_nprim3320000_30.root'
    # fDenom = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/HL_TCT5INOUT_relSett/FL_TCT5IN_roundthinB1_2nd/results_hilumi_ir1_hybrid_b1_exp_20MeV_nprim5319000_30.root'
    # subfolder = wwwpath + 'TCT/HL/compNomRetrCollSett/perTCThit/'
    # lTextNum = 'nominal'
    # lTextDenom = 'retracted'
    # normDenom, normNum, yrel = 1./normTCT5INb1, 1./normTCT5INb1nom, '/s'
    # normDenom, normNum, yrel = 1., 1., '/TCT hit'
    # tagDenom,tagNum =  '_BH_HL_tct5inrdB1_20MeV','_BH_HL_tct5inrdB1_nomCollSett_20MeV'
    # dColor, nColor = kMagenta-2, kBlue-2

    # fNum =  '/afs/cern.ch/project/lhc_mib/crabcfb1/runs_usrbin/results_hilumi_ir1b1_exp_20MeV_nominalCollSett_nprim4269100_30.root'
    # fDenom = '/afs/cern.ch/project/lhc_mib/tct_simulations/FlukaRuns/runs_modTAN/results_hilumi_ir1b1_exp_20MeV_nominalCollSett_modTAN_nprim1390500_30.root'
    # subfolder = wwwpath + 'TCT/HL/compCrabsTAN/'
    # lTextNum = 'nom TAXN'
    # lTextDenom = 'mod TAXN'
    # normNum, normDenom, yrel = 1., 1., '/TCT hit'
    # tagDenom, tagNum =  '_crabcfb1_modTAN', '_crabcfb1'
    # dColor, nColor = kMagenta+4, kBlue+3

    # ------------------------------------------------------------------------

    # all at 6.5 TeV
    f1 = workpath + 'runs/FL_6500GeV_HaloB1_20MeV/results_ir1_BH_6500GeV_b1_20MeV_nprim4752000_30.root'
    f2 = workpath + 'runs/FL_6500GeV_HaloB2_20MeV/results_ir1_6500GeV_b2_20MeV_nprim3646000_30.root'
    f3 = projectpath + 'bbgen/6.5TeV/results_ir1_BG_bs_6500GeV_b1_20MeV_nprim3198000_67.root' # hat falschen tag!
    filenames = [f1,f2,f3]

    subfolder = wwwpath + 'TCT/6.5TeV/compAllBKG/'

    lTexts = ['Halo B1', 'Halo B2', 'beam-gas']
    tags   = ['_BH_6500GeV_haloB1_20MeV','_BH_6500GeV_haloB2_20MeV', '_BG_6500GeV_flat_20GeV_bs']
    cols   = [kAzure+9, kPink-8, kYellow-2]
    mars   = [ 20, 24, 33 ]
    dOpt   = [ 'h', 'hsame', 'hsame']
    # ------------------------------------------------------------------------

    # need one file to generate sDict
    bbgFile = f1
    print "Opening for sDict generation ...", bbgFile
    tag = tags[0]
    yrel = '/interaction' 
    norm = float(bbgFile.split('nprim')[-1].split('_')[0])
    tBBG = TFile.Open(bbgFile).Get(treeName)
    sDict = generate_sDict(tag, norm, tBBG, yrel)

    if not os.path.exists(subfolder):
        print 'making dir',  subfolder
        os.mkdir(subfolder)

    rfs = [  TFile.Open(f_i) for f_i in filenames ]

    msize = 0.05
    for skey in sDict.keys():

        if skey.count('XY'): continue
        if skey.count('Orig'): continue
        if skey.startswith('Prof'): continue
        if skey.count('Sel'): continue
        if skey.count('Z'): continue

        cv = TCanvas( 'cv'+skey, 'cv'+skey,  10, 10, 1200, 900 )     

        x1, y1, x2, y2 = 0.65,0.78,0.9,0.9 # right corner        

        if skey.count("PhiEnAll") or skey.count("PhiEnPhot") or skey.count("PhiNAllE") or skey.count("PhiNP") or skey.count("EnPro"):
            x1, y1, x2, y2 = 0.2,0.78,0.45,0.9 # left corner

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
        

        print "Have in hists", hists
        for i in range(len(hists)):

            isLogx, isLogy = 0, 0

            try:
                hname  =  hnames[i]

                if hname.count('Ekin') or hname.count("En") or hname.startswith("Rad") or hname.startswith("Phi"):
                    isLogy = 1
                    if hname.count("Ekin"): 
                        isLogx = 1

                hists[i].GetXaxis().SetTitle(xtitle)
                hists[i].GetYaxis().SetTitle(ytitle)

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
                print Ymin, " for", hname

            except AttributeError:
                print "WARNING : histogram", hnames[i], "doesn't exist in", filenames[i]
                break

        # skip all histograms when one is missing        
       
        cv.cd()
        if isLogx:  cv.SetLogx()
        if isLogy:  cv.SetLogy()

        for i in range(len(hists)):
            if hists[i]:
                hists[i].Draw(dOpt[i])
                mlegend.AddEntry(hists[i], lTexts[i], "lp")
            else:
                break

        mlegend.Draw()

        lab = mylabel(42)
        lab.DrawLatex(0.356, 0.955, sDict[skey][6])
        lab = mylabel(62)
        lab.SetTextSize(0.055)
        lab.DrawLatex(x1+0.06,y1-0.06,'6.5 TeV')

        lab = mylabel(42)
        lab.SetTextSize(0.1)
#        lab.SetTextColor(col)


        if hnames[i].count('Ekin'):
            YurMin, YurMax = 0.0001, 5*max(Ymax)
            if hnames[i].count('EkinProt'):
                YurMin, YurMax = 0.000001, 30*max(Ymax)
        if hnames[i].count("Rad"):
            XurMin, XurMax = 0.00001, 600.
            YurMin, YurMax = 1e-9, 10*max(Ymax)

        if hnames[i].count("Phi"):
            XurMin, XurMax = -3.14, 3.01
            YurMin, YurMax = 0.5*min(Ymin), 4*max(Ymax)
            if hnames[i].count("All"):
                YurMin, YurMax = 0.1*min(Ymin), 10*max(Ymax)
            elif hnames[i].count("EnPro"):
                YurMin, YurMax = 0.1, 10*max(Ymax)
            elif hnames[i].count("EnMuE"):
                YurMin, YurMax = 1e-3, 10*max(Ymax)

        print "Setting y axes", YurMin, YurMax
        # set the axes
        if XurMin != -1:
            hists[0].GetXaxis().SetRangeUser(XurMin,XurMax)

        if YurMin != -1:
            hists[0].GetYaxis().SetRangeUser(YurMin,YurMax)



        gPad.RedrawAxis()

        pname = subfolder+hnames[i].split('_')[0]+'.pdf'

        print pname
        cv.SaveAs(pname)
