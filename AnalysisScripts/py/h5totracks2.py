#!/usr/bin/python
#
# Jan, 2015, rkwee
# -----------------------------------------------------------------------------------
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", dest="fname", type="string",
                  help="put data file produced by h5dump")

(options, args) = parser.parse_args()

fname = options.fname

# -----------------------------------------------------------------------------------

def convert(fname):

    cnt = 0
    part1, part2 = [],[]
    incr = 1000

    outfilename = fname + '.rawlist'
    print("writing ... " + outfilename )

    outfile = open(outfilename, 'w')
    dataChunk = []

    def writeToFile(somelist, somefile):
        for ele in somelist: somefile.write(' '.join(ele) + '\n')
        # print "writing!"

    with open(fname) as mf:

        for line in mf:

            if not line.split()[0].count("("): continue

            try:
                datacols = line.split("): ")[1].split(',')[:-1]

                if cnt%2==0: 
                    part1 = datacols 
                    # print "part1 =", part1
                else:   
                    if line.split()[0].count(',0)'):
                        print "getting rubbish", line, "for part2 at ",cnt," !! returning."
                        return

                    part2 = datacols
                    # print "part2 =", part2

                    wholeData = part1 + part2             
                    # print "whole data", wholeData

                    dataChunk += [wholeData]

                    if cnt == 0:
                        k = len(dataChunk)
                        # print "Size of DataChunk ", k, " : ", dataChunk
                        dataChunk.pop(0)
                        # print "Size of DataChunk now ", k, " : ", dataChunk

                if cnt%incr == 0:
                    writeToFile(dataChunk, outfile)
                    # print "Writing full chunk at ", cnt, dataChunk 
                    dataChunk = []

                cnt += 1

            except:
                print line        

    writeToFile(dataChunk, outfile)
    outfile.close()
    print "closing " , outfilename

if __name__ == "__main__":

    convert(fname)
