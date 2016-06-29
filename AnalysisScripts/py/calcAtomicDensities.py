#!/usr/bin/python
#
#
#
# R Kwee, 2013
# 
# --------------------------------------------------------------------------------
import optparse
from optparse import OptionParser

parser = OptionParser()

parser.add_option("-t", dest="trackfile", type="string",
                      help="input trackfile")

parser.add_option("-b", dest="bgfile", type="string",
                      help="put file with beamgas profile")
(options, args) = parser.parse_args()

trackfile = options.trackfile
bgfile    = options.bgfile

# --------------------------------------------------------------------------------
def calc():
# --------------------------------------------------------------------------------
# density profile is given in the following format:
# densities per molecule as function of s-coordinate
# x,y,z, cx, cy, cz as function of (different s-coordinate)
# merge densities with coordinates
# note, that the source routine needs fluka units, ie *cm*!

    outfname = 'BGDATA.dat'
    outfile  = open(outfname,'w')
    line = "Writing in this directory the file " + outfname
    print(line)

    # -- writing the header
    # number of different atoms
    natoms = '3'
    line   = natoms
    outfile.write(line + '\n')

    # flukae number of the atoms
    flukaN = '3 6 8' # for H C O
    line   = flukaN
    outfile.write(line + '\n')
    
    offsetIP_tk  = 0. ## from IP1: 9997.98 # m
    offsetIP_bg  = 0. ## from IP1: 9997.98 # m

    conditio = 10. # cm

    # format of trackfile
    # default output of mgdraw_idealPath.f
    # CTRACKcum   CMTRCK   CTRACK  x   y   z   cx   cy   cz
    path_trackfile = '/home/rkwee/R2E/P6/testruns/checkIR4_B1/ir4_exp001_trackfile'
    path_bgfile    = '/home/rkwee/R2E/P6/templates/data/LSS4_IP4_Beam_1_Fill2736_Regina.csv'

    trackfile = open(path_trackfile)
    bgfile = open(path_bgfile)
    
    # atomic densities
    rho_C, rho_H, rho_O = 0., 0., 0.

    # .....................
    # for each s-coordinate
    cntOK, cntKO = 0,0
    for line_track in trackfile:

        if line_track.count("CTRACKcum"):
            continue
       
        line_track = line_track.rstrip()
        line_tk = line_track.split()

        x  = line_tk[3]
        y  = line_tk[4]
        z  = line_tk[5]
        cx = line_tk[6]
        cy = line_tk[7]
        cz = line_tk[8]
        
        s_tk  = float(line_tk[0])

        # .........................................
        # for each distance from IP4 step in meter!

        # count how often per trackline the condition fulfilled is, expect once!
        cntrho = 0
        for line_beamgas in bgfile:

            if line_beamgas.count("Distance"):
                continue
            
            line_beamgas = line_beamgas.rstrip()
            line_bg = line_beamgas.split(',')

            if not line_bg[0]:
                continue

            rho_C, rho_H, rho_O = 0., 0., 0.

            # condition that we are at the same z-postion

            z_bg = float(line_bg[0])*100. # convert to cm
            z_tk = float(z)
            
            if z_bg < 0. and z_tk < 0:
                diff = abs(z_bg - z_tk)

            elif z_bg > 0. and z_tk > 0:
                diff = abs(z_bg - z_tk)

            else:
                diff = abs(z_bg) - abs(z_tk)

                
            if abs(diff) < conditio:
                cntOK += 1

                # get the data, convert to cm3

                rho_H2   = float(line_bg[1])*1e-6
                rho_CH4  = float(line_bg[2])*1e-6
                rho_CO   = float(line_bg[3])*1e-6
                rho_CO2  = float(line_bg[4])*1e-6

                # compute atomic rhos

                rho_H  = 2.0*rho_H2
                rho_H += 4.0*rho_CH4

                rho_C  = 1.0*rho_CH4
                rho_C += 1.0*rho_CO
                rho_C += 1.0*rho_CO2

                rho_O  = 1.0*rho_CO
                rho_O += 2.0*rho_CO2

                break
            

        line = line_tk[0] + ' ' + x + ' ' + y + ' ' + z + ' ' + cx + ' ' + cy + ' ' + cz + ' ' + str(rho_H) + ' ' + str(rho_C) + ' ' + str(rho_O)        

        outfile.write(line + '\n')
        
            
        bgfile = open(path_bgfile)   


    # close this file
    outfile.close()


## -----------------------------------------------------------------------------------

if __name__ == "__main__":

    calc()
