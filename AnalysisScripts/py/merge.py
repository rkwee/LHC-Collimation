#!/usr/bin/python
#

# Regina Kwee-Hinzmann @ RHUL
# 2013, June
# -----------------------------------------------------------------
import os, stat, sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-r", "", dest="rundir", type="string",
                  help="this is the main rundir with the run_X dirs")

(options, args) = parser.parse_args()
rundir = options.rundir

# rundir = '/afs/cern.ch/work/r/rkwee/public/sixtrack_example/'

# 2 types of merging: 1. append, 2. add up

# all files to append:
fApp = ['LPI_BLP_out.s',           
        'FirstImpacts.dat',
        'survival.dat',
        'impacts_fake.dat',
        'impacts_real.dat',
        ]

# specified to work only with this file!
fAdd = ['coll_summary.dat',
        ]

# -----------------------------------------------------------------
def findGoodFiles(targetfile,rundir):

    debug = 0

    # all goodfiles
    resFiles = []

    if not rundir.endswith('/'):
        rundir += '/'

    # find the correct path 
    subdirs = os.listdir(rundir)


    # exclude dirs
    excludeDirs =  [ 'run_000'+str(i) for i in range(1,10)]
    excludeDirs += [ 'run_00'+str(i) for i in range(10,21)]

    # ------------
    # get all good files into a list

    for subdir in subdirs:

        if subdir in excludeDirs:
            continue

        if debug: 
            print("Finding " + subdir)

        # directory with results 
        rdir = rundir + subdir + "/"

        if debug:
            print("Using this dir " + rdir )

        if not os.path.isdir(rdir):
            continue

        thisfile = rdir + targetfile

        if debug:
            print("adding file " + thisfile)

        if not os.path.exists(thisfile):
            continue

        resFiles += [thisfile]

    if debug:
        print("Returning " + str(len(resFiles)) + " files.")

    return resFiles

# -----------------------------------------------------------------
def doAppend(fApp,rundir):

    debug = 0 

    if not rundir.endswith('/'):
        rundir += '/'

    print("Using " + rundir)

    for targetfile in fApp:

        foutname = rundir + targetfile.split('.')[0] + '_merged.' + targetfile.split('.')[-1]
        print('-'*20)
        print("Writing summary file " + foutname)

        # open one new file for merged info
        fileout  = open(foutname,'w')

        resFiles = findGoodFiles(targetfile,rundir)
        cnt      = 0

        # ------------
        for rFile in resFiles:

            cnt += 1

            if debug:
                print("opening this file" + thisfile)
            
            with open(rFile) as rf:

                for line in rf:

                    if cnt < 2 and line.count("#"):
                        fileout.write(line)

                    if not line.count('#'):
                        fileout.write(line)

        fileout.close()

# -----------------------------------------------------------------
                    
def doAddup(fAdd,rundir):

    # ---------------
    # this is for coll_summary.dat only!
    # ---------------

    debug = 0

    if not rundir.endswith('/'):
        rundir += '/'

    for targetfile in fAdd:

        foutname = rundir + targetfile.split('.')[0] + '_merged.' + targetfile.split('.')[-1]
        print('-'*20)
        print("Writing summary file " + foutname)

        # open one new file for merged info
        fileout  = open(foutname,'w')

        resFiles = findGoodFiles(targetfile,rundir)
        cnt      = 0
        icoll, collname, length = '','',''
        nimp, nabs, imp_av, imp_sig = -9999.,-9999.,-9999.,-9999.
        
        # ------------

        for rFile in resFiles:

            cnt += 1

            if debug:
                print("opening file # " + str(cnt) + ": " + rFile)
            
            if cnt == 1:
                # create dict while reading first file
                allLines = []

            with open(rFile) as rf:
                
                for line in rf:

                    if cnt < 2 and line.count("#"):
                        fileout.write(line)

                    if not line.count('#'):
                        
                        icoll    = line.split()[0]
                        collname = line.split()[1]
                        nimp     = float(line.split()[2])
                        nabs     = float(line.split()[3])
                        imp_av   = float(line.split()[4])
                        imp_sig  = float(line.split()[5])
                        length   = line.split()[6]

                        # single line     # 0        1     2      3      4        5
                        sline = [ icoll, [collname, nimp, nabs, imp_av, imp_sig, length] ]

                        if cnt == 1:
                            allLines += [sline]
                        else:
                            if debug:
                                print(cnt, icoll, nimp, cDict[icoll])

                            # dict already exists, so average and add up
                            if cDict[icoll][1]:
                                cDict[ icoll ][3]  = imp_av * nimp/(cDict[icoll][1] + nimp) + cDict[icoll][1]/(cDict[icoll][1]+nimp) * cDict[icoll][3]
                                cDict[ icoll ][4]  = imp_sig* nimp/(cDict[icoll][1] + nimp) + cDict[icoll][1]/(cDict[icoll][1]+nimp) * cDict[icoll][4]

                            cDict[ icoll ][1] += nimp
                            cDict[ icoll ][2] += nabs

                            
            # create once the dict
            if cnt == 1:
                cDict = dict(allLines)
        
        # ----------
        
        # use sorted keys
        cKeys = [str(i) for i in range(73)]

        for k in cKeys:

            try:

                #print cDict[k][0]
                line ='{0:3s} {1:15s} {2:10} {3:10} {4:15f}E-3 {5:10f}E-3    {6:10s}'.format(k, cDict[k][0], cDict[k][1], cDict[k][2], cDict[k][3]*1e3, cDict[k][4]*1e3, cDict[k][5])

                #print line
                fileout.write(line + '\n')


            except KeyError:
                pass


        fileout.close()

        
# -----------------------------------------------------------------
if __name__ == "__main__":

    doAppend(fApp,rundir)
    doAddup(fAdd,rundir)
