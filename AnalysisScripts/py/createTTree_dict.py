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

# ---------------------------------------------------------------------------------
sometext = 'HL LHC'
pID      = 1
cEkin    = 9
cX,cY,cZ = 4,5,13
tag      = 'HL'
csfile_H = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/ats-HL_LHC_1.0/nominal_settings/hor-B1/coll_summary_hor-B1.dat'
csfile_V = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/ats-HL_LHC_1.0/nominal_settings/ver-B1/coll_summary_ver-B1.dat'
Ntct_H   = 15793 # ats-HL_LHC_1.0/nominal_settings/impacts_real_on_52_TCTH.4L1.B1.dat
Ntct_V   = 5817 # ats-HL_LHC_1.0/nominal_settings/impacts_real_on_53_TCTVA.4L1.B1.dat
NtotBeam = 2.2e11*2808
nprim    = -9999
subfolder= 'TCT/HL/nominalSettings/'

# for ttree
pID      = 'particle'
cEkin    = 'energy_ke'
cX,cY,cZ = 'x','y','z_interact'
varList_HL = [sometext,pID,cEkin,cX,cY,cZ,tag,csfile_H,csfile_V,Ntct_H,Ntct_V, NtotBeam,subfolder]
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
varList_4TeV = [sometext,pID,cEkin,cX,cY,cZ,tag,csfile_H,csfile_V,Ntct_H,Ntct_V, NtotBeam,subfolder]
# ---------------------------------------------------------------------------------
