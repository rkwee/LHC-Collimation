#
#
# rkwee, Feb 2015
# -----------------------------------------------------------------------------------
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-t", dest="tracksfile", type="string",
                  help="put data file produced by h5dump")

parser.add_option("-l", dest="lossfile", type="string",
                  help="put data file produced by h5dump")

(options, args) = parser.parse_args()

tracks2File = options.tracksfile
LPIfile     = options.lossfile

# -----------------------------------------------------------------------------------

outfilename = tracks2File + ".extract"
outfile = open(outfilename,'w')
print "writing ", outfilename

with open(LPIfile) as lf:

        for lline in lf:
		
		pline = lline.split()
		LPIpos = float(pline[2])
		LPIID = pline[0]
		#print "checking particle ", LPIID
		with open(tracks2File) as tf:
			for tline in tf:
				try:
					sline=tline.split()
					tID = sline[0]
					if (tID == LPIID):
						print>>outfile, tline.rstrip()
						# print "writing ", tline
				except: print "Ignoring", tline
