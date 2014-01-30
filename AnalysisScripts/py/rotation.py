#!/usr/bin/python
# needs numpy
#
# transform sixtrack coordinates to fluka coordinates
# do it SEPRATELY for TCTV and TCTH coordinates
# rkwee, Sept 2013
# ----------------------------------------------------------------------------------------
import numpy, os
from numpy import *
from optparse import OptionParser
import math as m

parser = OptionParser()

parser.add_option("-f", dest="file", type="string",
                  help='put filtered file of impacts_real')

parser.add_option("-c", dest="colltype", type="string",
                  help='put collimator type TCTH or anything')

parser.add_option("-r", dest="resultdir", type="string",
                  help='put subfolder destination on lxplus for result files, am already in /afs/cern.ch/work/r/rkwee/HL-LHC/runs/TCT/rotate/')

parser.add_option("-t", dest="tag", type="string",
                  help='put name tag for result files like _SOMETAG that identifies the input file.')

(options, args) = parser.parse_args()
f = options.file
subfolder = options.resultdir
rel = options.tag
doTCTH = options.colltype.count("TCTH")
# ...........................................................................................
# header of impacts file is: # 1=icoll 2=c_rotation 3=s 4=x 5=xp 6=y 7=yp 8=nabs 9=np 10=ntu

#subfolder = 'noCrossAngle/'
#subfolder = 'posBigAngle/'
#subfolder = 'refAngle/'
#subfolder = 'HL/TCTV/'
#subfolder = 'TCTH.B2/'
# ...........................................................................................
phiRadCross = 0.000047 # unit in radians, pos angle => beta_y goes down towards z<0 CROSSING ANGLE AT TCTs!!!!!
phiDegGeo   = 6.4689724016E-02 # in degree, corresponds to 1.12 mrad
phiRadGeo   = phiDegGeo*m.pi/180.
# -------------------------------------------------------------------------------------------
def doRotGeo(vect, doPrint):

    # rotation due to geometry
    # needs array as input

    nvect  = []

    # -- rotation around y-axis as indicated in fluka
    phi     = phiDegGeo
    rotDeg  = array([[ m.cos(phi), 0, m.sin(phi)],
                     [        0, 1,        0],
                     [-m.sin(phi), 0, m.cos(phi)]]
                    )
    phiRad  = phiDegGeo*m.pi/180.
    
    rotRad  = array([[ m.cos(phiRad), 0, m.sin(phiRad)],
                     [        0, 1,        0],
                     [-m.sin(phiRad), 0, m.cos(phiRad)]]
                    )
    
    print 'rotation matrix in radians ',rotRad
    rot = rotRad

    (nRows, nCols) = vect.shape

    if doPrint:
        fout2 = '/Users/rkwee/work/HL-LHC/runs/TCT/rotate/rotatedGeo_hits'+rel+'.dat'
        fout2 = '/Users/rkwee/work/HL-LHC/runs/TCT/rotate/hits_geo'+rel+'.dat'
        foutrot = open(fout2, 'w')

        print("Writing rotated data to " + fout2)

        # fileout.write( "x' y' z' \n" )

    for i in range(nRows):

        line = dot(rot,vect[i,:])
        xRot = line[0] 
        yRot = line[1] 
        zRot = line[2] 
        nvect += [ [xRot, yRot, zRot] ]

        if doPrint: foutrot.write( str(xRot) + ' ' + str(yRot) + ' ' + str(zRot) +'\n')

    if doPrint:
        foutrot.close()
        cmd = 'scp ' + fout2 +' lxplus:/afs/cern.ch/work/r/rkwee/HL-LHC/runs/TCT/rotate/' + subfolder
        print cmd
        os.system(cmd)
        
    return array(nvect)

# -------------------------------------------------------------------------------------------

def doOffset(vect, doPrint):

    # needs an array as input

    nvect = []

    if doPrint:

        fout1 = '/Users/rkwee/work/HL-LHC/runs/TCT/rotate/hits_influka_units'+rel+'.dat'
        fout1 = '/Users/rkwee/work/HL-LHC/runs/TCT/rotate/hits_offset'+rel+'.dat'

        fileout = open(fout1, 'w')
        print("Writing rotated data to " + fout1)

    # TCTV.B2
    xOffset, yOffset, zOffset = -8.338366732, 0.20755, 1.4584E+04 + 50.

    # TCTH.B2
    if doTCTH: xOffset, yOffset, zOffset = -8.5280469902, 0.20755, 1.4752E+04 + 50. 

    (nRows, nCols) = vect.shape

    for i in range(nRows):
        line   = vect[i,:]
        xshift = line[0] + xOffset

        yshift = line[1] + yOffset
        zshift = zOffset - line[2] 

        nvect += [ [xshift, yshift, zshift] ]

        if doPrint: fileout.write( str(xshift) + ' ' + str(yshift) + ' ' + str(zshift) +'\n')


    if doPrint:
        fileout.close()
        cmd = 'scp ' + fout1 +' lxplus:/afs/cern.ch/work/r/rkwee/HL-LHC/runs/TCT/rotate/' + subfolder
        print cmd
        os.system(cmd)

    return array(nvect)

