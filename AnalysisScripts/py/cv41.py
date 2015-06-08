#!/usr/bin/python
#
# Mar 2015, rkwee
## -------------------------------------------------------------------------------
import pymadx
## -------------------------------------------------------------------------------
import ROOT, sys, os, time, math
from ROOT import *
import lossmap, helpers, array, random
from helpers import wwwpath, length_LHC, mylabel, gitpath, makeTGraph
from array import array
# -----------------------------------------------------------------------------------
def cv41():

    # twiss file
    tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/SixTrackConfig/6.5TeV/MED800/B1/twiss_lhcb1_med_new_thin_800.tfs')

    # locations of sampling the beam-size
    pointsName = ['TCTH.4L1.B1', 'TCTVA.4L1.B1']

    # number of randomly produced values per s location
    N = 1000

    emittance_norm = 3.75e-6
    gamma_rel = 6.5e3/0.938
    emittance_geo = emittance_norm/gamma_rel
    gauss1 = TF1('gauss1', 'exp(-0.5*(x**2))', -5.,5.)
    gauss2 = TF1('gauss2', 'exp(-0.5*(x**2))', -5.,5.)
    gauss3 = TF1('gauss3', 'exp(-0.5*(x**2))', -5.,5.)
    gauss4 = TF1('gauss4', 'exp(-0.5*(x**2))', -5.,5.)
    gauss5 = TF1('gauss5', 'exp(-0.5*(x**2))', -5.,5.)
    gauss6 = TF1('gauss6', 'exp(-0.5*(x**2))', -5.,5.)

    h1 = TH2F("f1","f1",200,-0.004,0.004,200,-0.1e-4,0.1e-4)
    h2 = TH2F("f2","f2",200,-0.2e-2,0.2e-2,200,-3.e-5,3.e-5)

    c1 = TGraph()
    c1.Set(N)
    c2 = TGraph()
    c2.Set(N)
    c3 = TGraph()
    c3.Set(N)
    c_y1 = TGraph()
    c_y1.Set(N)
    c_y2 = TGraph()
    c_y2.Set(N)
    c_y3 = TGraph()
    c_y3.Set(N)
    for name in pointsName:

        for i in range(N):

            row = tf.GetRowDict(name)
            betx = row['BETX']
            alfx = row['ALFX']
            bety = row['BETY']
            alfy = row['ALFY']

            sigx = math.sqrt(emittance_geo * betx)
            sigy = math.sqrt(emittance_geo * bety)
            big_x  = gauss1.GetRandom()
            big_xp = gauss2.GetRandom()
            small_xp = math.sqrt(emittance_geo/betx) * (big_xp - alfx*big_x)
            small_x  = big_x*sigx 
            h1.Fill(small_x,small_xp)

            phi = 2*random.random()*math.pi
            big_x  = math.cos(phi)
            big_xp = math.sin(phi)
            small_xp = math.sqrt(emittance_geo/betx) * (big_xp - alfx*big_x)
            small_x  = big_x*sigx 
            c1.SetPoint(i+1,small_x,small_xp)

            big_x  = 2*math.cos(phi)
            big_xp = 2*math.sin(phi)
            small_xp = math.sqrt(emittance_geo/betx) * (big_xp - alfx*big_x)
            small_x  = big_x*sigx 
            c2.SetPoint(i+1,small_x,small_xp)

            big_x  = 3*math.cos(phi)
            big_xp = 3*math.sin(phi)
            small_xp = math.sqrt(emittance_geo/betx) * (big_xp - alfx*big_x)
            small_x  = big_x*sigx 
            c3.SetPoint(i+1,small_x,small_xp)

            big_y  = gauss3.GetRandom()
            big_yp = gauss4.GetRandom()
            small_yp = math.sqrt(emittance_geo/bety) * (big_yp - alfy*big_y)
            small_y  = math.sqrt(bety*emittance_geo) * big_y
            h2.Fill(small_y,small_yp)

            phi = 2*random.random()*math.pi
            big_y  = math.cos(phi)
            big_yp = math.sin(phi)
            small_yp = math.sqrt(emittance_geo/bety) * (big_yp - alfy*big_y)
            small_y  = big_y*sigy 
            c_y1.SetPoint(i+1,small_y,small_yp)

            big_y  = 2*math.cos(phi)
            big_yp = 2*math.sin(phi)
            small_yp = math.sqrt(emittance_geo/bety) * (big_yp - alfy*big_y)
            small_y  = big_y*sigy
            c_y2.SetPoint(i+1,small_y,small_yp)

            big_y  = 3*math.cos(phi)
            big_yp = 3*math.sin(phi)
            small_yp = math.sqrt(emittance_geo/bety) * (big_yp - alfy*big_y)
            small_y  = big_y*sigy 
            c_y3.SetPoint(i+1,small_y,small_yp)


        a,b = 2,1
        cv = TCanvas( 'cv'+name, 'cv' + name, a*600, b*600)
        cv.Divide(a,b)
        cv.SetRightMargin(0.3)
        cv.SetLeftMargin(0.2)
        cv.SetTopMargin(0.15)
        xtitle, ytitle = 'x [m]', "x' [rad]"
        h1.GetXaxis().SetLabelSize(0.02)
        h1.GetYaxis().SetLabelSize(0.03)
        h1.GetZaxis().SetLabelSize(0.03)
        h1.GetXaxis().SetTitle(xtitle)
        h1.GetYaxis().SetTitle(ytitle)
        c1.SetMarkerSize(0.3)
        c1.SetMarkerColor(kRed+2)
        c2.SetMarkerSize(0.4)
        c2.SetMarkerColor(kRed)
        c3.SetMarkerSize(0.4)
        c3.SetMarkerColor(kRed-7)
        xtitle, ytitle = 'y [m]', "y' [rad]"
        h2.GetXaxis().SetLabelSize(0.02)
        h2.GetYaxis().SetLabelSize(0.03)
        h2.GetZaxis().SetLabelSize(0.03)
        h2.GetXaxis().SetTitle(xtitle)
        h2.GetYaxis().SetTitle(ytitle)
        c_y1.SetMarkerSize(0.3)
        c_y1.SetMarkerColor(kGreen+2)
        c_y2.SetMarkerSize(0.4)
        c_y2.SetMarkerColor(kGreen+1)
        c_y3.SetMarkerSize(0.4)
        c_y3.SetMarkerColor(kGreen-10)
        xtitle, ytitle = '#sigma_{x}', "#sigma_{y}"

        cv.cd(1)
        h1.Draw('colz')
        c1.Draw("SAMEP")
        c2.Draw("SAMEP")
        c3.Draw("SAMEP")
        cv.cd(2)
        h2.Draw('colz')
        c_y1.Draw("SAMEP")
        c_y2.Draw("SAMEP")
        c_y3.Draw("SAMEP")

        rel = 'gauss_' + name
        pname  = wwwpath
        subfolder = 'TCT/6.5TeV/beamgas/'
        pname += subfolder + 'twiss_b1'+rel+'.png'

        print('Saving file as ' + pname ) 
        cv.SaveAs(pname)
        
# ----------------------------------------------------------------------------





