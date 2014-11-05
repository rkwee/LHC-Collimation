#!/usr/bin/python
#
# Nov, 2014 rkwee
# -----------------------------------------------------------------------------------
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-c", dest="colls", type="string",
                  help="put list of coll id's")
parser.add_option("-f", dest="fname", type="string",
                  help="put file name of impacts real")

(options, args) = parser.parse_args()

fname = options.fname
Colls = options.colls

colls = Colls.split(",")
# -----------------------------------------------------------------------------------
def collsummary(fname,colls):
    
    # counts lines in impacts_real for each coll in colls

    if not fname.count('.gz'):

        collHits = []

        for coll in colls:

            nhits = 0
            with open(fname) as ifile:
                for line in ifile:
                    if line.startswith("  "+coll): nhits += 1

            collHits += [nhits]

        for i,j in enumerate(colls):
            print("collimator " + j + " absorbed " + str(collHits[i]) + " protons.")

# -----------------------------------------------------------------------------------
if __name__ == "__main__":

    collsummary(fname,colls)


