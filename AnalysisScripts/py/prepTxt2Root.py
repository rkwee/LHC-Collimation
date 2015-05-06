#!/usr/bin/python
#
# Apr 2015, rkwee
# -------------------------------------------------------------------------------
import helpers, gzip, os, subprocess
from helpers import *

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", dest="fname", type="string",
                  help="file name to be converted")

(options, args) = parser.parse_args()

fname = options.fname
# -------------------------------------------------------------------------------
newfilename = fname + '.new'
newfile = open(newfilename, 'w')
with open(fname) as mf:

    for i,line in enumerate(mf):
        newline = " ".join(line.split()) + " \n"
        newfile.write(newline)


newfile.close()
