#!/usr/bin/python
#
# Mar 2015, rkwee
## -------------------------------------------------------------------------------
import helpers, gzip, os, subprocess
from helpers import *

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-d", dest="dirs", type="string",
                  help="directories with impacts real file")

(options, args) = parser.parse_args()

dirs = options.dirs
#dirs = 'H5_HL*TCT5IN*relaxColl*vHaloB1*sround*'
#dirs = 'pencil*B*'
# -----------------------------------------------------------------------------------
def extractHits(f):

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

         # 'TCTH.5L5.B1',
         # 'TCTVA.5L5.B1', 
         # 'TCTH.4L5.B1',  
         # 'TCTVA.4L5.B1', 

    # -- pencil beam run

    # colls = [

    #     'TCP.6L3.B1', 
    #     'TCTH.4L1.B1', 
    #     'TCTVA.4L1.B1',
    #     'TCTH.4L5.B1',  
    #     'TCTVA.4L5.B1', 

    #     'TCP.6R3.B2',
    #     'TCTH.4R5.B2',    
    #     'TCTVA.4R5.B2',   
    #     'TCTH.4R1.B2',    
    #     'TCTVA.4R1.B2',   
    #     ]
    tag = f.split('/')[0]
    tagOnly = tag.split('/')[-1]
    collsummary = tag + '/coll_summary_' + tagOnly + '.dat'
    print 'using this collsummary file', collsummary

    
    cDict = collDict(collsummary)

    allcolls = cDict.keys()

    if f.endswith('gz'):

        for coll in colls:
            if coll not in allcolls:
                print "Did not find ", coll, "in ", collsummary
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

    else:
        
        for icoll,coll in colls:
            with open(f) as mf:
                
                filename = f.split('.dat')[0] + '_' + icoll + '_' + coll + '.txt'
                print('writing', filename)

                hfile = open(filename, 'w')

                for line in mf: 
                    if line.split()[0].count(icoll): 
                        hfile.write(line)


                cmd = 'wc -l ' + filename
                print cmd
                os.system(cmd)



        # print('Please gzip file first')

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

    cmd = 'ls -1 ' + dirs + '/imp*gz'
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    myStdOut = process.stdout.read()
    files = myStdOut.split()

    print "Taking ",len(files)," files: ", files
    #files = []
    
    for f in files: 
        print '.'*30, f, '.'*30
        extractHits(f)

    #extractHits(f)
    #normaliseTCThits()
