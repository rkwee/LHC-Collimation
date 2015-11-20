#!/usr/bin/python
#
# June 2015, rkwee
## -------------------------------------------------------------------------------
import ROOT
from ROOT import TH1F, TCanvas
import helpers
from helpers import wwwpath, length_LHC, mylabel
# from cv54
# -----------------------------------------------------------------------------------
def cv57():


    # number of randomly produced values per s location
    myfile = '/afs/cern.ch/project/lhc_mib/beamgas/4TeV_beamsize/runBG_UVcorr/ir1_4TeV_settings_from_TWISS_20MeV_b1_nprim2952500_91'

    hname, nbins, xmin, xmax = "spositions", 519790, 0.5, 519790.5

    histspos   = TH1F(hname, hname, nbins, xmin, xmax)
    histspos.GetXaxis().SetTitle('s [cm]')
    histspos.GetYaxis().SetTitle('entries')

    with open(myfile) as mf:

        for line in mf:

            # format is: XIN(NIN), YIN(NIN), ZIN(NIN), UIN(NIN), VIN(NIN),tIn(NIN)
            histspos.Fill(float(line.rstrip()))



    a,b = 1,1
    cv = TCanvas( 'cv'+hname, 'cv'+hname, 10, 10, a*900, b*600) 
    cv.Divide(a,b)

    histspos.Draw('p')
    pname = '~/public/www/HL-LCH/TCT/4TeV/beamgas/randomID.png'

    cv.SaveAs(pname)



# ----------------------------------------------------------------------------





