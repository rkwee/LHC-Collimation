#!/usr/bin/python
#
# Mar 2015, rkwee
## -------------------------------------------------------------------------------
# depths plots of FLUKA input for halo
## -------------------------------------------------------------------------------
import ROOT, sys, os, time, math
from ROOT import *
import helpers, array
from helpers import *
from array import array
# -----------------------------------------------------------------------------------
def cv60():

    showInfo = 1

    # for each set serveral plots

    sets = [

    # # flat beam HL
    #     [gitpath  + "SixTrackConfig/7TeV/hilumiLHC/TCThaloStudies_relaxedCollSettings/b1/collgaps.dat.TCT5LIN",\
    #          workpath + "runs/HL_TCT5INOUT_relSett/impacts_real_HL_TCT5IN_relaxColl_HaloB1_flatthin.txt.root", \
    #          gitpath  + "SixTrackConfig/7TeV/hilumiLHC/TCThaloStudies_relaxedCollSettings/b1/collgaps.dat.TCT5LIN",\
    #          'TCT/HL/relaxedColl/newScatt/', 'HL flat B1 ', 1., \
    #          100,0., 20.,
    #         ],

    #     # nomCollSett HL
    #     [ projectpath + 'HL1.0/H5_HL_nomSett_hHalo_b1/coll_summary_H5_HL_nomSett_hHalo_b1.dat',\
    #           projectpath + 'HL1.0/impacts_real_HL_TCT5IN_nomColl_haloB1.txt.root',\
    #           projectpath + 'HL1.0/test/run_00002/collgaps.dat',\
    #           'TCT/HL/nominalColl/2015/', 'HL TCT5IN Halo B1', 1.,
    #           100,0., 5.,
    #         ],

    #     [ workpath + "runs/H5_HL_TCT5IN_relaxColl_hHaloB1_roundthin/coll_summary_H5_HL_TCT5IN_relaxColl_hHaloB1_roundthin.dat", \
    #           workpath + 'runs/sourcedirs/HL_TCT_7TeV/fluka/hybrid/b1/tct5inrd.dat.root', \
    #           gitpath  + "SixTrackConfig/7TeV/hilumiLHC/TCThaloStudies_relaxedCollSettings/b1/collgaps.dat.TCT5LIN",\
    #           'TCT/HL/relaxedColl/newScatt/', \
    #           'HL 7 TeV', 0.1,\
    #           100,0., 5.,
    #       ],

    #    [ workpath + "runs/H5_HL_TCT5IN_relaxColl_hHaloB1_roundthin/coll_summary_H5_HL_TCT5IN_relaxColl_hHaloB1_roundthin.dat", \
    #           workpath + 'runs/sourcedirs/HL_TCT_7TeV/fluka/hybrid/b1/tct5inrd.dat.root', \
    #           gitpath  + "SixTrackConfig/7TeV/hilumiLHC/TCThaloStudies_relaxedCollSettings/b1/collgaps.dat.TCT5LIN",\
    #           'TCT/HL/relaxedColl/newScatt/', \
    #           'HL 7 TeV', 0.1, \
    #           100,0., 5.,
    #       ],

    #     [ workpath + "runs/H5_HL_TCT5LOUT_relaxColl_hHaloB1_roundthin/coll_summary_H5_HL_TCT5LOUT_relaxColl_hHaloB1_roundthin.dat", \
    #           workpath + 'runs/sourcedirs/HL_TCT_7TeV/fluka/hybrid/b1/tct5otrd.dat.root', \
    #           gitpath  + "SixTrackConfig/7TeV/hilumiLHC/TCThaloStudies_relaxedCollSettings/b1/collgaps.dat.TCT5LOFF",\
    #           'TCT/HL/relaxedColl/newScatt/', \
    #           'HL 7 TeV', 0.07, \
    #           100,0., 20.,
    #       ],

    #     [ gitpath + 'SixTrackConfig/7TeV/hilumiLHC/TCThaloStudies_relaxedCollSettings/b2/collgaps.dat.TCT5LIN',\
    #           workpath + 'runs/sourcedirs/HL_TCT_7TeV/fluka/hybrid/b2/tcinrdb2.dat.root', \
    #           gitpath + 'SixTrackConfig/7TeV/hilumiLHC/TCThaloStudies_relaxedCollSettings/b2/collgaps.dat.TCT5LIN',\
    #           'TCT/HL/relaxedColl/newScatt/', \
    #           'HL 7 TeV', 0.07, \
    #           100,0., 5.,
    #       ],

    #     [ gitpath + 'SixTrackConfig/7TeV/hilumiLHC/TCThaloStudies_relaxedCollSettings/b2/collgaps.dat.TCT5LOUT',\
    #           workpath + 'runs/sourcedirs/HL_TCT_7TeV/fluka/hybrid/b2/tcotrdb2.dat.root', \
    #           gitpath + 'SixTrackConfig/7TeV/hilumiLHC/TCThaloStudies_relaxedCollSettings/b2/collgaps.dat.TCT5LOUT',\
    #           'TCT/HL/relaxedColl/newScatt/', \
    #           'HL 7 TeV', 0.07, \
    #           100,0., 20.,

    #       ],
        
        # [ workpath + 'runs/6.5TeV_hHaloB1_h5/coll_summary_6.5TeV_hHaloB1_h5.dat', \
        #       gitpath + 'FlukaRoutines/6.5TeV/b1/HALOB1.dat.root', \
        #       gitpath  + 'SixTrackConfig/6.5TeV/MED800/B1/collgaps.dat',\
        #       'TCT/6.5TeV/', '6.5 TeV B1', 0.7, \
        #       100,0., 10.,
        #   ],

        # [ workpath + 'runs/6.5TeV_hHaloB2_h5/coll_summary_6.5TeV_hHaloB2_h5.dat', \
        #       gitpath + 'FlukaRoutines/6.5TeV/b2/HALOB2.dat.root', \
        #       gitpath  + 'SixTrackConfig/6.5TeV/MED800/B2/collgaps.dat',\
        #       'TCT/6.5TeV/', '6.5 TeV B2', 5.e-1, \
        #       100,0., 10.,
        #   ],

        # # 4 TeV
        # [ workpath + 'runs/4TeV_Halo/coll_summary_TCT_4TeV_B2hHalo.dat',\
        #       workpath + 'runs/4TeV_Halo/HALO4TeVB2.dat.root',\
        #       gitpath + 'SixTrackConfig/4TeV/TCThaloStudies/b2/collgaps.dat',\
        #       'TCT/4TeV/B2/', '4 TeV B2', 1., \
        #       100,0., 10.,
        #     ],

        # [ workpath + 'runs/4TeV_Halo/coll_summary_TCT_4TeV_B1hHalo.dat',\
        #       workpath + 'runs/sourcedirs/TCT_4TeV_60cm/fluka/impacts_real_HALO.dat.root',\
        #       gitpath + 'SixTrackConfig/4TeV/TCThaloStudies/b1/collgaps.dat',\
        #       'TCT/4TeV/B1/', '4 TeV B1', 1., \
        #       100,0., 10.,
        #     ],

        # [ workpath + 'runs/4TeV_Halo/coll_summary_NewScatt_TCT_4TeV_B2hHalo.dat',\
        #       workpath + 'runs/4TeV_Halo/impacts_real_NewScatt_TCT_4TeV_B2.txt.root',\
        #       gitpath + 'SixTrackConfig/4TeV/TCThaloStudies/b2/collgaps.dat',\
        #       'TCT/4TeV/', '4 TeV B2', 1., \
        #       100,0., 10.,
        #     ],

        # [ projectpath + 'bgChecks2/NewScatt_4TeV_hHaloB1/coll_summary_NewScatt_4TeV_hHaloB1.dat',\
        #       projectpath + 'bgChecks2/impacts_real_NewScatt_4TeV_haloB1.txt.root',\
        #       projectpath + 'bgChecks2/NewScatt_4TeV_hHaloB1/run_test/collgaps.dat',\
        #       'TCT/4TeV/', '4 TeV B1', 1., \
        #       100,0., 10.,
        #     ],

        [ projectpath + 'bgChecks2/NewScatt_4TeV_hHaloB2/coll_summary_NewScatt_4TeV_hHaloB2.dat',\
              projectpath + 'bgChecks2/impacts_real_NewScatt_4TeV_haloB2.txt.root',\
              projectpath + 'bgChecks2/NewScatt_4TeV_hHaloB2/run_test/collgaps.dat',\
              'TCT/4TeV/', '4 TeV B2', 1., \
              100,0., 10.,
            ],

    #     # crabs tct5 in
    #     [ projectpath + 'tct_simulations/jobs/coll_summary.dat',\
    #           projectpath + 'tct_simulations/jobs/impacts_real_tct5inb1_crabs.dat.root', \
    #           projectpath + 'tct_simulations/jobs/collgaps.dat',\
    #           'TCT/HL/crabcf/v3/', 'HL crabs failure - TCT5 in', 1., \
    #           100,0., 5.,
    #         ],

    #     # crabs tct5 out
    #     [ projectpath + 'tct_simulations/no_tct5_jobs/Kyrre/coll_summary.dat',\
    #           projectpath + 'tct_simulations/no_tct5_jobs/Kyrre/impacts_real_tct5otb1_crabs.dat.root', \
    #           projectpath + 'tct_simulations/no_tct5_jobs/Kyrre/collgaps.dat',\
    #           'TCT/HL/crabcf/v3/tct5otrd/', 'HL crabs failure - TCT4 only', 1.,
    #           100,0., 5.,
    #         ],

        # # Hectors off momentum 4 TeV, minus 500Hz, IR1, B1
        # [ projectpath + 'offmom/LHC_4.0TeV/minus_500Hz/B1/collgap.lowb.hor.b1.dat',\
        #       projectpath + 'offmom/LHC_4.0TeV/minus_500Hz/B1/impacts_real_minus500Hz_4TeVB1.txt.root',\
        #       projectpath + 'offmom/LHC_4.0TeV/minus_500Hz/B1/collgap.lowb.hor.b1.dat',\
        #       'TCT/4TeV/offmom/', '4TeV B1 -500 Hz', 1., \
        #       100,0., 20.,
        #     ],

        # # Hectors off momentum 4 TeV, minus 500Hz, IR1, B2
        # [ projectpath + 'offmom/LHC_4.0TeV/minus_500Hz/B2/collgap.lowb.hor.b2.dat',\
        #       projectpath + 'offmom/LHC_4.0TeV/minus_500Hz/B2/impacts_real_minus500Hz_4TeVB2.txt.root',\
        #       projectpath + 'offmom/LHC_4.0TeV/minus_500Hz/B2/collgap.lowb.hor.b2.dat',\
        #       'TCT/4TeV/offmom/', '4TeV B2 -500 Hz', 1., \
        #       100,0., 20.,
        #     ],

        # # Hectors off momentum 6.5 TeV, plus 500Hz, IR1
        # [ projectpath + 'offmom/LHC_6.5TeV/plus_500Hz/B2/collgap.lowb.hor.b2.dat',\
        #       projectpath + 'offmom/LHC_6.5TeV/plus_500Hz/B2/impacts_real_6500GeV_plus500Hz_TCT_B2.txt.root',\
        #       projectpath + 'offmom/LHC_6.5TeV/plus_500Hz/B2/collgap.lowb.hor.b2.dat',\
        #       'TCT/6.5TeV/offmom/', '6.5TeV B2 +500 Hz', 1., \
        #       100,0., 20., 
        #     ],

        # # Hectors off momentum 6.5 TeV, plus 500Hz, IR5
        # [ projectpath + 'offmom/LHC_6.5TeV/plus_500Hz/B1/collgap.lowb.hor.b1.dat',\
        #       projectpath + 'offmom/LHC_6.5TeV/plus_500Hz/B1/impacts_real_6500GeV_plus500Hz_TCT_B1.txt.root',\
        #       projectpath + 'offmom/LHC_6.5TeV/plus_500Hz/B1/collgap.lowb.hor.b1.dat',\
        #       'TCT/6.5TeV/offmom/', '6.5TeV B1 +500 Hz', 1., \
        #       100,0., 20.,
        #     ],

        # # # Hectors off momentum 6.5 TeV, minus 500Hz, IR5
        # [ projectpath + 'offmom/LHC_6.5TeV/minus_500Hz/B1/collgap.lowb.hor.b1.dat',\
        #       projectpath + 'offmom/LHC_6.5TeV/minus_500Hz/B1/impacts_real_6500GeV_minus500Hz_TCT_b1.txt.root',\
        #       projectpath + 'offmom/LHC_6.5TeV/minus_500Hz/B1/collgap.lowb.hor.b1.dat',\
        #       'TCT/6.5TeV/offmom/', '6.5TeV B1 -500 Hz', 1., \
        #       100,0., 20.,
        #     ],



        # # Hectors off momentum 4 TeV, plus 500Hz, IR1, B1
        # [ projectpath + 'offmom/LHC_4.0TeV/plus_500Hz/B1/collgap.lowb.hor.b1.dat',\
        #       projectpath + 'offmom/LHC_4.0TeV/plus_500Hz/B1/impacts_real_4TeV_plus500Hz_TCT_B1.txt.root',\
        #       projectpath + 'offmom/LHC_4.0TeV/plus_500Hz/B1/collgap.lowb.hor.b1.dat',\
        #       'TCT/4TeV/offmom/', '4TeV B1 +500 Hz', 1., \
        #       100,0., 20.,
        #     ],

        # # Hectors off momentum 4 TeV, plus 500Hz, IR1, B2
        # [ projectpath + 'offmom/LHC_4.0TeV/plus_500Hz/B2/collgap.lowb.hor.b2.dat',\
        #       projectpath + 'offmom/LHC_4.0TeV/plus_500Hz/B2/impacts_real_4TeV_plus500Hz_TCT_B2.txt.root',\
        #       projectpath + 'offmom/LHC_4.0TeV/plus_500Hz/B2/collgap.lowb.hor.b2.dat',\
        #       'TCT/4TeV/offmom/', '4TeV B2 +500 Hz', 1., \
        #       100,0., 20.,
        #     ],

        ]

    # activate only last entry
    # sets = [sets[-1]]

    # collimators
    colls = [
         'TCTH.5L1.B1',
         'TCTVA.5L1.B1',
         'TCTH.4L1.B1', 
         'TCTVA.4L1.B1',
         'TCTH.4L5.B1', 
         'TCTVA.4L5.B1',
         'TCTH.5R1.B2',
         'TCTVA.5R1.B2',
         'TCTH.4R1.B2', 
         'TCTVA.4R1.B2',
         'TCTH.4R5.B2', 
         'TCTVA.4R5.B2',
        ]

    # for each collimator fix a color
    bCol = [
         kBlue,
         kCyan,
         kCyan-2,
         kOrange-6,
         kRed-5,
         kMagenta+1,
         kMagenta+2,
         kViolet,
         kGreen+2,
         kOrange-2,
         kRed+2,
         kGreen-2,
         kMagenta-2,
        ]


    hDict = {
        ## x,y in [m] #0 var #1 xnbins, xmin, xmax, ynbins, ymin, ymax, #2 xtitle, #3 ytitle , #4 doNormalise
        # 'xxpHist':['xp:x', [300,-20.,20., 300,-0.3,0.3],'x', 'x\'[mrad]',0,],
        'yypHist':['yp:y', [300,-20.,20., 300,-0.3,0.3],'y', 'y\'[mrad]', 1,],
        # 'xsHist' :['x:s',  [300,0,1, 300,-15.,15.],'s[m]', 'x[m]',0,],
        # 'ysHist' :['y:s',  [300,0,1,300,-15.,15.],'s[m]', 'y[m]',0,],
        # 'xyHist':['y:x', [300,-15.,15., 300,-15.,15.],'x [mm]', 'y [mm]',0,],
        'ypHist':['yp', [300,-0.3,0.3], 'y\'[mrad]', 'entries',0,],
        }

    # -----------------------------------------------------------------------------------
    def doDraw(hist):

        # canvas
        a,b = 1,1
        cv = TCanvas( 'cv', 'cv', a*900, b*700)
        cv.Divide(a,b)
        cv.SetTopMargin(0.18)
        cv.SetRightMargin(0.18)
        cv.SetGridx(1)
        cv.SetGridy(1)
        # name+mean
        #gStyle.SetOptStat(101)
        gStyle.SetOptStat(111)
        gStyle.SetPalette(1)

        x1, y1, x2, y2 = 0.2, 0.98, 0.84, 0.9
        lab = mylabel(42)

        if   type(hist) == TH1F: hist.Draw("HIST")
        elif type(hist) == TH2F: hist.Draw("COLZ")

        entries = hist.GetEntries()
        meanval = hist.GetMean()
        collName = hist.GetName().split(rel + '_')[-1].replace('_', '.')
        hname = hist.GetName()
        if showInfo: print 'INFO: Plotting', hname

        #lab.DrawLatex(x1+0.45, y1-0.1, "entries " + str(int(entries)))        
        #lab.DrawLatex(x1+0.45, y1-0.2, "rms " + str(meanval))
        lab.DrawLatex(0.2, 0.9, energy)
        lab.DrawLatex(0.4, 0.9, collName)

        pname  = wwwpath
        subfolder = 'TCT/4TeV/haloShower/cv60/'
        pname += subfolder + hname + '.png'

        print('Saving file as ' + pname ) 
        cv.SaveAs(pname)

    # -----------------------------------------------------------------------------------
    # get the histograms
    for myset in sets:

        cfile = myset[0] 

        if cfile.count("collgap"):
            cDict = collDict(cfile)
        elif cfile.count("summary"):
            cDict = collgapsDict(cfile)
        else:
            print "Cannot get the name identifier from", cfile
            sys.exit()

        rfname = myset[1]
        print "Opening","."*33, rfname
        rf = TFile.Open(rfname)
        mt = rf.Get('particle')
        rel = rfname.split('/')[-1].split('.')[0]

        print "rel", rel

        collgaps = myset[2]
        cgDict = collgapsDict(collgaps)
        print "and using","."*33, collgaps

        subfolder, energy, ymax = myset[3], myset[4], myset[5]
        for collName in colls:

            try:
                collid = cDict[collName][0]
            except KeyError:
                print(collName, 'key not found')
                continue

            cut = 'icoll == ' + collid

            for hkey in hDict.keys():

                # define histograms
                hname = hkey + '_' + rel + '_' + collName.replace('.', '_')

                var = hDict[hkey][0]
                if var.count(":"):
                    xnbins, xmin, xmax = hDict[hkey][1][0],hDict[hkey][1][1],hDict[hkey][1][2]
                    ynbins, ymin, ymax = hDict[hkey][1][3],hDict[hkey][1][4],hDict[hkey][1][5]
                    hist = TH2F(hname, hname, xnbins, xmin, xmax, ynbins, ymin, ymax)
                else:
                    xnbins, xmin, xmax = hDict[hkey][1][0],hDict[hkey][1][1],hDict[hkey][1][2]
                    hist = TH1F(hname, hname, xnbins, xmin, xmax)

                xtitle, ytitle = hDict[hkey][2],hDict[hkey][3]
                hist.GetXaxis().SetTitle(xtitle)
                hist.GetYaxis().SetTitle(ytitle)

                # store sum of squares of weights 
                hist.Sumw2()
                if showInfo: print 'INFO: will fill these variables ', var, 'into', hname
                if showInfo: print 'INFO: will apply a cut of ', cut, 'to', hname
                mt.Project(hname, var, cut)
                entries = hist.GetEntries()
                if showInfo: print 'INFO: Have ',entries, ' entries in', hname, ' for ', collName
                print hist
                if entries: doDraw(hist)


# ----------------------------------------------------------------------------





