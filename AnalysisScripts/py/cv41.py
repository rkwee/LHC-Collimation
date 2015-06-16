#!/usr/bin/python
#
# Mar 2015, rkwee
## -------------------------------------------------------------------------------
import pymadx
## -------------------------------------------------------------------------------
import ROOT, sys, os, time, math
from ROOT import *
import lossmap, helpers, array, random
from helpers import wwwpath, length_LHC, mylabel, gitpath, length_LHC
from array import array
# -----------------------------------------------------------------------------------
def cv41():

    # twiss file
    tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/SixTrackConfig/6.5TeV/MED800/B1/twiss_lhcb1_med_new_thin_800.tfs')

    # locations of sampling the beam-size
    pointsName = ['TCTH.4L1.B1', 'TCTVA.4L1.B1', 'MBRC.4L1.B1','MQXA.1L1..2', 'MQXB.B2L1..16', 'BPTX.5L1.B1', "MB.A8L1.B1..2", "MCD.9L1.B1", "MCBCH.10L1.B1", "MB.C13L1.B1..2"]

    # number of randomly produced values per s location
    N = 500

    # canvas
    a,b = 2,len(pointsName)
    cv = TCanvas( 'cv', 'cv', a*600, b*600)
    cv.Divide(a,b)
    cv.SetRightMargin(0.3)
    cv.SetLeftMargin(0.2)
    cv.SetTopMargin(0.15)

    emittance_norm = 3.75e-6
    gamma_rel = 6.5e3/0.938
    emittance_geo = emittance_norm/gamma_rel
    gauss1 = TF1('gauss1', 'exp(-0.5*(x**2))', -5.,5.)
    gauss2 = TF1('gauss2', 'exp(-0.5*(x**2))', -5.,5.)
    gauss3 = TF1('gauss3', 'exp(-0.5*(x**2))', -5.,5.)
    gauss4 = TF1('gauss4', 'exp(-0.5*(x**2))', -5.,5.)
    gauss5 = TF1('gauss5', 'exp(-0.5*(x**2))', -5.,5.)
    gauss6 = TF1('gauss6', 'exp(-0.5*(x**2))', -5.,5.)

    j = 1
    hx, c_x1, c_x2, c_x3, hy, c_y1, c_y2, c_y3 = [],[],[],[], [],[],[],[]
    for name in pointsName:

        hx += [ TH2F("f1" + name,"f1" + name,200,-0.004,0.004,200,-0.1e-4,0.1e-4) ]
        hy += [ TH2F("f2" + name,"f2" + name,200,-0.2e-2,0.2e-2,200,-3.e-5,3.e-5) ]

        c_x1 += [ TGraph() ]
        c_x1[-1].Set(N)
        c_x2 += [ TGraph() ]
        c_x2[-1].Set(N)
        c_x3 += [ TGraph() ]
        c_x3[-1].Set(N)
        c_y1 += [ TGraph() ]
        c_y1[-1].Set(N)
        c_y2 += [ TGraph() ]
        c_y2[-1].Set(N)
        c_y3 += [ TGraph() ]
        c_y3[-1].Set(N)

        row = tf.GetRowDict(name)
        betx = row['BETX']
        alfx = row['ALFX']
        bety = row['BETY']
        alfy = row['ALFY']
        s    = str(row['S']-length_LHC)

        sigx = math.sqrt(emittance_geo * betx)
        sigy = math.sqrt(emittance_geo * bety)

        for i in range(N):

            big_x  = gauss1.GetRandom()
            big_xp = gauss2.GetRandom()
            small_xp = math.sqrt(emittance_geo/betx) * (big_xp - alfx*big_x)
            small_x  = big_x*sigx 
            hx[-1].Fill(small_x,small_xp)

            phi = 2*random.random()*math.pi
            big_x  = math.cos(phi)
            big_xp = math.sin(phi)
            small_xp = math.sqrt(emittance_geo/betx) * (big_xp - alfx*big_x)
            small_x  = big_x*sigx 
            c_x1[-1].SetPoint(i+1,small_x,small_xp)

            big_x  = 2*math.cos(phi)
            big_xp = 2*math.sin(phi)
            small_xp = math.sqrt(emittance_geo/betx) * (big_xp - alfx*big_x)
            small_x  = big_x*sigx 
            c_x2[-1].SetPoint(i+1,small_x,small_xp)

            big_x  = 3*math.cos(phi)
            big_xp = 3*math.sin(phi)
            small_xp = math.sqrt(emittance_geo/betx) * (big_xp - alfx*big_x)
            small_x  = big_x*sigx 
            c_x3[-1].SetPoint(i+1,small_x,small_xp)

            big_y  = gauss3.GetRandom()
            big_yp = gauss4.GetRandom()
            small_yp = math.sqrt(emittance_geo/bety) * (big_yp - alfy*big_y)
            small_y  = math.sqrt(bety*emittance_geo) * big_y
            hy[-1].Fill(small_y,small_yp)

            phi = 2*random.random()*math.pi
            big_y  = math.cos(phi)
            big_yp = math.sin(phi)
            small_yp = math.sqrt(emittance_geo/bety) * (big_yp - alfy*big_y)
            small_y  = big_y*sigy 
            c_y1[-1].SetPoint(i+1,small_y,small_yp)

            big_y  = 2*math.cos(phi)
            big_yp = 2*math.sin(phi)
            small_yp = math.sqrt(emittance_geo/bety) * (big_yp - alfy*big_y)
            small_y  = big_y*sigy
            c_y2[-1].SetPoint(i+1,small_y,small_yp)

            big_y  = 3*math.cos(phi)
            big_yp = 3*math.sin(phi)
            small_yp = math.sqrt(emittance_geo/bety) * (big_yp - alfy*big_y)
            small_y  = big_y*sigy 
            c_y3[-1].SetPoint(i+1,small_y,small_yp)

        cStyle = 6
        xtitle, ytitle = 'x [m]', "x' [rad]"
        hx[-1].GetXaxis().SetLabelSize(0.02)
        hx[-1].GetYaxis().SetLabelSize(0.03)
        hx[-1].GetZaxis().SetLabelSize(0.03)
        hx[-1].GetXaxis().SetTitle(xtitle)
        hx[-1].GetYaxis().SetTitle(ytitle)
        c_x1[-1].SetMarkerSize(0.3)
        c_x1[-1].SetMarkerColor(kRed+2)
        c_x2[-1].SetMarkerSize(0.3)
        c_x2[-1].SetMarkerColor(kRed)
        c_x3[-1].SetMarkerSize(0.3)
        c_x3[-1].SetMarkerColor(kRed-7)
        c_x1[-1].SetMarkerStyle(cStyle)
        c_x2[-1].SetMarkerStyle(cStyle)
        c_x3[-1].SetMarkerStyle(cStyle)
        xtitle, ytitle = 'y [m]', "y' [rad]"
        hy[-1].GetXaxis().SetLabelSize(0.02)
        hy[-1].GetYaxis().SetLabelSize(0.03)
        hy[-1].GetZaxis().SetLabelSize(0.03)
        hy[-1].GetXaxis().SetTitle(xtitle)
        hy[-1].GetYaxis().SetTitle(ytitle)
        c_y1[-1].SetMarkerSize(0.3)
        c_y1[-1].SetMarkerColor(kGreen+2)
        c_y1[-1].SetMarkerStyle(cStyle)
        c_y2[-1].SetMarkerSize(0.3)
        c_y2[-1].SetMarkerStyle(cStyle)
        c_y2[-1].SetMarkerColor(kGreen+1)
        c_y3[-1].SetMarkerSize(0.3)
        c_y3[-1].SetMarkerStyle(cStyle)
        c_y3[-1].SetMarkerColor(kGreen-10)
        xtitle, ytitle = '#sigma_{x}', "#sigma_{y}"
        m,n = j*2-1,j*2
        print m,n

        lab = mylabel(42)
        cv.cd(m)
        hx[-1].Draw('colz')
        c_x1[-1].Draw("SAMEP")
        c_x2[-1].Draw("SAMEP")
        c_x3[-1].Draw("SAMEP")
        lab.DrawLatex(0.3, 0.98, name + ' ('+s+')')

        cv.cd(n)
        hy[-1].Draw('colz')
        c_y1[-1].Draw("SAMEP")
        c_y2[-1].Draw("SAMEP")
        c_y3[-1].Draw("SAMEP")

        lab.DrawLatex(0.26, 0.98, name + ' (' + row["KEYWORD"] + ')')

        j+=1

    rel = '_gauss' 
    pname  = wwwpath
    subfolder = 'TCT/6.5TeV/beamgas/'
    pname += subfolder + 'twiss_b1'+rel+'.png'

    print('Saving file as ' + pname ) 
    cv.SaveAs(pname)
        
# ----------------------------------------------------------------------------





