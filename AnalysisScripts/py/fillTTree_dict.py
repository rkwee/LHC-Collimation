#!/usr/bin/python
#
# R Kwee-Hinzmann, 2013
# ---------------------------------------------------------------------------------
import ROOT, math
from ROOT import *
from helpers import workpath
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
R12m    = 146563140 # Hz from cv07
R100h   = 293126 #Hz from cv07
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# dict  key = hname  #0 particleTypes #1 norm #2 nbins #3 xmin #4 xmax #5 ttree #6 prettyName 
                     #7 hcolor #8 othercut[as string OR float/int] #9 xtitle #10 ytitle #11 ynbin #12 ymin #13 ymax
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
def generate_sDict( tag, norm, tBBG, yrel ):
    sDict_gen = { 
 'EkinAll'+tag:[ ['all'],norm,60, 1e-2, 1e4, tBBG, 'all',kBlack, '-9999','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'EkinMuons'+tag:[ ['10', '11'], norm,60, 1e-2, 1e4, tBBG, '#mu^{#pm}',kAzure, '-9999','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'EkinProtons'+tag:[ ['1'], norm,60, 1e-2, 1e4, tBBG, 'protons', kCyan, '-9999','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'EkinNeutrons'+tag:[ ['8'], norm,60, 1e-2, 1e4, tBBG, 'neutrons', kRed, '-9999','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'EkinPhotons'+tag:[ ['7'], norm,60, 1e-2, 1e4, tBBG, '#gamma',kOrange+1, '-9999','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'EkinElecPosi'+tag:[ ['3', '4'],norm,60, 1e-2, 1e4, tBBG, 'e^{#pm}', kOrange-2, '-9999','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'EkinSel1'+tag:[ ['3','4','1','7','8','10','11'], norm, 60, 1e-2, 1e4, tBBG, 'e^{#pm}, #mu^{#pm}, #gamma, p, n', kYellow-7, '-9999','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'EkinPions'+tag:[ ['13','14'], norm,60, 1e-2, 1e4, tBBG, '#pi^{#pm}', kPink+1, '-9999','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'EkinKaons'+tag:[ ['15','16','24'], norm,60, 1e-2, 1e4, tBBG, 'K^{#pm,0}', kSpring-1,'-9999','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'EkinSel2'+tag:[ ['3','4','1','7','8','10','11','13','14','23'], norm, 60, 1e-2, 1e4, tBBG, 'e^{#pm}, #mu^{#pm}, #gamma, p, n, #pi^{#pm,0}', kViolet, '-9999','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'EkinSel3'+tag:[ ['3','4','1','7','8','10','11','13','14','23','15','16','24'], norm, 60, 1e-2, 1e4, tBBG, 'e^{#pm}, #mu^{#pm}, #gamma, p, n, #pi^{#pm,0}, K^{#pm,0}', kRed, '-9999','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],

 'EkinPos'+tag:[ ['1','10','4','15','13'], norm,60, 1e-2, 1e4, tBBG,'p,K^{+},e^{+},#mu^{+},#pi^{+}', kGreen+1, '-9999','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'EkinNeg'+tag:[ ['11','3','14','16'], norm,60, 1e-2, 1e4 , tBBG, 'K^{-}, e^{-},#mu^{-},#pi^{-}', kMagenta+1, '-9999','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'EkinNeu'+tag:[ ['7','24','8'], norm, 60, 1e-2, 1e4, tBBG, 'n,K^{0},#gamma', kBlue, '-9999','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'EkinPiPlus'+tag:[ ['13'], norm, 60, 1e-2, 1e4, tBBG, '#pi^{+}', kPink+2, '-9999','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'EkinPiMinus'+tag:[ ['14'], norm, 60, 1e-2, 1e4, tBBG, '#pi^{-}', kPink+3, '-9999','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],

 'EkinAllRInBP'+tag:[ ['all'],norm,60, 1e-2, 1e4, tBBG, 'all r < r_{bp}', kBlue-3, '<:6.9','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'EkinAllROutBP'+tag:[ ['all'],norm,60, 1e-2, 1e4, tBBG, 'all r #geq r_{bp}', kMagenta, '>=:6.9','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'EkinPiPlusRInBP'+tag:[ ['13'], norm,60, 1e-2, 1e4, tBBG, '#pi^{+} r < r_{bp}', kCyan-2, '<:6.9','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'EkinPiPlusROutBP'+tag:[ ['13'], norm,60, 1e-2, 1e4, tBBG, '#pi^{+} r #geq r_{bp}', kPink-2, '>=:6.9','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'EkinPiMinusRInBP'+tag:[ ['14'], norm,60, 1e-2, 1e4, tBBG, '#pi^{-} r < r_{bp}', kCyan+1, '<:6.9','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'EkinPiMinusROutBP'+tag:[ ['14'], norm,60, 1e-2, 1e4, tBBG, '#pi^{-} r #geq r_{bp}', kPink+1, '>=:6.9','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'EkinNeutronsRInBP'+tag:[ ['8'], norm,60, 1e-2, 1e4, tBBG, 'n r < r_{bp}', kRed+1, '<:6.9','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'EkinNeutronsROutBP'+tag:[ ['8'], norm,60, 1e-2, 1e4, tBBG, 'n r #geq r_{bp}', kRed+2, '>=:6.9','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'EkinPiKaRInBP'+tag:[ ['13','14','15','16'], norm,60, 1e-2, 1e4, tBBG, '#pi^{#pm}, K^{#pm} r < r_{bp}', kCyan-2, '<:6.9','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'EkinPiKaRInBP'+tag:[ ['13','14','15','16'], norm,60, 1e-2, 1e4, tBBG, '#pi^{#pm}, K^{#pm} r #geq r_{bp}', kCyan-2, '>=:6.9','E [GeV]', '#frac{dN(counts'+yrel+')}{dlog E}', -9999, -9999, -9999, ],
 'RadNAll'+tag:[ ['all'],norm, 240, 0, 1200, tBBG, 'all', kBlack, '-9999','r [cm]', 'particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'RadNMuons'+tag:[ ['10', '11'], norm, 240, 0, 1200, tBBG, '#mu^{#pm} ', kAzure, '-9999','r [cm]', 'particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'RadNNeutrons'+tag:[ ['8'], norm, 240, 0, 1200, tBBG, 'neutrons',kRed, '-9999','r [cm]', 'particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'RadNProtons'+tag:[ ['1'], norm, 240, 0, 1200, tBBG, 'protons', kCyan, '-9999','r [cm]', 'particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'RadNPhotons'+tag:[ ['7'], norm, 240, 0, 1200, tBBG, '#gamma', kOrange+1, '-9999','r [cm]', 'particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'RadNElecPosi'+tag:[ ['3','4'], norm, 240, 0, 1200, tBBG, 'e^{#pm}', kOrange-2, '-9999','r [cm]', 'particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'RadNPions'+tag:[ ['13','14'], norm, 240, 0, 1200, tBBG, '#pi^{#pm}',kPink+1, '-9999','r [cm]', 'particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'RadNKaons'+tag:[ ['15','16','24'], norm, 240, 0, 1200, tBBG, 'K^{#pm,0}', kSpring-1, '-9999','r [cm]', 'particles/cm^{2}'+yrel, -9999, -9999, -9999, ],

 'RadNMuonsEAll'+tag:[ ['10', '11'], norm, 240, 0, 1200, tBBG, '#mu^{#pm}', kRed-10, '-9999','r [cm]', 'particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'RadNMuonsE20'+tag:[ ['10', '11'], norm, 240, 0, 1200, tBBG, '#mu^{#pm} with E_{kin} > 20 GeV', kRed-7,'20.','r [cm]', 'particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'RadNMuonsE100'+tag:[ ['10', '11'], norm, 240, 0, 1200, tBBG, '#mu^{#pm} with E_{kin} > 100 GeV', kRed-6,'100.','r [cm]', 'particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'RadNMuonsE500'+tag:[ ['10', '11'], norm, 240, 0, 1200, tBBG, '#mu^{#pm} with E_{kin} > 500 GeV', kRed-1,'500.','r [cm]', 'particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'RadNMuonsE1000'+tag:[ ['10', '11'], norm, 240, 0, 1200, tBBG, '#mu^{#pm} with E_{kin} > 1 TeV', kRed-1,'1000.','r [cm]', 'particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 
 'RadNNeg'+ tag:[ ['11','3','14','16'], norm, 240, 0, 1200, tBBG, 'K^{-}, e^{-},#mu^{-},#pi^{-}', kMagenta+1, '-9999','r [cm]', 'particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'RadNPos'+ tag:[ ['1','10','4','15','13'], norm, 240, 0, 1200, tBBG, 'p,K^{+},e^{+},#mu^{+},#pi^{+}', kGreen+1, '-9999','r [cm]', 'particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'RadNNeu'+tag:[ ['7','24','8'], norm, 240, 0, 1200, tBBG, 'n,K^{0},#gamma', kBlue, '-9999','r [cm]', 'particles/cm^{2}'+yrel, -9999, -9999, -9999, ],

 'RadEnAll'+tag:[ ['all'],norm, 240, 0, 1200, tBBG, 'all', kBlack, '-9999','r [cm]', 'GeV/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'RadEnMuons'+tag:[ ['10', '11'], norm, 240, 0, 1200, tBBG, '#mu^{#pm} ', kAzure, '-9999','r [cm]', 'GeV/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'RadEnNeutrons'+tag:[ ['8'], norm, 240, 0, 1200, tBBG, 'neutrons',kRed, '-9999','r [cm]', 'GeV/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'RadEnProtons'+tag:[ ['1'], norm, 240, 0, 1200, tBBG, 'protons', kCyan, '-9999','r [cm]', 'GeV/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'RadEnPhotons'+tag:[ ['7'], norm, 240, 0, 1200, tBBG, '#gamma', kOrange+1, '-9999','r [cm]', 'GeV/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'RadEnElecPosi'+tag:[ ['3','4'], norm, 240, 0, 1200, tBBG, 'e^{#pm}', kOrange-2, '-9999','r [cm]', 'GeV/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'RadEnPions'+tag:[ ['13','14'], norm, 240, 0, 1200, tBBG, '#pi^{#pm}', kPink+1, '-9999','r [cm]', 'GeV/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'RadEnKaons'+tag:[ ['15','16','24'], norm, 240, 0, 1200, tBBG, 'K^{#pm,0}', kSpring-1, '-9999','r [cm]', 'GeV/cm^{2}'+yrel, -9999, -9999, -9999, ],
 
 'RadEnNeg'+tag:[ ['11','3','14','16'], norm, 240, 0, 1200, tBBG, 'K^{-}, e^{-},#mu^{-},#pi^{-}', kMagenta+1, '-9999','r [cm]', 'particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'RadEnPos'+tag:[ ['1','10','4','15','13'], norm, 240, 0, 1200, tBBG, 'p,K^{+},e^{+},#mu^{+},#pi^{+}', kGreen+1, '-9999','r [cm]', 'particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'RadEnNeu'+tag:[ ['7','24','8'], norm, 240, 0, 1200, tBBG, 'n,K^{0},#gamma', kBlue, '-9999','r [cm]', 'particles/cm^{2}'+yrel, -9999, -9999, -9999, ],

 'PhiNAll'+tag:[ ['all'],norm, 100, -math.pi, math.pi, tBBG, 'all',kBlack, '-9999','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNMuons'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} ',kAzure, '-9999','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNMuE100'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm}  E > 100 GeV',kAzure+1, 'E > 100','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNNeutrons'+tag:[ ['8'], norm, 100, -math.pi, math.pi, tBBG, 'neutrons', kRed, '-9999','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ], 
 'PhiNProtons'+tag:[ ['1'], norm, 100, -math.pi, math.pi, tBBG, 'protons',kCyan, '-9999','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNPhotons'+tag:[ ['7'], norm, 100, -math.pi, math.pi, tBBG, '#gamma', kOrange+1, '-9999','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNElecPosi'+tag:[ ['3', '4'],norm, 100, -math.pi, math.pi, tBBG, 'e^{#pm}',kOrange-2, '-9999','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNPionsChar'+tag:[ ['13','14',], norm, 100, -math.pi, math.pi, tBBG, '#pi^{#pm}', kViolet, '-9999','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNKaonsChar'+tag:[ ['15','16'], norm, 100, -math.pi, math.pi, tBBG, 'K^{#pm}',kSpring-1, '-9999','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],

 'PhiNNeg'+tag:[ ['11','3','14','16'], norm, 100, -math.pi, math.pi, tBBG, 'K^{-}, e^{-},#mu^{-},#pi^{-}',kMagenta+1,'-9999','r [cm]','particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'PhiNPos'+tag:[ ['1','10','4','15','13'], norm, 100, -math.pi, math.pi, tBBG, 'p,K^{+},e^{+},#mu^{+},#pi^{+}',kGreen+1,'-9999','r [cm]','particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'PhiNNeu'+tag:[ ['7','24','8'], norm, 100, -math.pi, math.pi, tBBG, 'n,K^{0},#gamma',kBlue,'-9999','r [cm]','particles/cm^{2}'+yrel, -9999, -9999, -9999, ],

 'PhiNMuPlus'+tag:[ ['10'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{+} ',kCyan-8, '-9999','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNMuMinus'+tag:[ ['11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{-} ',kAzure+8, '-9999','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNMuR10'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r > 10 cm',kAzure+4, 'r > 10','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNMuR50'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r > 50 cm',kAzure+5, 'r > 50','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNMuR100'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r > 100 cm',kAzure+6,'r > 100','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNMuR200'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r > 200 cm',kAzure-1,'r > 200','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNMuR300'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r > 300 cm',kCyan-6,'r > 300','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNMuR400'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r > 400 cm',kCyan-4,'r > 400','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNMuR500'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r > 500 cm',kAzure+3,'r > 500','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNMuR1000'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r > 1000 cm',kCyan-8,'r > 1000','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNMuRlt10'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r < 10 cm',kAzure+4, 'r < 10','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNMuRlt50'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r < 50 cm',kAzure+5, 'r < 50','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNMuRlt100'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r < 100 cm',kAzure+6,'r < 100','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNMuRlt200'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r < 200 cm',kAzure-1,'r < 200','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNMuRlt300'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r < 300 cm',kCyan-6,'r < 300','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNMuRlt400'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r < 400 cm',kCyan-4,'r < 400','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNMuRlt500'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r < 500 cm',kAzure+3,'r < 500','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 'PhiNMuRlt1000'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r < 1000 cm',kCyan-8,'r < 1000','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 
 'PhiEnAll'+tag:[ ['all'],norm, 100, -math.pi, math.pi, tBBG, 'all',kBlack, '-9999','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnMuons'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} ',kAzure, '-9999','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnNeutrons'+tag:[ ['8'], norm, 100, -math.pi, math.pi, tBBG, 'neutrons', kRed, '-9999','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnProtons'+tag:[ ['1'], norm, 100, -math.pi, math.pi, tBBG, 'protons',kCyan, '-9999','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnPhotons'+tag:[ ['7'], norm, 100, -math.pi, math.pi, tBBG, '#gamma',kOrange+1, '-9999','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnElecPosi'+tag:[ ['3','4'], norm, 100, -math.pi, math.pi, tBBG, 'e^{#pm}',kOrange-2, '-9999','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnPions'+tag:[ ['13','14'],norm, 100, -math.pi, math.pi, tBBG, '#pi^{#pm}',kPink+1, '-9999','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnKaons'+tag:[ ['15','16','24'],norm, 100, -math.pi, math.pi, tBBG, 'K^{#pm,0}',kSpring-1, '-9999','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],

 'PhiEnMuPlus'+tag:[ ['10'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{+} ',kCyan-8, '-9999','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnMuMinus'+tag:[ ['11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{-} ',kAzure+8, '-9999','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnMuE100'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} E > 100 GeV',kAzure+1, 'E > 100','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnMuR10'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r > 10 cm ',kAzure+4,'r > 10','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnMuR50'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r > 50 cm ',kAzure+5,'r > 50','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnMuR100'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r > 100 cm ',kAzure+6,'r > 100','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnMuR200'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r > 200 cm ',kAzure-1,'r > 200','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnMuR300'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r > 300 cm ',kCyan-6,'r > 300','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnMuR400'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r > 400 cm ',kCyan-4,'r > 400','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnMuR500'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r > 500 cm ',kAzure+3,'r > 500','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnMuR1000'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r > 1000 cm ',kCyan-8,'r > 1000','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],

 'PhiEnMuRlt10'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r < 10 cm ',kAzure+4,'r < 10','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnMuRlt50'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r < 50 cm ',kAzure+5,'r < 50','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnMuRlt100'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r < 100 cm ',kAzure+6,'r < 100','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnMuRlt200'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r < 200 cm ',kAzure-1,'r < 200','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnMuRlt300'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r < 300 cm ',kCyan-6,'r < 300','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnMuRlt400'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r < 400 cm ',kCyan-4,'r < 400','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnMuRlt500'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r < 500 cm ',kAzure+3,'r < 500','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnMuRlt1000'+tag:[ ['10', '11'], norm, 100, -math.pi, math.pi, tBBG, '#mu^{#pm} r < 1000 cm ',kCyan-8,'r < 1000','#phi [rad]', 'GeV/rad'+yrel, -9999, -9999, -9999, ],

 'PhiEnNeg'+tag:[ ['11','3','14','16'], norm, 100, -math.pi, math.pi, tBBG, 'K^{-}, e^{-},#mu^{-},#pi^{-}',kMagenta+1,'-9999','#phi [rad]','GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnPosP'+tag:[ ['1','10','4','15','13'], norm, 100, -math.pi, math.pi, tBBG, 'p,K^{+},e^{+},#mu^{+},#pi^{+}',kGreen+1,'-9999','#phi [rad]','GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnPos'+tag:[ ['10','4','15','13'], norm, 100, -math.pi, math.pi, tBBG, 'K^{+},e^{+},#mu^{+},#pi^{+}',kGreen+1,'-9999','#phi [rad]','GeV/rad'+yrel, -9999, -9999, -9999, ],
 'PhiEnNeu'+tag:[ ['7','24','8'], norm, 100, -math.pi, math.pi, tBBG, 'n,K^{0},#gamma',kBlue,'-9999','#phi [rad]','GeV/rad'+yrel, -9999, -9999, -9999, ],
 'XcoorNNeg'+tag:[ ['11','3','14','16'], norm, 160, -400., 400., tBBG, 'K^{-}, e^{-},#mu^{-},#pi^{-}',kMagenta+1,'-9999','x [cm]','particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'XcoorNPos'+tag:[ ['1','10','4','15','13'], norm, 160, -400., 400., tBBG, 'p,K^{+},e^{+},#mu^{+},#pi^{+}',kGreen+1,'-9999','x [cm]','particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'XcoorNNeu'+tag:[ ['7','24','8'], norm, 160, -400., 400., tBBG, 'n,K^{0},#gamma',kBlue,'-9999','x [cm]','particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
        
 'YcoorNNeg'+tag:[ ['11','3','14','16'], norm, 160, -400., 400., tBBG, 'K^{-}, e^{-},#mu^{-},#pi^{-}',kMagenta+1,'-9999','y [cm]','particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'YcoorNPos'+tag:[ ['1','10','4','15','13'], norm, 160, -400., 400., tBBG, 'p,K^{+},e^{+},#mu^{+},#pi^{+}',kGreen+1,'-9999','y [cm]','particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 'YcoorNNeu'+tag:[ ['7','24','8'], norm, 160, -400., 400., tBBG, 'n,K^{0},#gamma',kBlue,'-9999','y [cm]','particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 
 'XYNAll'+tag:[ ['all'],norm, 240, -120, 120, tBBG, 'all', kWhite, '-9999','x [cm]','y [cm]', 120, -120, 120, ],
 'XYNPhotons'+tag:[ ['7'], norm, 240, -120, 120, tBBG, '#gamma', kWhite, '-9999','x [cm]','y [cm]', 120, -120, 120, ],
 'XYNElecPosi'+tag:[ ['3','4'], norm, 240, -120, 120, tBBG, 'e^{#pm}', kWhite, '-9999','x [cm]','y [cm]', 120, -120, 120, ],
 'XYNMuons'+tag:[ ['10', '11'], norm, 240, -120, 120, tBBG, '#mu^{#pm} ', kWhite, '-9999','x [cm]','y [cm]', 120, -120, 120, ],
 'XYNChar'+tag:[ ['11','3','14','16','1','10','4','15','13'], norm, 960, -120, 120, tBBG, 'p,K^{#pm},e^{#pm},#mu^{#pm},#pi^{#pm} ', kWhite, '-9999','x [cm]','y [cm]', 120, -120, 120, ],
 
 'XYNElecPosiE'+tag:[ ['3','4'], norm, 240, -120, 120, tBBG, 'e^{#pm} 10 GeV < E_{kin} < 150 GeV',kWhite, '10.:150.','x [cm]','y [cm]', 240, -120, 120, ],
 'XYNPhotonsE'+tag:[ ['7'], norm, 240, -120, 120, tBBG, '#gamma 10 GeV < E_{kin} < 150 GeV',kWhite, '10.:150.','x [cm]','y [cm]', 240, -120, 120, ],
 'XYNNeutronsE'+tag:[ ['8'], norm, 240, -120, 120, tBBG, 'neutrons 10 GeV < E_{kin} < 150 GeV',kWhite, '10.:150.','x [cm]','y [cm]', 240, -120, 120, ],
 'XYNProtonsE'+tag:[ ['1'], norm, 240, -120, 120, tBBG, 'protons 10 GeV < E_{kin} < 150 GeV', kWhite, '10.:150.','x [cm]','y [cm]', 240, -120, 120, ],
 'XYNPiPlusE'+tag:[ ['13'], norm, 240, -120, 120, tBBG, '#pi^{+} 10 GeV < E_{kin} < 150 GeV',kWhite, '10.:150.','x [cm]','y [cm]', 240, -120, 120, ],
 'XYNPiMinusE'+tag:[ ['14'], norm, 240, -120, 120, tBBG, '#pi^{-} 10 GeV < E_{kin} < 150 GeV',kWhite, '10.:150.','x [cm]','y [cm]', 240, -120, 120, ],
 'XYNKaonsE'+tag:[ ['15','16'], norm, 240, -120, 120, tBBG, 'K^{#pm} 10 GeV < E_{kin} < 150 GeV',kWhite, '10.:150.','x [cm]','y [cm]', 240, -120, 120, ],
 'XYNKaonPlusE'+tag:[ ['15'], norm, 240, -120, 120, tBBG, 'K^{+} 10 GeV < E_{kin} < 150 GeV', kWhite, '10.:150.','x [cm]','y [cm]', 240, -120, 120, ],
 'XYNKaonMinusE'+tag:[ ['16'], norm, 240, -120, 120, tBBG, 'K^{-} 10 GeV < E_{kin} < 150 GeV', kWhite, '10.:150.','x [cm]','y [cm]', 240, -120, 120, ],
 'XYNMuonsE10'+tag:[ ['10', '11'], norm, 240, -120, 120, tBBG, '#mu^{#pm} E_{kin} > 10 GeV', kWhite, '10.','x [cm]','y [cm]', 240, -120, 120, ], 
 'XYNMuonsE500'+tag:[ ['10', '11'], norm, 240, -120, 120, tBBG, '#mu^{#pm} E_{kin} > 500 GeV', kWhite, '100.','x [cm]','y [cm]', 240, -120, 120, ], 
 
 'OrigXYMuon'+tag:[ ['10', '11'],  norm, 240, -120, 120, tBBG, '#mu^{#pm} ', kWhite, '-9999','x [cm]','y [cm]', 240, -120, 120, ],
 'OrigXZMuon'+tag:[ ['10', '11'],  norm, 386, 2260.0, 21560.0, tBBG, '#mu^{#pm} ', kWhite, '-9999','z [cm]','x [cm]', 240, -120, 120, ],
 'ProfOrigXZMuon'+tag:[ ['10', '11'],  norm, 386, 2260.0, 21560.0, tBBG, '#mu^{#pm} ', kBlue-3, '-9999','z [cm]','x [cm]', 240, -120, 120, ],
 'ProfOrigYZMuon'+tag:[ ['10', '11'],  norm, 386, 2260.0, 21560.0, tBBG, '#mu^{#pm} ', kBlue-3, '-9999','z [cm]','y [cm]', 240, -120, 120, ],
 'OrigYZMuon'+tag:[ ['10', '11'],  norm, 386, 2260.0, 21560.0, tBBG, '#mu^{#pm} ', kWhite, '-9999','z [cm]','y [cm]', 240, -120, 120, ],
 'OrigXYMuonsE100'+tag:[ ['10', '11'], norm, 240, -120, 120, tBBG, '#mu^{#pm} E_{kin} > 100 GeV', kWhite, '100.','x [cm]','y [cm]', 240, -120, 120, ], 
 'OrigXZMuonsE100'+tag:[ ['10', '11'], norm, 386, 2260.0, 21560.0, tBBG, '#mu^{#pm} E_{kin} > 100 GeV', kWhite, '100.','z [cm]','x [cm]', 240, -120, 120, ], 
 'OrigYZMuonsE100'+tag:[ ['10', '11'], norm, 386, 2260.0, 21560.0, tBBG, '#mu^{#pm} E_{kin} > 100 GeV', kWhite, '100.','z [cm]','y [cm]', 240, -120, 120, ], 

 'ZcoorOrigMu'+tag:[ ['11','10'], norm, 386, 2260., 21560., tBBG, '#mu^{#pm}',kMagenta+1,'-9999','z [cm]','particles/cm^{2}'+yrel, -9999, -9999, -9999, ],
 }
    return sDict_gen
# ---------------------------------------------------------------------------------
# comp plots BG vs BH
# ---------------------------------------------------------------------------------
# BG norm: scaling to higher bunch intensity
normBGst = 1.15/2.2
normBGac = 1.15/1.1 # additional factor 2 due to higher contribution from SR

R12m    = 146563140 # Hz from cv07                                                                                                                                                
R100h   = 293126 #Hz from cv07      

# norm is already appplied when root file was produced
#R12m ,R100h,nprim = 1.,1.,1.
# HL -2013-

treeName = 'particle'
# -- beamgas for start up scenario, high 
bbgFile = workpath + 'data/HL/hilumi_ir1_fort_scaled_startup_max_30.root'
print "Opening...", bbgFile
rfBGst  = TFile(bbgFile)
tBGst   = rfBGst.Get(treeName)

# -- HL beamgas after conditioning, high
bbgFile = workpath + 'data/HL/hilumi_ir1_fort_scaled_afterconditioning_max_30.root'
print "Opening...", bbgFile
rfBGac  = TFile(bbgFile)
tBGac   = rfBGac.Get(treeName)

# -- HL beamhalo
bbgFile = workpath + 'data/HL/hllhc_ir1_b2_nprim7330000_30.root'
print "Opening...", bbgFile
rfBH    = TFile(bbgFile)
tBH     = rfBH.Get(treeName)
nprim   = 7330000.

sDict_HL_comp = {

 "EkinMuBGst": [ ['10', '11'], normBGst,60, 1e-2,1e4, tBGst, ' BG startup',kBlue-1, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
 "EkinMuBGac": [ ['10', '11'], normBGac,60, 1e-2,1e4, tBGac, ' BG after Cond',kAzure-3, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
 "EkinMuBHds": [ ['10', '11'], nprim/R12m,60, 1e-2, 1e4, tBH,' BH 12 min loss',kPink-9, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
 "EkinMuBHop": [ ['10', '11'], nprim/R100h,60, 1e-2,1e4, tBH,' BH 100h loss',kGreen+2, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],

 "EkinPrBGst": [ ['1'], normBGst,60, 1e-2,1e4, tBGst, ' BG startup',kBlue-1, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
 "EkinPrBGac": [ ['1'], normBGac,60, 1e-2,1e4, tBGac, ' BG after Cond',kAzure-3, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
 "EkinPrBHds": [ ['1'], nprim/R12m,60, 1e-2, 1e4, tBH,' BH 12 min loss',kPink-9, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
 "EkinPrBHop": [ ['1'], nprim/R100h,60, 1e-2,1e4, tBH,' BH 100h loss',kGreen+2, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],

 "EkinNeBGst": [ ['8'], normBGst,60, 1e-2,1e4, tBGst, ' BG startup',kBlue-1, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
 "EkinNeBGac": [ ['8'], normBGac,60, 1e-2,1e4, tBGac, ' BG after Cond',kAzure-3, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
 "EkinNeBHds": [ ['8'], nprim/R12m,60, 1e-2, 1e4, tBH,' BH 12 min loss',kPink-9, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
 "EkinNeBHop": [ ['8'], nprim/R100h,60, 1e-2,1e4, tBH,' BH 100h loss',kGreen+2, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],

 "EkinEpBGst": [ ['3', '4'], normBGst,60, 1e-2,1e4, tBGst, ' BG startup',kBlue-1, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
 "EkinEpBGac": [ ['3', '4'], normBGac,60, 1e-2,1e4, tBGac, ' BG after Cond',kAzure-3, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
 "EkinEpBHds": [ ['3', '4'], nprim/R12m,60, 1e-2, 1e4, tBH,' BH 12 min loss',kPink-9, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
 "EkinEpBHop": [ ['3', '4'], nprim/R100h,60, 1e-2,1e4, tBH,' BH 100h loss',kGreen+2, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],

 "EkinPhBGst": [ ['7'], normBGst,60, 1e-2,1e4, tBGst, ' BG startup',kBlue-1, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
 "EkinPhBGac": [ ['7'], normBGac,60, 1e-2,1e4, tBGac, ' BG after Cond',kAzure-3, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
 "EkinPhBHds": [ ['7'], nprim/R12m,60, 1e-2, 1e4, tBH,' BH 12 min loss',kPink-9, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
 "EkinPhBHop": [ ['7'], nprim/R100h,60, 1e-2,1e4, tBH,' BH 100h loss',kGreen+2, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],

 "EkinChBGst": [ ['13','14','15','16'], normBGst,60, 1e-2,1e4, tBGst, ' BG startup',kBlue-1, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
 "EkinChBGac": [ ['13','14','15','16'], normBGac,60, 1e-2,1e4, tBGac, ' BG after Cond',kAzure-3, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
 "EkinChBHds": [ ['13','14','15','16'], nprim/R12m,60, 1e-2, 1e4, tBH,' BH 12 min loss',kPink-9, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],
 "EkinChBHop": [ ['13','14','15','16'], nprim/R100h,60, 1e-2,1e4, tBH,' BH 100h loss',kGreen+2, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', ],

 "RadNMuBGst": [ ['10', '11'], normBGst, 242, 0, 1210, tBGst, 'BG startup', kBlue-1,'-9999','r [cm]','particles/cm^{2}/s'],
 "RadNMuBGac": [ ['10', '11'], normBGac, 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,'-9999','r [cm]','particles/cm^{2}/s'],
 "RadNMuBHds": [ ['10', '11'], nprim/R12m, 242, 0, 1210, tBH, 'BH 12 min loss ', kPink-9,'-9999','r [cm]','particles/cm^{2}/s'],
 "RadNMuBHop": [ ['10', '11'], nprim/R100h , 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,'-9999','r [cm]','particles/cm^{2}/s'],

 "RadNNeBGst": [ ['8'], normBGst, 242, 0, 1210, tBGst, 'BG startup', kBlue-1,'-9999','r [cm]','particles/cm^{2}/s'],
 "RadNNeBGac": [ ['8'], normBGac, 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,'-9999','r [cm]','particles/cm^{2}/s'],
 "RadNNeBHds": [ ['8'], nprim/R12m, 242, 0, 1210, tBH, 'BH 12 min loss', kPink-9,'-9999','r [cm]','particles/cm^{2}/s'],
 "RadNNeBHop": [ ['8'], nprim/R100h , 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,'-9999','r [cm]','particles/cm^{2}/s'],

 "RadNPrBGst": [ ['1'], normBGst, 242, 0, 1210, tBGst, 'BG startup', kBlue-1,'-9999','r [cm]','particles/cm^{2}/s'],
 "RadNPrBGac": [ ['1'], normBGac, 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,'-9999','r [cm]','particles/cm^{2}/s'],
 "RadNPrBHds": [ ['1'], nprim/R12m, 242, 0, 1210, tBH, 'BH 12 min loss', kPink-9,'-9999','r [cm]','particles/cm^{2}/s'],
 "RadNPrBHop": [ ['1'], nprim/R100h , 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,'-9999','r [cm]','particles/cm^{2}/s'],

 "RadNPhBGst": [ ['7'], normBGst, 242, 0, 1210, tBGst, 'BG startup', kBlue-1,'-9999','r [cm]','particles/cm^{2}/s'],
 "RadNPhBGac": [ ['7'], normBGac, 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,'-9999','r [cm]','particles/cm^{2}/s'],
 "RadNPhBHds": [ ['7'], nprim/R12m, 242, 0, 1210, tBH, 'BH 12min loss', kPink-9,'-9999','r [cm]','particles/cm^{2}/s'],
 "RadNPhBHop": [ ['7'], nprim/R100h , 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,'-9999','r [cm]','particles/cm^{2}/s'],

 "RadNChBGst": [ ['13','14','15','16'], normBGst, 242, 0, 1210, tBGst, 'BG startup', kBlue-1,'-9999','r [cm]','particles/cm^{2}/s'],
 "RadNChBGac": [ ['13','14','15','16'], normBGac, 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,'-9999','r [cm]','particles/cm^{2}/s'],
 "RadNChBHds": [ ['13','14','15','16'], nprim/R12m, 242, 0, 1210, tBH, 'BH 12 min loss', kPink-9,'-9999','r [cm]','particles/cm^{2}/s'],
 "RadNChBHop": [ ['13','14','15','16'], nprim/R100h , 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,'-9999','r [cm]','particles/cm^{2}/s'],

 "RadNEpBGst": [ ['3', '4'], normBGst, 242, 0, 1210, tBGst, 'BG startup', kBlue-1,'-9999','r [cm]','particles/cm^{2}/s'],
 "RadNEpBGac": [ ['3', '4'], normBGac, 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,'-9999','r [cm]','particles/cm^{2}/s'],
 "RadNEpBHds": [ ['3', '4'], nprim/R12m, 242, 0, 1210, tBH, 'BH 12 min loss', kPink-9,'-9999','r [cm]','particles/cm^{2}/s'],
 "RadNEpBHop": [ ['3', '4'], nprim/R100h , 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,'-9999','r [cm]','particles/cm^{2}/s'],

 "RadEnMuBGst": [ ['10', '11'], normBGst, 242, 0, 1210, tBGst, 'BG startup', kBlue-1,'-9999','r [cm]','GeV/cm^{2}/s'],
 "RadEnMuBGac": [ ['10', '11'], normBGac, 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,'-9999','r [cm]','GeV/cm^{2}/s'],
 "RadEnMuBHds": [ ['10', '11'], nprim/R12m, 242, 0, 1210, tBH, 'BH 12 min loss ', kPink-9,'-9999','r [cm]','GeV/cm^{2}/s'],
 "RadEnMuBHop": [ ['10', '11'], nprim/R100h , 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,'-9999','r [cm]','GeV/cm^{2}/s'],

 "RadEnNeBGst": [ ['8'], normBGst, 242, 0, 1210, tBGst, 'BG startup', kBlue-1,'-9999','r [cm]','GeV/cm^{2}/s'],
 "RadEnNeBGac": [ ['8'], normBGac, 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,'-9999','r [cm]','GeV/cm^{2}/s'],
 "RadEnNeBHds": [ ['8'], nprim/R12m, 242, 0, 1210, tBH, 'BH 12 min loss', kPink-9,'-9999','r [cm]','GeV/cm^{2}/s'],
 "RadEnNeBHop": [ ['8'], nprim/R100h , 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,'-9999','r [cm]','GeV/cm^{2}/s'],

 "RadEnPrBGst": [ ['1'], normBGst, 242, 0, 1210, tBGst, 'BG startup', kBlue-1,'-9999','r [cm]','GeV/cm^{2}/s'],
 "RadEnPrBGac": [ ['1'], normBGac, 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,'-9999','r [cm]','GeV/cm^{2}/s'],
 "RadEnPrBHds": [ ['1'], nprim/R12m, 242, 0, 1210, tBH, 'BH 12 min loss', kPink-9,'-9999','r [cm]','GeV/cm^{2}/s'],
 "RadEnPrBHop": [ ['1'], nprim/R100h , 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,'-9999','r [cm]','GeV/cm^{2}/s'],

 "RadEnPhBGst": [ ['7'], normBGst, 242, 0, 1210, tBGst, 'BG startup', kBlue-1,'-9999','r [cm]','GeV/cm^{2}/s'],
 "RadEnPhBGac": [ ['7'], normBGac, 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,'-9999','r [cm]','GeV/cm^{2}/s'],
 "RadEnPhBHds": [ ['7'], nprim/R12m, 242, 0, 1210, tBH, 'BH 12min loss', kPink-9,'-9999','r [cm]','GeV/cm^{2}/s'],
 "RadEnPhBHop": [ ['7'], nprim/R100h , 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,'-9999','r [cm]','GeV/cm^{2}/s'],

 "RadEnChBGst": [ ['13','14','15','16'], normBGst, 242, 0, 1210, tBGst, 'BG startup', kBlue-1,'-9999','r [cm]','GeV/cm^{2}/s'],
 "RadEnChBGac": [ ['13','14','15','16'], normBGac, 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,'-9999','r [cm]','GeV/cm^{2}/s'],
 "RadEnChBHds": [ ['13','14','15','16'], nprim/R12m, 242, 0, 1210, tBH, 'BH 12 min loss', kPink-9,'-9999','r [cm]','GeV/cm^{2}/s'],
 "RadEnChBHop": [ ['13','14','15','16'], nprim/R100h , 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,'-9999','r [cm]','GeV/cm^{2}/s'],

 "RadEnEpBGst": [ ['3', '4'], normBGst, 242, 0, 1210, tBGst, 'BG startup', kBlue-1,'-9999','r [cm]','GeV/cm^{2}/s'],
 "RadEnEpBGac": [ ['3', '4'], normBGac, 242, 0, 1210, tBGac, 'BG after cond', kAzure-3,'-9999','r [cm]','GeV/cm^{2}/s'],
 "RadEnEpBHds": [ ['3', '4'], nprim/R12m, 242, 0, 1210, tBH, 'BH 12 min loss', kPink-9,'-9999','r [cm]','GeV/cm^{2}/s'],
 "RadEnEpBHop": [ ['3', '4'], nprim/R100h, 242, 0, 1210, tBH, 'BH 100h loss', kGreen+2,'-9999','r [cm]','GeV/cm^{2}/s'],
}


# ---------------------------------------------------------------------------------
# comp plots TCT5IN vs TCT5LOUT
# ---------------------------------------------------------------------------------
N_beam = 2736*2.2e11
tau_12m = 60*12
def calcR12m(N_tcts, N_abs):
    tau_12m = 60*12
    N_beam = 2736*2.2e11
    r=N_beam*N_tcts/(tau_12m * N_abs)
    return r


# wc -l sourcedirs/HL_TCT_7TeV/fluka/hybrid/b1/tct5inrd.dat 
N_tcts = 13073 
# awk '{ sum += $4; } END { print sum; }' H5_HL_TCT5IN_relaxColl_hHaloB1_roundthin/coll_summary_H5_HL_TCT5IN_relaxColl_hHaloB1_roundthin.dat
# awk '{ sum += $4; } END { print sum; }' H5_HL_TCT5IN_relaxColl_vHaloB1_roundthin/coll_summary_H5_HL_TCT5IN_relaxColl_vHaloB1_roundthin.dat
N_abs  = 63740261+61392508

R12m = calcR12m(N_tcts, N_abs)

treeName = 'particle'
bbgFile  = workpath + 'runs/FL_TCT5IN_roundthinB1_2nd/hilumi_ir1_hybrid_b1_exp_20MeV_nprim3972000_30.root'
print "Opening...", bbgFile
rf_tct5inrd  = TFile(bbgFile)
tIN = rf_tct5inrd.Get(treeName)
nprimIN = float(bbgFile.split('nprim')[-1].split('_')[0])
normIN = nprimIN/R12m
print "r12m", R12m

# .................................................................................

# wc -l sourcedirs/HL_TCT_7TeV/fluka/hybrid/b1/tct5otrd.dat 
N_tcts = 12091.
# awk '{ sum += $4; } END { print sum; }' H5_HL_TCT5LOUT_relaxColl_vHaloB1_roundthin/coll_summary_H5_HL_TCT5LOUT_relaxColl_vHaloB1_roundthin.dat
# awk '{ sum += $4; } END { print sum; }' H5_HL_TCT5LOUT_relaxColl_hHaloB1_roundthin/coll_summary_H5_HL_TCT5LOUT_relaxColl_hHaloB1_roundthin.dat
N_abs  = 63828643 + 61405975
R12m = N_beam/tau_12m * N_tcts/N_abs
R12m = 81889013 # from cv07

bbgFile  = workpath + 'runs/FL_TCT5LOUT_roundthinB1_2nd/hilumi_ir1_hybrid_b1_exp_20MeV_nprim5350000_30.root'
print "Opening...", bbgFile
rf_tct5otrd  = TFile(bbgFile)
tOUT = rf_tct5otrd.Get(treeName)
nprimOUT = float(bbgFile.split('nprim')[-1].split('_')[0])
normOUT = nprimOUT/R12m

print "r12m", R12m
# ---------------------------------------------------------------------------------
# dict  key = hname  #0 particleTypes #1 norm #2 nbins #3 xmin #4 xmax #5 ttree #6 prettyName 
                     #7 hcolor #8 othercut[as string OR float/int] #9 xtitle #10 ytitle #11 ynbin #12 ymin #13 ymax
# ---------------------------------------------------------------------------------
yrel = '/primary'
yrel = '/s'
sDict_HL_hybridComp = {
 "EkinAllIN": [ ['all'], normIN,60, 1e-2,1e4, tIN, 'TCT5 and TCT4',kBlue-1, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', -9999, -9999, -9999, ],
 "EkinAllOUT": [ ['all'], normOUT,60, 1e-2,1e4, tOUT, 'TCT4 only',kAzure-3, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', -9999, -9999, -9999, ],

 "EkinPrIN": [ ['1'], normIN,60, 1e-2,1e4, tIN, 'TCT5 and TCT4',kBlue-1, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', -9999, -9999, -9999, ],
 "EkinPrOUT": [ ['1'], normOUT,60, 1e-2,1e4, tOUT, ' TCT4 only',kAzure-3, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', -9999, -9999, -9999, ],

 "EkinNeIN": [ ['8'], normIN,60, 1e-2,1e4, tIN, 'TCT5 and TCT4',kBlue-1, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', -9999, -9999, -9999, ],
 "EkinNeOUT": [ ['8'], normOUT,60, 1e-2,1e4, tOUT, ' TCT4 only',kAzure-3, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', -9999, -9999, -9999, ],

 "EkinMuIN": [ ['10', '11'], normIN,60, 1e-2,1e4, tIN, 'TCT5 and TCT4',kBlue-1, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', -9999, -9999, -9999, ],
 "EkinMuOUT": [ ['10', '11'], normOUT,60, 1e-2,1e4, tOUT, 'TCT4 only',kAzure-3, '-9999','E [GeV]', '#frac{dN(counts/s)}{dlog E}', -9999, -9999, -9999, ],

 "RadEnAllIN": [ ['all'], normIN, 242, 0, 1210, tIN, 'TCT5 and TCT4',kBlue-1, '-9999','r [cm]','GeV/cm^{2}/s', -9999, -9999, -9999, ],
 "RadEnAllOUT": [ ['all'], normOUT, 242, 0,1210, tOUT, 'TCT4 only',kAzure-3, '-9999','r [cm]','GeV/cm^{2}/s', -9999, -9999, -9999, ],

 "RadEnChIN": [ ['13','14','15','16'], normIN, 242, 0, 1210, tIN, 'TCT5 and TCT4', kBlue-1,'-9999','r [cm]','GeV/cm^{2}/s', -9999, -9999, -9999, ],
 "RadEnChOUT": [ ['13','14','15','16'], normOUT, 242, 0, 1210, tOUT, 'TCT4 only', kAzure-3,'-9999','r [cm]','GeV/cm^{2}/s', -9999, -9999, -9999, ],

 "RadEnMuIN": [ ['10', '11'], normIN, 242, 0, 1210, tIN, 'TCT5 and TCT4', kBlue-1,'-9999','r [cm]','GeV/cm^{2}/s', -9999, -9999, -9999, ],
 "RadEnMuOUT": [ ['10', '11'], normOUT, 242, 0, 1210, tOUT, 'TCT4 only', kAzure-3,'-9999','r [cm]','GeV/cm^{2}/s', -9999, -9999, -9999, ],

 "RadNMuIN": [ ['10', '11'], normIN, 242, 0, 1210, tIN, 'TCT5 and TCT4', kBlue-1,'-9999','r [cm]','particles/cm^{2}/s', -9999, -9999, -9999, ],
 "RadNMuOUT": [ ['10', '11'], normOUT, 242, 0, 1210, tOUT, 'TCT4 only', kAzure-3,'-9999','r [cm]','particles/cm^{2}/s', -9999, -9999, -9999, ],

 "PhiNAllIN" : [ ['all'],normIN, 100, -math.pi, math.pi, tIN, 'TCT5 and TCT4',kBlue-1, '-9999','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
 "PhiNAllOUT" : [ ['all'],normOUT, 100, -math.pi, math.pi, tOUT, 'TCT4 only',kAzure-3, '-9999','#phi [rad]', 'particles/rad'+yrel, -9999, -9999, -9999, ],
}
