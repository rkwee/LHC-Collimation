#!/usr/bin/python
#
# Mar 2015, rkwee
## -------------------------------------------------------------------------------
# depths plots of FLUKA input for halo
## -------------------------------------------------------------------------------
import ROOT, sys, os, time, math
from ROOT import *
import lossmap, helpers, array
from helpers import *
from array import array
# -----------------------------------------------------------------------------------
def cv43():

    showInfo = 1

    # for each set serveral plots

    sets = [

        [ workpath + "runs/H5_HL_TCT5IN_relaxColl_hHaloB1_roundthin/coll_summary_H5_HL_TCT5IN_relaxColl_hHaloB1_roundthin.dat", \
              workpath + 'runs/sourcedirs/HL_TCT_7TeV/fluka/hybrid/b1/tct5inrd.dat.root', \
              gitpath  + "SixTrackConfig/7TeV/hilumiLHC/TCThaloStudies_relaxedCollSettings/b1/collgaps.dat.TCT5LIN",\
              'TCT/HL/relaxedColl/newScatt/', \
              'HL 7 TeV', 0.1,\
          ],

        [ workpath + "runs/H5_HL_TCT5LOUT_relaxColl_hHaloB1_roundthin/coll_summary_H5_HL_TCT5LOUT_relaxColl_hHaloB1_roundthin.dat", \
              workpath + 'runs/sourcedirs/HL_TCT_7TeV/fluka/hybrid/b1/tct5otrd.dat.root', \
              gitpath  + "SixTrackConfig/7TeV/hilumiLHC/TCThaloStudies_relaxedCollSettings/b1/collgaps.dat.TCT5LOFF",\
              'TCT/HL/relaxedColl/newScatt/', \
              'HL 7 TeV', 0.07, \
          ],

        [ workpath + 'runs/H5_HL_TCT5IN_relaxColl_hHaloB2_roundthin/coll_summary_H5_HL_TCT5IN_relaxColl_hHaloB2_roundthin.dat',\
              workpath + 'runs/sourcedirs/HL_TCT_7TeV/fluka/hybrid/b2/tcinrdb2.dat.root', \
              workpath + 'runs/H5_HL_TCT5IN_relaxColl_hHaloB2_roundthin/test/collgaps.dat',\
              'TCT/HL/relaxedColl/newScatt/', \
              'HL 7 TeV', 0.07, \
          ],

        [ workpath + 'runs/H5_HL_TCT5LOUT_relaxColl_hHaloB2_roundthin/coll_summary_H5_HL_TCT5LOUT_relaxColl_hHaloB2_roundthin.dat',\
              workpath + 'runs/sourcedirs/HL_TCT_7TeV/fluka/hybrid/b2/tcotrdb2.dat.root', \
              workpath + 'runs/H5_HL_TCT5IN_relaxColl_hHaloB2_roundthin/test/collgaps.dat',\
              'TCT/HL/relaxedColl/newScatt/', \
              'HL 7 TeV', 0.07, \

          ],
        
        [ workpath + 'runs/6.5TeV_hHaloB1_h5/coll_summary_6.5TeV_hHaloB1_h5.dat', \
              gitpath + 'FlukaRoutines/6.5TeV/b1/HALOB1.dat.root', \
              gitpath  + 'SixTrackConfig/6.5TeV/MED800/B1/collgaps.dat',\
              'TCT/6.5TeV/', \
              '6.5 TeV', 0.7, \
          ],

        [ workpath + 'runs/6.5TeV_hHaloB2_h5/coll_summary_6.5TeV_hHaloB2_h5.dat', \
              gitpath + 'FlukaRoutines/6.5TeV/b2/HALOB2.dat.root', \
              gitpath  + 'SixTrackConfig/6.5TeV/MED800/B2/collgaps.dat',\
              'TCT/6.5TeV/', \
              '6.5 TeV', 5.e-1\
          ],


        [ workpath + 'runs/H5_HL_TCT5LOUT_relaxColl_hHaloB1_roundthin/coll_summary_H5_HL_TCT5LOUT_relaxColl_hHaloB1_roundthin.dat',\
              workpath + 'runs/sourcedirs/HL_TCT_7TeV/fluka/hybrid/b1/crabcfb1.dat.root', \
              gitpath  + "SixTrackConfig/7TeV/hilumiLHC/TCThaloStudies_relaxedCollSettings/b1/collgaps.dat.TCT5LOFF",\
              'TCT/HL/', \
              'HL 7 TeV', 1.e-3, \
          ],

        # 4 TeV
        [ workpath + 'runs/4TeV_Halo/coll_summary_TCT_4TeV_B2hHalo.dat',\
              workpath + 'runs/4TeV_Halo/HALO4TeVB2.dat.root',\
              gitpath + 'SixTrackConfig/4TeV/TCThaloStudies/b2/collgaps.dat',\
              'TCT/4TeV/B2/', '4 TeV B2', 1.,
            ],

        [ workpath + 'runs/4TeV_Halo/coll_summary_TCT_4TeV_B1hHalo.dat',\
              workpath + 'runs/sourcedirs/TCT_4TeV_60cm/fluka/impacts_real_HALO.dat.root',\
              gitpath + 'SixTrackConfig/4TeV/TCThaloStudies/b1/collgaps.dat',\
              'TCT/4TeV/B1/', '4 TeV B1', 1.,
            ],

        ]

    # activate only last entry
    sets = [sets[-1]]
        
    nbins, xmin, xmax = 100,0., 5.
    hx = []

    # collimators
    colls = [
         'TCTH.5L1.B1',
         'TCTVA.5L1.B1',
         'TCTH.4L1.B1', 
         'TCTVA.4L1.B1',
         'TCTH.5R1.B2',
         'TCTVA.5R1.B2',
         'TCTH.4R1.B2', 
         'TCTVA.4R1.B2',
        ]

    # for each collimator fix a color
    bCol = [
         kBlue,
         kCyan,
         kCyan-2,
         kMagenta+1,
         kMagenta+2,
         kViolet,
         kGreen+2,
         kOrange-2,
         kRed+2,
        ]
    # -----------------------------------------------------------------------------------
    # draw the histograms

    def doDraw(hx,subfolder,energy,ymax):

        showInfo = 0
        # canvas
        a,b = 1,len(hx) + 1
        cv = TCanvas( 'cv', 'cv', a*900, b*700)
        cv.Divide(a,b)
        cv.SetRightMargin(0.3)
        cv.SetLeftMargin(0.2)
        cv.SetTopMargin(0.15)

        x1, y1, x2, y2 = 0.2, 0.98, 0.84, 0.9
        lab = mylabel(60)
        hy = []
        for i,hist in enumerate(hx):

            hy += [hist.Clone('cloon' +  hist.GetName())]
            cv.cd(i+1)
            if not i: dOpt = 'hist'
            else: dOpt = 'histsame'
            hist.SetFillColor(kBlue)
            hist.Draw(dOpt)

            hname = hist.GetName().split(rel + '_')[-1].replace('_', '.')
            if showInfo: print 'INFO: Plotting', hname

            lab.DrawLatex(x1, y1-0.1, hname)


        x1, y1, x2, y2 = 0.63,0.7,0.9,0.93
        thelegend = TLegend( x1, y1, x2, y2)
        thelegend.SetFillColor(0)
        thelegend.SetFillStyle(0)
        thelegend.SetLineColor(0)
        thelegend.SetTextSize(0.03)
        thelegend.SetShadowColor(0)
        thelegend.SetBorderSize(0)
        thelegend.SetTextSize(0.04)

        nentries = mt.GetEntries()

        for i,hist in enumerate(hy):

            cv.cd(len(hx)+1)
            pad = cv.GetPad(len(hx)+1)
            pad.SetLogy(1)
            if not i: dOpt = 'hist'
            else: dOpt = 'histsame'

            hist.Scale(1./nentries)
            hist.SetLineColor(bCol[i])
            hist.SetFillColor(bCol[i])
            hist.SetLineStyle(1)
            hist.SetFillStyle(3001+i)
            hist.GetYaxis().SetTitle('normalised entries')
            hist.GetYaxis().SetRangeUser(0.0006,ymax)
            hist.Draw(dOpt)

            hname = hist.GetName().split(rel + '_')[-1].replace('_', '.')
            if showInfo: print 'INFO: Plotting', hname

            thelegend.AddEntry(hist, hname, "fl")

        thelegend.Draw()
        lab.DrawLatex(0.45, y2+0.03, rel)
        lab.DrawLatex(0.2, y2-0.05, energy)
        pname  = wwwpath
        pname += subfolder + 'inelposition_'+rel+'.pdf'

        print('Saving file as ' + pname ) 
        cv.SaveAs(pname)
    # -----------------------------------------------------------------------------------
    # get the histograms
    for myset in sets:
        hx = []
        collsummary = myset[0] 
        cDict = collDict(collsummary)

        rfname = myset[1]
        print "Opening","."*33, rfname
        rf = TFile.Open(rfname)
        mt = rf.Get('particle')
        rel = rfname.split('/')[-1].split('.dat')[0]

        collgaps = myset[2]
        cgDict = collgapsDict(collgaps)
        print "and using","."*33, collgaps

        for collName in colls:

            try:
                collid = cDict[collName][0]
            except KeyError:
                print(collName, 'key not found')
                continue

            cut = 'icoll == ' + collid

            # get halfgap in mm as x and y are in mm.
            halfgap = float(cgDict[collName][5]) * 1000.
            var = ''
            if collName.count('TCTV'): var = 'TMath::Abs(y)'
            elif collName.count('TCTH'): var = 'TMath::Abs(x)'
            if var: var+= ' - ' + str(halfgap)

            va = 'x'
            print 'INFO: histgramming var', var

            # define histograms
            hname = 'hist_' + rel + '_' + collName.replace('.', '_')
            hx += [ TH1F(hname,hname,nbins, xmin, xmax) ]

            if showInfo: print 'INFO: will apply a cut of ', cut, 'to', hname
            mt.Project(hname, var, cut)
            if showInfo: print 'INFO: Have ', hx[-1].GetEntries(), ' entries in', hname, ' for ', collName

            xtitle, ytitle = 'depth [mm]', "entries"
            hx[-1].GetXaxis().SetLabelSize(0.05)
            hx[-1].GetYaxis().SetLabelSize(0.05)
            hx[-1].GetXaxis().SetTitle(xtitle)
            hx[-1].GetYaxis().SetTitle(ytitle)
            subfolder, energy, ymax = myset[3], myset[4], myset[5]
            doDraw(hx,subfolder,energy, ymax)
        
# ----------------------------------------------------------------------------





