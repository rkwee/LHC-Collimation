#!/usr/bin/python
#
# # compare all BKG types at 4 TeV
#   Sep 16 rkwee
#   cv16->this 
## -------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
from helpers import *
from createTTree import treeName
from fillTTree_dict import generate_sDict
## -------------------------------------------------------------------------------
def cv68():
    # new halo (new scatt)
    norm4TeVB1newHalo = 1380 *1.4e11/360000 * 0.5*(622.0/60948098 + 930.0/64935501) 
    # IR5: (866+92 + 170.0+456 )/(60948098 + 64935501) = 1.26e-5,>>> (866+92)/60948098 + (170.0+456)/64935501 = 9.64e-06

    norm4TeVB2newHalo = 1380 * 1.4e11/360000 * (1179.0/59198135 +967/56887051.)/2.  
    # IR5: (1893.0 + 135)/(59198135 +56887051) = 1.75e-5, >>> 1893.0/59198135 +135/56887051. = 3.435e-05

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

    # fNum   = workpath + 'results/results_ir1_4TeV_settings_from_TWISS_b2_nprim7825000_66.root'
    # fDenom = workpath + 'results/results_ir1_4TeV_settings_from_TWISS_20MeV_b2_nprim5356000_66.root'
    # subfolder = wwwpath + 'TCT/4TeV/compB2oldB2new/'
    # lTextNum = 'B2 old'
    # lTextDenom = 'B2 new'
    # tagNum, tagDenom = 'BH_4TeV_B2', 'BH_4TeV_B2_20MeV'
    # nColor, dColor = kCyan+1, kTeal

    # #fNum   = workpath + 'results/results_ir1_4TeV_settings_from_TWISS_20MeV_b1_nprim7964000_66.root'
    # #fDenom = workpath + 'results/results_ir1_4TeV_settings_from_TWISS_20MeV_b2_nprim5356000_66.root'
    # fNum = workpath + 'runs/4TeV_Halo/results_ir1_4TeV_settings_from_TWISS_20MeV_b2_nprim7945000_66.root'
    # fDenom   = workpath + 'runs/4TeV_Halo/results_ir1_4TeV_settings_from_TWISS_20MeV_b1_nprim7964000_66.root'
    # normDenom, normNum = 1./norm4TeVB1oldHalo, 1./norm4TeVB2oldHalo
    # subfolder = wwwpath + 'TCT/4TeV/tctimpacts/oldScatt/compB1B2oldScatt/'
    # fNum = projectpath + 'bgChecks2/FL_NewHalo_4TeV_B2/results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b2_nprim6914000_30.root'
    # fDenom = projectpath + 'bgChecks2/FL_NewHalo_4TeV_B1/results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b1_nprim6904000_30.root'
    # #    normDenom, normNum = 1./norm4TeVB1newHalo, 1./norm4TeVB2newHalo
    # normDenom, normNum = 1., 1.
    # subfolder = wwwpath + 'TCT/4TeV/tctimpacts/newScatt/compB1B2/perTCThit/'
    # lTextNum = 'B2'
    # lTextDenom = 'B1'
    # tagDenom, tagNum = '_BH_4TeV_B1_20MeV', '_BH_4TeV_B2_20MeV'
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

    # fNum = projectpath + 'bgChecks2/FL_NewHalo_4TeV_B2/results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b2_nprim6914000_30.root'
    # fDenom = workpath + 'runs/3.5TeV/results_beam-halo_3.5TeV-R1_D1_20MeV_b2_nprim2344800_66.root'
    # subfolder = wwwpath + 'TCT/4TeV/compB2_3p5vs4TeV/'
    # lTextNum, lTextDenom = '4 TeV w/ x-ing', '3.5 TeV w/o x-ing'
    # #normNum, normDenom = 1./norm4TeVB2, 1./(run1iniFlux * norm3500GeVB2)
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
    # lTextNum, lTextDenom = '4 TeV', '3.5 TeV'
    # #normNum, normDenom, yrel, addon = 1./norm4TeVB1, 1./(run1iniFlux * norm3500GeVB1), '/s', 'normalised/'
    # normNum, normDenom, yrel, addon = 1.,1., '/TCT hit', ''
    # tagDenom, tagNum = '_BH_3p5TeV_B1_20MeV', '_BH_4TeV_B1_20MeV'
    # nColor, dColor = kOrange+3, kMagenta-3
    # subfolder = wwwpath + 'TCT/4TeV/compBHB1_3p5vs4TeV/' + addon 
    

    # # comparison BG 3.5 vs 4 TeV 
    # fNum = projectpath + '4TeVBGnoBS/results_beam-gas_4TeV-IR1_to_arc_20MeV_cutoff_100M_nprim7283044_66.root'
    # fDenom = projectpath + '4TeVBGnoBS/results_beam_gas_3.5TeV_IR1_to_arc_20MeV_100M_nprim7660649_66.root'
    # subfolder = wwwpath + 'TCT/4TeV/compBG_3p5_vs_4TeV/'
    # lTextDenom, lTextNum = '3.5 TeV w/o x-ing', '4 TeV w/ x-ing'
    # normDenom, normNum = 1.,1.
    # tagDenom, tagNum = '_BG_3p5TeV_20MeV', '_BG_4TeV_20MeV'
    # nColor, dColor = kOrange-1, kRed-2
    # yrel = '/inel.BG int.'

    # ------------------------------------------------------------------------
    # # beamgas 4 TeV
    # fNum = projectpath + '4TeVBGnoBS/results_beam-gas_4TeV-IR1_to_arc_20MeV_cutoff_100M_nprim7283044_66.root'
    # #fNum = projectpath + 'bbgen/4TeV/beamgas/results_ir1_BG_bs_4TeV_settings_from_TWISS_20MeV_b1_nprim5925000_67.root'
    # #fNum = projectpath + 'beamisze/4TeV_beamsize/runBG_UVcorr/results_ir1_BG_4TeV_settings_from_TWISS_20MeV_b1_nprim4414500_67.root'
    # fDenom = '/afs/cern.ch/project/lhc_mib/valBG4TeV/results_ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67.root'
    # subfolder = wwwpath + 'TCT/4TeV/beamgas/beamsizeRatio/'
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
    normTCT5LOUTb1 = HLinitialFlux * 0.5*(9024.0/54609869.0 + 3071.0/52175081.0)##12091./(63828643+61405975) # 9.7e-5
    normTCT5LOUTb2 = HLinitialFlux * 0.5*(9936.0/40392116.0 + 11898.0/53157089.0)#21822/(47196776+63051589) # 2e-4
    normTCT5INb1 = HLinitialFlux * 0.5*(9712.0/54532193.0 + 3366.0/52154816.0)
    normTCT5INb2 = HLinitialFlux * 0.5 * (9948.0/40401333.0 + 6064.0/26614313.0)## 11172./(47203328+63096910) # 1e-4 sum of all tcts over protons lost on primary for h and v separately

    # nominal cases
    normTCT5INb1nom = HLinitialFlux * 0.5*(32557.0/52836357.0 + 15813.0/50278617.0)#(15813.0/61193703 + 32557.0/63640747) # 7.7e-4

    # fDenom = workpath + 'runs/FL_6500GeV_HaloB1_20MeV/results_ir1_6500GeV_b1_20MeV_nprim4752000_30.root'
    # fNum = projectpath + 'HL1.0/FL_HL_TCT5IN_nomCollSett_haloB1/results_hilumi_BH_ir1b1_exp_20MeV_nominalCollSett_nprim3320000_30.root'
    # subfolder = wwwpath + 'TCT/HL/compHLnomRun2B1/'
    # lTextNum, lTextDenom = 'HL nominal', '6.5 TeV'
    # tagNum, tagDenom = '_BH_HL_tct5inrdB1_nomCollSett_20MeV', '_BH_6500GeV_haloB1_20MeV'
    # normNum, normDenom = 1./normTCT5INb1, 1./norm6500GeVB1
    # dColor, nColor = kPink-1, kBlue-4
    # yrel = '/s'
 
    # fNum = workpath + 'runs/HL_TCT5INOUT_relSett/FL_TCT5LOUT_roundthinB1_2nd/results_hilumi_ir1_hybrid_b1_exp_20MeV_nprim5350000_30.root'
    # fDenom = workpath + 'runs/HL_TCT5INOUT_relSett/FL_TCT5IN_roundthinB1_2nd/results_hilumi_ir1_hybrid_b1_exp_20MeV_nprim5319000_30.root'
    # subfolder = wwwpath + 'TCT/HL/relaxedColl/newScatt/fluka/compINOUTB1/perTCThit/'
    # lTextNum = 'TCT4 only'
    # lTextDenom = 'TCT5 in'
    # tagDenom, tagNum =  '_BH_HL_tct5inrdB1_20MeV', '_BH_HL_tct5otrdB1_20MeV'
    # yrel,normDenom, normNum = '/s',1./normTCT5INb1, 1./normTCT5LOUTb1
    # yrel,normDenom, normNum = '/TCT hit',1., 1.
    # dColor, nColor = kPink-1, kBlue-1
    

    # fNum = workpath + 'runs/HL_TCT5INOUT_relSett/FL_TCT5IN_roundthinB1_2nd/results_hilumi_ir1_hybrid_b1_exp_20MeV_nprim5319000_30.root'
    # fDenom = workpath + 'runs/HL_TCT5INOUT_relSett/FL_TCT5IN_roundthin_B2/results_hilumi_ir1_hybrid_b2_exp_20MeV_nprim5315000_30.root'
    # subfolder = wwwpath + 'TCT/HL/relaxedColl/newScatt/fluka/compINB1B2/perTCThit/'
    # lTextNum = 'TCT5 in, B1'
    # lTextDenom = 'TCT5 in, B2'
    # tagDenom, tagNum = '_BH_HL_tct5inrdB2_20MeV', '_BH_HL_tct5inrdB1_20MeV'
    # #normDenom, normNum,yrel =  1./normTCT5INb2, 1./normTCT5INb1, "/s"
    # normDenom, normNum,yrel =  1., 1., "/TCT hit"
    # dColor, nColor = kPink, kBlue+2


    # fNum = workpath + 'runs/HL_TCT5INOUT_relSett/FL_TCT5LOUT_roundthin_B2/results_hilumi_ir1_hybrid_b2_exp_20MeV_nprim5001000_30.root'
    # fDenom = workpath + 'runs/HL_TCT5INOUT_relSett/FL_TCT5IN_roundthin_B2/results_hilumi_ir1_hybrid_b2_exp_20MeV_nprim5315000_30.root'
    # subfolder = wwwpath + 'TCT/HL/relaxedColl/newScatt/fluka/compINOUTB2/perTCThit/'
    # lTextNum = 'TCT4 only'
    # lTextDenom = 'TCT5 in'
    # normDenom, normNum, yrel = 1./normTCT5INb2, 1./normTCT5LOUTb2, '/s'
    # normDenom, normNum, yrel = 1., 1., '/TCT hit'
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

    # all at 4 TeV
    f1 = projectpath + 'bgChecks2/FL_NewHalo_4TeV_B1/results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b1_nprim6904000_30.root'
    f2 = projectpath + 'bgChecks2/FL_NewHalo_4TeV_B2/results_ir1_BH_4TeV_settings_from_TWISS_20MeV_b2_nprim6914000_30.root'
    f3 = '/afs/cern.ch/project/lhc_mib/valBG4TeV/results_ir1_BG_bs_4TeV_20MeV_b1_nprim5925000_67.root'
    f4 = '/afs/cern.ch/project/lhc_mib/offmom/FL_4TeVplusB2/results_ir1_offplus500Hz_4TeV_settings_from_TWISS_20MeV_b2_nprim3980000_30.root'
    f5 = '/afs/cern.ch/project/lhc_mib/offmom/FL_4TeVminusB2/results_ir1_offmin500Hz4TeV_settings_from_TWISS_20MeV_b2_nprim3987000_30.root'
    filenames = [f1,f2,f3,f4,f5]

    subfolder = wwwpath + 'TCT/4TeV/compAllBKG/'

    lTexts = ['Halo B1', 'Halo B2', 'beam-gas','+500 Hz', '-500 Hz']
    tags   = ['_BH_4TeV_B1_20MeV', '_BH_4TeV_B2_20MeV', '_BG_4TeV_20MeV_bs' , '_offplus500Hz_4TeV_B2_20MeV', '_offmin500Hz_4TeV_B2_20MeV']
    cols   = [kBlue, kRed, kOrange-3,kMagenta+4, kBlue+3]
    mars   = [ 20, 24, 33, 22, 23 ]
    dOpt   = [ 'h', 'hsame', 'hsame', 'hsame', 'hsame']
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

        x1, y1, x2, y2 = 0.65,0.73,0.9,0.9 # right corner        

        if skey.count("PhiEnAll") or skey.count("PhiEnPhot") or skey.count("PhiNAllE") or skey.count("PhiNP") or skey.count("EnPro"):
            x1, y1, x2, y2 = 0.2,0.75,0.4,0.9 # left corner

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
        if not hists[0]: continue
       
        cv.cd()
        if isLogx:  cv.SetLogx()
        if isLogy:  cv.SetLogy()

        for i in range(len(hists)):
            hists[i].Draw(dOpt[i])
            mlegend.AddEntry(hists[i], lTexts[i], "lp")

        mlegend.Draw()

        lab = mylabel(42)
        lab.DrawLatex(0.356, 0.955, sDict[skey][6])
        lab = mylabel(62)
        lab.SetTextSize(0.055)
        lab.DrawLatex(.8,y1-0.07,'')

        lab = mylabel(42)
        lab.SetTextSize(0.1)
#        lab.SetTextColor(col)


        if hnames[i].count('Ekin'):
            YurMin, YurMax = 0.0001, 5*max(Ymax)

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
