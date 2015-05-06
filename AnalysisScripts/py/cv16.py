#!/usr/bin/python
#
# # depends on-the-fly on sDict funtion in fillTTree_dict.py # #
# Feb  2014, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
from helpers import workpath, wwwpath, mylabel
from createTTree import treeName
from fillTTree_dict import generate_sDict, nprimIN, nprimOUT, normOUT, normIN
## -------------------------------------------------------------------------------
def cv16():

    fNum   = workpath + 'results/results_ir1_4TeV_settings_from_TWISS_b2_nprim7825000_66.root'
    fDenom = workpath + 'results/results_ir1_4TeV_settings_from_TWISS_20MeV_b2_nprim5356000_66.root'
    subfolder = wwwpath + 'TCT/4TeV/compB2oldB2new/'
    lTextNum = 'B2 old'
    lTextDenom = 'B2 new'
    tagNum, tagDenom = 'BH_4TeV_B2', 'BH_4TeV_B2_20MeV'
    nColor, dColor = kCyan+1, kTeal

    fNum   = workpath + 'results/results_ir1_4TeV_settings_from_TWISS_20MeV_b1_nprim7964000_66.root'
    fDenom = workpath + 'results/results_ir1_4TeV_settings_from_TWISS_20MeV_b2_nprim5356000_66.root'
    subfolder = wwwpath + 'TCT/4TeV/compB1B2/'
    lTextNum = 'B1'
    lTextDenom = 'B2'
    tagNum, tagDenom = 'BH_4TeV_B1', 'BH_4TeV_B2'
    nColor, dColor = kOrange-3, kPink-7

    fDenom = workpath + 'results/results_ir1_4TeV_settings_from_TWISS_20MeV_b2_nprim5356000_66.root'
    fNum = workpath + 'results/results_beam-halo_3.5TeV-R1_D1_nprim2344800_66.root'
    subfolder = wwwpath + 'TCT/4TeV/compB2_3p5vs4TeV/'
    lTextNum = 'B2 3.5 TeV'
    lTextDenom = 'B2 4 TeV'
    tagNum, tagDenom = 'BH_3p5TeV', 'BH_4TeV_B2_20MeV'
    nColor, dColor = kOrange+1, kBlue-3

    fNum = workpath + 'runs/FL_TCT5LOUT_roundthinB1_2nd/results_hilumi_ir1_hybrid_b1_exp_20MeV_nprim5350000_30.root'
    fDenom = workpath + 'runs/FL_TCT5IN_roundthinB1_2nd/results_hilumi_ir1_hybrid_b1_exp_20MeV_nprim5319000_30.root'
    fDenom = workpath + 'runs/FL_TCT5LOUT_roundthinB1_2nd/results_hilumi_ir1_hybrid_b1_exp_20MeV_nprim5350000_30.root'
    fNum = workpath + 'runs/FL_TCT5IN_roundthinB1_2nd/results_hilumi_ir1_hybrid_b1_exp_20MeV_nprim5319000_30.root'
    subfolder = wwwpath + 'TCT/HL/relaxedColl/newScatt/fluka/comp/ratios/normalised/swap/'
    lTextNum = 'TCT4 only'
    lTextDenom = 'TCT5 in'
    lTextDenom = 'TCT4 only'
    lTextNum = 'TCT5 in'
    # tagNum, tagDenom = '_BH_HL_tct5otrdB1_20MeV', '_BH_HL_tct5inrdB1_20MeV'
    normNum, normDenom = normOUT/nprimOUT, normIN/nprimIN
    tagDenom, tagNum = '_BH_HL_tct5otrdB1_20MeV', '_BH_HL_tct5inrdB1_20MeV'
    normDenom, normNum = normOUT/nprimOUT, normIN/nprimIN
    dColor, nColor = kRed-4, kBlue-3

    rCol = kPink-7
    # need one file to generate sDict
    bbgFile = fNum
    print "Opening for sDict generation ...", bbgFile
    tag = tagNum
    norm = float(bbgFile.split('nprim')[-1].split('_')[0])
    tBBG = TFile.Open(bbgFile).Get(treeName)
    yrel = '/s'
    sDict = generate_sDict(tag, norm, tBBG, yrel)

    if not os.path.exists(subfolder):
        print 'making dir',  subfolder
        os.mkdir(subfolder)

    if fNum.count('B1') or fNum.count('b1'): Beam, beam = 'B1', 'b1'
    elif fNum.count('B2') or fNum.count('b2'): Beam, beam = 'B2','b2'
    else: Beam, beam = '', ''

    rfNum = TFile.Open(fNum)
    rfDenom = TFile.Open(fDenom)
    print 'opening as numerator', fNum
    print 'opening as denominator', fDenom

    print sDict.keys()

    msize = 0.05
    for skey in sDict.keys():

        if skey.count('XY'): continue
        if skey.startswith('Orig'): continue
        # if not skey.count('EkinNeutro'): continue

        cv = TCanvas( 'cv'+skey, 'cv'+skey, 100, 120, 600, 600 )

        x1, y1, x2, y2 = 0.65,0.75,0.9,0.9
        mlegend = TLegend( x1, y1, x2, y2)
        mlegend.SetFillColor(0)
        mlegend.SetFillStyle(0)
        mlegend.SetLineColor(0)
        mlegend.SetTextSize(0.055)
        mlegend.SetShadowColor(0)
        mlegend.SetBorderSize(0)

        p1 = TPad('p1'+skey,'p1'+skey,0.01,0.35,0.99,0.99)

        ymax = 2.
        XurMin, XurMax = -1, -1
        YurMin, YurMax = -1, -1
        dOptNum, dOptDenom = 'h', 'hsame'
        if skey.count('Ekin'): 
            p1.SetLogx(1)
            p1.SetLogy(1)
            ymax = 3.
            XurMin, XurMax = 0.02, 7.0e3

        if skey.count('En') or skey.startswith('Rad'): 
            p1.SetLogy(1)
            ymax = 3.
            XurMin, XurMax = 0.0, 600.

        if skey.count('Zcoor'):
            p1.SetLogy(1)
            p1.SetGridx(1)
            p1.SetGridy(1)

        p1.Draw()
        p1.SetBottomMargin(0.00)

        p2 = TPad('p2'+skey,'p2'+skey,0.01,0.01,0.99,.35)
        if skey.count('Ekin'):
            p2.SetLogx(1)

        p2.Draw()
        p2.SetTopMargin(0.00)
        p2.SetBottomMargin(0.25)

        p1.cd()
        hnameNum = skey
        hnameDenom = hnameNum.replace(tagNum, tagDenom)
        print 'plotting ratio of ', hnameNum, 'and', hnameDenom

        xtitle, ytitle = sDict[skey][9], sDict[skey][10]
        histNum  = rfNum.Get(hnameNum)
        histDenom  = rfDenom.Get(hnameDenom)

        integralNum = histNum.Integral()
        integralDenom = histDenom.Integral()

        ratioInts = integralNum/integralDenom
        print "ratio int", ratioInts, ' ', hnameNum

        if hnameNum.count('Rad'):
            histNum.Rebin()
            histDenom.Rebin()
            # pass

        histNum.GetXaxis().SetTitle(xtitle)
        histNum.GetYaxis().SetTitle(ytitle)
        histDenom.GetXaxis().SetTitle(xtitle)
        histDenom.GetYaxis().SetTitle(ytitle)

        histNum.SetLineWidth(3)
        histNum.SetLineStyle(2)
        histDenom.SetLineColor(dColor)
        histNum.SetLineColor(nColor)
        histDenom.SetLineColor(dColor)
        histNum.SetMarkerColor(nColor)
        histDenom.SetMarkerColor(dColor)
        histNum.SetMarkerStyle(21)
        histDenom.SetMarkerStyle(20)
        histDenom.SetMarkerSize(msize)
        histNum.SetMarkerSize(msize)
        print normNum, normDenom
        histNum.Scale(1./normNum)
        histDenom.Scale(1./normDenom)

        histNum.GetXaxis().SetLabelSize(0.04)
        histDenom.GetXaxis().SetLabelSize(0.04)

        if XurMin != -1:
            histNum.GetXaxis().SetRangeUser(XurMin,XurMax)

        if YurMin != -1:
            histNum.GetXaxis().SetRangeUser(YurMin,YurMax)

        if dOptNum.count("same"):
            histDenom.Draw(dOptDenom)
            histNum.Draw(dOptNum)
        else:
            histNum.Draw(dOptNum)
            histDenom.Draw(dOptDenom)


        mlegend.AddEntry(histNum, lTextNum, "l")
        mlegend.AddEntry(histDenom, lTextDenom, "l")
        mlegend.Draw()

        lab = mylabel(42)
        lab.DrawLatex(0.56, 0.955, sDict[skey][6])
        lab = mylabel(62)
        lab.SetTextSize(0.055)
        lab.DrawLatex(.8,y1-0.07,Beam)

        hnameRatio = 'ratio'+hnameNum
        hRatio = histNum.Clone(hnameRatio)

        hRatio.Divide(histNum, histDenom, 1, 1)
        hRatio.SetLineStyle(1)
        hRatio.SetLineWidth(2)
        hRatio.SetLineColor(rCol)
        hRatio.SetMarkerColor(rCol)
        hRatio.SetMarkerStyle(22)
        hRatio.SetMarkerSize(msize)

        l = TLine()
        l.SetLineWidth(1)
        l.SetLineColor(kGray) #kSpring
        if XurMin == -1:
            XurMin = hRatio.GetBinLowEdge(1)
            XurMax = hRatio.GetBinLowEdge( hRatio.GetNbinsX()+1 )

        p2.cd()

        drawOpt = 'pe'
        if hnameNum.count('Rad') or hRatio.GetMaximum()>200:
           # hRatio.GetYaxis().SetRangeUser(0.1,2.6)
            pass

        hRatio.GetXaxis().SetLabelSize(0.1)
        hRatio.GetYaxis().SetLabelSize(0.08)
        hRatio.GetYaxis().SetTitleOffset(0.6)
        hRatio.GetYaxis().SetTitleSize(0.08)
        hRatio.GetXaxis().SetTitleSize(0.08)
        hRatio.Draw()
        hRatio.GetYaxis().SetTitle('ratio ' + lTextNum + '/' + lTextDenom + " ")
        l.DrawLine(XurMin,1,XurMax,1)
        pname = subfolder+hnameRatio.split('_')[0]+'.pdf'

        print pname
        cv.SaveAs(pname)
