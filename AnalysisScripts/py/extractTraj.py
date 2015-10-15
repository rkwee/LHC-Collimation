#
#
# rkwee, Feb 2015
# -----------------------------------------------------------------------------------
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", dest="fortfile", type="string",
                  help="put filename of merged fort 67 file")

(options, args) = parser.parse_args()

fortfile = options.fortfile
# -----------------------------------------------------------------------------------

outfilename = fortfile + ".corrected"
outfile = open(outfilename,'w')
print "writing ", outfilename

with open(fortfile) as ff:
	
        for i,line in enumerate(ff):
		
		if i%2:

			lineP1 = line
		else:

			wholeLine = lineP1.rstrip() + " " + line

			print wholeLine
