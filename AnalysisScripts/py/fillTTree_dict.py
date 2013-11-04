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
# plotting from several rootfiles of the same format!!:
treeName     = "particle"
fortformat66 = "event/I:generation/I:particle/I:energy_ke/F:weight/F:x/F:y/F:xp/F:yp/F:age/F:energy_tot/F:x_interact/F:y_interact/F:z_interact/F:t_interact/F"
fortformat30 = "event/I:particle/I:generation/I:weight/F:x/F:y/F:xp/F:yp/F:energy_tot/F:energy_ke/F:age/F:x_interact/F:y_interact/F:z_interact/F"

# HL 
# -- beamgas for start up scenario, high
fBGst  = '/Users/rkwee/Documents/RHUL/work/runs/TCT/HL/beamgas/lxplus/hilumi_ir1_fort_scaled_startup_max_30.root'
bbgFile = fBGst
print "Opening...", bbgFile
rfBGst = TFile(bbgFile)
tBGst  = rfBGst.Get(treeName)

# -- beamgas after conditioning, high
fBGac  = '/Users/rkwee/Documents/RHUL/work/runs/TCT/HL/beamgas/lxplus/hilumi_ir1_fort_scaled_afterconditioning_max_30.root'
bbgFile = fBGac
print "Opening...", bbgFile
rfBGac = TFile(bbgFile)
tBGac  = rfBGac.Get(treeName)

# -- beamhalo
fBH     = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/FL_ats-HL_LHC_nominal/hllhc_ir1_b2_nprim7330000_30.root'
fBH     = '/Users/rkwee/Documents/RHUL/work/runs/TCT/HL/beamhalo/hllhc_ir1_b2_nprim7330000_30.root'
bbgFile = fBH
print "Opening...", bbgFile
rfBH    = TFile(bbgFile)
tBH     = rfBH.Get(treeName)
R12m    = 146563140 # Hz from cv07
R100h   = 293126 #Hz from cv07

# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# dict  key = hname  #0 particleTypes #1 nprim #2 nbins #3 xmin #4 xmax #5 ttree #6 prettyName 
                     #7 hcolor #8 othercut[as string OR float/int] #9 xtitle #10 ytitle
