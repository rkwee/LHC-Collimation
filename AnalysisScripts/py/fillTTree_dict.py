#!/usr/bin/python
#
# R Kwee-Hinzmann, 2013
# ---------------------------------------------------------------------------------
import ROOT, math
from ROOT import *

#######################################################################################
    # FORMAT RODERIK

    # http://bbgen.web.cern.ch/bbgen/bruce/fluka_beam_gas_arc_4TeV/flukaIR15.html
    # 1  FLUKA run number (between 1 and 3000)
    # 2  ID of primary particle (between 1 and 60 000 in each run)
    # 3  FLUKA particle type (an explanation of the numbers can be found at http://www.fluka.org/fluka.php?id=man_onl&sub=7)
    # 4  kinetic energy (GeV)
    # 5  statistical weight (should be 1 for all particles)
    # 6  X (cm)
    # 7  Y (cm)
    # 8  directional cosine w.r.t X-axis
    # 9  directional cosine w.r.t Y-axis
    # 10 time (s) since start of primary particle
    # 11 total energy (GeV)
    # 12 X_start (cm) : starting position of primary particle
    # 13 Y_start (cm)
    # 14 Z_start (cm)
    # 15 t_start (s) : starting time of primary particle where t=0 is at the entrance of the TCTH
#######################################################################################
    # FORMAT FLUKA GUYS

    # Scoring from Region No  1754 to  1753
    # Col  1: primary event number
    # -- Particle information --
    # Col  2: FLUKA particle type ID
    # Col  3: generation number
    # Col  4: statistical weight
    # -- Crossing at scoring plane --
    # Col  5: x coord (cm)
    # Col  6: y coord (cm)
    # Col  7: x dir cosine
    # Col  8: y dir cosine
    # Col  9: total energy (GeV)
    # Col 10: kinetic energy (GeV)
    # Col 11: particle age since primary event (sec)
    # -- Primary event --
    # Col 12: x coord TCT impact (cm)
    # Col 13: y coord TCT impact (cm)
    # Col 14: z coord TCT impact (cm)
#######################################################################################
sometext = 'HL LHC'
pID      = 1
cEkin    = 9
cX,cY,cZ = 4,5,13
tag      = 'HL'
csfile_H = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/ats-HL_LHC_1.0/nominal_settings/hor-B1/coll_summary_hor-B1.dat'
csfile_V = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/ats-HL_LHC_1.0/nominal_settings/ver-B1/coll_summary_ver-B1.dat'
Ntct_H   = 15793 # ats-HL_LHC_1.0/nominal_settings/impacts_real_on_52_TCTH.4L1.B1.dat
Ntct_V   = 5817 # ats-HL_LHC_1.0/nominal_settings/impacts_real_on_53_TCTVA.4L1.B1.dat
NtotBeam = 1.6e11*2808
nprim    = 1e3*7390

# for ttree
pID      = 'particle'
cEkin    = 'energy_ke'
cX,cY,cZ = 'x','y','z_interact'
varList_HL = [sometext,pID,cEkin,cX,cY,cZ,tag,csfile_H,csfile_V,Ntct_H,Ntct_V, NtotBeam,nprim]
# ---------------------------------------------------------------------------------
sometext = '4 TeV beam'
cEkin    = 3
pID      = 2
cX,cY,cZ = 5,6,13
tag      = '4TeV'
csfile_H = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/TCT_4TeV_B2hHalo/coll_summary_TCT_4TeV_B2hHalo.dat'
csfile_V = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/TCT_4TeV_B2vHalo/coll_summary_TCT_4TeV_B2vHalo.dat'
Ntct_V   = 3 # wc -l TCT_4TeV_B2vHalo/impacts_real_on_71_TCTH.4R1.B2_B2vHalo.dat
Ntct_H   = 452 # wc -l TCT_4TeV_B2vHalo/impacts_real_on_72_TCTVA.4R1.B2_B2vHalo.dat
NtotBeam = 1.5e11*1380
nprim    = 1.57e7 # number of simulated primary interactions in fluka
# for ttree
pID      = 'particle'
cEkin    = 'energy_ke'
cX,cY,cZ = 'x','y','z_interact'
varList_4TeV = [sometext,pID,cEkin,cX,cY,cZ,tag,csfile_H,csfile_V,Ntct_H,Ntct_V, NtotBeam,nprim]
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# dict  key = hname  #0 particleTypes #1 colNumbers #2 nbins #3 xmin #4 xmax #5 drawOpt #6 prettyName 
                     #7 hcolor #8 ekinCut [GeV] #9 xtitle #10 ytitle
