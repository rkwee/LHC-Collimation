#!/usr/bin/python
#
#
#
# R Kwee-Hinzmann, October 2013 
# ----------------------------------------------------------------------------------------------------------------------
import os, stat, sys, shutil, re
import optparse
from optparse import OptionParser

parser = OptionParser()

parser.add_option("-r", dest="rundir", type="string",
                      help="put rundir in which file are to be merged")

parser.add_option("-s", dest="scoringType", type="string",
                      help="put scoringtype usrtrack, usrbin or usrbdx or text")

parser.add_option("-u", dest="unit", type="string",
                      help="put corresponding fluka unit. if several seperate by ,")

parser.add_option("-o", dest="outpath", type="string",
                      help="put output path and full filename. If empty use inp file name in main run dir.")

(options, args) = parser.parse_args()

rundir = options.rundir
if not rundir.endswith('/'): rundir += '/'
scoringType = options.scoringType

outpath = options.outpath
if outpath == "": outpath = rundir
else:
    if not outpath.endswith('/'): outpath += '/'

unit = options.unit
if unit == '66' or unit == '67':
    skipN = 9
#elif  unit == '30': 
#    skipN = 8
#    print 'skipping first', skipN, 'characters of each file'
else: skipN = -9999
beam = 'B2'
if rundir.count('B1'): beam = 'b1'
# ----------------------------------------------------------------------------------------------------------------------
# define run files and parameters
debug      = 1
doRun      = 0

flukatool  = ''
flukapath  = '/afs/cern.ch/work/r/rkwee/Fluka/fluka20112clinuxAA/'
if scoringType.count('usrbin'):   flukatool   = flukapath + 'flutil/usbsuw'
elif scoringType.count('usrtrk'): flukatool   = flukapath + 'flutil/ustsuw'
elif scoringType.count('usrbdx'): flukatool   = flukapath + 'flutil/usxsuw'
elif scoringType.count('text'):   flukatool   = ''

# flukanumbers
flukaNumber = [i for i in unit.split(',')]    
# ----------------------------------------------------------------------------------------------------------------------
def ListFortFiles(fn):
    
    # create a list with all fortfile to be merged, ie per flukanumber!
    allfortfiles = []
    
    # get all sub dirs like run_12345
    alldirs = os.listdir(rundir)

    # for each subrundir 
    for adir in alldirs:

        if not os.path.isdir(rundir+adir): continue

        # all file in each subrundir
        filesInAdir = os.listdir(rundir+adir)

        for afile in filesInAdir:

            if not afile.endswith("_fort." + fn): continue
            allfortfiles += [rundir + adir +'/' + afile]
    
    # remove the last 3 characters as they indicate the cycle number
    #   example of file: ir1_4TeV_settings_from_TWISS_b2001_fort.53
    onefile = allfortfiles[-1].split('/')[-1]
    onefile = onefile.split('_fort')[0]
    onefile = onefile[:-3]

    # per fn return a list
    return allfortfiles, onefile
# ----------------------------------------------------------------------------------------------------------------------
def joinTextFiles(fn):
    # all subfiles are joined replacing the first colum (first 8 characters) by runnumber and cyclenumber

    allfortfiles,inpfile = ListFortFiles(fn)
    
    print "name of inpfile is", inpfile

    fdummy   = rundir + inpfile + '_' + fn + '.dummy'
    foutname = rundir + inpfile + '_' + fn 
    #foutname = '/tmp/rkwee/' + inpfile + '_' + fn 
    foutname = outpath + inpfile + '_' + fn 
    fout     = open(foutname, 'w')

    foutdummy= open(fdummy, 'w')
    cnt = 0
    for afile in allfortfiles:

        if not afile.count("run"): continue

        foutdummy.write(afile+"\n")
        cnt += 1

        runnumber   = afile.split('run_')[-1].split('/')[0]
        cyclenumber = afile.split('/')[-1].split(beam)[-1].split('_fort.' + fn)[0][-1]
        print("for file", afile, "found runnumber ", runnumber, ' and cyclenumber', cyclenumber)

        with open(afile) as af:

            for line in af:
                #line = line.rstrip()

                if line.count("#"): continue

                if skipN > 0: 
                    skippedPart = line.split()[0]
                    outline  = runnumber + cyclenumber + '  ' + line[skipN:]
                    #print "skippedPart", skippedPart, line 
                else: outline = line

                fout.write(outline)

    fout.close()
    foutdummy.close()

    print("Wrote " + foutname + " from ", cnt, " fort files.")

    return foutname
# ----------------------------------------------------------------------------------------------------------------------
def mergeFortfiles():

    if scoringType == 'text':

        for fn in flukaNumber: joinTextFiles(fn)

        return


    for fn in flukaNumber:

        allfortfiles,inpfile = ListFortFiles(fn)

        fdummy   = rundir + inpfile + '_' + fn + '.dummy'
        foutname = rundir + inpfile + '_' + fn 

        fout     = open(fdummy, 'w')

        for afile in allfortfiles: fout.write(afile +"\n")

        # add a newline
        fout.write("\n")

        # add filename of merged file. IMPORTANT: add newline
        fout.write(foutname + '\n')

        fout.close()

        # create the merged binary
        cmd = flukatool + ' < ' + fdummy
        print cmd
        
        if doRun:
            os.system(cmd)            

    
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    mergeFortfiles()
