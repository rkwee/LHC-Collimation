#!/usr/bin/python
#
# merges SixTrack output of single runs
# needs to be pointed to a directory that contains sub-directories for each run result
# like: rundir == main_run_dir and in are the main_run_dir/run_XXXXX
# 
# Regina Kwee-Hinzmann @ RHUL
# 2013, June
# -----------------------------------------------------------------
import os, stat, sys, gzip, time
import helpers
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-r", "", dest="rundir", type="string",
                  help="this is the main rundir with the run_X dirs")
parser.add_option("-t", "", dest="tag", type="string",
                  help="tag of merged file, just some string name like _nominal ")

(options, args) = parser.parse_args()
rundir = options.rundir
tag    = options.tag
#tag = rundir.split('7TeVPostLS1')[-1]
# -----------------------------------------------------------------
# rundir = '/afs/cern.ch/work/r/rkwee/public/sixtrack_example/'

# 2 types of merging: 1. append, 2. add up

# all files to append, doCountLines only
fApp = [
    ('FirstImpacts.dat',1),
    ('LPI_BLP_out.s',   0),    
    ('impacts_real.dat',0),
    #('impacts_all_fake.dat',0),
    #('impacts_all_real.dat',0),
    ]

# specified to work only with this file!
fAdd = ['coll_summary.dat',
        ]

# common pattern to all header lines
headerPattern = 'icoll'
# -----------------------------------------------------------------
def findGoodFiles(targetfile,rundir):

    debug = 0

    # all goodfiles
    resFiles = []

    if not rundir.endswith('/'):
        rundir += '/'

    # find the correct path 
    subdirs = os.listdir(rundir)

    if debug: print "Found these files ", subdirs

    # -- exclude dirs
    #excludeDirs =  [ 'run_000'+str(i) for i in range(1,10)]
    #excludeDirs += [ 'run_00'+str(i) for i in range(10,21)]
    excludeDirs = []

    missing1, missing2 = helpers.checkSameOutput()
    missing = missing1+missing2

    newMissing = []
    for n in missing: 
        if n < 100: continue
        else: newMissing += [n]

    for m in newMissing:
        index = str(m)

        if len(index) < 5:
            index = '0'*(5-len(str(m)))+str(m)
            mdir = 'run_' + index
            excludeDirs += [mdir]

    if excludeDirs:
        print("INFO: Excluding " + str(len(excludeDirs)) + " run dirs.")
    
    # ------------
    # get all good files into a list

    for subdir in subdirs:

        if subdir in excludeDirs:
            continue

        # directory with results 
        rdir = rundir + subdir + "/"

        if debug: print("Finding " + rdir)

        if not os.path.isdir(rdir): continue

        thisfile = rdir + targetfile

        if debug: print("Finding " + thisfile)

        if not os.path.exists(thisfile) and not os.path.exists(thisfile + '.gz'): continue

        if os.path.exists(thisfile):
            resFiles += [thisfile]
        elif os.path.exists(thisfile + '.gz'):
            resFiles += [thisfile+'.gz']

        if debug:
            print("adding file " + resFiles[-1])

    if debug:
        print("Returning " + str(len(resFiles)) + " files.")

    return resFiles

# -----------------------------------------------------------------
def doAppend(fApp,rundir):

    debug  = 0
    g = -1
    if not rundir.endswith('/'):
        rundir += '/'

    print("Using files in " + rundir)

    for targetfile,doCountLines in fApp:

        foutname = rundir + targetfile.split('.')[0] + tag + '.' + targetfile.split('.')[-1]
        print('-'*20)
        print("Writing summary file " + foutname)

        # open one new file for merged info
        fileout  = open(foutname,'w')

        t0 = time.time()
        resFiles = findGoodFiles(targetfile,rundir)
        t1 = time.time()

        print(str(t1-t0)+" for finding a list")

        print len(resFiles),' for targetfile', targetfile
        # ------------
        if g == 0:
            h = 'goodfilelist'
            outfile = open(h, 'w')
            for t in resFiles: outfile.write(t+'\n')
            g = 1
            print 'wrote', h
        
        # ------------
        t0 = time.time()
        nlines = 0

        for cnt,rFile in enumerate(resFiles):
            
            if doCountLines:                
                if not rFile.count('.gz'):
                    with open(rFile) as rf:
                        for line in rf:
                            if not line.count(headerPattern):
                                nlines += 1
                else:
                    rf = gzip.open(rFile)
                    for line in rf:
                        
                        if not line.count(headerPattern):
                            nlines += 1

            else:

                if not rFile.count('.gz'):
                    with open(rFile) as rf:
                        for line in rf:

                            if cnt < 1 and line.count(headerPattern):
                                fileout.write(line)
                            elif not line.count(headerPattern):
                                fileout.write(line)                
                else:

                    rf = gzip.open(rFile)
                    for line in rf:

                        if cnt < 1 and line.count(headerPattern):
                            fileout.write(line)
                        elif not line.count(headerPattern):
                            fileout.write(line)                

            if doCountLines and cnt == len(resFiles)-1:
                fileout.write(str(nlines))

        fileout.close()
        t1 = time.time()
        print(str(t1-t0)+" for wrting " + foutname)

# -----------------------------------------------------------------
                    
def doAddup(fAdd,rundir):

    # ---------------
    # this is for coll_summary.dat only!
    # ---------------

    debug = 0

    if not rundir.endswith('/'):
        rundir += '/'

    for targetfile in fAdd:

        foutname = rundir + targetfile.split('.')[0] + tag + '.' + targetfile.split('.')[-1]
        print('-'*20)
        print("Writing summary file " + foutname)

        # open one new file for merged info
        fileout  = open(foutname,'w')

        resFiles = findGoodFiles(targetfile,rundir)
        cnt      = 0
        icoll, collname, length = '','',''
        nimp, nabs, imp_av, imp_sig = -9999.,-9999.,-9999.,-9999.
        
        # ------------
        os.system('date')
        for rFile in resFiles:

            cnt += 1

            if debug:
                print("opening file # " + str(cnt) + ": " + rFile)
            
            if cnt == 1:
                # create dict while reading first file
                allLines = []

            # - if not gzipped
            if not rFile.endswith('.gz'):

                with open(rFile) as rf:

                    for line in rf:

                        if cnt < 1 and line.count("#"):
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

            # - if gzipped - only opening different!
            else:
                            
                rf = gzip.open(rFile)

                for line in rf:

                    if cnt < 1 and line.count(headerPattern):
                        fileout.write(line)

                    if not line.count(headerPattern):

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

        print('saving data in dictionary done')
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

    os.system('date')
    t0 = time.time()
    doAppend(fApp,rundir)
    t1 = time.time()
    print(str(t1-t0)+" for doAppend")
    doAddup(fAdd,rundir)
    t2 = time.time()
    print(str(t2-t1)+" for doAddup")
    os.system('date')