# -------------------------------------------------------------------------------------------

def doConvertUnits(f,doPrint):

    # convert sixtrack units to fluka units
    # x,y in mm
    # z (==s) in m

    vect = []


    if doPrint:

        fout = '/Users/rkwee/work/HL-LHC/runs/TCT/rotate/rawhits_influka_units'+rel+'.dat'
        fileout = open(fout, 'w')
        print("Writing rotated data to " + fout)

    with open(f) as myfile:
        
        for i,line in enumerate(myfile):
            if i == 0:
                continue
        
            # mirror x-value! 

            vect += [[-0.1*float(line.split()[3]), 0.1*float(line.split()[5]), 100.*float(line.split()[2])]]
            if i < -1:
                print '.'*23
                print 'line content 3, 5, 2',line.split()[3], line.split()[5], line.split()[2]
                print 'converted to cm', vect[-1]
                print 'intofile',  str(vect[-1][0]) + ' ' + str(vect[-1][1]) + ' ' + str(vect[-1][2]) 
            if doPrint: fileout.write( str(vect[-1][0]) + ' ' + str(vect[-1][1]) + ' ' + str(vect[-1][2]) +'\n')


    if doPrint: 
        fileout.close()
        cmd = 'scp ' + fout +' lxplus:/afs/cern.ch/work/r/rkwee/HL-LHC/runs/TCT/rotate/' + subfolder
        print cmd
        os.system(cmd)

    return array(vect)

# -------------------------------------------------------------------------------------------
def doAngles(f, vect, doPrint):

    # needs an array as input

    nlist = []

    if doPrint:

        fout = '/Users/rkwee/work/HL-LHC/runs/TCT/rotate/final_hits_and_angles'+rel+'.dat'
        fileout = open(fout, 'w')
        print("Writing rotated data to " + fout)

    (nRows, nCols) = vect.shape
        
    with open(f) as myfile:
        nErr = 0
        for i,line in enumerate(myfile):
            try:        
                xp_raw  = float(line.split()[4])
                yp_raw  = float(line.split()[6])

                print 'xp_raw', xp_raw, 'yp_raw', yp_raw
                print "adding geo angle", phiRadGeo
                print "adding crossing angle", phiRadCross
                # convert from mrad to rad by 1/1000!!! phiRadCross is in rad already!
                # geo angle for B2 : substract, crossing angle for B2 : go down -> substract

                # # #   xp, yp  = 1e-3 * xp_raw + phiRadGeo, 1e-3 * yp_raw - phiRadCross
                xp, yp  = 1e-3 * xp_raw + phiRadGeo, 1e-3 * yp_raw + phiRadCross
                print 'xp, yp', xp, yp

                print '.'*30
                nline   = [ str(vect[i-nErr][0]), str(vect[i-nErr][1]), str(vect[i-nErr][2]), str(xp), str(yp) ]
                nlist  += [" ".join(nline) +'\n']

                if doPrint: fileout.write(nlist[-1])
            except ValueError:
                nErr += 1
                print("ValueError for this line:", line)
            except IndexError:
                nErr += 1
                print("IndexError at", i-nErr)


    if i != nRows:
        print("ERROR: different number of particles considered?! positions dont match to angles!")
        sys.exit()
    
    if doPrint:
        fileout.close()
        cmd = 'scp ' + fout +' lxplus:/afs/cern.ch/work/r/rkwee/HL-LHC/runs/TCT/rotate/' + subfolder
        print cmd
        os.system(cmd)

    return nlist
# -------------------------------------------------------------------------------------------
def doRoderiksFormat(mylist,doPrint):

    # gets a list as input
    
    debug = 0

    if doPrint:
        
        fout = '/Users/rkwee/work/HL-LHC/runs/TCT/rotate/oldFormat_final_hits_and_angles'+rel+'.dat'
        fileout = open(fout, 'w')
        print("Writing rotated data to " + fout)
        
    for line in mylist:

            # adding for the old format also the tIN variable which is for TCTs 0.
            nline = line.rstrip() + " " + " 0.0 \n" 
            if debug : print(" doRoderiksFormat: " + nline)
            if doPrint: fileout.write(nline)

    if doPrint:
        fileout.close()
        cmd = 'scp ' + fout +' lxplus:/afs/cern.ch/work/r/rkwee/HL-LHC/runs/TCT/rotate/' + subfolder
        print cmd
        os.system(cmd)

    print("--fin--")
# -------------------------------------------------------------------------------------------
if __name__ == "__main__":
 

    doPrint = 1
    nvect = doConvertUnits(f,1)
    nvect = doOffset(nvect, doPrint)
    nvect = doAngles(f,nvect,doPrint)
    doRoderiksFormat(nvect,doPrint)