# ---------------------------------------------------------------------------------
sDict = { 
    
    "EkinAll"           : [ ['all'],      [cEkin],      60, 1e-2,  1e4, 'HIST',     'all',      kBlack, -9999,'E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    "EkinMuons"         : [ ['10', '11'], [cEkin],      60, 1e-2,  1e4, 'SAMEHIST', '#mu^{#pm}',kAzure -7, -9999,'E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    "EkinProtons"       : [ ['1'],        [cEkin],      60, 1e-2,  1e4, 'SAMEHIST', 'protons',  kAzure -2, -9999,'E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    "EkinNeutrons"      : [ ['8'],        [cEkin],      60, 1e-2,  1e4, 'SAMEHIST', 'neutrons', kAzure -9, -9999,'E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    "EkinPhotons"       : [ ['7'],        [cEkin],      60, 1e-2,  1e4, 'SAMEHIST', '#gamma',   kAzure +1, -9999,'E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    "EkinElecPosi"      : [ ['3', '4'],   [cEkin],      60, 1e-2,  1e4, 'SAMEHIST', 'e^{#pm}',  kBlue,+4   -9999,'E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],

    "RadNMuonsEAll"      : [ ['10', '11'], [cX,cY,cZ,cEkin], 242,    0, 1210, 'HIST',     '#mu^{#pm}',                        kRed-10, -9999,'r [cm]', 'particles/cm^{2}/TCT hit'],
    "RadNMuonsE20"       : [ ['10', '11'], [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', '#mu^{#pm} with E_{kin} >  20 GeV', kRed-7,   20.,'r [cm]',  'particles/cm^{2}/TCT hit'],
    "RadNMuonsE100"      : [ ['10', '11'], [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', '#mu^{#pm} with E_{kin} > 100 GeV', kRed-1,  100.,'r [cm]',  'particles/cm^{2}/TCT hit'],
    
    "RadEnAll"          : [ ['all'],      [cX,cY,cZ,cEkin], 242,    0, 1210, 'HIST',     'all',        kBlack, -9999,'r [cm]', 'GeV/cm^{2}/TCT hit'],
    "RadEnMuons"        : [ ['10', '11'], [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', '#mu^{#pm} ', kGreen+7,  -9999,'r [cm]', 'GeV/cm^{2}/TCT hit'],
    "RadEnNeutrons"     : [ ['8'],        [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', 'neutrons',   kGreen+1,  -9999,'r [cm]', 'GeV/cm^{2}/TCT hit'],
    "RadEnProtons"      : [ ['1'],        [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', 'protons',    kGreen,    -9999,'r [cm]', 'GeV/cm^{2}/TCT hit'],
    "RadEnPhotons"      : [ ['7'],        [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', '#gamma',     kGreen-7,  -9999,'r [cm]', 'GeV/cm^{2}/TCT hit'],
    "RadEnElecPosi"     : [ ['3','4'],    [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', 'e^{#pm}',    kGreen-10, -9999,'r [cm]', 'GeV/cm^{2}/TCT hit'],

    "PhiNAll"           : [ ['all'],      [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HIST',     'all',          kBlack,    -9999,'#phi [rad]', 'particles/rad/TCT hit'],
    "PhiNMuons"         : [ ['10', '11'], [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HISTSAME', '#mu^{#pm} ',   kOrange+4,  -9999,'#phi [rad]', 'particles/rad/TCT hit'],
    "PhiNNeutrons"      : [ ['8'],        [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HISTSAME', 'neutrons',     kOrange+3,  -9999,'#phi [rad]', 'particles/rad/TCT hit'], 
    "PhiNProtons"       : [ ['1'],        [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HISTSAME', 'protons',      kOrange-3,  -9999,'#phi [rad]', 'particles/rad/TCT hit'],
    "PhiNPhotons"       : [ ['7'],        [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HISTSAME', '#gamma',       kOrange-1,  -9999,'#phi [rad]', 'particles/rad/TCT hit'],
    "PhiNElecPosi"      : [ ['3', '4'],   [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HISTSAME', 'e^{#pm}',      kOrange-4,  -9999,'#phi [rad]', 'particles/rad/TCT hit'],

    "PhiEnAll"         : [ ['all'],      [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HIST',     'all',          kBlack, -9999,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnMuons"       : [ ['10', '11'], [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HISTSAME', '#mu^{#pm} ',   kPink+10,  -9999,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnNeutrons"    : [ ['8'],        [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HISTSAME', 'neutrons',     kPink+4,  -9999,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnProtons"     : [ ['1'],        [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HISTSAME', 'protons',      kPink-1,  -9999,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnPhotons"     : [ ['7'],        [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HISTSAME', '#gamma',       kPink-4,  -9999,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnElecPosi"    : [ ['3','4'],    [cX,cY,cZ,cEkin], 50,  -math.pi, math.pi, 'HISTSAME', 'e^{#pm}',      kPink-7,  -9999,'#phi [rad]', 'GeV/rad/TCT hit'],
    }

# ---------------------------------------------------------------------------------
# dict for histograms
# ---------------------------------------------------------------------------------
hDict_4TeV   = { # vkey = pname; #0 list of hists #1 legend x1 #2 y1 #3 x2 #4 y2 #5 doLogx #6 doLogy #7 XurMin #8 XurMax #9 YurMin #10 YurMax #11 doFill
        'Ekin_TCT' : [["EkinAll", "EkinMuons", "EkinPhotons", "EkinElecPosi","EkinNeutrons", "EkinProtons" ],0.72, 0.75, 0.98, 0.9, 1,1, 2e-2,1e4,-1,-1, 0],
        'RadNMuons_TCT': [ ["RadNMuonsEAll", "RadNMuonsE20", "RadNMuonsE100" ],0.52, 0.75, 0.98, 0.9, 0,1, 0.,1200.,-1,-1, 1,],
        'RadialEnDist_TCT':[ ["RadEnAll", "RadEnMuons", "RadEnNeutrons", "RadEnProtons", "RadEnPhotons", "RadEnElecPosi" ],0.72, 0.75, 0.98, 0.9, 0,1, -1,-1,-1,-1, 1,],
        'PhiNDist_TCT': [ ["PhiNAll", "PhiNMuons", "PhiNPhotons", "PhiNNeutrons","PhiNElecPosi","PhiNProtons", ],0.72, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-5,9e-3, 0,],
        'PhiEnDist_TCT':[ [ "PhiEnAll", "PhiEnMuons", "PhiEnNeutrons", "PhiEnProtons", "PhiEnPhotons", "PhiEnElecPosi" ],0.72, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-6,4, 0,],
        }

hDict_HL_halo   = { # hkey = pname; #0 list of hists #1 legend x1 #2 y1 #3 x2 #4 y2 #5 doLogx #6 doLogy #7 XurMin #8 XurMax #9 YurMin #10 YurMax #11 doFill
    #'Ekin_TCT' : [["EkinAll", "EkinMuons", "EkinPhotons", "EkinElecPosi","EkinNeutrons", "EkinProtons" ],0.72, 0.75, 0.98, 0.9, 1,1, 2e-2,1e4,1e-6,9e-1, 0],
    'Ekin_TCT' : [[ "EkinElecPosi" ],0.72, 0.75, 0.98, 0.9, 1,1, 2e-2,1e4,1e-6,9e-1, 0],
    #'RadNMuons_TCT': [ ["RadNMuonsEAll", "RadNMuonsE20", "RadNMuonsE100" ],0.52, 0.75, 0.98, 0.9, 0,1, 0.,1200.,-1,-1, 1,],
    #'RadialEnDist_TCT':[ ["RadEnAll", "RadEnMuons", "RadEnNeutrons", "RadEnProtons", "RadEnPhotons", "RadEnElecPosi" ],0.72, 0.75, 0.98, 0.9, 0,1, 0,1200,-1,-1, 1,],
    # 'PhiNDist_TCT': [ ["PhiNAll", "PhiNMuons","PhiNNeutrons","PhiNProtons","PhiNPhotons", "PhiNElecPosi", ],0.72, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-7,9e-1, 0,],
    #'PhiEnDist_TCT':[ [ "PhiEnAll", "PhiEnMuons", "PhiEnNeutrons", "PhiEnProtons", "PhiEnPhotons", "PhiEnElecPosi" ],0.72, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-3,5e2, 0,],
    }
# ---------------------------------------------------------------------------------
