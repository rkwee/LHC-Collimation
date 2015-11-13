#!/usr/bin/python
#
# Mar 2015, rkwee
## -------------------------------------------------------------------------------
import helpers, gzip, os, subprocess, sys
from helpers import *

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-d", dest="dirs", type="string",
                  help="directories with impacts real file")


parser.add_option("-c", dest="cfile", type="string",
                  help="collgaps file")


(options, args) = parser.parse_args()
cfile = options.cfile #= projectpath + 'offmom/LHC_6.5TeV/plus_500Hz/B1/collgap.lowb.hor.b1.dat'
dirs = options.dirs
#dirs = 'H5_HL*TCT5IN*relaxColl*vHaloB1*sround*'
#dirs = 'pencil*B*'
# -----------------------------------------------------------------------------------


def extractFromOneFileGz(f,colls,cDict,cfile):

    if not f.endswith("gz"): 
        print('Please gzip file first')
        sys.exit()

    allcolls = cDict.keys()

    for coll in colls:
        if coll not in allcolls:
            print "Did not find ", coll, "in ", cfile
            continue
        mf = gzip.open(f)
        icoll = cDict[coll][0]
        print coll, icoll
        filename = f.split('.dat.gz')[0] + '_' + icoll + '_' + coll + '.txt'
        print('writing', filename)

        hfile = open(filename, 'w')
        for line in mf: 
            if line.split()[0].count(icoll): 
                hfile.write(line)

        cmd = 'wc -l ' + filename
        print cmd
        os.system(cmd)

def extractFromFilelistDat(colls,cDict,cfile):
        
    allcolls = cDict.keys()
    for coll in colls:

        if coll not in allcolls:
            print "Did not find ", coll, "in ", cfile
            continue

        icoll = cDict[coll][0]
        
        filename =  cfile.split("/coll")[0] + '/impacts_real_' + icoll + '_' + coll + '.txt.new'
        print('writing', filename)

        hfile = open(filename, 'w')

        cmd = "grep "
        if len(str(icoll)) == 1:   cmd += '"^   '+ str(icoll) + ' "'
        elif len(str(icoll)) == 2: cmd += '"^  '+ str(icoll) + ' "'

        cmd += ' ' + dirs + '/imp*dat >| ' + filename
        print cmd
        os.system(cmd)


        cmd = 'wc -l ' + filename
        print cmd
        os.system(cmd)


        cmd = """awk '{$1=""; print}' """ + filename + """ > """ + filename.split(".new")[0]
        print cmd
        os.system(cmd)

        cmd = "rm " + filename 
        print cmd
        os.system(cmd)

# ----------------------------------------------------------------------------
def extractHits(files):

    # -- HL runs
    colls = [
         'TCTH.5L1.B1',
         'TCTVA.5L1.B1',
         'TCTH.4L1.B1', 
         'TCTVA.4L1.B1',
         'TCTH.5R1.B2',
         'TCTVA.5R1.B2',
         'TCTH.4R1.B2', 
         'TCTVA.4R1.B2',
         ]

    collsB2 = [
         'TCTH.5R5.B2',
         'TCTVA.5R5.B2',
         'TCTH.4R5.B2', 
         'TCTVA.4R5.B2',
        ]

    collsB1 = [
         'TCTH.5L5.B1',
         'TCTVA.5L5.B1', 
         'TCTH.4L5.B1',  
         'TCTVA.4L5.B1', 
         ]


    # -- pencil/off-mom beam run

    collsOFF = [

        'TCP.6L3.B1', 
        'TCTH.4L1.B1', 
        'TCTVA.4L1.B1',
        'TCTH.4L5.B1',  
        'TCTVA.4L5.B1', 

        'TCP.6R3.B2',
        'TCTH.4R5.B2',    
        'TCTVA.4R5.B2',   
        'TCTH.4R1.B2',    
        'TCTVA.4R1.B2',   
        ]
    # tag = f.split('/')[0]
    # tagOnly = tag.split('/')[-1]
    # collsummary = tag + '/coll_summary_' + tagOnly + '.dat'
    #print 'using this collsummary file', collsummary

    if cfile.count("collgap"): 
        cDict = collgapsDict(cfile)
    elif cfile.count("coll_summary"):
        cDict = collDict(cfile)
    else:
        print "cannot define cfile", cfile
        sys.exit()

    #extractFromFilelistDat(colls,cDict,cfile)

    extractFromOneFileGz(f,colls,cDict,cfile)
# ----------------------------------------------------------------------------
def normaliseTCThits():

    cmd = 'for i in `ls -d '+dirs+'`; do echo $i; done'
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    myStdOut = process.stdout.read()
    mydirs= myStdOut.split()

    # for each dir go in there get nprim, get the counts, normalise the counts
    for mdir in mydirs:

        print '-'*22, mdir, '-'*22
        cmd = 'grep "for targetfile LPI" ' + mdir + '/nprim*.txt'
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        myStdOut = process.stdout.read()
        nprim = float(myStdOut.split()[0]) * 6400.        

        cmd = 'wc -l '+mdir+'/im*txt'
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        myStdOut = process.stdout.read()
        wcResult = myStdOut.split()

        # removing information of total size
        del wcResult[-1]
        del wcResult[-1]

        print "using", wcResult

        for res in wcResult:

            try:
                wcr = float(res)/nprim
                print 'normalising', res, ' counts by', nprim, 'nb of primaries:', wcr
            except:
                print res

    
    

# ----------------------------------------------------------------------------
if __name__ == "__main__":

    cmd = 'ls -1 ' + dirs + '/imp*dat.gz'
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    myStdOut = process.stdout.read()
    files = myStdOut.split()

    #print "Taking ",len(files)," files: "#, files


    for f in files: 
        print '.'*30, f, '.'*30
        extractHits(f)

    #extractHits(files)
    #normaliseTCThits()
