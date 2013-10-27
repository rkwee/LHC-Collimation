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
nprim    = -9999
subfolder= 'TCT/HL/nominalSettings/'

# for ttree
pID      = 'particle'
cEkin    = 'energy_ke'
cX,cY,cZ = 'x','y','z_interact'
varList_HL = [sometext,pID,cEkin,cX,cY,cZ,tag,csfile_H,csfile_V,Ntct_H,Ntct_V, NtotBeam,nprim,subfolder]
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
subfolder= 'TCT/'

# for ttree
pID      = 'particle'
cEkin    = 'energy_ke'
cX,cY,cZ = 'x','y','z_interact'
varList_4TeV = [sometext,pID,cEkin,cX,cY,cZ,tag,csfile_H,csfile_V,Ntct_H,Ntct_V, NtotBeam,nprim,subfolder]
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# dict  key = hname  #0 particleTypes #1 colNumbers #2 nbins #3 xmin #4 xmax #5 drawOpt #6 prettyName 
                     #7 hcolor #8 ekinCut [GeV] #9 xtitle #10 ytitle
# ---------------------------------------------------------------------------------
sDict = { 
    
    "EkinAll"           : [ ['all'],      [cEkin],      60, 1e-2,  1e4, 'HIST',     'all',      kBlack, -9999,'E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    "EkinMuons"         : [ ['10', '11'], [cEkin],      60, 1e-2,  1e4, 'SAMEHIST', '#mu^{#pm}',kAzure, -9999,'E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    "EkinProtons"       : [ ['1'],        [cEkin],      60, 1e-2,  1e4, 'SAMEHIST', 'protons',  kCyan, -9999,'E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    "EkinNeutrons"      : [ ['8'],        [cEkin],      60, 1e-2,  1e4, 'SAMEHIST', 'neutrons', kRed -9, -9999,'E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    "EkinPhotons"       : [ ['7'],        [cEkin],      60, 1e-2,  1e4, 'SAMEHIST', '#gamma',   kOrange, -9999,'E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    "EkinElecPosi"      : [ ['3', '4'],   [cEkin],      60, 1e-2,  1e4, 'SAMEHIST', 'e^{#pm}',  kYellow,  -9999,'E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    "EkinSel1":[['3','4','1','7','8','10','11'], [cEkin], 60, 1e-2,  1e4, 'SAMEHIST', 'e^{#pm}, #mu^{#pm}, #gamma, p, n',  kYellow-7,  -9999,'E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    "EkinPions":[['13','14','23'],        [cEkin], 60, 1e-2,  1e4, 'SAMEHIST', '#pi^{#pm,0}',  kPink+1,  -9999,'E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    "EkinKaons":[['15','16','24'],        [cEkin], 60, 1e-2,  1e4, 'SAMEHIST', 'K^{#pm,0}',  kSpring+1,   -9999,'E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    "EkinSel2":[['3','4','1','7','8','10','11','13','14','23'], [cEkin], 60, 1e-2,  1e4, 'SAMEHIST', 'e^{#pm}, #mu^{#pm}, #gamma, p, n, #pi^{#pm,0}',  kViolet,  -9999,'E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    "EkinSel3":[['3','4','1','7','8','10','11','13','14','23','15','16','24'], [cEkin], 60, 1e-2,  1e4, 'SAMEHIST', 'e^{#pm}, #mu^{#pm}, #gamma, p, n, #pi^{#pm,0}, K^{#pm,0}',  kRed,  -9999,'E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],

    "RadNAll"           : [ ['all'],      [cX,cY,cZ,cEkin], 242,    0, 1210, 'HIST',     'all',        kBlack, -9999,'r [cm]', 'particles/cm^{2}/TCT hit'],
    "RadNMuons"         : [ ['10', '11'], [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', '#mu^{#pm} ', kAzure,  -9999,'r [cm]',  'particles/cm^{2}/TCT hit'],
    "RadNNeutrons"      : [ ['8'],        [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', 'neutrons',   kRed,  -9999,'r [cm]',  'particles/cm^{2}/TCT hit'],
    "RadNProtons"       : [ ['1'],        [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', 'protons',    kCyan,  -9999,'r [cm]',  'particles/cm^{2}/TCT hit'],
    "RadNPhotons"       : [ ['7'],        [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', '#gamma',     kOrange,  -9999,'r [cm]',  'particles/cm^{2}/TCT hit'],
    "RadNElecPosi"      : [ ['3','4'],    [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', 'e^{#pm}',    kYellow,  -9999,'r [cm]',  'particles/cm^{2}/TCT hit'],
    "RadNPions":       [['13','14','23'], [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', '#pi^{#pm,0}',kPink+1,  -9999,'r [cm]',  'particles/cm^{2}/TCT hit'],
    "RadNKaons":       [['15','16','24'], [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', 'K^{#pm,0}',  kSpring+1,  -9999,'r [cm]',  'particles/cm^{2}/TCT hit'],

    "RadNMuonsEAll"      : [ ['10', '11'], [cX,cY,cZ,cEkin], 242,    0, 1210, 'HIST',     '#mu^{#pm}',                        kRed-10, -9999,'r [cm]', 'particles/cm^{2}/TCT hit'],
    "RadNMuonsE20"       : [ ['10', '11'], [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', '#mu^{#pm} with E_{kin} >  20 GeV', kRed-7,   20.,'r [cm]',  'particles/cm^{2}/TCT hit'],
    "RadNMuonsE100"      : [ ['10', '11'], [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', '#mu^{#pm} with E_{kin} > 100 GeV', kRed-6,  100.,'r [cm]',  'particles/cm^{2}/TCT hit'],
    "RadNMuonsE1000"     : [ ['10', '11'], [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', '#mu^{#pm} with E_{kin} > 1 TeV', kRed-1,  1000.,'r [cm]',  'particles/cm^{2}/TCT hit'],
    
    "RadNNeg":       [['11','3','14','16'], [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', 'K^{-}, e^{-},#mu^{-},#pi^{-}',  kMagenta+1,  -9999,'r [cm]',  'particles/cm^{2}/TCT hit'],
    "RadNPos":       [['1','10','4','15','13'], [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', 'p,K^{+},e^{+},#mu^{+},#pi^{+}',  kGreen+1,  -9999,'r [cm]',  'particles/cm^{2}/TCT hit'],
    "RadNNeu":       [['7','23','24','8'], [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', 'n,K^{0},#gamma,#pi^{0}',  kBlue,  -9999,'r [cm]',  'particles/cm^{2}/TCT hit'],

    "RadEnAll"          : [ ['all'],      [cX,cY,cZ,cEkin], 242,    0, 1210, 'HIST',     'all',        kBlack, -9999,'r [cm]', 'GeV/cm^{2}/TCT hit'],
    "RadEnMuons"        : [ ['10', '11'], [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', '#mu^{#pm} ', kAzure,  -9999,'r [cm]', 'GeV/cm^{2}/TCT hit'],
    "RadEnNeutrons"     : [ ['8'],        [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', 'neutrons',   kRed,  -9999,'r [cm]', 'GeV/cm^{2}/TCT hit'],
    "RadEnProtons"      : [ ['1'],        [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', 'protons',    kCyan,    -9999,'r [cm]', 'GeV/cm^{2}/TCT hit'],
    "RadEnPhotons"      : [ ['7'],        [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', '#gamma',     kOrange,  -9999,'r [cm]', 'GeV/cm^{2}/TCT hit'],
    "RadEnElecPosi"     : [ ['3','4'],    [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', 'e^{#pm}',    kYellow, -9999,'r [cm]', 'GeV/cm^{2}/TCT hit'],
    "RadEnPions"      : [ ['13','14','23'],    [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', '#pi^{#pm,0}', kPink+1, -9999,'r [cm]', 'GeV/cm^{2}/TCT hit'],
    "RadEnKaons"      : [ ['15','16','24'],    [cX,cY,cZ,cEkin], 242,    0, 1210, 'HISTSAME', 'K^{#pm,0}', kSpring+1, -9999,'r [cm]', 'GeV/cm^{2}/TCT hit'],

    "PhiNAll"           : [ ['all'],      [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HIST',     'all',          kBlack,    -9999,'#phi [rad]', 'particles/rad/TCT hit'],
    "PhiNMuons"         : [ ['10', '11'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', '#mu^{#pm} ',   kAzure,  -9999,'#phi [rad]', 'particles/rad/TCT hit'],
    "PhiNNeutrons"      : [ ['8'],        [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', 'neutrons',     kRed,  -9999,'#phi [rad]', 'particles/rad/TCT hit'], 
    "PhiNProtons"       : [ ['1'],        [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', 'protons',      kCyan,  -9999,'#phi [rad]', 'particles/rad/TCT hit'],
    "PhiNPhotons"       : [ ['7'],        [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', '#gamma',       kOrange,  -9999,'#phi [rad]', 'particles/rad/TCT hit'],
    "PhiNElecPosi"      : [ ['3', '4'],   [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', 'e^{#pm}',      kYellow,  -9999,'#phi [rad]', 'particles/rad/TCT hit'],
    "PhiNPionsChar"     : [ ['13','14',], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', '#pi^{#pm}',  kViolet,  -9999,'#phi [rad]', 'particles/rad/TCT hit'],
    "PhiNKaonsChar"     : [ ['15','16'],  [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', 'K^{#pm}',    kSpring+1,  -9999,'#phi [rad]', 'particles/rad/TCT hit'],

    "PhiNNeg":       [['11','3','14','16'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', 'K^{-}, e^{-},#mu^{-},#pi^{-}',  kMagenta+1,  -9999,'r [cm]',  'particles/cm^{2}/TCT hit'],
    "PhiNPos":       [['1','10','4','15','13'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', 'p,K^{+},e^{+},#mu^{+},#pi^{+}',  kGreen+1,  -9999,'r [cm]',  'particles/cm^{2}/TCT hit'],
    "PhiNNeu":       [['7','23','24','8'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', 'n,K^{0},#gamma,#pi^{0}',  kBlue,  -9999,'r [cm]',  'particles/cm^{2}/TCT hit'],

    "PhiNMuPlus"        : [ ['10'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', '#mu^{+} ',   kCyan-10,  -9999,'#phi [rad]', 'particles/rad/TCT hit'],
    "PhiNMuMinus"       : [ ['11'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', '#mu^{-} ',   kAzure+8,  -9999,'#phi [rad]', 'particles/rad/TCT hit'],
    "PhiNMuR10"         : [ ['10', '11'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', '#mu^{#pm} r > 10 cm ',   kAzure+4,  10,'#phi [rad]', 'particles/rad/TCT hit'],
    "PhiNMuR50"         : [ ['10', '11'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', '#mu^{#pm} r > 50 cm ',   kAzure+5,  50,'#phi [rad]', 'particles/rad/TCT hit'],
    "PhiNMuR100"        : [ ['10', '11'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', '#mu^{#pm} r > 100 cm ',   kAzure+6,  100,'#phi [rad]', 'particles/rad/TCT hit'],
    "PhiNMuR200"        : [ ['10', '11'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', '#mu^{#pm} r > 200 cm ',   kAzure-1,  200,'#phi [rad]', 'particles/rad/TCT hit'],
    "PhiNMuR300"        : [ ['10', '11'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', '#mu^{#pm} r > 300 cm ',   kCyan-6,  300,'#phi [rad]', 'particles/rad/TCT hit'],
    "PhiNMuR400"        : [ ['10', '11'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', '#mu^{#pm} r > 400 cm ',   kCyan-4,  400,'#phi [rad]', 'particles/rad/TCT hit'],
    "PhiNMuR500"         : [ ['10', '11'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HIST',     '#mu^{#pm} r > 500 cm ',   kAzure+3,  500,'#phi [rad]', 'particles/rad/TCT hit'],
    "PhiNMuR1000"        : [ ['10', '11'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HIST',     '#mu^{#pm} r > 1000 cm ',   kCyan-10,  1000,'#phi [rad]', 'particles/rad/TCT hit'],

    "PhiEnAll"         : [ ['all'],      [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HIST',     'all',          kBlack, -9999,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnMuons"       : [ ['10', '11'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', '#mu^{#pm} ',   kAzure,  -9999,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnNeutrons"    : [ ['8'],        [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', 'neutrons',     kRed,  -9999,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnProtons"     : [ ['1'],        [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', 'protons',      kCyan,  -9999,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnPhotons"     : [ ['7'],        [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', '#gamma',       kOrange,  -9999,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnElecPosi"    : [ ['3','4'],    [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', 'e^{#pm}',      kYellow,  -9999,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnPions"    : [ ['13','14','23'],    [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', '#pi^{#pm,0}',kPink+1,  -9999,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnKaons"    : [ ['15','16','24'],    [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', 'K^{#pm,0}',kSpring+1,  -9999,'#phi [rad]', 'GeV/rad/TCT hit'],

    "PhiEnMuPlus"     : [ ['10'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', '#mu^{+} ',   kCyan-10,  -9999,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnMuMinus"    : [ ['11'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', '#mu^{-} ',   kAzure+8,  -9999,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnMuR10"      : [ ['10', '11'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', '#mu^{#pm} r > 10 cm ',   kAzure+4,  10,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnMuR50"      : [ ['10', '11'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', '#mu^{#pm} r > 50 cm ',   kAzure+5,  50,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnMuR100"     : [ ['10', '11'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', '#mu^{#pm} r > 100 cm ',   kAzure+6,  100,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnMuR200"     : [ ['10', '11'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', '#mu^{#pm} r > 200 cm ',   kAzure-1,  200,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnMuR300"     : [ ['10', '11'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', '#mu^{#pm} r > 300 cm ',   kCyan-6,  300,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnMuR400"     : [ ['10', '11'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', '#mu^{#pm} r > 400 cm ',   kCyan-4,  400,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnMuR500"      : [ ['10', '11'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HIST',     '#mu^{#pm} r > 500 cm ',   kAzure+3,  500,'#phi [rad]', 'GeV/rad/TCT hit'],
    "PhiEnMuR1000"     : [ ['10', '11'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HIST',     '#mu^{#pm} r > 1000 cm ',   kCyan-10,  1000,'#phi [rad]', 'GeV/rad/TCT hit'],

    "PhiEnNeg":       [['11','3','14','16'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', 'K^{-}, e^{-},#mu^{-},#pi^{-}',  kMagenta+1,  -9999,'r [cm]',  'particles/cm^{2}/TCT hit'],
    "PhiEnPos":       [['1','10','4','15','13'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', 'p,K^{+},e^{+},#mu^{+},#pi^{+}',  kGreen+1,  -9999,'r [cm]',  'particles/cm^{2}/TCT hit'],
    "PhiEnNeu":       [['7','23','24','8'], [cX,cY,cZ,cEkin], 100,  -math.pi, math.pi, 'HISTSAME', 'n,K^{0},#gamma,#pi^{0}',  kBlue,  -9999,'r [cm]',  'particles/cm^{2}/TCT hit'],

    "XcoorNNeg":       [['11','3','14','16'], [cX,cY,cZ,cEkin], 160,  -400., 400., 'HISTSAME', 'K^{-}, e^{-},#mu^{-},#pi^{-}',  kMagenta+1,  -9999,'x [cm]',  'particles/cm^{2}/TCT hit'],
    "XcoorNPos":       [['1','10','4','15','13'], [cX,cY,cZ,cEkin], 160,  -400., 400., 'HISTSAME', 'p,K^{+},e^{+},#mu^{+},#pi^{+}',  kGreen+1,  -9999,'x [cm]',  'particles/cm^{2}/TCT hit'],
    "XcoorNNeu":       [['7','23','24','8'], [cX,cY,cZ,cEkin], 160,  -400., 400., 'HISTSAME', 'n,K^{0},#gamma,#pi^{0}',  kBlue,  -9999,'x [cm]',  'particles/cm^{2}/TCT hit'],

    "YcoorNNeg":       [['11','3','14','16'], [cX,cY,cZ,cEkin], 160,  -400., 400., 'HISTSAME', 'K^{-}, e^{-},#mu^{-},#pi^{-}',  kMagenta+1,  -9999,'y [cm]',  'particles/cm^{2}/TCT hit'],
    "YcoorNPos":       [['1','10','4','15','13'], [cX,cY,cZ,cEkin], 160,  -400., 400., 'HISTSAME', 'p,K^{+},e^{+},#mu^{+},#pi^{+}',  kGreen+1,  -9999,'y [cm]',  'particles/cm^{2}/TCT hit'],
    "YcoorNNeu":       [['7','23','24','8'], [cX,cY,cZ,cEkin], 160,  -400., 400., 'HISTSAME', 'n,K^{0},#gamma,#pi^{0}',  kBlue,  -9999,'y [cm]',  'particles/cm^{2}/TCT hit'],
    }

# ---------------------------------------------------------------------------------
# dict for histograms
# ---------------------------------------------------------------------------------
hDict_4TeV   = { # vkey = pname; #0 list of hists #1 legend x1 #2 y1 #3 x2 #4 y2 #5 doLogx #6 doLogy #7 XurMin #8 XurMax #9 YurMin #10 YurMax #11 doFill
        'Ekin_TCT' : [["EkinAll", "EkinMuons", "EkinPhotons", "EkinElecPosi","EkinNeutrons", "EkinProtons" ],0.72, 0.75, 0.98, 0.9, 1,1, 2e-2,1e4,-1,-1, 0],
        'RadNMuons_TCT':[ ["RadNMuonsEAll", "RadNMuonsE20", "RadNMuonsE100" ],0.52, 0.75, 0.98, 0.9, 0,1, 0.,1200.,-1,-1, 1,],
        'RadNDist_TCT': [ ["RadNAll", "RadNMuons", "RadNNeutrons", "RadNProtons", "RadNPhotons", "RadNElecPosi" ],0.72, 0.75, 0.98, 0.9, 0,1, -1,-1,-1,-1, 1,],
        'RadEnDist_TCT':[ ["RadEnAll", "RadEnMuons", "RadEnNeutrons", "RadEnProtons", "RadEnPhotons", "RadEnElecPosi" ],0.72, 0.75, 0.98, 0.9, 0,1, -1,-1,-1,-1, 1,],
        'PhiNDist_TCT': [ ["PhiNAll", "PhiNMuons", "PhiNPhotons", "PhiNNeutrons","PhiNElecPosi","PhiNProtons", ],0.72, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-5,9e-3, 0,],
        'PhiEnDist_TCT':[ [ "PhiEnAll", "PhiEnMuons", "PhiEnNeutrons", "PhiEnProtons", "PhiEnPhotons", "PhiEnElecPosi" ],0.72, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-6,4, 0,],
        }

hDict_HL_halo   = { # hkey = pname; #0 list of hists #1 legend x1 #2 y1 #3 x2 #4 y2 #5 doLogx #6 doLogy #7 XurMin #8 XurMax #9 YurMin #10 YurMax #11 doFill
    #'Ekin_TCT' : [["EkinAll", "EkinMuons", "EkinPhotons", "EkinElecPosi","EkinNeutrons", "EkinProtons","EkinPions", "EkinKaons"  ],0.72, 0.7, 0.98, 0.9, 1,1, 2e-2,1e4,1e-6,9, 0],
    # 'Ekin_TCT_more' : [[ "EkinAll","EkinSel3","EkinSel2","EkinSel1","EkinPions", "EkinKaons" ],0.52, 0.75, 0.98, 0.9, 1,1, 2e-2,1e4,1e-6,9, 1],
    #'RadNDist_TCT': [ ["RadNAll", "RadNMuons", "RadNNeutrons", "RadNProtons", "RadNPhotons", "RadNElecPosi", "RadNPions", "RadNKaons" ],0.72, 0.7, 0.98, 0.9, 0,1, 0,1200,-1,-1, 0,],
    # 'RadNMuons_TCT': [ ["RadNMuonsEAll", "RadNMuonsE20", "RadNMuonsE100","RadNMuonsE1000" ],0.52, 0.75, 0.98, 0.9, 0,1, 0.,1200.,-1,-1, 1,],
    # 'RadEnChar_TCT': [ ["RadEnNeg", "RadEnPos", "RadEnNeu","RadEnNeutrons","RadEnPhotons" ],0.52, 0.75, 0.98, 0.9, 0,1, 0.,1200.,-1,-1, 0,],
    #'RadEnDist_TCT':[ ["RadEnAll", "RadEnMuons", "RadEnNeutrons", "RadEnProtons", "RadEnPhotons", "RadEnElecPosi", "RadEnPions","RadEnKaons" ],0.72, 0.65, 0.98, 0.9, 0,1, 0,1200,-1,-1, 0,],
    # 'PhiNDist_TCT': [ ["PhiNAll", "PhiNMuons","PhiNNeutrons","PhiNProtons","PhiNPhotons", "PhiNElecPosi", "PhiNPionsChar", "PhiNKaonsChar" ],0.72, 0.74, 0.98, 0.92, 0,1, -1,-1,1e-3,9, 0,],
    # 'PhiEnChar_TCT': [ ["PhiEnNeg", "PhiEnPos", "PhiEnNeu","PhiEnNeutrons","PhiEnPhotons" ],0.52, 0.75, 0.98, 0.9, 0,1, -1,-1.,1e-2,1e2, 0,],
    # 'PhiNMu_TCT': [ ["PhiNMuons","PhiNMuR10","PhiNMuR50","PhiNMuR100","PhiNMuR200","PhiNMuR300","PhiNMuR400","PhiNMuR500","PhiNMuR1000" ],0.4, 0.64, 0.7, 0.92, 0,1, -3.14,3.,1e-5,9-1, 1,],
    # 'PhiEnMu_TCT': [ ["PhiEnMuons","PhiEnMuR10","PhiEnMuR50","PhiEnMuR100","PhiEnMuR200","PhiEnMuR300","PhiEnMuR400","PhiEnMuR500","PhiEnMuR1000" ],0.2, 0.8, 0.5, 1.0, 0,1, -3.14,3.,1e-5,9-1, 0,],
    #'PhiEnDist_TCT':[ [ "PhiEnAll", "PhiEnMuons", "PhiEnNeutrons", "PhiEnProtons", "PhiEnPhotons", "PhiEnElecPosi", "PhiEnPions","PhiEnKaons" ],0.72, 0.7, 0.98, 0.9, 0,1, -1,-1,5e-3,5e2, 0,],
    # 'XcoorNChar_TCT': [ ["XcoorNNeg", "XcoorNPos", "XcoorNNeu" ],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-6,1e1, 0,],
    'YcoorNChar_TCT': [ ["YcoorNNeg", "YcoorNPos", "YcoorNNeu" ],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-6,1e1, 0,],
    }
# ---------------------------------------------------------------------------------
