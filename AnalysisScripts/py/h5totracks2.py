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
    cnt_l = -9999
    incr = 9

    outfilename = fname + '.rawlist'
    print("writing ... " + outfilename )

    outfile = open(outfilename, 'w')
    dataChunk = []
    ncol = 9
    nextData, dmiss= 0, 0
    parts = []

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
                dataCols = line.split("): ")[1].split(',')
                if dataCols[-1] == '' or dataCols[-1] == '\n': 
                    dataCols = dataCols[:-1]
                    # print "removing last element, datacols becomes", dataCols
                lenData = len(dataCols)
                moodulo = cnt%2
                # print "dataCols", dataCols
                # print 'moodulo', moodulo
                # print "col", c
                # print "row ", r
                # print "lenData", lenData
                # print "line", line

                if cnt == 1: cnt_l = r-1 # -1 because it is going to be increased by 1

                if moodulo == 1:
                    parts += dataCols
                    dmiss = ncol - len(parts)
                    # print "parts is", parts

                    # print 'dmiss in mod1', dmiss

                    if len(parts)==ncol:
                        dataChunk += [parts]
                        parts = []
                        cnt_l += 1
                        # print 'saving row ',r,'in chunk'

                elif moodulo == 0:
                    if dmiss: parts += dataCols[:dmiss]
                    else: parts = dataCols

                    if len(parts)==ncol:
                        dataChunk += [parts]
                        parts = []
                        cnt_l += 1
                        # print 'saving row ',r,'in chunk'

                        nextData = lenData - dmiss 
                        # print "Is data left ? ", nextData

                        ## -- #if there is data, fill new
                        if nextData:
                            parts = dataCols[nextData-1:]
                            nextData = lenData - dmiss 
                            # print "parts refilled", parts


                #     print 'dmiss in mod0', dmiss

                if len(dataChunk) == incr:
                    writeToFile(dataChunk, outfile)
                    # print "Writing full chunk at line ", cnt_l, " last element:", dataChunk[-1]
                    dataChunk = []

                cnt += 1
            except IndexError:
                print "This line didnt work", line

        print "writing last chunk of ", len(dataChunk), " elments with incr =", incr
        print("last element is ", dataChunk[-1])

        writeToFile(dataChunk, outfile)
        outfile.close()
        print "closing " , outfilename

if __name__ == "__main__":

    convert(fname)
