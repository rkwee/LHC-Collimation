#!/usr/bin/python
#
# Mar 2015, rkwee
## -------------------------------------------------------------------------------
import helpers, gzip, os, subprocess
from helpers import *

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", dest="file", type="string",
                  help="impacts real file")

(options, args) = parser.parse_args()
f = options.file
dirs = 'H5_HL*TCT5IN*relaxColl*B1*'
# -----------------------------------------------------------------------------------
def extractHits(f):

    colls = [
        ('54', 'TCTH.5L1.B1'),
        ('55', 'TCTVA.5L1.B1'),
        ('52', 'TCTH.4L1.B1'), 
        ('53', 'TCTVA.4L1.B1'),
    #     ]
    # collsIR5 = [
        ('56', 'TCTH.5L5.B1'),
        ('57', 'TCTVA.5L5.B1'), 
        ('19', 'TCTH.4L5.B1'),  
        ('20', 'TCTVA.4L5.B1'), 
        ]



    if f.endswith('gz'):

        mf = gzip.open(f)
        for icoll,coll in colls:
            filename = f.split('.dat.gz')[0] + '_' + icoll + '_' + coll + '.txt'
            print('writing', filename)
            
            hfile = open(filename, 'w')
            for line in mf: 
                if line.split()[0].count(icoll): 
                    hfile.write(line)
        print('line cnt')
        os.system('wc -l ' + filename)

    else:
        
        for icoll,coll in colls:
            with open(f) as mf:
                
                filename = f.split('.dat')[0] + '_' + icoll + '_' + coll + '.txt'
                print('writing', filename)

                hfile = open(filename, 'w')

                for line in mf: 
                    if line.split()[0].count(icoll): 
                        hfile.write(line)

        print('line cnt')
        os.system('wc -l ' + filename)



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

    files = []
    
    for f in files: 
        print '.'*30, f, '.'*30
        extractHits(f)

    extractHits(f)
    #normaliseTCThits()