# ---------------------------------------------------------------------------------
tag = '_BH'
nprim = 7330000.
sDict_HL_BH = { 
    
    'EkinAll'      + tag : [ ['all'],      nprim,60, 1e-2,  1e4, tBH, 'all',      kBlack, '-9999','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    'EkinMuons'    + tag : [ ['10', '11'], nprim,60, 1e-2,  1e4, tBH, '#mu^{#pm}',kAzure, '-9999','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    'EkinProtons'  + tag : [ ['1'],        nprim,60, 1e-2,  1e4, tBH, 'protons',  kCyan, '-9999','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    'EkinNeutrons' + tag : [ ['8'],        nprim,60, 1e-2,  1e4, tBH, 'neutrons', kRed -9, '-9999','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    'EkinPhotons'  + tag : [ ['7'],        nprim,60, 1e-2,  1e4, tBH, '#gamma',   kOrange, '-9999','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    'EkinElecPosi' + tag : [ ['3', '4'],   nprim,60, 1e-2,  1e4, tBH, 'e^{#pm}',  kYellow,  '-9999','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    'EkinSel1'+ tag : [['3','4','1','7','8','10','11'], nprim, 60, 1e-2,  1e4, tBH, 'e^{#pm}, #mu^{#pm}, #gamma, p, n',  kYellow-7,  '-9999','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    'EkinPions'+ tag : [['13','14','23'],        nprim,60, 1e-2,  1e4, tBH, '#pi^{#pm,0}',  kPink+1,  '-9999','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    'EkinKaons'+ tag : [['15','16','24'],        nprim,60, 1e-2,  1e4, tBH, 'K^{#pm,0}',  kSpring+1,   '-9999','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    'EkinSel2'+ tag : [['3','4','1','7','8','10','11','13','14','23'], nprim, 60, 1e-2,  1e4, tBH, 'e^{#pm}, #mu^{#pm}, #gamma, p, n, #pi^{#pm,0}',  kViolet,  '-9999','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    'EkinSel3'+ tag : [['3','4','1','7','8','10','11','13','14','23','15','16','24'], nprim, 60, 1e-2,  1e4, tBH, 'e^{#pm}, #mu^{#pm}, #gamma, p, n, #pi^{#pm,0}, K^{#pm,0}',  kRed,  '-9999','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],

    'EkinPos'+ tag : [['1','10','4','15','13'], nprim,60, 1e-2,  1e4, tBH,'p,K^{+},e^{+},#mu^{+},#pi^{+}', kGreen+1,  '-9999','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    'EkinNeg'+ tag : [['11','3','14','16'], nprim,60, 1e-2,  1e4 , tBH, 'K^{-}, e^{-},#mu^{-},#pi^{-}',  kMagenta+1,  '-9999','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    'EkinNeu'+ tag : [['7','23','24','8'], nprim, 60, 1e-2,  1e4, tBH, 'n,K^{0},#gamma,#pi^{0}',  kBlue,  '-9999','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    'EkinPiPlus'+ tag : [['13'],        nprim, 60, 1e-2,  1e4, tBH, '#pi^{+}',  kPink+2,  '-9999','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    'EkinPiMinus'+ tag : [['14'],        nprim, 60, 1e-2,  1e4, tBH, '#pi^{-}',  kPink+3,  '-9999','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    'EkinPiZero'+ tag : [['23'],        nprim, 60, 1e-2,  1e4, tBH, '#pi^{0}',  kPink,  '-9999','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],

    'EkinAllRInBP'      + tag : [ ['all'],nprim,60, 1e-2,  1e4, tBH, 'all r < r_{bp}',    kBlue-3, '<:6.9','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    'EkinAllROutBP'     + tag : [ ['all'],nprim,60, 1e-2,  1e4, tBH, 'all r #geq r_{bp}', kMagenta, '>=:6.9','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    'EkinPiPlusRInBP'   + tag : [ ['13'], nprim,60, 1e-2,  1e4, tBH, '#pi^{+} r < r_{bp}',    kCyan-2, '<:6.9','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    'EkinPiPlusROutBP'  + tag : [ ['13'], nprim,60, 1e-2,  1e4, tBH, '#pi^{+} r #geq r_{bp}', kPink-2, '>=:6.9','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    'EkinPiMinusRInBP'  + tag : [ ['14'], nprim,60, 1e-2,  1e4, tBH, '#pi^{-} r < r_{bp}',    kCyan+1, '<:6.9','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    'EkinPiMinusROutBP' + tag : [ ['14'], nprim,60, 1e-2,  1e4, tBH, '#pi^{-} r #geq r_{bp}', kPink+1, '>=:6.9','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    'EkinNeutronsRInBP' + tag : [ ['8'],  nprim,60, 1e-2,  1e4, tBH, 'n r < r_{bp}',    kGreen, '<:6.9','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],
    'EkinNeutronsROutBP'+ tag : [ ['8'],  nprim,60, 1e-2,  1e4, tBH, 'n r #geq r_{bp}', kPink+2, '>=:6.9','E [GeV]', '#frac{dN(counts/TCT hit)}{dlog E}', ],

    'RadNAll'       + tag : [ ['all'],      nprim, 242,    0, 1210, tBH, 'all',        kBlack, '-9999','r [cm]', 'particles/cm^{2}/TCT hit'],
    'RadNMuons'     + tag : [ ['10', '11'], nprim, 242,    0, 1210, tBH, '#mu^{#pm} ', kAzure,  '-9999','r [cm]',  'particles/cm^{2}/TCT hit'],
    'RadNNeutrons'  + tag : [ ['8'],        nprim, 242,    0, 1210, tBH, 'neutrons',   kRed,  '-9999','r [cm]',  'particles/cm^{2}/TCT hit'],
    'RadNProtons'   + tag : [ ['1'],        nprim, 242,    0, 1210, tBH, 'protons',    kCyan,  '-9999','r [cm]',  'particles/cm^{2}/TCT hit'],
    'RadNPhotons'   + tag : [ ['7'],        nprim, 242,    0, 1210, tBH, '#gamma',     kOrange,  '-9999','r [cm]',  'particles/cm^{2}/TCT hit'],
    'RadNElecPosi'  + tag : [ ['3','4'],    nprim, 242,    0, 1210, tBH, 'e^{#pm}',    kYellow,  '-9999','r [cm]',  'particles/cm^{2}/TCT hit'],
    'RadNPions'     + tag : [['13','14'], nprim, 242,    0, 1210, tBH, '#pi^{#pm}',kPink+1,  '-9999','r [cm]',  'particles/cm^{2}/TCT hit'],
    'RadNKaons'     + tag : [['15','16','24'], nprim, 242,    0, 1210, tBH, 'K^{#pm,0}',  kSpring+1,  '-9999','r [cm]',  'particles/cm^{2}/TCT hit'],

    'RadNMuonsEAll' + tag : [ ['10', '11'], nprim, 242,    0, 1210, tBH, '#mu^{#pm}', kRed-10, '-9999','r [cm]', 'particles/cm^{2}/TCT hit'],
    'RadNMuonsE20'  + tag : [ ['10', '11'], nprim, 242,    0, 1210, tBH, '#mu^{#pm} with E_{kin} >  20 GeV', kRed-7,'20.','r [cm]',  'particles/cm^{2}/TCT hit'],
    'RadNMuonsE100' + tag : [ ['10', '11'], nprim, 242,    0, 1210, tBH, '#mu^{#pm} with E_{kin} > 100 GeV', kRed-6,'100.','r [cm]',  'particles/cm^{2}/TCT hit'],
    'RadNMuonsE1000'+ tag : [ ['10', '11'], nprim, 242,    0, 1210, tBH, '#mu^{#pm} with E_{kin} > 1 TeV', kRed-1,'1000.','r [cm]',  'particles/cm^{2}/TCT hit'],
    
    'RadNNeg'+ tag :       [['11','3','14','16'], nprim, 242,    0, 1210, tBH, 'K^{-}, e^{-},#mu^{-},#pi^{-}',  kMagenta+1,  '-9999','r [cm]',  'particles/cm^{2}/TCT hit'],
    'RadNPos'+ tag :       [['1','10','4','15','13'], nprim, 242,    0, 1210, tBH, 'p,K^{+},e^{+},#mu^{+},#pi^{+}',  kGreen+1,  '-9999','r [cm]',  'particles/cm^{2}/TCT hit'],
    'RadNNeu'+ tag : [['7','23','24','8'], nprim, 242,    0, 1210, tBH, 'n,K^{0},#gamma,#pi^{0}',  kBlue,  '-9999','r [cm]',  'particles/cm^{2}/TCT hit'],

    'RadEnAll'       + tag : [ ['all'],      nprim, 242,    0, 1210, tBH, 'all',        kBlack, '-9999','r [cm]', 'GeV/cm^{2}/TCT hit'],
    'RadEnMuons'     + tag : [ ['10', '11'], nprim, 242,    0, 1210, tBH, '#mu^{#pm} ', kAzure,  '-9999','r [cm]', 'GeV/cm^{2}/TCT hit'],
    'RadEnNeutrons'  + tag : [ ['8'],        nprim, 242,    0, 1210, tBH, 'neutrons',   kRed,  '-9999','r [cm]', 'GeV/cm^{2}/TCT hit'],
    'RadEnProtons'   + tag : [ ['1'],        nprim, 242,    0, 1210, tBH, 'protons',    kCyan,    '-9999','r [cm]', 'GeV/cm^{2}/TCT hit'],
    'RadEnPhotons'   + tag : [ ['7'],        nprim, 242,    0, 1210, tBH, '#gamma',     kOrange,  '-9999','r [cm]', 'GeV/cm^{2}/TCT hit'],
    'RadEnElecPosi'  + tag : [ ['3','4'],    nprim, 242,    0, 1210, tBH, 'e^{#pm}',    kYellow, '-9999','r [cm]', 'GeV/cm^{2}/TCT hit'],
    'RadEnPions'     + tag : [ ['13','14'],    nprim, 242,    0, 1210, tBH, '#pi^{#pm}', kPink+1, '-9999','r [cm]', 'GeV/cm^{2}/TCT hit'],
    'RadEnKaons'     + tag : [ ['15','16','24'],    nprim, 242,    0, 1210, tBH, 'K^{#pm,0}', kSpring+1, '-9999','r [cm]', 'GeV/cm^{2}/TCT hit'],

    'RadEnNeg'+ tag : [['11','3','14','16'], nprim, 242,    0, 1210, tBH, 'K^{-}, e^{-},#mu^{-},#pi^{-}',  kMagenta+1,  '-9999','r [cm]',  'particles/cm^{2}/TCT hit'],
    'RadEnPos'+ tag : [['1','10','4','15','13'], nprim, 242,    0, 1210, tBH, 'p,K^{+},e^{+},#mu^{+},#pi^{+}',  kGreen+1,  '-9999','r [cm]',  'particles/cm^{2}/TCT hit'],
    'RadEnNeu'+ tag : [['7','23','24','8'], nprim, 242,    0, 1210, tBH, 'n,K^{0},#gamma,#pi^{0}',  kBlue,  '-9999','r [cm]',  'particles/cm^{2}/TCT hit'],


    'PhiNAll'      + tag : [ ['all'],      nprim, 100,  -math.pi, math.pi, tBH, 'all',       kBlack,    '-9999','#phi [rad]', 'particles/rad/TCT hit'],
    'PhiNMuons'    + tag : [ ['10', '11'], nprim, 100,  -math.pi, math.pi, tBH, '#mu^{#pm} ',kAzure,  '-9999','#phi [rad]', 'particles/rad/TCT hit'],
    'PhiNNeutrons' + tag : [ ['8'],        nprim, 100,  -math.pi, math.pi, tBH, 'neutrons',  kRed,  '-9999','#phi [rad]', 'particles/rad/TCT hit'], 
    'PhiNProtons'  + tag : [ ['1'],        nprim, 100,  -math.pi, math.pi, tBH, 'protons',   kCyan,  '-9999','#phi [rad]', 'particles/rad/TCT hit'],
    'PhiNPhotons'  + tag : [ ['7'],        nprim, 100,  -math.pi, math.pi, tBH, '#gamma',    kOrange,  '-9999','#phi [rad]', 'particles/rad/TCT hit'],
    'PhiNElecPosi' + tag : [ ['3', '4'],   nprim, 100,  -math.pi, math.pi, tBH, 'e^{#pm}',   kYellow,  '-9999','#phi [rad]', 'particles/rad/TCT hit'],
    'PhiNPionsChar'+ tag : [ ['13','14',], nprim, 100,  -math.pi, math.pi, tBH, '#pi^{#pm}', kViolet,  '-9999','#phi [rad]', 'particles/rad/TCT hit'],
    'PhiNKaonsChar'+ tag : [ ['15','16'],  nprim, 100,  -math.pi, math.pi, tBH, 'K^{#pm}',   kSpring+1,  '-9999','#phi [rad]', 'particles/rad/TCT hit'],

    'PhiNNeg'+ tag : [['11','3','14','16'], nprim, 100,  -math.pi, math.pi, tBH, 'K^{-}, e^{-},#mu^{-},#pi^{-}',kMagenta+1,'-9999','r [cm]','particles/cm^{2}/TCT hit'],
    'PhiNPos'+ tag : [['1','10','4','15','13'], nprim, 100,  -math.pi, math.pi, tBH, 'p,K^{+},e^{+},#mu^{+},#pi^{+}',kGreen+1,'-9999','r [cm]','particles/cm^{2}/TCT hit'],
    'PhiNNeu'+ tag : [['7','23','24','8'], nprim, 100,  -math.pi, math.pi, tBH, 'n,K^{0},#gamma,#pi^{0}',kBlue,'-9999','r [cm]','particles/cm^{2}/TCT hit'],

    'PhiNMuPlus'  + tag : [ ['10'], nprim, 100,  -math.pi, math.pi, tBH, '#mu^{+} ',   kCyan-10,  '-9999','#phi [rad]', 'particles/rad/TCT hit'],
    'PhiNMuMinus' + tag : [ ['11'], nprim, 100,  -math.pi, math.pi, tBH, '#mu^{-} ',   kAzure+8,  '-9999','#phi [rad]', 'particles/rad/TCT hit'],
    'PhiNMuR10'   + tag : [ ['10', '11'], nprim, 100,  -math.pi, math.pi, tBH, '#mu^{#pm} r > 10 cm',kAzure+4, '10','#phi [rad]', 'particles/rad/TCT hit'],
    'PhiNMuR50'   + tag : [ ['10', '11'], nprim, 100,  -math.pi, math.pi, tBH, '#mu^{#pm} r > 50 cm',kAzure+5, '50','#phi [rad]', 'particles/rad/TCT hit'],
    'PhiNMuR100'  + tag : [ ['10', '11'], nprim, 100,  -math.pi, math.pi, tBH, '#mu^{#pm} r > 100 cm',kAzure+6,'100','#phi [rad]', 'particles/rad/TCT hit'],
    'PhiNMuR200'  + tag : [ ['10', '11'], nprim, 100,  -math.pi, math.pi, tBH, '#mu^{#pm} r > 200 cm',kAzure-1,'200','#phi [rad]', 'particles/rad/TCT hit'],
    'PhiNMuR300'  + tag : [ ['10', '11'], nprim, 100,  -math.pi, math.pi, tBH, '#mu^{#pm} r > 300 cm',kCyan-6,'300','#phi [rad]', 'particles/rad/TCT hit'],
    'PhiNMuR400'  + tag : [ ['10', '11'], nprim, 100,  -math.pi, math.pi, tBH, '#mu^{#pm} r > 400 cm',kCyan-4,'400','#phi [rad]', 'particles/rad/TCT hit'],
    'PhiNMuR500'   + tag : [ ['10', '11'], nprim, 100,  -math.pi, math.pi, tBH, '#mu^{#pm} r > 500 cm',kAzure+3,'500','#phi [rad]', 'particles/rad/TCT hit'],
    'PhiNMuR1000'  + tag : [ ['10', '11'], nprim, 100,  -math.pi, math.pi, tBH, '#mu^{#pm} r > 1000 cm',kCyan-10,'1000','#phi [rad]', 'particles/rad/TCT hit'],

    'PhiEnAll'      + tag : [ ['all'],      nprim, 100,  -math.pi, math.pi, tBH, 'all',          kBlack, '-9999','#phi [rad]', 'GeV/rad/TCT hit'],
    'PhiEnMuons'    + tag : [ ['10', '11'], nprim, 100,  -math.pi, math.pi, tBH, '#mu^{#pm} ',   kAzure,  '-9999','#phi [rad]', 'GeV/rad/TCT hit'],
    'PhiEnNeutrons' + tag : [ ['8'],        nprim, 100,  -math.pi, math.pi, tBH, 'neutrons',     kRed,  '-9999','#phi [rad]', 'GeV/rad/TCT hit'],
    'PhiEnProtons'  + tag : [ ['1'],        nprim, 100,  -math.pi, math.pi, tBH, 'protons',      kCyan,  '-9999','#phi [rad]', 'GeV/rad/TCT hit'],
    'PhiEnPhotons'  + tag : [ ['7'],        nprim, 100,  -math.pi, math.pi, tBH, '#gamma',       kOrange,  '-9999','#phi [rad]', 'GeV/rad/TCT hit'],
    'PhiEnElecPosi' + tag : [ ['3','4'],    nprim, 100,  -math.pi, math.pi, tBH, 'e^{#pm}',      kYellow,  '-9999','#phi [rad]', 'GeV/rad/TCT hit'],
    'PhiEnPions'    + tag : [ ['13','14','23'],nprim, 100,  -math.pi, math.pi, tBH, '#pi^{#pm,0}',kPink+1,  '-9999','#phi [rad]', 'GeV/rad/TCT hit'],
    'PhiEnKaons'    + tag : [ ['15','16','24'],nprim, 100,  -math.pi, math.pi, tBH, 'K^{#pm,0}',kSpring+1,  '-9999','#phi [rad]', 'GeV/rad/TCT hit'],

    'PhiEnMuPlus'  + tag : [ ['10'], nprim, 100,  -math.pi, math.pi, tBH, '#mu^{+} ',   kCyan-10,  '-9999','#phi [rad]', 'GeV/rad/TCT hit'],
    'PhiEnMuMinus' + tag : [ ['11'], nprim, 100,  -math.pi, math.pi, tBH, '#mu^{-} ',   kAzure+8,  '-9999','#phi [rad]', 'GeV/rad/TCT hit'],
    'PhiEnMuR10'   + tag : [ ['10', '11'], nprim, 100,  -math.pi, math.pi, tBH, '#mu^{#pm} r > 10 cm ',   kAzure+4,'10','#phi [rad]', 'GeV/rad/TCT hit'],
    'PhiEnMuR50'   + tag : [ ['10', '11'], nprim, 100,  -math.pi, math.pi, tBH, '#mu^{#pm} r > 50 cm ',   kAzure+5,'50','#phi [rad]', 'GeV/rad/TCT hit'],
    'PhiEnMuR100'  + tag : [ ['10', '11'], nprim, 100,  -math.pi, math.pi, tBH, '#mu^{#pm} r > 100 cm ',   kAzure+6,'100','#phi [rad]', 'GeV/rad/TCT hit'],
    'PhiEnMuR200'  + tag : [ ['10', '11'], nprim, 100,  -math.pi, math.pi, tBH, '#mu^{#pm} r > 200 cm ',   kAzure-1,'200','#phi [rad]', 'GeV/rad/TCT hit'],
    'PhiEnMuR300'  + tag : [ ['10', '11'], nprim, 100,  -math.pi, math.pi, tBH, '#mu^{#pm} r > 300 cm ',   kCyan-6,'300','#phi [rad]', 'GeV/rad/TCT hit'],
    'PhiEnMuR400'  + tag : [ ['10', '11'], nprim, 100,  -math.pi, math.pi, tBH, '#mu^{#pm} r > 400 cm ',   kCyan-4,'400','#phi [rad]', 'GeV/rad/TCT hit'],
    'PhiEnMuR500'   + tag : [ ['10', '11'], nprim, 100,  -math.pi, math.pi, tBH,     '#mu^{#pm} r > 500 cm ',   kAzure+3,'500','#phi [rad]', 'GeV/rad/TCT hit'],
    'PhiEnMuR1000'  + tag : [ ['10', '11'], nprim, 100,  -math.pi, math.pi, tBH,     '#mu^{#pm} r > 1000 cm ',   kCyan-10,'1000','#phi [rad]', 'GeV/rad/TCT hit'],

    'PhiEnNeg'+ tag : [['11','3','14','16'], nprim, 100,  -math.pi, math.pi, tBH, 'K^{-}, e^{-},#mu^{-},#pi^{-}',kMagenta+1,'-9999','r [cm]','particles/cm^{2}/TCT hit'],
    'PhiEnPos'+ tag : [['1','10','4','15','13'], nprim, 100,  -math.pi, math.pi, tBH, 'p,K^{+},e^{+},#mu^{+},#pi^{+}',kGreen+1,'-9999','r [cm]','particles/cm^{2}/TCT hit'],
    'PhiEnNeu'+ tag : [['7','23','24','8'], nprim, 100,  -math.pi, math.pi, tBH, 'n,K^{0},#gamma,#pi^{0}',kBlue,'-9999','r [cm]','particles/cm^{2}/TCT hit'],

    'XcoorNNeg'+ tag : [['11','3','14','16'], nprim, 160,  -400., 400., tBH, 'K^{-}, e^{-},#mu^{-},#pi^{-}',kMagenta+1,'-9999','x [cm]','particles/cm^{2}/TCT hit'],
    'XcoorNPos'+ tag : [['1','10','4','15','13'], nprim, 160,  -400., 400., tBH, 'p,K^{+},e^{+},#mu^{+},#pi^{+}',kGreen+1,'-9999','x [cm]','particles/cm^{2}/TCT hit'],
    'XcoorNNeu'+ tag : [['7','23','24','8'], nprim, 160,  -400., 400., tBH, 'n,K^{0},#gamma,#pi^{0}',kBlue,'-9999','x [cm]','particles/cm^{2}/TCT hit'],

    'YcoorNNeg'+ tag : [['11','3','14','16'], nprim, 160,  -400., 400., tBH, 'K^{-}, e^{-},#mu^{-},#pi^{-}',kMagenta+1,'-9999','y [cm]','particles/cm^{2}/TCT hit'],
    'YcoorNPos'+ tag : [['1','10','4','15','13'], nprim, 160,  -400., 400., tBH, 'p,K^{+},e^{+},#mu^{+},#pi^{+}',kGreen+1,'-9999','y [cm]','particles/cm^{2}/TCT hit'],
    'YcoorNNeu'+ tag : [['7','23','24','8'], nprim, 160,  -400., 400., tBH, 'n,K^{0},#gamma,#pi^{0}',kBlue,'-9999','y [cm]','particles/cm^{2}/TCT hit'],


    'XYNAll'           + tag : [ ['all'],      nprim, 120, -120, 120, tBH, 'all',        kWhite, '-9999','x [cm]','y [cm]',],
    'XYNPhotons'       + tag : [ ['7'],        nprim, 120, -120, 120, tBH, '#gamma',     kWhite,  '-9999','x [cm]','y [cm]',],
    'XYNElecPosi'      + tag : [ ['3','4'],    nprim, 120, -120, 120, tBH, 'e^{#pm}',    kWhite,  '-9999','x [cm]','y [cm]',],
    'XYNMuons'         + tag : [ ['10', '11'], nprim, 120, -120, 120, tBH, '#mu^{#pm} ', kWhite,  '-9999','x [cm]','y [cm]',],

    'XYNNeutronsE'  + tag : [ ['8'], nprim, 120, -120, 120, tBH, 'neutrons 10 GeV < E_{kin} < 150 GeV',   kWhite,  '10.:150.','x [cm]','y [cm]',],
    'XYNProtonsE'   + tag : [ ['1'], nprim, 120, -120, 120, tBH, 'protons 10 GeV < E_{kin} < 150 GeV',    kWhite,  '10.:150.','x [cm]','y [cm]',],
    'XYNPiPlusE' + tag :   [['13'], nprim, 120, -120, 120, tBH, '#pi^{+} 10 GeV < E_{kin} < 150 GeV',kWhite,  '10.:150.','x [cm]','y [cm]',],
    'XYNPiMinusE' + tag :  [['14'], nprim, 120, -120, 120, tBH, '#pi^{-} 10 GeV < E_{kin} < 150 GeV',kWhite,  '10.:150.','x [cm]','y [cm]',],
    'XYNKaonPlusE'+ tag : [['15'], nprim, 120, -120, 120, tBH, 'K^{+} 10 GeV < E_{kin} < 150 GeV',kWhite,  '10.:150.','x [cm]','y [cm]',],
    'XYNKaonMinusE'+ tag : [['16'], nprim, 120, -120, 120, tBH, 'K^{-} 10 GeV < E_{kin} < 150 GeV', kWhite,  '10.:150.','x [cm]','y [cm]',],

    'XYNAllZoom'       + tag : [ ['all'],      nprim, 60, -30, 30, tBH, 'all',        kWhite, '-9999','x [cm]','y [cm]',],
    'XYNMuonsZoom'     + tag : [ ['10', '11'], nprim, 60, -30, 30, tBH, '#mu^{#pm} ', kWhite,  '-9999','x [cm]','y [cm]',],
    'XYNNeutronsZoom'  + tag : [ ['8'],        nprim, 60, -30, 30, tBH, 'neutrons',   kWhite,  '-9999','x [cm]','y [cm]',],
    'XYNProtonsZoom'   + tag : [ ['1'],        nprim, 60, -30, 30, tBH, 'protons',    kWhite,  '-9999','x [cm]','y [cm]',],
    'XYNPhotonsZoom'   + tag : [ ['7'],        nprim, 60, -30, 30, tBH, '#gamma',     kWhite,  '-9999','x [cm]','y [cm]',],
    'XYNElecPosiZoom'  + tag : [ ['3','4'],    nprim, 60, -30, 30, tBH, 'e^{#pm}',    kWhite,  '-9999','x [cm]','y [cm]',],
    'XYNPiPlusZoom'+ tag :[['13'], nprim, 60, -30, 30, tBH, '#pi^{+}',kWhite,  '-9999','x [cm]','y [cm]',],
    'XYNPiMinusZoom'+ tag :[['14'], nprim, 60, -30, 30, tBH, '#pi^{-}',kWhite,  '-9999','x [cm]','y [cm]',],
    'XYNKaonPlusZoom'+ tag :[['15'], nprim, 60, -30, 30, tBH, 'K^{+}',kWhite,  '-9999','x [cm]','y [cm]',],
    'XYNKaonMinusZoom'+ tag : [['16'], nprim, 60, -30, 30, tBH, 'K^{-}',kWhite,  '-9999','x [cm]','y [cm]',],

    }

# ---------------------------------------------------------------------------------
tBG = tBGac
tag = '_BGac'
sDict_HL_BGac = {
    
    'EkinAll'    + tag : [ ['all'],      1.,60, 1e-2,  1e4, tBG, 'all',      kBlack, '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinMuons'  + tag : [ ['10', '11'], 1.,60, 1e-2,  1e4, tBG, '#mu^{#pm}',kAzure, '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinProtons'+ tag : [ ['1'],        1.,60, 1e-2,  1e4, tBG, 'protons',  kCyan, '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinNeutrons'+ tag : [ ['8'],        1.,60, 1e-2,  1e4, tBG, 'neutrons', kRed -9, '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinPhotons'+ tag : [ ['7'],        1.,60, 1e-2,  1e4, tBG, '#gamma',   kOrange, '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinElecPosi'+ tag : [ ['3', '4'],   1.,60, 1e-2,  1e4, tBG, 'e^{#pm}',  kYellow,  '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinSel1'+ tag : [['3','4','1','7','8','10','11'], 1., 60, 1e-2,  1e4, tBG, 'e^{#pm}, #mu^{#pm}, #gamma, p, n',  kYellow-7,  '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinPions'+ tag : [['13','14','23'],        1.,60, 1e-2,  1e4, tBG, '#pi^{#pm,0}',  kPink+1,  '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinKaons'+ tag : [['15','16','24'],        1.,60, 1e-2,  1e4, tBG, 'K^{#pm,0}',  kSpring+1,   '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinSel2'+ tag : [['3','4','1','7','8','10','11','13','14','23'], 1., 60, 1e-2,  1e4, tBG, 'e^{#pm}, #mu^{#pm}, #gamma, p, n, #pi^{#pm,0}',  kViolet,  '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinSel3'+ tag : [['3','4','1','7','8','10','11','13','14','23','15','16','24'], 1., 60, 1e-2,  1e4, tBG, 'e^{#pm}, #mu^{#pm}, #gamma, p, n, #pi^{#pm,0}, K^{#pm,0}',  kRed,  '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],

    'EkinPos'+ tag : [['1','10','4','15','13'], 1.,60, 1e-2,  1e4, tBG,'p,K^{+},e^{+},#mu^{+},#pi^{+}', kGreen+1,  '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinNeg'+ tag : [['11','3','14','16'], 1.,60, 1e-2,  1e4 , tBG, 'K^{-}, e^{-},#mu^{-},#pi^{-}',  kMagenta+1,  '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinNeu'+ tag : [['7','23','24','8'], 1., 60, 1e-2,  1e4, tBG, 'n,K^{0},#gamma,#pi^{0}',  kBlue,  '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinPiPlus'+ tag : [['13'],   1., 60, 1e-2,  1e4, tBG, '#pi^{+}',  kPink+2,  '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinPiMinus'+ tag : [['14'],   1., 60, 1e-2,  1e4, tBG, '#pi^{-}',  kPink+3,  '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinPiZero'+ tag : [['23'],   1., 60, 1e-2,  1e4, tBG, '#pi^{0}',  kPink,  '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],

    'EkinAllRInBP'     + tag : [ ['all'],1.,60, 1e-2,  1e4, tBG, 'all r < r_{bp}',    kBlue-3, '<:6.9','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinAllROutBP'    + tag : [ ['all'],1.,60, 1e-2,  1e4, tBG, 'all r #geq r_{bp}', kMagenta, '>=:6.9','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinPiPlusRInBP'  + tag : [ ['13'], 1.,60, 1e-2,  1e4, tBG, '#pi^{+} r < r_{bp}',    kCyan-2, '<:6.9','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinPiPlusROutBP' + tag : [ ['13'], 1.,60, 1e-2,  1e4, tBG, '#pi^{+} r #geq r_{bp}', kPink-2, '>=:6.9','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinPiMinusRInBP' + tag : [ ['14'], 1.,60, 1e-2,  1e4, tBG, '#pi^{-} r < r_{bp}',    kCyan+1, '<:6.9','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinPiMinusROutBP'+ tag : [ ['14'], 1.,60, 1e-2,  1e4, tBG, '#pi^{-} r #geq r_{bp}', kPink+1, '>=:6.9','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinNeutronsRInBP'+ tag : [ ['8'],  1.,60, 1e-2,  1e4, tBG, 'n r < r_{bp}',    kGreen, '<:6.9','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinNeutronsROutBP'+ tag : [ ['8'],  1.,60, 1e-2,  1e4, tBG, 'n r #geq r_{bp}', kPink+2, '>=:6.9','E [GeV]', '#frac{dN(counts)}{dlog E}', ],

    'RadNAll'       + tag : [ ['all'],      1., 242,    0, 1210, tBG, 'all',        kBlack, '-9999','r [cm]', 'particles/cm^{2}'],
    'RadNMuons'     + tag : [ ['10', '11'], 1., 242,    0, 1210, tBG, '#mu^{#pm} ', kAzure,  '-9999','r [cm]',  'particles/cm^{2}'],
    'RadNNeutrons'  + tag : [ ['8'],        1., 242,    0, 1210, tBG, 'neutrons',   kRed,  '-9999','r [cm]',  'particles/cm^{2}'],
    'RadNProtons'   + tag : [ ['1'],        1., 242,    0, 1210, tBG, 'protons',    kCyan,  '-9999','r [cm]',  'particles/cm^{2}'],
    'RadNPhotons'   + tag : [ ['7'],        1., 242,    0, 1210, tBG, '#gamma',     kOrange,  '-9999','r [cm]',  'particles/cm^{2}'],
    'RadNElecPosi'  + tag : [ ['3','4'],    1., 242,    0, 1210, tBG, 'e^{#pm}',    kYellow,  '-9999','r [cm]',  'particles/cm^{2}'],
    'RadNPions'     + tag : [['13','14'], 1., 242,    0, 1210, tBG, '#pi^{#pm}',kPink+1,  '-9999','r [cm]',  'particles/cm^{2}'],
    'RadNKaons'     + tag : [['15','16','24'], 1., 242,    0, 1210, tBG, 'K^{#pm,0}',  kSpring+1,  '-9999','r [cm]',  'particles/cm^{2}'],

    'RadNMuonsEAll' + tag : [ ['10', '11'], 1., 242,    0, 1210, tBG, '#mu^{#pm}', kRed-10, '-9999','r [cm]', 'particles/cm^{2}'],
    'RadNMuonsE20'  + tag : [ ['10', '11'], 1., 242,    0, 1210, tBG, '#mu^{#pm} with E_{kin} >  20 GeV', kRed-7,'20.','r [cm]',  'particles/cm^{2}'],
    'RadNMuonsE100' + tag : [ ['10', '11'], 1., 242,    0, 1210, tBG, '#mu^{#pm} with E_{kin} > 100 GeV', kRed-6,'100.','r [cm]',  'particles/cm^{2}'],
    'RadNMuonsE1000'+ tag : [ ['10', '11'], 1., 242,    0, 1210, tBG, '#mu^{#pm} with E_{kin} > 1 TeV', kRed-1,'1000.','r [cm]',  'particles/cm^{2}'],
    
    'RadNNeg'+ tag : [['11','3','14','16'], 1., 242,    0, 1210, tBG, 'K^{-}, e^{-},#mu^{-},#pi^{-}',  kMagenta+1,  '-9999','r [cm]',  'particles/cm^{2}'],
    'RadNPos'+ tag : [['1','10','4','15','13'], 1., 242,    0, 1210, tBG, 'p,K^{+},e^{+},#mu^{+},#pi^{+}',  kGreen+1,  '-9999','r [cm]',  'particles/cm^{2}'],
    'RadNNeu'+ tag : [['7','23','24','8'], 1., 242,    0, 1210, tBG, 'n,K^{0},#gamma,#pi^{0}',  kBlue,  '-9999','r [cm]',  'particles/cm^{2}'],

    'RadEnAll'    + tag : [ ['all'],      1., 242,    0, 1210, tBG, 'all',        kBlack, '-9999','r [cm]', 'GeV/cm^{2}'],
    'RadEnMuons'  + tag : [ ['10', '11'], 1., 242,    0, 1210, tBG, '#mu^{#pm} ', kAzure,  '-9999','r [cm]', 'GeV/cm^{2}'],
    'RadEnNeutrons'+ tag : [ ['8'],        1., 242,    0, 1210, tBG, 'neutrons',   kRed,  '-9999','r [cm]', 'GeV/cm^{2}'],
    'RadEnProtons'+ tag : [ ['1'],        1., 242,    0, 1210, tBG, 'protons',    kCyan,    '-9999','r [cm]', 'GeV/cm^{2}'],
    'RadEnPhotons'+ tag : [ ['7'],        1., 242,    0, 1210, tBG, '#gamma',     kOrange,  '-9999','r [cm]', 'GeV/cm^{2}'],
    'RadEnElecPosi'+ tag : [ ['3','4'],    1., 242,    0, 1210, tBG, 'e^{#pm}',    kYellow, '-9999','r [cm]', 'GeV/cm^{2}'],
    'RadEnPions'  + tag : [ ['13','14','23'],1., 242,    0, 1210, tBG, '#pi^{#pm,0}', kPink+1, '-9999','r [cm]', 'GeV/cm^{2}'],
    'RadEnKaons'  + tag : [ ['15','16','24'],1., 242,    0, 1210, tBG, 'K^{#pm,0}', kSpring+1, '-9999','r [cm]', 'GeV/cm^{2}'],

    'RadEnNeg'+ tag : [['11','3','14','16'], 1., 242,    0, 1210, tBG, 'K^{-}, e^{-},#mu^{-},#pi^{-}',  kMagenta+1,  '-9999','r [cm]',  'particles/cm^{2}'],
    'RadEnPos'+ tag : [['1','10','4','15','13'], 1., 242,    0, 1210, tBG, 'p,K^{+},e^{+},#mu^{+},#pi^{+}',  kGreen+1,  '-9999','r [cm]',  'particles/cm^{2}'],
    'RadEnNeu'+ tag : [['7','23','24','8'], 1., 242,    0, 1210, tBG, 'n,K^{0},#gamma,#pi^{0}',  kBlue,  '-9999','r [cm]',  'particles/cm^{2}'],

    'PhiNAll'     + tag : [ ['all'],      1., 100,  -math.pi, math.pi, tBG, 'all',       kBlack,    '-9999','#phi [rad]', 'particles/rad'],
    'PhiNMuons'   + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} ',kAzure,  '-9999','#phi [rad]', 'particles/rad'],
    'PhiNNeutrons'+ tag : [ ['8'],        1., 100,  -math.pi, math.pi, tBG, 'neutrons',  kRed,  '-9999','#phi [rad]', 'particles/rad'], 
    'PhiNProtons' + tag : [ ['1'],        1., 100,  -math.pi, math.pi, tBG, 'protons',   kCyan,  '-9999','#phi [rad]', 'particles/rad'],
    'PhiNPhotons' + tag : [ ['7'],        1., 100,  -math.pi, math.pi, tBG, '#gamma',    kOrange,  '-9999','#phi [rad]', 'particles/rad'],
    'PhiNElecPosi'+ tag : [ ['3', '4'],   1., 100,  -math.pi, math.pi, tBG, 'e^{#pm}',   kYellow,  '-9999','#phi [rad]', 'particles/rad'],
    'PhiNPionsChar'+ tag : [ ['13','14',], 1., 100,  -math.pi, math.pi, tBG, '#pi^{#pm}', kViolet,  '-9999','#phi [rad]', 'particles/rad'],
    'PhiNKaonsChar'+ tag : [ ['15','16'],  1., 100,  -math.pi, math.pi, tBG, 'K^{#pm}',   kSpring+1,  '-9999','#phi [rad]', 'particles/rad'],

    'PhiNNeg'+ tag : [['11','3','14','16'], 1., 100,  -math.pi, math.pi, tBG, 'K^{-}, e^{-},#mu^{-},#pi^{-}',kMagenta+1,'-9999','r [cm]','particles/cm^{2}'],
    'PhiNPos'+ tag : [['1','10','4','15','13'], 1., 100,  -math.pi, math.pi, tBG, 'p,K^{+},e^{+},#mu^{+},#pi^{+}',kGreen+1,'-9999','r [cm]','particles/cm^{2}'],
    'PhiNNeu'+ tag : [['7','23','24','8'], 1., 100,  -math.pi, math.pi, tBG, 'n,K^{0},#gamma,#pi^{0}',kBlue,'-9999','r [cm]','particles/cm^{2}'],

    'PhiNMuPlus' + tag : [ ['10'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{+} ',   kCyan-10,  '-9999','#phi [rad]', 'particles/rad'],
    'PhiNMuMinus'+ tag : [ ['11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{-} ',   kAzure+8,  '-9999','#phi [rad]', 'particles/rad'],
    'PhiNMuR10'  + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 10 cm',kAzure+4, '10','#phi [rad]', 'particles/rad'],
    'PhiNMuR50'  + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 50 cm',kAzure+5, '50','#phi [rad]', 'particles/rad'],
    'PhiNMuR100' + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 100 cm',kAzure+6,'100','#phi [rad]', 'particles/rad'],
    'PhiNMuR200' + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 200 cm',kAzure-1,'200','#phi [rad]', 'particles/rad'],
    'PhiNMuR300' + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 300 cm',kCyan-6,'300','#phi [rad]', 'particles/rad'],
    'PhiNMuR400' + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 400 cm',kCyan-4,'400','#phi [rad]', 'particles/rad'],
    'PhiNMuR500'  + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 500 cm',kAzure+3,'500','#phi [rad]', 'particles/rad'],
    'PhiNMuR1000' + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 1000 cm',kCyan-10,'1000','#phi [rad]', 'particles/rad'],

    'PhiEnAll'     + tag : [ ['all'],      1., 100,  -math.pi, math.pi, tBG, 'all',          kBlack, '-9999','#phi [rad]', 'GeV/rad'],
    'PhiEnMuons'   + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} ',   kAzure,  '-9999','#phi [rad]', 'GeV/rad'],
    'PhiEnNeutrons'+ tag : [ ['8'],        1., 100,  -math.pi, math.pi, tBG, 'neutrons',     kRed,  '-9999','#phi [rad]', 'GeV/rad'],
    'PhiEnProtons' + tag : [ ['1'],        1., 100,  -math.pi, math.pi, tBG, 'protons',      kCyan,  '-9999','#phi [rad]', 'GeV/rad'],
    'PhiEnPhotons' + tag : [ ['7'],        1., 100,  -math.pi, math.pi, tBG, '#gamma',       kOrange,  '-9999','#phi [rad]', 'GeV/rad'],
    'PhiEnElecPosi'+ tag : [ ['3','4'],    1., 100,  -math.pi, math.pi, tBG, 'e^{#pm}',      kYellow,  '-9999','#phi [rad]', 'GeV/rad'],
    'PhiEnPions'   + tag : [ ['13','14'],1., 100,  -math.pi, math.pi, tBG, '#pi^{#pm}',kPink+1,  '-9999','#phi [rad]', 'GeV/rad'],
    'PhiEnKaons'   + tag : [ ['15','16','24'],1., 100,  -math.pi, math.pi, tBG, 'K^{#pm,0}',kSpring+1,  '-9999','#phi [rad]', 'GeV/rad'],

    'PhiEnMuPlus' + tag : [ ['10'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{+} ',   kCyan-10,  '-9999','#phi [rad]', 'GeV/rad'],
    'PhiEnMuMinus'+ tag : [ ['11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{-} ',   kAzure+8,  '-9999','#phi [rad]', 'GeV/rad'],
    'PhiEnMuR10'  + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 10 cm ',   kAzure+4,'10','#phi [rad]', 'GeV/rad'],
    'PhiEnMuR50'  + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 50 cm ',   kAzure+5,'50','#phi [rad]', 'GeV/rad'],
    'PhiEnMuR100' + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 100 cm ',   kAzure+6,'100','#phi [rad]', 'GeV/rad'],
    'PhiEnMuR200' + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 200 cm ',   kAzure-1,'200','#phi [rad]', 'GeV/rad'],
    'PhiEnMuR300' + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 300 cm ',   kCyan-6,'300','#phi [rad]', 'GeV/rad'],
    'PhiEnMuR400' + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 400 cm ',   kCyan-4,'400','#phi [rad]', 'GeV/rad'],
    'PhiEnMuR500'  + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG,     '#mu^{#pm} r > 500 cm ',   kAzure+3,'500','#phi [rad]', 'GeV/rad'],
    'PhiEnMuR1000' + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG,     '#mu^{#pm} r > 1000 cm ',   kCyan-10,'1000','#phi [rad]', 'GeV/rad'],

    'PhiEnNeg'+ tag : [['11','3','14','16'], 1., 100,  -math.pi, math.pi, tBG, 'K^{-}, e^{-},#mu^{-},#pi^{-}',kMagenta+1,'-9999','r [cm]','particles/cm^{2}'],
    'PhiEnPos'+ tag : [['1','10','4','15','13'], 1., 100,  -math.pi, math.pi, tBG, 'p,K^{+},e^{+},#mu^{+},#pi^{+}',kGreen+1,'-9999','r [cm]','particles/cm^{2}'],
    'PhiEnNeu'+ tag : [['7','23','24','8'], 1., 100,  -math.pi, math.pi, tBG, 'n,K^{0},#gamma,#pi^{0}',kBlue,'-9999','r [cm]','particles/cm^{2}'],

    'XcoorNNeg'+ tag : [['11','3','14','16'], 1., 160,  -400., 400., tBG, 'K^{-}, e^{-},#mu^{-},#pi^{-}',kMagenta+1,'-9999','x [cm]','particles/cm^{2}'],
    'XcoorNPos'+ tag : [['1','10','4','15','13'], 1., 160,  -400., 400., tBG, 'p,K^{+},e^{+},#mu^{+},#pi^{+}',kGreen+1,'-9999','x [cm]','particles/cm^{2}'],
    'XcoorNNeu'+ tag : [['7','23','24','8'], 1., 160,  -400., 400., tBG, 'n,K^{0},#gamma,#pi^{0}',kBlue,'-9999','x [cm]','particles/cm^{2}'],

    'YcoorNNeg'+ tag : [['11','3','14','16'], 1., 160,  -400., 400., tBG, 'K^{-}, e^{-},#mu^{-},#pi^{-}',kMagenta+1,'-9999','y [cm]','particles/cm^{2}'],
    'YcoorNPos'+ tag : [['1','10','4','15','13'], 1., 160,  -400., 400., tBG, 'p,K^{+},e^{+},#mu^{+},#pi^{+}',kGreen+1,'-9999','y [cm]','particles/cm^{2}'],
    'YcoorNNeu'+ tag : [['7','23','24','8'], 1., 160,  -400., 400., tBG, 'n,K^{0},#gamma,#pi^{0}',kBlue,'-9999','y [cm]','particles/cm^{2}'],


    'XYNAll'          + tag : [ ['all'],      1., 120, -120, 120, tBG, 'all',        kWhite, '-9999','x [cm]','y [cm]',],
    'XYNPhotons'      + tag : [ ['7'],        1., 120, -120, 120, tBG, '#gamma',     kWhite,  '-9999','x [cm]','y [cm]',],
    'XYNElecPosi'     + tag : [ ['3','4'],    1., 120, -120, 120, tBG, 'e^{#pm}',    kWhite,  '-9999','x [cm]','y [cm]',],
    'XYNMuons'        + tag : [ ['10', '11'], 1., 120, -120, 120, tBG, '#mu^{#pm} ', kWhite,  '-9999','x [cm]','y [cm]',],

    'XYNNeutronsE' + tag : [ ['8'], 1., 120, -120, 120, tBG, 'neutrons 10 GeV < E_{kin} < 150 GeV',   kWhite,  '10.:150.','x [cm]','y [cm]',],
    'XYNProtonsE'  + tag : [ ['1'], 1., 120, -120, 120, tBG, 'protons 10 GeV < E_{kin} < 150 GeV',    kWhite,  '10.:150.','x [cm]','y [cm]',],
    'XYNPiPlusE' + tag : [['13'], 1., 120, -120, 120, tBG, '#pi^{+} 10 GeV < E_{kin} < 150 GeV',kWhite,  '10.:150.','x [cm]','y [cm]',],
    'XYNPiMinusE' + tag : [['14'], 1., 120, -120, 120, tBG, '#pi^{-} 10 GeV < E_{kin} < 150 GeV',kWhite,  '10.:150.','x [cm]','y [cm]',],
    'XYNKaonPlusE'+ tag : [['15'], 1., 120, -120, 120, tBG, 'K^{+} 10 GeV < E_{kin} < 150 GeV',kWhite,  '10.:150.','x [cm]','y [cm]',],
    'XYNKaonMinusE'+ tag : [['16'], 1., 120, -120, 120, tBG, 'K^{-} 10 GeV < E_{kin} < 150 GeV', kWhite,  '10.:150.','x [cm]','y [cm]',],
}
# ---------------------------------------------------------------------------------
tBG = tBGst
tag = '_BGst'
sDict_HL_BGst = {
    
    'EkinAll'    + tag : [ ['all'],      1.,60, 1e-2,  1e4, tBG, 'all',      kBlack, '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
   'EkinMuons'  + tag : [ ['10', '11'], 1.,60, 1e-2,  1e4, tBG, '#mu^{#pm}',kAzure, '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinProtons'+ tag : [ ['1'],        1.,60, 1e-2,  1e4, tBG, 'protons',  kCyan, '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinNeutrons'+ tag : [ ['8'],        1.,60, 1e-2,  1e4, tBG, 'neutrons', kRed -9, '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinPhotons'+ tag : [ ['7'],        1.,60, 1e-2,  1e4, tBG, '#gamma',   kOrange, '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinElecPosi'+ tag : [ ['3', '4'],   1.,60, 1e-2,  1e4, tBG, 'e^{#pm}',  kYellow,  '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinSel1'+ tag : [['3','4','1','7','8','10','11'], 1., 60, 1e-2,  1e4, tBG, 'e^{#pm}, #mu^{#pm}, #gamma, p, n',  kYellow-7,  '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinPions'+ tag : [['13','14','23'],        1.,60, 1e-2,  1e4, tBG, '#pi^{#pm,0}',  kPink+1,  '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinKaons'+ tag : [['15','16','24'],        1.,60, 1e-2,  1e4, tBG, 'K^{#pm,0}',  kSpring+1,   '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinSel2'+ tag : [['3','4','1','7','8','10','11','13','14','23'], 1., 60, 1e-2,  1e4, tBG, 'e^{#pm}, #mu^{#pm}, #gamma, p, n, #pi^{#pm,0}',  kViolet,  '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinSel3'+ tag : [['3','4','1','7','8','10','11','13','14','23','15','16','24'], 1., 60, 1e-2,  1e4, tBG, 'e^{#pm}, #mu^{#pm}, #gamma, p, n, #pi^{#pm,0}, K^{#pm,0}',  kRed,  '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],

    'EkinPos'+ tag : [['1','10','4','15','13'], 1.,60, 1e-2,  1e4, tBG,'p,K^{+},e^{+},#mu^{+},#pi^{+}', kGreen+1,  '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinNeg'+ tag : [['11','3','14','16'], 1.,60, 1e-2,  1e4 , tBG, 'K^{-}, e^{-},#mu^{-},#pi^{-}',  kMagenta+1,  '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinNeu'+ tag : [['7','23','24','8'], 1., 60, 1e-2,  1e4, tBG, 'n,K^{0},#gamma,#pi^{0}',  kBlue,  '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinPiPlus'+ tag : [['13'],   1., 60, 1e-2,  1e4, tBG, '#pi^{+}',  kPink+2,  '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinPiMinus'+ tag : [['14'],   1., 60, 1e-2,  1e4, tBG, '#pi^{-}',  kPink+3,  '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinPiZero'+ tag : [['23'],   1., 60, 1e-2,  1e4, tBG, '#pi^{0}',  kPink,  '-9999','E [GeV]', '#frac{dN(counts)}{dlog E}', ],

    'EkinAllRInBP'     + tag : [ ['all'],1.,60, 1e-2,  1e4, tBG, 'all r < r_{bp}',    kBlue-3, '<:6.9','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinAllROutBP'    + tag : [ ['all'],1.,60, 1e-2,  1e4, tBG, 'all r #geq r_{bp}', kMagenta, '>=:6.9','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinPiPlusRInBP'  + tag : [ ['13'], 1.,60, 1e-2,  1e4, tBG, '#pi^{+} r < r_{bp}',    kCyan-2, '<:6.9','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinPiPlusROutBP' + tag : [ ['13'], 1.,60, 1e-2,  1e4, tBG, '#pi^{+} r #geq r_{bp}', kPink-2, '>=:6.9','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinPiMinusRInBP' + tag : [ ['14'], 1.,60, 1e-2,  1e4, tBG, '#pi^{-} r < r_{bp}',    kCyan+1, '<:6.9','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinPiMinusROutBP'+ tag : [ ['14'], 1.,60, 1e-2,  1e4, tBG, '#pi^{-} r #geq r_{bp}', kPink+1, '>=:6.9','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinNeutronsRInBP'+ tag : [ ['8'],  1.,60, 1e-2,  1e4, tBG, 'n r < r_{bp}',    kGreen, '<:6.9','E [GeV]', '#frac{dN(counts)}{dlog E}', ],
    'EkinNeutronsROutBP'+ tag : [ ['8'],  1.,60, 1e-2,  1e4, tBG, 'n r #geq r_{bp}', kPink+2, '>=:6.9','E [GeV]', '#frac{dN(counts)}{dlog E}', ],

    'RadNAll'       + tag : [ ['all'],      1., 242,    0, 1210, tBG, 'all',        kBlack, '-9999','r [cm]', 'particles/cm^{2}'],
    'RadNMuons'     + tag : [ ['10', '11'], 1., 242,    0, 1210, tBG, '#mu^{#pm} ', kAzure,  '-9999','r [cm]',  'particles/cm^{2}'],
    'RadNNeutrons'  + tag : [ ['8'],        1., 242,    0, 1210, tBG, 'neutrons',   kRed,  '-9999','r [cm]',  'particles/cm^{2}'],
    'RadNProtons'   + tag : [ ['1'],        1., 242,    0, 1210, tBG, 'protons',    kCyan,  '-9999','r [cm]',  'particles/cm^{2}'],
    'RadNPhotons'   + tag : [ ['7'],        1., 242,    0, 1210, tBG, '#gamma',     kOrange,  '-9999','r [cm]',  'particles/cm^{2}'],
    'RadNElecPosi'  + tag : [ ['3','4'],    1., 242,    0, 1210, tBG, 'e^{#pm}',    kYellow,  '-9999','r [cm]',  'particles/cm^{2}'],
    'RadNPions'     + tag : [['13','14'], 1., 242,    0, 1210, tBG, '#pi^{#pm}',kPink+1,  '-9999','r [cm]',  'particles/cm^{2}'],
    'RadNKaons'     + tag : [['15','16','24'], 1., 242,    0, 1210, tBG, 'K^{#pm,0}',  kSpring+1,  '-9999','r [cm]',  'particles/cm^{2}'],

    'RadNMuonsEAll' + tag : [ ['10', '11'], 1., 242,    0, 1210, tBG, '#mu^{#pm}', kRed-10, '-9999','r [cm]', 'particles/cm^{2}'],
    'RadNMuonsE20'  + tag : [ ['10', '11'], 1., 242,    0, 1210, tBG, '#mu^{#pm} with E_{kin} >  20 GeV', kRed-7,'20.','r [cm]',  'particles/cm^{2}'],
    'RadNMuonsE100' + tag : [ ['10', '11'], 1., 242,    0, 1210, tBG, '#mu^{#pm} with E_{kin} > 100 GeV', kRed-6,'100.','r [cm]',  'particles/cm^{2}'],
    'RadNMuonsE1000'+ tag : [ ['10', '11'], 1., 242,    0, 1210, tBG, '#mu^{#pm} with E_{kin} > 1 TeV', kRed-1,'1000.','r [cm]',  'particles/cm^{2}'],
    
    'RadNNeg'+ tag : [['11','3','14','16'], 1., 242,    0, 1210, tBG, 'K^{-}, e^{-},#mu^{-},#pi^{-}',  kMagenta+1,  '-9999','r [cm]',  'particles/cm^{2}'],
    'RadNPos'+ tag : [['1','10','4','15','13'], 1., 242,    0, 1210, tBG, 'p,K^{+},e^{+},#mu^{+},#pi^{+}',  kGreen+1,  '-9999','r [cm]',  'particles/cm^{2}'],
    'RadNNeu'+ tag : [['7','23','24','8'], 1., 242,    0, 1210, tBG, 'n,K^{0},#gamma,#pi^{0}',  kBlue,  '-9999','r [cm]',  'particles/cm^{2}'],

    'RadEnAll'    + tag : [ ['all'],      1., 242,    0, 1210, tBG, 'all',        kBlack, '-9999','r [cm]', 'GeV/cm^{2}'],
    'RadEnMuons'  + tag : [ ['10', '11'], 1., 242,    0, 1210, tBG, '#mu^{#pm} ', kAzure,  '-9999','r [cm]', 'GeV/cm^{2}'],
    'RadEnNeutrons'+ tag : [ ['8'],        1., 242,    0, 1210, tBG, 'neutrons',   kRed,  '-9999','r [cm]', 'GeV/cm^{2}'],
    'RadEnProtons'+ tag : [ ['1'],        1., 242,    0, 1210, tBG, 'protons',    kCyan,    '-9999','r [cm]', 'GeV/cm^{2}'],
    'RadEnPhotons'+ tag : [ ['7'],        1., 242,    0, 1210, tBG, '#gamma',     kOrange,  '-9999','r [cm]', 'GeV/cm^{2}'],
    'RadEnElecPosi'+ tag : [ ['3','4'],    1., 242,    0, 1210, tBG, 'e^{#pm}',    kYellow, '-9999','r [cm]', 'GeV/cm^{2}'],
    'RadEnPions'  + tag : [ ['13','14','23'],1., 242,    0, 1210, tBG, '#pi^{#pm,0}', kPink+1, '-9999','r [cm]', 'GeV/cm^{2}'],
    'RadEnKaons'  + tag : [ ['15','16','24'],1., 242,    0, 1210, tBG, 'K^{#pm,0}', kSpring+1, '-9999','r [cm]', 'GeV/cm^{2}'],

    'RadEnNeg'+ tag : [['11','3','14','16'], 1., 242,    0, 1210, tBG, 'K^{-}, e^{-},#mu^{-},#pi^{-}',  kMagenta+1,  '-9999','r [cm]',  'particles/cm^{2}'],
    'RadEnPos'+ tag : [['1','10','4','15','13'], 1., 242,    0, 1210, tBG, 'p,K^{+},e^{+},#mu^{+},#pi^{+}',  kGreen+1,  '-9999','r [cm]',  'particles/cm^{2}'],
    'RadEnNeu'+ tag : [['7','23','24','8'], 1., 242,    0, 1210, tBG, 'n,K^{0},#gamma,#pi^{0}',  kBlue,  '-9999','r [cm]',  'particles/cm^{2}'],

    'PhiNAll'     + tag : [ ['all'],      1., 100,  -math.pi, math.pi, tBG, 'all',       kBlack,    '-9999','#phi [rad]', 'particles/rad'],
    'PhiNMuons'   + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} ',kAzure,  '-9999','#phi [rad]', 'particles/rad'],
    'PhiNNeutrons'+ tag : [ ['8'],        1., 100,  -math.pi, math.pi, tBG, 'neutrons',  kRed,  '-9999','#phi [rad]', 'particles/rad'], 
    'PhiNProtons' + tag : [ ['1'],        1., 100,  -math.pi, math.pi, tBG, 'protons',   kCyan,  '-9999','#phi [rad]', 'particles/rad'],
    'PhiNPhotons' + tag : [ ['7'],        1., 100,  -math.pi, math.pi, tBG, '#gamma',    kOrange,  '-9999','#phi [rad]', 'particles/rad'],
    'PhiNElecPosi'+ tag : [ ['3', '4'],   1., 100,  -math.pi, math.pi, tBG, 'e^{#pm}',   kYellow,  '-9999','#phi [rad]', 'particles/rad'],
    'PhiNPionsChar'+ tag : [ ['13','14',], 1., 100,  -math.pi, math.pi, tBG, '#pi^{#pm}', kViolet,  '-9999','#phi [rad]', 'particles/rad'],
    'PhiNKaonsChar'+ tag : [ ['15','16'],  1., 100,  -math.pi, math.pi, tBG, 'K^{#pm}',   kSpring+1,  '-9999','#phi [rad]', 'particles/rad'],

    'PhiNNeg'+ tag : [['11','3','14','16'], 1., 100,  -math.pi, math.pi, tBG, 'K^{-}, e^{-},#mu^{-},#pi^{-}',kMagenta+1,'-9999','r [cm]','particles/cm^{2}'],
    'PhiNPos'+ tag : [['1','10','4','15','13'], 1., 100,  -math.pi, math.pi, tBG, 'p,K^{+},e^{+},#mu^{+},#pi^{+}',kGreen+1,'-9999','r [cm]','particles/cm^{2}'],
    'PhiNNeu'+ tag : [['7','23','24','8'], 1., 100,  -math.pi, math.pi, tBG, 'n,K^{0},#gamma,#pi^{0}',kBlue,'-9999','r [cm]','particles/cm^{2}'],

    'PhiNMuPlus' + tag : [ ['10'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{+} ',   kCyan-10,  '-9999','#phi [rad]', 'particles/rad'],
    'PhiNMuMinus'+ tag : [ ['11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{-} ',   kAzure+8,  '-9999','#phi [rad]', 'particles/rad'],
    'PhiNMuR10'  + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 10 cm',kAzure+4, '10','#phi [rad]', 'particles/rad'],
    'PhiNMuR50'  + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 50 cm',kAzure+5, '50','#phi [rad]', 'particles/rad'],
    'PhiNMuR100' + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 100 cm',kAzure+6,'100','#phi [rad]', 'particles/rad'],
    'PhiNMuR200' + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 200 cm',kAzure-1,'200','#phi [rad]', 'particles/rad'],
    'PhiNMuR300' + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 300 cm',kCyan-6,'300','#phi [rad]', 'particles/rad'],
    'PhiNMuR400' + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 400 cm',kCyan-4,'400','#phi [rad]', 'particles/rad'],
    'PhiNMuR500'  + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 500 cm',kAzure+3,'500','#phi [rad]', 'particles/rad'],
    'PhiNMuR1000' + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 1000 cm',kCyan-10,'1000','#phi [rad]', 'particles/rad'],

    'PhiEnAll'     + tag : [ ['all'],      1., 100,  -math.pi, math.pi, tBG, 'all',          kBlack, '-9999','#phi [rad]', 'GeV/rad'],
    'PhiEnMuons'   + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} ',   kAzure,  '-9999','#phi [rad]', 'GeV/rad'],
    'PhiEnNeutrons'+ tag : [ ['8'],        1., 100,  -math.pi, math.pi, tBG, 'neutrons',     kRed,  '-9999','#phi [rad]', 'GeV/rad'],
    'PhiEnProtons' + tag : [ ['1'],        1., 100,  -math.pi, math.pi, tBG, 'protons',      kCyan,  '-9999','#phi [rad]', 'GeV/rad'],
    'PhiEnPhotons' + tag : [ ['7'],        1., 100,  -math.pi, math.pi, tBG, '#gamma',       kOrange,  '-9999','#phi [rad]', 'GeV/rad'],
    'PhiEnElecPosi'+ tag : [ ['3','4'],    1., 100,  -math.pi, math.pi, tBG, 'e^{#pm}',      kYellow,  '-9999','#phi [rad]', 'GeV/rad'],
    'PhiEnPions'   + tag : [ ['13','14'],1., 100,  -math.pi, math.pi, tBG, '#pi^{#pm}',kPink+1,  '-9999','#phi [rad]', 'GeV/rad'],
    'PhiEnKaons'   + tag : [ ['15','16','24'],1., 100,  -math.pi, math.pi, tBG, 'K^{#pm,0}',kSpring+1,  '-9999','#phi [rad]', 'GeV/rad'],

    'PhiEnMuPlus' + tag : [ ['10'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{+} ',   kCyan-10,  '-9999','#phi [rad]', 'GeV/rad'],
    'PhiEnMuMinus'+ tag : [ ['11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{-} ',   kAzure+8,  '-9999','#phi [rad]', 'GeV/rad'],
    'PhiEnMuR10'  + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 10 cm ',   kAzure+4,'10','#phi [rad]', 'GeV/rad'],
    'PhiEnMuR50'  + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 50 cm ',   kAzure+5,'50','#phi [rad]', 'GeV/rad'],
    'PhiEnMuR100' + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 100 cm ',   kAzure+6,'100','#phi [rad]', 'GeV/rad'],
    'PhiEnMuR200' + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 200 cm ',   kAzure-1,'200','#phi [rad]', 'GeV/rad'],
    'PhiEnMuR300' + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 300 cm ',   kCyan-6,'300','#phi [rad]', 'GeV/rad'],
    'PhiEnMuR400' + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG, '#mu^{#pm} r > 400 cm ',   kCyan-4,'400','#phi [rad]', 'GeV/rad'],
    'PhiEnMuR500'  + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG,     '#mu^{#pm} r > 500 cm ',   kAzure+3,'500','#phi [rad]', 'GeV/rad'],
    'PhiEnMuR1000' + tag : [ ['10', '11'], 1., 100,  -math.pi, math.pi, tBG,     '#mu^{#pm} r > 1000 cm ',   kCyan-10,'1000','#phi [rad]', 'GeV/rad'],

    'PhiEnNeg'+ tag : [['11','3','14','16'], 1., 100,  -math.pi, math.pi, tBG, 'K^{-}, e^{-},#mu^{-},#pi^{-}',kMagenta+1,'-9999','r [cm]','particles/cm^{2}'],
    'PhiEnPos'+ tag : [['1','10','4','15','13'], 1., 100,  -math.pi, math.pi, tBG, 'p,K^{+},e^{+},#mu^{+},#pi^{+}',kGreen+1,'-9999','r [cm]','particles/cm^{2}'],
    'PhiEnNeu'+ tag : [['7','23','24','8'], 1., 100,  -math.pi, math.pi, tBG, 'n,K^{0},#gamma,#pi^{0}',kBlue,'-9999','r [cm]','particles/cm^{2}'],

    'XcoorNNeg'+ tag : [['11','3','14','16'], 1., 160,  -400., 400., tBG, 'K^{-}, e^{-},#mu^{-},#pi^{-}',kMagenta+1,'-9999','x [cm]','particles/cm^{2}'],
    'XcoorNPos'+ tag : [['1','10','4','15','13'], 1., 160,  -400., 400., tBG, 'p,K^{+},e^{+},#mu^{+},#pi^{+}',kGreen+1,'-9999','x [cm]','particles/cm^{2}'],
    'XcoorNNeu'+ tag : [['7','23','24','8'], 1., 160,  -400., 400., tBG, 'n,K^{0},#gamma,#pi^{0}',kBlue,'-9999','x [cm]','particles/cm^{2}'],

    'YcoorNNeg'+ tag : [['11','3','14','16'], 1., 160,  -400., 400., tBG, 'K^{-}, e^{-},#mu^{-},#pi^{-}',kMagenta+1,'-9999','y [cm]','particles/cm^{2}'],
    'YcoorNPos'+ tag : [['1','10','4','15','13'], 1., 160,  -400., 400., tBG, 'p,K^{+},e^{+},#mu^{+},#pi^{+}',kGreen+1,'-9999','y [cm]','particles/cm^{2}'],
    'YcoorNNeu'+ tag : [['7','23','24','8'], 1., 160,  -400., 400., tBG, 'n,K^{0},#gamma,#pi^{0}',kBlue,'-9999','y [cm]','particles/cm^{2}'],


    'XYNAll'          + tag : [ ['all'],      1., 120, -120, 120, tBG, 'all',        kWhite, '-9999','x [cm]','y [cm]',],
    'XYNPhotons'      + tag : [ ['7'],        1., 120, -120, 120, tBG, '#gamma',     kWhite,  '-9999','x [cm]','y [cm]',],
    'XYNElecPosi'     + tag : [ ['3','4'],    1., 120, -120, 120, tBG, 'e^{#pm}',    kWhite,  '-9999','x [cm]','y [cm]',],
    'XYNMuons'        + tag : [ ['10', '11'], 1., 120, -120, 120, tBG, '#mu^{#pm} ', kWhite,  '-9999','x [cm]','y [cm]',],

    'XYNNeutronsE' + tag : [ ['8'], 1., 120, -120, 120, tBG, 'neutrons 10 GeV < E_{kin} < 150 GeV',   kWhite,  '10.:150.','x [cm]','y [cm]',],
    'XYNProtonsE'  + tag : [ ['1'], 1., 120, -120, 120, tBG, 'protons 10 GeV < E_{kin} < 150 GeV',    kWhite,  '10.:150.','x [cm]','y [cm]',],
    'XYNPiPlusE' + tag : [['13'], 1., 120, -120, 120, tBG, '#pi^{+} 10 GeV < E_{kin} < 150 GeV',kWhite,  '10.:150.','x [cm]','y [cm]',],
    'XYNPiMinusE' + tag : [['14'], 1., 120, -120, 120, tBG, '#pi^{-} 10 GeV < E_{kin} < 150 GeV',kWhite,  '10.:150.','x [cm]','y [cm]',],
    'XYNKaonPlusE'+ tag : [['15'], 1., 120, -120, 120, tBG, 'K^{+} 10 GeV < E_{kin} < 150 GeV',kWhite,  '10.:150.','x [cm]','y [cm]',],
    'XYNKaonMinusE'+ tag : [['16'], 1., 120, -120, 120, tBG, 'K^{-} 10 GeV < E_{kin} < 150 GeV', kWhite,  '10.:150.','x [cm]','y [cm]',],

}

# ---------------------------------------------------------------------------------
# comp plots
# ---------------------------------------------------------------------------------

sDict_HL_comp = {

    "EkinMuBGst"  : [ ['10', '11'], 1.,      60, 1e-2,  1e4, tBGst, ' BG startup',kBlue-1, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
    "EkinMuBGac"  : [ ['10', '11'], 1.,      60, 1e-2,  1e4, tBGac, ' BG after Cond',kAzure-3, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
    "EkinMuBHds"  : [ ['10', '11'], nprim/R12m,  60, 1e-2, 1e4, tBH,' BH 12 min loss',kPink-9, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
    "EkinMuBHop"  : [ ['10', '11'], nprim/R100h,  60, 1e-2,1e4, tBH,' BH 100h loss',kGreen+2, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],

    "EkinPrBGst"  : [ ['1'], 1.,      60, 1e-2,  1e4, tBGst, ' BG startup',kBlue-1, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
    "EkinPrBGac"  : [ ['1'], 1.,      60, 1e-2,  1e4, tBGac, ' BG after Cond',kAzure-3, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
    "EkinPrBHds"  : [ ['1'], nprim/R12m,  60, 1e-2, 1e4, tBH,' BH 12 min loss',kPink-9, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
    "EkinPrBHop"  : [ ['1'], nprim/R100h,  60, 1e-2,1e4, tBH,' BH 100h loss',kGreen+2, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],

    "EkinNeBGst"  : [ ['8'], 1.,      60, 1e-2,  1e4, tBGst, ' BG startup',kBlue-1, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
    "EkinNeBGac"  : [ ['8'], 1.,      60, 1e-2,  1e4, tBGac, ' BG after Cond',kAzure-3, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
    "EkinNeBHds"  : [ ['8'], nprim/R12m,  60, 1e-2, 1e4, tBH,' BH 12 min loss',kPink-9, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
    "EkinNeBHop"  : [ ['8'], nprim/R100h,  60, 1e-2,1e4, tBH,' BH 100h loss',kGreen+2, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],

    "EkinEpBGst"  : [ ['3', '4'], 1.,      60, 1e-2,  1e4, tBGst, ' BG startup',kBlue-1, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
    "EkinEpBGac"  : [ ['3', '4'], 1.,      60, 1e-2,  1e4, tBGac, ' BG after Cond',kAzure-3, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
    "EkinEpBHds"  : [ ['3', '4'], nprim/R12m,  60, 1e-2, 1e4, tBH,' BH 12 min loss',kPink-9, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
    "EkinEpBHop"  : [ ['3', '4'], nprim/R100h,  60, 1e-2,1e4, tBH,' BH 100h loss',kGreen+2, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],

    "EkinPhBGst"  : [ ['7'], 1.,      60, 1e-2,  1e4, tBGst, ' BG startup',kBlue-1, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
    "EkinPhBGac"  : [ ['7'], 1.,      60, 1e-2,  1e4, tBGac, ' BG after Cond',kAzure-3, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
    "EkinPhBHds"  : [ ['7'], nprim/R12m,  60, 1e-2, 1e4, tBH,' BH 12 min loss',kPink-9, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
    "EkinPhBHop"  : [ ['7'], nprim/R100h,  60, 1e-2,1e4, tBH,' BH 100h loss',kGreen+2, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],

    "EkinChBGst"  : [ ['13','14','15','16'], 1.,      60, 1e-2,  1e4, tBGst, ' BG startup',kBlue-1, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
    "EkinChBGac"  : [ ['13','14','15','16'], 1.,      60, 1e-2,  1e4, tBGac, ' BG after Cond',kAzure-3, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
    "EkinChBHds"  : [ ['13','14','15','16'], nprim/R12m,  60, 1e-2, 1e4, tBH,' BH 12 min loss',kPink-9, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
    "EkinChBHop"  : [ ['13','14','15','16'], nprim/R100h,  60, 1e-2,1e4, tBH,' BH 100h loss',kGreen+2, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],

    "RadNMuBGst"  : [ ['10', '11'], 1. , 242, 0, 1210, tBGst, 'BG startup', kBlue-1,  '-9999','r [cm]',  'particles/cm^{2}/s'],
    "RadNMuBGac"  : [ ['10', '11'], 1. , 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,  '-9999','r [cm]',  'particles/cm^{2}/s'],
    "RadNMuBHds"  : [ ['10', '11'], nprim/R12m  , 242, 0, 1210, tBH, 'BH 12 min loss ', kPink-9,  '-9999','r [cm]',  'particles/cm^{2}/s'],
    "RadNMuBHop"  : [ ['10', '11'], nprim/R100h , 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,  '-9999','r [cm]',  'particles/cm^{2}/s'],

    "RadNNeBGst"  : [ ['8'], 1. , 242, 0, 1210, tBGst, 'BG startup', kBlue-1,  '-9999','r [cm]',  'particles/cm^{2}/s'],
    "RadNNeBGac"  : [ ['8'], 1. , 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,  '-9999','r [cm]',  'particles/cm^{2}/s'],
    "RadNNeBHds"  : [ ['8'], nprim/R12m  , 242, 0, 1210, tBH, 'BH 12 min loss', kPink-9,  '-9999','r [cm]',  'particles/cm^{2}/s'],
    "RadNNeBHop"  : [ ['8'], nprim/R100h , 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,  '-9999','r [cm]',  'particles/cm^{2}/s'],

    "RadNPrBGst"  : [ ['1'], 1. , 242, 0, 1210, tBGst, 'BG startup', kBlue-1,  '-9999','r [cm]',  'particles/cm^{2}/s'],
    "RadNPrBGac"  : [ ['1'], 1. , 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,  '-9999','r [cm]',  'particles/cm^{2}/s'],
    "RadNPrBHds"  : [ ['1'], nprim/R12m  , 242, 0, 1210, tBH, 'BH 12 min loss', kPink-9,  '-9999','r [cm]',  'particles/cm^{2}/s'],
    "RadNPrBHop"  : [ ['1'], nprim/R100h , 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,  '-9999','r [cm]',  'particles/cm^{2}/s'],

    "RadNPhBGst"  : [ ['7'], 1. , 242, 0, 1210, tBGst, 'BG startup', kBlue-1,  '-9999','r [cm]',  'particles/cm^{2}/s'],
    "RadNPhBGac"  : [ ['7'], 1. , 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,  '-9999','r [cm]',  'particles/cm^{2}/s'],
    "RadNPhBHds"  : [ ['7'], nprim/R12m  , 242, 0, 1210, tBH, 'BH 12min loss', kPink-9,  '-9999','r [cm]',  'particles/cm^{2}/s'],
    "RadNPhBHop"  : [ ['7'], nprim/R100h , 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,  '-9999','r [cm]',  'particles/cm^{2}/s'],

    "RadNChBGst"  : [ ['13','14','15','16'], 1. , 242, 0, 1210, tBGst, 'BG startup', kBlue-1,  '-9999','r [cm]',  'particles/cm^{2}/s'],
    "RadNChBGac"  : [ ['13','14','15','16'], 1. , 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,  '-9999','r [cm]',  'particles/cm^{2}/s'],
    "RadNChBHds"  : [ ['13','14','15','16'], nprim/R12m  , 242, 0, 1210, tBH, 'BH 12 min loss', kPink-9,  '-9999','r [cm]',  'particles/cm^{2}/s'],
    "RadNChBHop"  : [ ['13','14','15','16'], nprim/R100h , 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,  '-9999','r [cm]',  'particles/cm^{2}/s'],

    "RadNEpBGst"  : [ ['3', '4'], 1. , 242, 0, 1210, tBGst, 'BG startup', kBlue-1,  '-9999','r [cm]',  'particles/cm^{2}/s'],
    "RadNEpBGac"  : [ ['3', '4'], 1. , 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,  '-9999','r [cm]',  'particles/cm^{2}/s'],
    "RadNEpBHds"  : [ ['3', '4'], nprim/R12m  , 242, 0, 1210, tBH, 'BH 12 min loss', kPink-9,  '-9999','r [cm]',  'particles/cm^{2}/s'],
    "RadNEpBHop"  : [ ['3', '4'], nprim/R100h , 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,  '-9999','r [cm]',  'particles/cm^{2}/s'],

    "RadEnMuBGst"  : [ ['10', '11'], 1. , 242, 0, 1210, tBGst, 'BG startup', kBlue-1,  '-9999','r [cm]',  'GeV/cm^{2}/s'],
    "RadEnMuBGac"  : [ ['10', '11'], 1. , 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,  '-9999','r [cm]',  'GeV/cm^{2}/s'],
    "RadEnMuBHds"  : [ ['10', '11'], nprim/R12m  , 242, 0, 1210, tBH, 'BH 12 min loss ', kPink-9,  '-9999','r [cm]',  'GeV/cm^{2}/s'],
    "RadEnMuBHop"  : [ ['10', '11'], nprim/R100h , 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,  '-9999','r [cm]',  'GeV/cm^{2}/s'],

    "RadEnNeBGst"  : [ ['8'], 1. , 242, 0, 1210, tBGst, 'BG startup', kBlue-1,  '-9999','r [cm]',  'GeV/cm^{2}/s'],
    "RadEnNeBGac"  : [ ['8'], 1. , 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,  '-9999','r [cm]',  'GeV/cm^{2}/s'],
    "RadEnNeBHds"  : [ ['8'], nprim/R12m  , 242, 0, 1210, tBH, 'BH 12 min loss', kPink-9,  '-9999','r [cm]',  'GeV/cm^{2}/s'],
    "RadEnNeBHop"  : [ ['8'], nprim/R100h , 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,  '-9999','r [cm]',  'GeV/cm^{2}/s'],

    "RadEnPrBGst"  : [ ['1'], 1. , 242, 0, 1210, tBGst, 'BG startup', kBlue-1,  '-9999','r [cm]',  'GeV/cm^{2}/s'],
    "RadEnPrBGac"  : [ ['1'], 1. , 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,  '-9999','r [cm]',  'GeV/cm^{2}/s'],
    "RadEnPrBHds"  : [ ['1'], nprim/R12m  , 242, 0, 1210, tBH, 'BH 12 min loss', kPink-9,  '-9999','r [cm]',  'GeV/cm^{2}/s'],
    "RadEnPrBHop"  : [ ['1'], nprim/R100h , 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,  '-9999','r [cm]',  'GeV/cm^{2}/s'],

    "RadEnPhBGst"  : [ ['7'], 1. , 242, 0, 1210, tBGst, 'BG startup', kBlue-1,  '-9999','r [cm]',  'GeV/cm^{2}/s'],
    "RadEnPhBGac"  : [ ['7'], 1. , 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,  '-9999','r [cm]',  'GeV/cm^{2}/s'],
    "RadEnPhBHds"  : [ ['7'], nprim/R12m  , 242, 0, 1210, tBH, 'BH 12min loss', kPink-9,  '-9999','r [cm]',  'GeV/cm^{2}/s'],
    "RadEnPhBHop"  : [ ['7'], nprim/R100h , 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,  '-9999','r [cm]',  'GeV/cm^{2}/s'],

    "RadEnChBGst"  : [ ['13','14','15','16'], 1. , 242, 0, 1210, tBGst, 'BG startup', kBlue-1,  '-9999','r [cm]',  'GeV/cm^{2}/s'],
    "RadEnChBGac"  : [ ['13','14','15','16'], 1. , 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,  '-9999','r [cm]',  'GeV/cm^{2}/s'],
    "RadEnChBHds"  : [ ['13','14','15','16'], nprim/R12m  , 242, 0, 1210, tBH, 'BH 12 min loss', kPink-9,  '-9999','r [cm]',  'GeV/cm^{2}/s'],
    "RadEnChBHop"  : [ ['13','14','15','16'], nprim/R100h , 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,  '-9999','r [cm]',  'GeV/cm^{2}/s'],

    "RadEnEpBGst"  : [ ['3', '4'], 1. , 242, 0, 1210, tBGst, 'BG startup', kBlue-1,  '-9999','r [cm]',  'GeV/cm^{2}/s'],
    "RadEnEpBGac"  : [ ['3', '4'], 1. , 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,  '-9999','r [cm]',  'GeV/cm^{2}/s'],
    "RadEnEpBHds"  : [ ['3', '4'], nprim/R12m  , 242, 0, 1210, tBH, 'BH 12 min loss', kPink-9,  '-9999','r [cm]',  'GeV/cm^{2}/s'],
    "RadEnEpBHop"  : [ ['3', '4'], nprim/R100h , 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,  '-9999','r [cm]',  'GeV/cm^{2}/s'],
}

# ---------------------------------------------------------------------------------
# 4 TeV case
# ---------------------------------------------------------------------------------

sDict_4TeV = {}
