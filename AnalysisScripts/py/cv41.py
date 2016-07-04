#!/usr/bin/python
#
# Mar 2015, rkwee
## -------------------------------------------------------------------------------
import pymadx
## -------------------------------------------------------------------------------
import ROOT, sys, os, time, math
from ROOT import *
import helpers, array, random
from helpers import wwwpath, length_LHC, mylabel, gitpath, length_LHC
from array import array
# -----------------------------------------------------------------------------------
def cv41():

    # twiss file
    #tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/SixTrackConfig/6.5TeV/MED800/B1/twiss_lhcb1_med_new_thin_800.tfs')
    #tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/runs/checkTrajectory6500GeV/4TeV/twiss_b2_mym.data') # erased
    # tf = pymadx.Tfs("/afs/cern.ch/user/r/rbruce/public/for_regina/MADX_4TeV/twiss_b1.data.thin") # alfa missing
    #    tf = pymadx.Tfs("/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/SixTrackConfig/4TeV/beamgas/twiss_b4.data.thin")
    tf = pymadx.Tfs("/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/SixTrackConfig/4TeV/beamgas/twiss_4tev_b1.data")

    # locations of sampling the beam-size
    # - passen nicht mehr auf tfs
    pointsName = ['TCTH.4L1.B1', 'TCTVA.4L1.B1', 'MBRC.4L1.B1','MQXA.1L1..2', 'MQXB.B2L1..16', 'BPTX.5L1.B1', "MB.A8L1.B1..2", "MCD.9L1.B1", "MCBCH.10L1.B1", "MB.C13L1.B1..2"]
    #pointsName = ["MYM.S"]
    #pointsName = ['TCTH.4L1.B1']

    energy = "6.5TeV"
    # number of randomly produced values per s location
    N = 1000

    doWrite = 1

    # canvas
    a,b = 2,len(pointsName)
    cv = TCanvas( 'cv', 'cv', a*600, b*600)
    cv.Divide(a,b)
    cv.SetRightMargin(0.3)
    cv.SetLeftMargin(0.2)
    cv.SetTopMargin(0.1)

    emittance_norm = 3.5e-6
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

        print '-'*55, name

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
        s    = str(row['S'])

        sigx = math.sqrt(emittance_geo * betx)
        sigy = math.sqrt(emittance_geo * bety)

        foutname = name + '_N' + str(N) + '.txt'
        if doWrite: fot = open(foutname, 'w')

        for i in range(N):

            # histogram 
            big_x  = gauss1.GetRandom()
            big_xp = gauss2.GetRandom()
            small_xp = math.sqrt(emittance_geo/betx) * big_xp - alfx*big_x/math.sqrt(betx * emittance_geo)
            small_x  = big_x*sigx 
            hx[-1].Fill(small_x,small_xp)

            line = str(i) + ' ' + str(small_x) + ' ' + str(small_xp) + ' '

            # 3 contour lines
            phi = 2*random.random()*math.pi
            big_x  = math.cos(phi)
            big_xp = math.sin(phi)
            small_xp = math.sqrt(emittance_geo/betx) * big_xp - alfx*big_x/math.sqrt(betx * emittance_geo)
            small_x  = big_x*sigx 
            c_x1[-1].SetPoint(i+1,small_x,small_xp)

            big_x  = 2*math.cos(phi)
            big_xp = 2*math.sin(phi)
            small_xp = math.sqrt(emittance_geo/betx) * big_xp - alfx*big_x/math.sqrt(betx * emittance_geo)
            small_x  = big_x*sigx 
            c_x2[-1].SetPoint(i+1,small_x,small_xp)

            big_x  = 3*math.cos(phi)
            big_xp = 3*math.sin(phi)
            small_xp = math.sqrt(emittance_geo/betx) * big_xp - alfx*big_x/math.sqrt(betx * emittance_geo)
            small_x  = big_x*sigx 
            c_x3[-1].SetPoint(i+1,small_x,small_xp)

            big_y  = gauss3.GetRandom()
            big_yp = gauss4.GetRandom()
            small_yp = math.sqrt(emittance_geo/bety) * big_yp - alfy*big_y/math.sqrt(emittance_geo*bety)
            small_y  = math.sqrt(bety*emittance_geo) * big_y
            hy[-1].Fill(small_y,small_yp)

            line  += str(small_y) + ' ' + str(small_yp) + ' \n'
            if doWrite: fot.write(line)

            phi = 2*random.random()*math.pi
            big_y  = math.cos(phi)
            big_yp = math.sin(phi)
            small_yp = math.sqrt(emittance_geo/bety) * big_yp - alfy*big_y/math.sqrt(emittance_geo*bety)
            small_y  = big_y*sigy 
            c_y1[-1].SetPoint(i+1,small_y,small_yp)

            big_y  = 2*math.cos(phi)
            big_yp = 2*math.sin(phi)
            small_yp = math.sqrt(emittance_geo/bety) * big_yp - alfy*big_y/math.sqrt(emittance_geo*bety)
            small_y  = big_y*sigy
            c_y2[-1].SetPoint(i+1,small_y,small_yp)

            big_y  = 3*math.cos(phi)
            big_yp = 3*math.sin(phi)
            small_yp = math.sqrt(emittance_geo/bety) * big_yp - alfy*big_y/math.sqrt(emittance_geo*bety)
            small_y  = big_y*sigy 
            c_y3[-1].SetPoint(i+1,small_y,small_yp)



        print 'wrote', foutname
        cStyle = 6
        ms = 0.01
        xtitle, ytitle = 'x [m]', "x' [rad]"
        hx[-1].GetXaxis().SetLabelSize(0.03)
        hx[-1].GetYaxis().SetLabelSize(0.03)
        hx[-1].GetZaxis().SetLabelSize(0.03)
        hx[-1].GetXaxis().SetTitle(xtitle)
        hx[-1].GetYaxis().SetTitle(ytitle)
        c_x1[-1].SetMarkerSize(ms)
        c_x1[-1].SetMarkerColor(kRed+2)
        c_x2[-1].SetMarkerSize(ms)
        c_x2[-1].SetMarkerColor(kRed)
        c_x3[-1].SetMarkerSize(ms)
        c_x3[-1].SetMarkerColor(kRed-7)
        c_x1[-1].SetMarkerStyle(cStyle)
        c_x2[-1].SetMarkerStyle(cStyle)
        c_x3[-1].SetMarkerStyle(cStyle)
        xtitle, ytitle = 'y [m]', "y' [rad]"
        hy[-1].GetXaxis().SetLabelSize(0.03)
        hy[-1].GetYaxis().SetLabelSize(0.03)
        hy[-1].GetZaxis().SetLabelSize(0.03)
        hy[-1].GetXaxis().SetTitle(xtitle)
        hy[-1].GetYaxis().SetTitle(ytitle)
        c_y1[-1].SetMarkerSize(ms)
        c_y1[-1].SetMarkerColor(kGreen+2)
        c_y1[-1].SetMarkerStyle(cStyle)
        c_y2[-1].SetMarkerSize(ms)
        c_y2[-1].SetMarkerStyle(cStyle)
        c_y2[-1].SetMarkerColor(kGreen+1)
        c_y3[-1].SetMarkerSize(ms)
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
        lab.DrawLatex(0.3, 0.85, name + ' ('+s+')')

        cv.cd(n)
        hy[-1].Draw('colz')
        c_y1[-1].Draw("SAMEP")
        c_y2[-1].Draw("SAMEP")
        c_y3[-1].Draw("SAMEP")

        #lab.DrawLatex(0.26, 0.87, name + ' (' + row["KEYWORD"] + ')')

        j+=1

    rel = '_gauss' 
    pname  = wwwpath
    subfolder = "TCT/"+energy+"/beamgas/"
    pname += subfolder + 'twiss'+rel+'_'+energy+'.pdf'

    print('Saving file as ' + pname ) 
    cv.SaveAs(pname)
        
# ----------------------------------------------------------------------------





