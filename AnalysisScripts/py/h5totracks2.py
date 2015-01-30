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

    cnt = 1
    part1, part2 = [],[]
    incr = 1024

    outfilename = fname + '.rawlist'
    print("writing ... " + outfilename )

    outfile = open(outfilename, 'w')
    dataChunk = []
    part1, part2 = [],[]
    ncol = 9
    nextData, dmiss= 0, 0
    parts = []
    wholeData = ''

    def writeToFile(somelist, somefile):
        for ele in somelist: somefile.write(' '.join(ele) + '\n')
        # print "writing!"

    with open(fname) as mf:

        for line in mf:
            
            if len(line.split()):                                
                if not line.split()[0].count("("): continue
            #print '-'*23

            try:
                # -- col and row index
                r = int(line.split(":")[0].split('(')[1].split(')')[0].split(',')[0])
                c = int(line.split(":")[0].split('(')[1].split(')')[0].split(',')[1])
                dataCols = line.split("): ")[1].split(',')[:-1]
                lenData = len(dataCols)
                moodulo = cnt%2
                # print "dataCols", dataCols
                # print 'moodulo', moodulo
                # print "col", c
                # print "row ", r
                # print "lenData", lenData

                if moodulo == 1:
                    line1 = dataCols
                    parts += dataCols
                    dmiss = ncol - len(parts)
                    # print "parts is", parts

                    # print 'dmiss in mod1', dmiss

                    if len(parts)==ncol:
                        wholeData = parts             
                        dataChunk += [wholeData]
                        parts = []
                        # print 'saving row ',r,'in chunk'
                elif moodulo == 0:
                    line2 = dataCols
                    if dmiss: parts += dataCols[:dmiss]
                    else: parts = dataCols
                    # print "parts now", parts

                    if len(parts)==ncol:
                        wholeData = parts             
                        dataChunk += [wholeData]
                        parts = []
                        # print 'saving row ',r,'in chunk'

                        nextData = lenData - dmiss 
                        # print "Is data left ? ", nextData

                        # if there is data, fill new
                        if nextData:
                            parts = line2[nextData-1:]
                            nextData = lenData - dmiss 
                            # print "parts refilled", parts

                    # print "whole data", wholeData
                #     print 'dmiss in mod0', dmiss

                # print 'dataChunk', dataChunk
                
                if len(dataChunk)%incr == 0:
                    writeToFile(dataChunk, outfile)
                    # print "Writing full chunk at ", cnt, dataChunk 
                    dataChunk = []
                    
                cnt += 1
            except IndexError:
                print "This line didnt work", line

    writeToFile(dataChunk, outfile)
    outfile.close()
    print "closing " , outfilename

if __name__ == "__main__":

    convert(fname)
