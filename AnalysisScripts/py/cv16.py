#!/usr/bin/python
#
# # depends on-the-fly on sDict funtion in fillTTree_dict.py # #
# Feb  2014, rkwee
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
from helpers import *
from createTTree import treeName
from fillTTree_dict import generate_sDict, nprimIN, nprimOUT, normOUT, normIN, calcR12m
## -------------------------------------------------------------------------------

def cv16():
    thispath = '/Users/rkwee/Documents/RHUL/work/HL-LHC/runs/TCT/'
    
    # DONT USE
    # --- norm4TeVB1  = 1380 *1.4e11/360000 * (265+95.)/(61832091+12732234) # 98 TCTH 65 TCTV, 6.37e6 6.1e6 primaries  
    # --- norm4TeVB2 = 1380 * 1.4e11/360000 * (521.0+454.0)/(69021155+63014399)
    #norm4TeVB1 = 1380 *1.4e11/360000 * (65+98.)/(6.1e6+6.37e6) # 98 TCTH 65 TCTV, 6.37e6 6.1e6 primaries  
    #norm4TeVB2 = 1380 * 1.4e11/360000 * (124.0+115)/(6.4e6+6.3e6)

    # old scatt
    norm4TeVB1oldHalo = 1380 *1.4e11/360000 * (265+95.)/(61832091+12732234) # 98 TCTH 65 TCTV, 6.37e6 6.1e6 primaries  
    norm4TeVB2oldHalo = 1380 * 1.4e11/360000 * (521.0+454.0)/(69021155+63014399)

    # new halo (new scatt)
    norm4TeVB1newHalo = 1380 *1.4e11/360000 * 0.5*(622.0/60948098 + 930.0/64935501) # = 1.2263654213882985e-05 with factor 0.5
    norm4TeVB1newHalo50h = 1380 *1.4e11/180000 * 0.5*(622.0/60948098 + 930.0/64935501) # = 1.2263654213882985e-05 with factor 0.5
    # IR5: (866+92 + 170.0+456 )/(60948098 + 64935501) = 1.26e-5,>>> (866+92)/60948098 + (170.0+456)/64935501 = 9.64e-06

    norm4TeVB2newHalo = 1380 * 1.4e11/360000 * (1179.0/59198135 +967/56887051.)/2.  
    # IR5: (1893.0 + 135)/(59198135 +56887051) = 1.75e-5, >>> 1893.0/59198135 +135/56887051. = 3.435e-05

    norm6500GeVB1Old = 2748 * 1.2e11/360000 *0.5*(739./53731448 +(312+273.)/52806720) # 1.24e-5
    norm6500GeVB2Old = 2748 * 1.2e11/360000 *0.5*(779./43692659+773./52962459.) # new 1.62e-5

    norm6500GeVB1 = 2041 * 1.12e11/360000 *0.5*(739./53731448 +(312+273.)/52806720) # 1.24e-5
    norm6500GeVB2 = 2041 * 1.12e11/360000 *0.5*(779./43692659+773./52962459.) # new 1.62e-5

    # python /afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/AnalysisScripts/py/collsummary.py -f 6.5TeV_vHaloB2_h5/coll_summary_6.5TeV_vHaloB2_h5.dat -c TCT*R5
    # IR5 B1: h:( 53754939.0 protons on IR7 primaries, 346.0 protons on TCT*L5.B1), v(52838656.0 on primaries IR7,  408.0 protons on TCTL5)
    # .5*( 346.0/53754939.0 + 408.0/52838656.0 ) = 7.0791187088930279e-06
    # IR5 B2: h:( 43718962.0 IR7,  302.0 protons ), v(53000835.0, 106.0 protons. )
    # 0.5 * (302.0/43718962.0 + 106.0/53000835.0) = 4.4538612500709768e-06

    run1iniFlux = 1380 * 1.5e11/180000. # from Roderiks NIM paper: 2010: 368 up to 2011 1380, lifetime only 50h!
    norm3500GeVB1 = 1.02813e-5 * run1iniFlux # from http://bbgen.web.cern.ch/bbgen/bruce/fluka_beam-halo_3.5TeV/flukaIR15.html
    norm3500GeVB2 = 2.25625e-5 * run1iniFlux # from http://bbgen.web.cern.ch/bbgen/bruce/fluka_beam-halo_3.5TeV/flukaIR15.html

    # fNum   = workpath + 'results/results_ir1_4TeV_settings_from_TWISS_b2_nprim7825000_66.root'
    # fDenom = workpath + 'results/results_ir1_4TeV_settings_from_TWISS_20MeV_b2_nprim5356000_66.root'
    # subfolder = wwwpath + 'TCT/4TeV/compB2oldB2new/'
    # lTextNum = 'B2 old'
    # lTextDenom = 'B2 new'
    # tagNum, tagDenom = 'BH_4TeV_B2', 'BH_4TeV_B2_20MeV'
    # nColor, dColor = kCyan+1, kTeal

    # fNum = workpath + 'runs/4TeV_Halo/results_ir1_4TeV_settings_from_TWISS_20MeV_b2_nprim7945000_66.root'
    # #fDenom   = workpath + 'runs/4TeV_Halo/results_ir1_4TeV_settings_from_TWISS_20MeV_b1_nprim7964000_66.root'
    # subfolder = wwwpath + 'TCT/4TeV/tctimpacts/compNewScattB1/'
    # fDenom = projectpath + 'bgChecks2/FL_NewHalo_4TeV_B2/results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b2_nprim6914000_30.root'
    # #fNum   = projectpath + 'bgChecks2/FL_NewHalo_4TeV_B1/results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b1_nprim6904000_30.root'
    # normDenom, normNum = 1., 1.
    # lTextNum = 'B2 old'
    # lTextDenom = 'B2 new'
    # tagDenom, tagNum = '_BH_4TeV_B2_20MeV', '_BH_4TeV_B2_20MeV'
    # nColor, dColor = kOrange-3, kPink-6
    # yrel = '/TCT hit'
    # # yrel = '/s'

    # fNum = projectpath + 'bgChecks2/FL_NewHalo_4TeV_B2/results_ir1_4TeV_settings_from_TWISS_20MeV_b2_nprim6914000_30.root'
    # fDenom   = workpath + 'runs/4TeV_Halo/results_ir1_4TeV_settings_from_TWISS_20MeV_b2_nprim7945000_66.root'
    # subfolder = wwwpath + 'TCT/4TeV/tctimpacts/compOldNewScattB2/perTCThit/'
    # lTextNum = 'new'
    # lTextDenom = 'old'
    # normDenom, normNum = 1./norm4TeVB2oldHalo, 1./norm4TeVB2newHalo
    # normDenom, normNum = 1., 1.
    # tagDenom, tagNum = '_BH_4TeV_B2_20MeV', '_BH_4TeV_B2_20MeV'
    # nColor, dColor = kOrange-3, kPink+8
    # yrel = '/s'
    # yrel = '/TCT hit'

    # fNum = projectpath + 'bgChecks2/FL_NewHalo_4TeV_B2/results_ir1_4TeV_settings_from_TWISS_20GeV_b2_nprim6914000_30.root'
    # fDenom = projectpath + 'bgChecks2/FL_NewHalo_4TeV_B2_20GeV/results_ir1_4TeV_settings_from_TWISS_20GeV_b2_nprim90520000_30.root'
    # subfolder = wwwpath + 'TCT/4TeV/tctimpacts/newScatt/compB2tail/'
    # lTextNum = 'all energies'
    # lTextDenom = '20 GeV tail'
    # normDenom, normNum = 1., 1.
    # tagDenom, tagNum = '_BH_4TeV_B2_20GeV', '_BH_4TeV_B2_20MeV'
    # nColor, dColor = kOrange-3, kPink+2
    # yrel = '/TCT hit'

    # fNum = projectpath + 'bgChecks2/FL_NewHalo_4TeV_B1/results_ir1_4TeV_settings_from_TWISS_20MeV_b1_nprim6904000_30.root'
    # fDenom = projectpath + 'bgChecks2/FL_NewHalo_4TeV_B1_20GeV/results_ir1_4TeV_settings_from_TWISS_20GeV_b1_nprim125170000_30.root'
    # subfolder = wwwpath + 'TCT/4TeV/tctimpacts/newScatt/compB1tail/'
    # lTextNum = 'all energies'
    # lTextDenom = '20 GeV tail'
    # normDenom, normNum = 1., 1.
    # tagDenom, tagNum = '_BH_4TeV_B1_20GeV', '_BH_4TeV_B1_20MeV'
    # nColor, dColor = kOrange-3, kPink-2
    # yrel = '/TCT hit'

    # fNum = projectpath + 'bgChecks2/FL_NewHalo_4TeV_B1/results_ir1_4TeV_settings_from_TWISS_20MeV_b1_nprim6904000_30.root'
    # fDenom   = workpath + 'runs/4TeV_Halo/results_ir1_4TeV_settings_from_TWISS_20MeV_b1_nprim7964000_66.root'
    # subfolder = wwwpath + 'TCT/4TeV/tctimpacts/compOldNewScattB1/perTCThit/'
    # lTextNum = 'new'
    # lTextDenom = 'old'
    # normDenom, normNum = 1./norm4TeVB1oldHalo, 1./norm4TeVB1newHalo
    # normDenom, normNum = 1., 1.
    # tagDenom, tagNum = '_BH_4TeV_B1_20MeV', '_BH_4TeV_B1_20MeV'
    # nColor, dColor = kOrange-3, kPink-2
    # yrel = '/s'
    # yrel = '/TCT hit'

    

    # fDenom = workpath + 'runs/3.5TeV/results_beam-halo_3.5TeV-R1_D1_20MeV_b2_nprim2344800_66.root'
    # fDenom="/Users/rkwee/Documents/RHUL/work/data/3p5TeV/results_beam-halo_3.5TeV-R1_D1_20MeV_b2_nprim2344800_66.root"
    # fNum=thispath+"results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b2_nprim6914000_30.root"
    # subfolder = wwwpath + 'TCT/4TeV/compB2_3p5vs4TeV/perTCThit/'
    # lTextNum, lTextDenom = '4 TeV w/ x-ing', '3.5 TeV w/o x-ing'
    # # #normNum, normDenom = 1./norm4TeVB2, 1./(norm3500GeVB2)
    # normNum, normDenom = 1., 1.
    # tagDenom, tagNum = '_BH_3p5TeV_B2_20MeV', '_BH_4TeV_B2_20MeV'
    # subfolder = wwwpath + 'TCT/4TeV/compB2_3p5vs4TeV/' 
    # nColor, dColor = kOrange+1, kBlue-3
    # yrel = '/TCT hit'

    # subfolder = wwwpath + 'TCT/4TeV/compB2_3p5vs4TeV/'
    # normDenom, normNum = 1.,1.     
    # yrel = '/TCT hit'

    # # - comparison BH 3.5 vs 4 TeV
    # # #-- OLD SIM    # fNum = workpath + 'data/4TeV/results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b1_nprim7964000_66.root'
    # fNum = projectpath + 'bgChecks2/FL_NewHalo_4TeV_B1/results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b1_nprim6904000_30.root'    
    # fDenom =  projectpath + 'bbgen/3.5TeV/results_beam-halo_3.5TeV-L1_20MeV_b1_nprim1731200_66.root'

    # fNum = thispath + 'results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b1_nprim6904000_30.root'
    # fDenom =  "/Users/rkwee/Documents/RHUL/work/data/3p5TeV/results_beam-halo_3.5TeV-L1_20MeV_b1_nprim1731200_66.root"
    # lTextNum, lTextDenom = '4 TeV', '3.5 TeV'
    # # normNum, normDenom, yrel = 1./norm4TeVB1newHalo50h, 1./norm3500GeVB1, '/s'
    # normNum, normDenom, yrel = 1.,1., '/TCT hit'
    # tagDenom, tagNum = '_BH_3p5TeV_B1_20MeV', '_BH_4TeV_B1_20MeV'
    # nColor, dColor = kOrange+3, kMagenta-3
    # subfolder = wwwpath + 'TCT/compBHB1_3p5vs4TeV/perTCThit/'
    

    # # # comparison BG 3.5 vs 4 TeV 
    # # fNum = projectpath + '4TeVBGnoBS/results_beam-gas_4TeV-IR1_to_arc_20MeV_cutoff_100M_nprim7283044_66.root' # erased, produce new....
    # # fDenom = projectpath + '4TeVBGnoBS/results_beam_gas_3.5TeV_IR1_to_arc_20MeV_100M_nprim7660649_66.root'
    # fNum = thispath + 'results_beam-gas_4TeV-IR1_to_arc_20MeV_cutoff_100M_nprim7283044_66.root' # erased, produce new....
    # fDenom = thispath + 'results_beam_gas_3.5TeV_IR1_to_arc_20MeV_100M_nprim7660649_66.root'
    # subfolder = wwwpath + 'TCT/4TeV/compBG_3p5_vs_4TeV/'
    # subfolder =  '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/4TeV/compBG_3p5_vs_4TeV/perBGint/'
    # lTextDenom, lTextNum = '3.5 TeV w/o x-ing', '4 TeV w/ x-ing'
    # normDenom, normNum = 1.,1.
    # tagDenom, tagNum = '_BG_3p5TeV_20MeV', '_BG_4TeV_20MeV'
    # nColor, dColor = kOrange-1, kRed-2
    # yrel = '/inel.BG int.'


    # # # comparison BG 3.5 vs 4 TeV with beamsize    
    # fNum = thispath + 'results_ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67.root'
    # fDenom = thispath + 'results_beam_gas_3.5TeV_IR1_to_arc_20MeV_100M_nprim7660649_66.root'
    # subfolder = wwwpath + 'TCT/4TeV/compBG_3p5_vs_4TeV/'
    # subfolder =  '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/4TeV/compBG_3p5_vs_4TeV/perBGint_bs/'
    # lTextDenom, lTextNum = '3.5 TeV w/o x-ing', '4 TeV w/x-ing + bs'
    # normDenom, normNum = 1.,1.
    # tagDenom, tagNum = '_BG_3p5TeV_20MeV', '_BG_4TeV_20MeV_bs'
    # nColor, dColor = kOrange-2, kRed+1
    # yrel = '/inel.BG int.'

    # ------------------------------------------------------------------------
    # # beamgas 4 TeV
    # fNum = projectpath + '4TeVBGnoBS/results_beam-gas_4TeV-IR1_to_arc_20MeV_cutoff_100M_nprim7283044_66.root'
    # fDenom = '/afs/cern.ch/project/lhc_mib/valBG4TeV/results_ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67.root'
    # subfolder = wwwpath + 'TCT/4TeV/beamgas/beamsizeRatio/'
    # fNum = thispath + "results_beam-gas_4TeV-IR1_to_arc_20MeV_cutoff_100M_nprim7283044_66.root"
    # fDenom = thispath + "results_ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67.root"
    # subfolder =  '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/4TeV/beamsizeRatio/'
    # lTextNum, lTextDenom = 'pointlike', 'w/ beamsize'
    # normDenom, normNum = 1.,1.
    # tagDenom, tagNum = '_BG_4TeV_20MeV_bs', '_BG_4TeV_20MeV'
    # nColor, dColor = kOrange-1, kRed-3
    # yrel = '/inel.BG int.'

    # # beamgas 4 TeV vs 6.5 TeV
    # fNum = projectpath + 'beamgas/6500GeV_beamsize/runs400/results_ir1_BG_bs_6500GeV_b1_20MeV_nprim2716000_67.root'
    # fDenom = projectpath + 'bbgen/4TeV/beamgas/withBeamSize/results_ir1_BG_4TeV_settings_from_TWISS_20MeV_b1_nprim5925000_67.root'
    # subfolder = wwwpath + 'TCT/compBG_4TeV_vs_6.5TeV/'
    # lTextNum, lTextDenom = '6.5 TeV bs', '4 TeV bs'
    # normDenom, normNum = 1.,1.
    # tagDenom, tagNum = '_BG_4TeV_20MeV_bs', '_BG_6500GeV_flat_20MeV_bs'
    # nColor, dColor = kOrange-1, kMagenta-3
    # yrel = '/inel.BG int.'

    # # # # beamgas 4 TeV vs 6.5 TeV reweighted
    # fNum = thispath + 'results_pressure2012_ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67.root'
    # fDenom = thispath + 'results_pressure2015_ir1_BG_bs_6500GeV_b1_20MeV_nprim3198000_67.root'
    # subfolder = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/compBGreweighted/'
    # lTextNum, lTextDenom = '4 TeV', '6.5 TeV'
    # normDenom, normNum = 1.,1. # IS ALREADY Normalised
    # tagNum, tagDenom = '_BG_4TeV_20MeV_bs_reweighted', '_BG_6500GeV_flat_20MeV_bs_reweighted'
    # nColor, dColor = kGray+2, kBlue+4
    # labelText = ''
    # yrel = '/s'

    # # # # beamgas 4 TeV vs 4 TeV reweighted vs flat
    # fDenom = thispath + 'results_pressure2012_ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67.root' the flat hists are not normalised, except for binning
    # fNum = thispath + 'results_pressure2012_ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67.root' the flat hists are not normalised, except for binning
    # subfolder = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/4TeV/compBGflat/'
    # lTextDenom, lTextNum = 'reweighted [1/s]', 'flat x10^{7}'
    # normNum, normDenom = 5925000./1e7,1.
    # tagDenom, tagNum = '_BG_4TeV_20MeV_bs_reweighted', '_BG_4TeV_20MeV_bs_flat'
    # nColor, dColor = kPink-3, kBlack
    # yrel = '/a.u.'

    # fDenom = thispath + 'results_pressure2015_ir1_BG_bs_6500GeV_b1_20MeV_nprim3198000_67.root'
    # fNum = thispath + 'results_pressure2015_ir1_BG_bs_6500GeV_b1_20MeV_nprim3198000_67.root'
    # subfolder = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/6500GeV/compBGflat/'
    # lTextDenom, lTextNum = 'reweighted [1/s]', 'flat x10^{7}'
    # normNum, normDenom = 3198000./1e7,1.
    # tagDenom, tagNum = '_BG_6500GeV_flat_20MeV_bs_reweighted', '_BG_6500GeV_flat_20MeV_bs_flat'
    # dColor, nColor = kYellow-3, kBlack
    # yrel = '/a.u.'
    
 #    # # beamgas 6.5 TeV, 20 MeV vs 6.5 TeV, 20 GeV
 # fNum = projectpath + 'bbgen/6.5TeV/runs400_20MeV/results_ir1_BG_bs_6500GeV_b1_20MeV_nprim2716000_67.root'
 #    fDenom = projectpath + 'beamgas/6500GeV_beamsize/runs10k_20GeV/results_ir1_BG_bs_6500GeV_b1_20GeV_nprim181730000_67.root'
 #    subfolder = wwwpath + 'TCT/compBG_6.5TeV/'
 #    lTextNum, lTextDenom = '20 MeV', '20 GeV'
 #    normDenom, normNum = 1.,1.
 #    tagDenom, tagNum = '_BG_6500GeV_flat_20GeV_bs', '_BG_6500GeV_flat_20MeV_bs'
 #    nColor, dColor = kBlue-1, kMagenta-3
 #    yrel = '/inel.BG int.'

    # # # beamgas 4 TeV 20 MeV vs 20 GeV
    # fNum = projectpath + 'bbgen/4TeV/beamgas/withBeamSize/results_ir1_BG_4TeV_settings_from_TWISS_20MeV_b1_nprim5925000_67.root'
    # fDenom = projectpath + 'BG/FL_4TeV_BG_20GeV_10k/results_ir1_BG_bs_4TeV_settings_from_TWISS_20GeV_b1_nprim89940000_67.root'
    # subfolder = wwwpath + 'TCT/4TeV/beamgas/fluka/bs/compBGtail/'
    # lTextNum, lTextDenom = '20 MeV', '20 GeV'
    # normDenom, normNum = 1.,1.
    # tagDenom, tagNum = '_BG_4TeV_20GeV_bs', '_BG_4TeV_20MeV_bs'
    # nColor, dColor = kOrange-1, kMagenta-3
    # yrel = '/inel.BG int.'

    # ------------------------------------------------------------------------
    # ---- HL -
    # awk '{ sum += $4; } END { print sum; }' H5_HL_TCT5LOUT_relaxColl_hHaloB1_roundthin/coll_summary_H5_HL_TCT5LOUT_relaxColl_hHaloB1_roundthin.dat
    # awk '{ sum += $4; } END { print sum; }' H5_HL_TCT5LOUT_relaxColl_vHaloB1_roundthin/coll_summary_H5_HL_TCT5LOUT_relaxColl_vHaloB1_roundthin.dat
    # awk '{ sum += $4; } END { print sum; }' H5_HL_TCT5LOUT_relaxColl_hHaloB2_roundthin/coll_summary_H5_HL_TCT5LOUT_relaxColl_hHaloB2_roundthin.dat 
    # awk '{ sum += $4; } END { print sum; }' H5_HL_TCT5LOUT_relaxColl_vHaloB2_roundthin/coll_summary_H5_HL_TCT5LOUT_relaxColl_vHaloB2_roundthin.dat 
    HLinitialFlux = 2736*2.2e11/360000 # 1.7e9

    # retracted settings
    normTCT5LOUTb1 = HLinitialFlux * 0.5*(9024.0/54609869.0 + 3071.0/52175081.0)# 0.00011205218641475149 #12091./(63828643+61405975) # 9.7e-5
    normTCT5LOUTb2 = HLinitialFlux * 0.5*(9936.0/40392116.0 + 11898.0/53157089.0)# 0.0002349078766943835 ### 21822/(47196776+63051589) # 2e-4
    normTCT5INb1 = HLinitialFlux * 0.5*(9712.0/54532193.0 + 3366.0/52154816.0) # 0.00012131762826402283
    normTCT5INb2 = HLinitialFlux * 0.5 * (9948.0/40401333.0 + 12028.0/53199970.0)# 0.0002361599262 # 11172./(47203328+63096910) # 1e-4 sum of all tcts over protons lost on primary for h and v separately


    # nominal cases
    normTCT5INb1nom = HLinitialFlux * 0.5*(32557.0/52836357.0 + 15813.0/50278617.0)#(15813.0/61193703 + 32557.0/63640747) # 7.7e-4

    
    # fDenom = thispath + 'results_ir1_BH_6500GeV_b1_20MeV_nprim4752000_30.root'     # 6.5TeV Halo B1
    # fNum = thispath + 'results_hilumi_ir1_hybrid_b1_exp_20MeV_nprim5319000_30.root' # HL retracted Halo B1 round    
    # subfolder = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/HL/compB1HaloRetrRun2/normalised/'
    # lTextNum, lTextDenom = 'HL', '6.5 TeV'
    # tagNum, tagDenom = '_BH_HL_tct5inrdB1_20MeV', '_BH_6500GeV_haloB1_20MeV'
    # normNum, normDenom, yrel = 1., 1.,'/TCT hit'
    # normNum, normDenom, yrel = 1./normTCT5INb1, 1./norm6500GeVB1, "/s"
    # dColor, nColor = kYellow+1, kBlue+2


    # fNum = thispath + "FL_TCT5In_retracted_rdB2_fixgaps/results_hilumi_ir1_hybrid_b2_exp_20MeV_nprim3425000_30.root"
    # fDenom = thispath + 'results_ir1_BH_6500GeV_b2_20MeV_nprim3646000_30.root'     # 6.5TeV Halo B2
    # subfolder = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/HL/compB2HaloRetrRun2/normalised/'
    # lTextNum, lTextDenom = 'HL', '6.5 TeV'
    # tagNum, tagDenom = '_BH_HL_tct5inrdB2_20MeV', '_BH_6500GeV_haloB2_20MeV'
    # normNum, normDenom, yrel = 1./normTCT5INb2, 1./norm6500GeVB2, '/s'
    # #normNum, normDenom, yrel = 1., 1.,'/TCT hit'
    # dColor, nColor = kYellow+2, kBlue+3

    
    # fDenom = workpath + 'runs/FL_6500GeV_HaloB1_20MeV/results_ir1_6500GeV_b1_20MeV_nprim4752000_30.root'
    # fNum = projectpath + 'HL1.0/FL_HL_TCT5IN_nomCollSett_haloB1/results_hilumi_BH_ir1b1_exp_20MeV_nominalCollSett_nprim3320000_30.root'
    # subfolder = wwwpath + 'TCT/HL/compHLnomRun2B1/'
    # lTextNum, lTextDenom = 'HL nominal', '6.5 TeV'
    # tagNum, tagDenom = '_BH_HL_tct5inrdB1_nomCollSett_20MeV', '_BH_6500GeV_haloB1_20MeV'
    # normNum, normDenom = 1./normTCT5INb1, 1./norm6500GeVB1
    # dColor, nColor = kPink-1, kBlue-4
    # yrel = '/s'

    # # fNum = workpath + 'runs/HL_TCT5INOUT_relSett/FL_TCT5LOUT_roundthinB1_2nd/results_hilumi_ir1_hybrid_b1_exp_20MeV_nprim5350000_30.root'
    # # fDenom = workpath + 'runs/HL_TCT5INOUT_relSett/FL_TCT5IN_roundthinB1_2nd/results_hilumi_ir1_hybrid_b1_exp_20MeV_nprim5319000_30.root'
    # # subfolder = wwwpath + 'TCT/HL/relaxedColl/newScatt/fluka/compINOUTB1/'
    # fNum = thispath + "results_hilumi_ir1_hybrid_b1_exp_20MeV_nprim5350000_30.root"
    # fDenom = thispath + "results_hilumi_ir1_hybrid_b1_exp_20MeV_nprim5550000_30.root"
    # subfolder = "/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/HL/compINOUTB1_retracted/normalised/"
    # lTextNum = 'TCT4 only'
    # lTextDenom = 'TCT5 in'
    # tagDenom, tagNum =  '_BH_HL_tct5inrdB1_20MeV', '_BH_HL_tct5otrdB1_20MeV'
    #yrel,normDenom, normNum = '/s',1./normTCT5INb1, 1./normTCT5LOUTb1
    # yrel,normDenom, normNum = '/TCT hit',1., 1.
    # dColor, nColor = kPink-1, kBlue-1
    

    # # fNum = workpath + 'runs/HL_TCT5INOUT_relSett/FL_TCT5IN_roundthinB1_2nd/results_hilumi_ir1_hybrid_b1_exp_20MeV_nprim5319000_30.root'
    # # fDenom = workpath + 'runs/HL_TCT5INOUT_relSett/FL_TCT5IN_roundthin_B2/results_hilumi_ir1_hybrid_b2_exp_20MeV_nprim6466000_30.root'
    # # subfolder = wwwpath + 'TCT/HL/relaxedColl/newScatt/fluka/compINB1B2/perTCThit/'
    # subfolder = "/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/HL/compINB1B2_retracted/perTCThit/"  
    # fDenom = thispath + "results_hilumi_ir1_hybrid_b1_exp_20MeV_nprim5550000_30.root"
    # fNum = thispath + "results_hilumi_ir1_hybrid_b2_exp_20MeV_nprim5924500_30.root"
    # lTextDenom = 'TCT5 in, B1'
    # lTextNum = 'TCT5 in, B2'
    # tagNum, tagDenom = '_BH_HL_tct5inrdB2_20MeV', '_BH_HL_tct5inrdB1_20MeV'
    # normNum, normDenom,yrel =  1./normTCT5INb2, 1./normTCT5INb1, "/s"
    # normDenom, normNum,yrel =  1., 1., "/TCT hit"
    # nColor, dColor = kPink, kBlue+2


    # fNum = thispath + "results_hilumi_ir1_hybrid_b2_exp_20MeV_nprim5001000_30.root"
    # fDenom = thispath + "results_hilumi_ir1_hybrid_b2_exp_20MeV_nprim5924500_30.root"
    # subfolder = "/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/HL/compINOUTB2_retracted/normalised/"
    # # # fNum = workpath + 'runs/HL_TCT5INOUT_relSett/FL_TCT5LOUT_roundthin_B2/results_hilumi_ir1_hybrid_b2_exp_20MeV_nprim5001000_30.root'    
    # # subfolder = wwwpath + 'TCT/HL/relaxedColl/newScatt/fluka/compINOUTB2/perTCThit/'
    # lTextNum = 'TCT4 only'
    # lTextDenom = 'TCT5 in'
    # normDenom, normNum, yrel = 1./normTCT5INb2, 1./normTCT5LOUTb2, '/s'
    # # normDenom, normNum, yrel = 1., 1., '/TCT hit'
    # tagNum, tagDenom = '_BH_HL_tct5otrdB2_20MeV', '_BH_HL_tct5inrdB2_20MeV'
    # dColor, nColor = kGreen-2, kMagenta+1


    # fDenom = workpath + 'runs/FL_TCT5IN_roundthinB1_2nd/results_hilumi_ir1_hybrid_b1_exp_20MeV_nprim5319000_30.root'
    # fNum = workpath + 'runs/FL_TCT5IN_roundthin_B2/results_hilumi_ir1_hybrid_b2_exp_20MeV_nprim5315000_30.root'
    # subfolder = wwwpath + 'TCT/HL/relaxedColl/newScatt/fluka/compINB1B2/'
    # lTextDenom = 'TCT5 in B1'
    # lTextNum = 'TCT5 in B2'
    # normDenom, normNum = 1./normTCT5INb1, 1./normTCT5INb2
    # tagDenom, tagNum = '_BH_HL_tct5inrdB1_20MeV', '_BH_HL_tct5inrdB2_20MeV'
    # dColor, nColor = kRed-3, kCyan-3

    # fDenom = workpath + 'runs/HL_TCT5INOUT_relSett/FL_TCT5LOUT_roundthinB1_2nd/results_hilumi_ir1_hybrid_b1_exp_20MeV_nprim5350000_30.root'
    # fNum = workpath + 'runs/HL_TCT5INOUT_relSett/FL_TCT5LOUT_roundthin_B2/results_hilumi_ir1_hybrid_b2_exp_20MeV_nprim5001000_30.root'
    # subfolder = wwwpath + 'TCT/HL/relaxedColl/newScatt/fluka/compOUTB1B2/stableOpRate/'
    # lTextNum = 'TCT5 out B2'
    # lTextDenom = 'TCT5 out B1'
    # normNum, normDenom = 1./normTCT5LOUTb2, 1./normTCT5LOUTb1
    # #    normDenom, normNum = 1.,1.
    # tagNum, tagDenom = '_BH_HL_tct5otrdB2_20MeV', '_BH_HL_tct5otrdB1_20MeV'
    # dColor, nColor = kRed-4, kBlue-3

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
    # subfolder = wwwpath + 'TCT/compBHB1_4TeV_vs_6.5TeVB1/'

    # ### ----- 4 TeV vs 6.5 TeV B1    
    # subfolder = "/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/compBHB1_4TeV_vs_6p5TeV/normalised/"
    # fNum = thispath + 'results_ir1_BH_6500GeV_b1_20MeV_nprim4752000_30.root'
    # fDenom = thispath + 'results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b1_nprim6904000_30.root'
    # lTextNum = '6.5 TeV'
    # lTextDenom = '4 TeV'
    # normDenom, normNum, yrel = 1./norm4TeVB1newHalo, 1./norm6500GeVB1, '/s'
    # #    normDenom, normNum, yrel = 1., 1., '/TCT hit'
    # tagNum, tagDenom = '_BH_6500GeV_haloB1_20MeV', '_BH_4TeV_B1_20MeV'
    # nColor, dColor = kOrange-3, kPink-5


    # # ### ----- 4 TeV vs 6.5 TeV B2
    # # # fNum = workpath + 'runs/FL_6500GeV_HaloB2_20MeV/results_BH_ir1_6500GeV_b2_20MeV_nprim3646000_30.root'
    # # # fDenom = projectpath + 'bgChecks2/FL_NewHalo_4TeV_B2/results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b2_nprim6914000_30.root'
    # # # subfolder = wwwpath + 'TCT/compBHB2_4TeV_vs_6.5TeV/'
    # # # # ## -- fDenom = workpath + 'runs/4TeV_Halo/results_ir1_4TeV_settings_from_TWISS_20MeV_b2_nprim5356000_66.root'     # -- 4TeV are old fluka sim -- newer exist!
    fDenom = thispath + "results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b2_nprim6914000_30.root"
    fNum = thispath + "results_ir1_BH_6500GeV_b2_20MeV_nprim3646000_30.root"
    subfolder = "/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/compBHB2_4TeV_vs_6p5TeV/normalised/"
    lTextNum = '6.5 TeV'
    lTextDenom = '4 TeV'
    #    normNum, normDenom, yrel = 1., 1., "/TCT hit"
    normNum, normDenom, yrel = 1./norm6500GeVB2,1./norm4TeVB2newHalo, "/s"
    tagDenom, tagNum = '_BH_4TeV_B2_20MeV','_BH_6500GeV_haloB2_20MeV'
    nColor, dColor = kOrange-3, kPink-4

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

    # # fNum = projectpath + 'HL1.0/FL_HL_TCT5IN_nomCollSett_haloB1/results_hilumi_BH_ir1b1_exp_20MeV_nominalCollSett_nprim3320000_30.root'
    # # fDenom = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/HL_TCT5INOUT_relSett/FL_TCT5IN_roundthinB1_2nd/results_hilumi_ir1_hybrid_b1_exp_20MeV_nprim5319000_30.root'
    # # subfolder = wwwpath + 'TCT/HL/compNomRetrCollSett/perTCThit/'
    # subfolder = "/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/figures/HL/compNomRetrCollSett/normalised/"
    # fNum = thispath + "results_hilumi_BH_ir1b1_exp_20MeV_nominalCollSett_nprim3320000_30.root"
    # fDenom = thispath + "results_hilumi_ir1_hybrid_b1_exp_20MeV_nprim5319000_30.root"
    # lTextNum = 'nominal'
    # lTextDenom = 'retracted'
    # normDenom, normNum, yrel = 1./normTCT5INb1, 1./normTCT5INb1nom, '/s'
    # #normDenom, normNum, yrel = 1., 1., '/TCT hit'
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

    # # BG ac and BG Run II reweighted
        
    # fDenom = thispath + 'results_hilumi_ir1_fort_scaled_afterconditioning_max_nprim1_30.root'
    # fNum = thispath + 'results_pressure2015_ir1_BG_bs_6500GeV_b1_20MeV_nprim3198000_67.root'
    # subfolder = wwwpath + 'TCT/HL/compBGRun2HL/'
    # lTextDenom, lTextNum = 'HL BG a.c.', 'Run II BG'
    # normDenom, normNum = 1.,1.
    # tagDenom, tagNum = '_BG_HL_ac_20MeV','_BG_6500GeV_flat_20MeV_bs_reweighted'
    # nColor, dColor = kOrange-1, kMagenta-3
    # yrel = '/s'


    # ------------------------------------------------------------------------

    # # # offmomentum 
    # fNum =  '/afs/cern.ch/project/lhc_mib/offmom/FL_4TeVminusB2/results_ir1_offmin500Hz4TeV_settings_from_TWISS_20MeV_b2_nprim3987000_30.root'
    # fDenom = '/afs/cern.ch/project/lhc_mib/offmom/FL_4TeVplusB2/results_ir1_offplus500Hz_4TeV_settings_from_TWISS_20MeV_b2_nprim3980000_30.root'
    # subfolder = wwwpath + 'TCT/4TeV/tctimpacts/newScatt/comppm500Hz/'
    # lTextNum = '-500 Hz'
    # lTextDenom = '+500 Hz'
    # normNum, normDenom, yrel = 1., 1., '/TCT hit'
    # tagNum, tagDenom =  '_offmin500Hz_4TeV_B2_20MeV', '_offplus500Hz_4TeV_B2_20MeV'
    # dColor, nColor = kMagenta+4, kBlue+3
    # ------------------------------------------------------------------------

    rCol = kPink-7
    # need one file to generate sDict
    bbgFile = fNum
    print "Opening for sDict generation ...", bbgFile
    tag = tagNum
    norm = float(bbgFile.split('nprim')[-1].split('_')[0])
    tBBG = TFile.Open(bbgFile).Get(treeName)
    sDict = generate_sDict(tag, norm, tBBG, yrel)

    nprimN = norm
    nprimD = float(fDenom.split('nprim')[-1].split('_')[0])

    print nprimN, nprimD, "nprimN, nprimD", ".."
    if not os.path.exists(subfolder):
        print 'making dir',  subfolder
        os.mkdir(subfolder)

    # only for label
    Beam, beam = '', ''
    if fNum.count('B1') or fNum.count('b1'): Beam, beam = 'B1', 'b1'
    elif fNum.count('B2') or fNum.count('b2'): Beam, beam = 'B2','b2'
    if fNum.count("BG"): Beam, beam = '', ''
    if not fDenom.count(beam): Beam, beam = '', ''

    rfNum = TFile.Open(fNum)
    rfDenom = TFile.Open(fDenom)
    print 'opening as numerator', fNum
    print 'opening as denominator', fDenom

    msize = 0.05
    for skey in sDict.keys():

        if skey.count('XY'): continue
        if skey.count('Orig'): continue
        if skey.startswith('Prof'): continue
        if skey.count('Sel'): continue

        # testing
        # if not skey.count('EkinMuon') : continue


        
        goLeft = 0
        if skey.count("Phi"): goLeft = 1

        cv = TCanvas( 'cv'+skey, 'cv'+skey, 100, 120, 600, 600 )
        x1, y1, x2, y2 = 0.65,0.75,0.9,0.9 # right corner
        if goLeft: x1, y1, x2, y2 = 0.2,0.75,0.4,0.9 # left corner
        mlegend = TLegend( x1, y1, x2, y2)
        mlegend.SetFillColor(0)
        mlegend.SetFillStyle(0)
        mlegend.SetLineColor(0)
        mlegend.SetTextSize(0.05)
        mlegend.SetShadowColor(0)
        mlegend.SetBorderSize(0)

        p1 = TPad('p1'+skey,'p1'+skey,0.01,0.35,0.99,0.99)

        XurMin, XurMax = -1, -1
        YurMin, YurMax = -1, -1

        if subfolder.count("normalised"):
            scalefactorNorm = 1e3
        else:
            scalefactorNorm = 1.


        if subfolder.count('_4TeV_vs_6p5TeV'):            
            if skey.count("Phi"):
                YurMin, YurMax = 1.e-2*scalefactorNorm,scalefactorNorm*1.e2
                if skey.count("EnMu"):
                    YurMin, YurMax = 1.e-1*scalefactorNorm,scalefactorNorm*1.e2
                if skey.count("NMu"):
                    YurMin, YurMax = 1.e-6*scalefactorNorm,scalefactorNorm
                    
        if subfolder.count('HaloRetrRun2') and not subfolder.count("perTCThit"):
            if skey.count("EkinA"):
                YurMin, YurMax = 1.1,5e5
            elif  skey.count("PhiEnAl"):
                YurMin, YurMax = 1.e4,5e6

        dOptNum, dOptDenom = 'h', 'hsame'
        isLogy = 0
        if skey.count('Ekin'): 
            p1.SetLogx(1)
            p1.SetLogy(1)
            XurMin, XurMax = 0.02, 8e3
            isLogy = 1

        if skey.count('En'):
            p1.SetLogy(1)
            isLogy = 1

        rbf = 8
        if skey.startswith('Rad'): 
            p1.SetLogy(1)
            isLogy = 1
            XurMin, XurMax = 0.0, 1190.
            #YurMin, YurMax = scalefactorNorm*2e-12,scalefactorNorm*9e-2
            if skey.count("reweighted") :
                YurMin, YurMax = 2,1e9
                if skey.count("Mu"):
                    YurMin, YurMax = 2e-2,8e5
                    rbf = 10
                    
        if skey.count('Phi'): 
            XurMin, XurMax = -3.14, 3.01
            if skey.endswith("reweighted"):
                YurMin, YurMax = 5e6,9e8
                if skey.count("EnMu"):
                    YurMin, YurMax = 2e3,9e6
            
            if skey.count('PhiN'):
                if not subfolder.count("beamsizeRatio"):
                    p1.SetLogy(1)
                if skey.endswith("reweighted"):
                    YurMin, YurMax = 1e5,9e9
                    YurMin, YurMax = -1,-1
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
        p2.SetBottomMargin(0.29)

        p1.cd()
        hnameNum = skey
        hnameDenom = hnameNum.replace(tagNum, tagDenom)
        print 'plotting ratio of num', hnameNum, 'and denom', hnameDenom

        xtitle, ytitle = sDict[skey][9], sDict[skey][10]
        if ytitle.count('/s') and not yrel.count('/s'): ytitle.replace('/s', yrel)

        histNum  = rfNum.Get(hnameNum)
        histDenom  = rfDenom.Get(hnameDenom)

        if not histNum:
            print "WARNING : Didn't find ", hnameNum
            continue

        if not histDenom:
            print "WARNING : Didn't find ", hnameDenom
            continue

        if histNum.GetName().endswith("reweighted") or histNum.GetName().endswith("_flat"):
            histNum = histNum.ProjectionX()

        if histDenom.GetName().endswith("reweighted") or histDenom.GetName().endswith("_flat"):
            histDenom = histDenom.ProjectionX()

        
        print "histNum.GetNbinsX(), histDenom.GetNbinsX()", histNum.GetNbinsX(), histDenom.GetNbinsX()


        if hnameNum.count('Rad'):
            #pass
            histNum = doRebin(histNum,rbf)
            histDenom = doRebin(histDenom,rbf)
        
        print "histNum.GetNbinsX(), histDenom.GetNbinsX()", histNum.GetNbinsX(), histDenom.GetNbinsX()

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
        print 'normalised factors',normNum, normDenom
        histNum.Scale(1./normNum)
        histDenom.Scale(1./normDenom)
        integralNum = histNum.Integral() #0
        integralDenom = histDenom.Integral() #0
        # for b in range(histNum.GetNbinsX()):
        #     integralNum+=histNum.GetBinContent(b+1)*histNum.GetBinWidth(b+1)
        #     integralDenom+=histDenom.GetBinContent(b+1)*histDenom.GetBinWidth(b+1)
        ratioIntegrals = 0.
        if integralDenom:
            ratioIntegrals = integralNum/integralDenom
            print "here: integralNum, integralDenom", integralNum, integralDenom,integralNum/integralDenom

        ls = 0.4
        histNum.GetXaxis().SetLabelSize(ls)
        histDenom.GetXaxis().SetLabelSize(ls)

        scaleYAxis = 1.3
        if isLogy:
            ymax = histNum.GetMaximum()
            ymin = histDenom.GetMinimum()

            # print "-"*59, 'ymin', ymin
            # if not ymin: ymin = 1.e-2
            # histNum.GetYaxis().SetRangeUser(ymin/20.,ymax*scaleYAxis)

            if skey.count('Ekin'):
                histNum.SetMaximum(5*ymax)

        if XurMin != -1:
            histNum.GetXaxis().SetRangeUser(XurMin,XurMax)

        
        if YurMin != -1:
            histNum.GetYaxis().SetRangeUser(YurMin,YurMax)

        print "XurMin,XurMax", XurMin,XurMax
        print "YurMin,YurMax", YurMin,YurMax
            # if skey.count('PhiEnMuPlus'): 
            #     histNum.GetYaxis().SetRangeUser(20,2e4)
        if dOptNum.count("same"):
            histDenom.Draw(dOptDenom)
            histNum.Draw(dOptNum)
        else:
            histNum.Draw(dOptNum)
            histDenom.Draw(dOptDenom)


        mlegend.AddEntry(histNum, lTextNum, "l")
        mlegend.AddEntry(histDenom, lTextDenom, "l")
        mlegend.Draw()
        doBig = 0
        if subfolder.count("beamsizeRatio") and skey.count("Z") and not skey.startswith("Orig"): doBig = 1
        lab = mylabel(42)

        xpos, ypos = 0.356, 0.955
        if doBig:
            fontsize = 0.09
            xpos, ypos = 0.18, 0.01955
            lab.SetTextSize(fontsize)
            
        lab.DrawLatex(xpos, ypos, sDict[skey][6].replace("z", "s"))
        lab = mylabel(62)
        lab.SetTextSize(0.055)
        lab.DrawLatex(x1+0.02,y1-0.07,Beam)

        hnameRatio = 'ratio'+hnameNum
        hRatio = histNum.Clone(hnameRatio)
        
        hRatio.Divide(histNum, histDenom, 1, 1)
        hRatio.SetLineStyle(1)
        hRatio.SetLineWidth(2)
        hRatio.SetLineColor(rCol)
        hRatio.SetMarkerColor(rCol)
        hRatio.SetMarkerStyle(22)
        hRatio.SetMarkerSize(msize)
        hRatioInt=0
        hWidth=0
        # for b in range(histNum.GetNbinsX()):
        #     hRatioInt+=hRatio.GetBinContent(b+1)*hRatio.GetBinWidth(b+1)
        #     hWidth+=hRatio.GetBinWidth(b+1)
        # print "hRatioInt/hWidth",hRatioInt/hWidth

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

        hRatio.GetXaxis().SetLabelSize(0.105)
        hRatio.GetYaxis().SetLabelSize(0.08)
        hRatio.GetYaxis().SetTitleOffset(0.8)
        hRatio.GetYaxis().SetTitleSize(0.08)
        hRatio.GetXaxis().SetTitleSize(0.1)
        hRatio.Draw()

        ratiorounded = str(round(ratioIntegrals,2))
        print ' ratio of integrals', ratiorounded
        hRatio.GetYaxis().SetTitle('ratio ' + lTextNum + '/' + lTextDenom + " ")

        if hRatio.GetMinimum() < 1.:
            l.DrawLine(XurMin,1,XurMax,1)

        lab = mylabel(42)
        lab.SetTextSize(0.1)
        lab.SetTextColor(rCol)
        if not subfolder.count("beamsizeRatio") and not subfolder.count("compBGflat"):lab.DrawLatex(0.195,0.88,ratiorounded)

        pname = subfolder+hnameRatio.split('_')[0]+'.pdf'

        print pname
        cv.SaveAs(pname)
