#!/usr/bin/python
#
# Jan, 2015, rkwee
# -----------------------------------------------------------------------------------
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", dest="fname", type="string",
                  help="put file name")

(options, args) = parser.parse_args()

fname = options.fname

# -----------------------------------------------------------------------------------

def ignorePattern():
    pattern = "!"
    fout = fname + '.new'

    fnew = open(fout, 'w')
    with open(fname) as mf:

        for line in mf:
            
            if line.startswith(pattern): continue
            else: fnew.write(line)

    fnew.close()
if __name__ == "__main__":

    ignorePattern()
