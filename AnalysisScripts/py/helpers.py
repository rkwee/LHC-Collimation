#!/usr/bin/python
#
#
# R Kwee, June 2013

import os, math, time, ROOT
from ROOT import TLatex, TGraph, TH1F
import gzip
# ------------------------------------------------------------------------------------------------
workpath = '/afs/cern.ch/work/r/rkwee/HL-LHC/'
wwwpath  = '/afs/cern.ch/user/r/rkwee/public/www/HL-LHC/'
source_dir  = workpath + 'runs/sourcedirs/'
gitpath  = '/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/'
projectpath = '/afs/cern.ch/project/lhc_mib/'
#workpath = '/Users/rkwee/Documents/RHUL/work/runs/TCT/'
#wwwpath  = '/Users/rkwee/Documents/RHUL/work/results/www/'
gitpath  = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/'
thispath = '/Users/rkwee/Documents/RHUL/work/HL-LHC/runs/TCT/'
wwwpath = '/Users/rkwee/Documents/RHUL/work/HL-LHC/LHC-Collimation/Documentation/ATS/HLHaloBackgroundNote/wwwlxplus/'
# ------------------------------------------------------------------------------------------------
# tags for bbG analysis *only for giving name!*
tag_BH_3p5TeV = "_BH_3p5TeV_B1_20MeV"
tag_BG_3p5TeV = "_BG_3p5TeV_20MeV"

tag_BH_4TeV = '_BH_4TeV_B2_20GeV'
tag_BH_4TeV = '_offmin500Hz_4TeV_B2_20MeV'
tag_BH_4TeV = '_offplus500Hz_4TeV_B2_20MeV'
#tag_BH_4TeV = '_BH_4TeV_B2_20MeV'
#tag_BH_4TeV = '_BH_4TeV_B2_20GeV'
#tag_BH_4TeV = '_BH_4TeV_B2_20GeV_from20MeV'

tag_BG_4TeV = '_BG_4TeV_20MeV'

tag_BH_7TeV = '_BH_HL_tct5inrdB1_nomCollSett_20MeV'
#tag_BH_7TeV = '_BH_HL_tct5inrdB1_20MeV'
#tag_BH_7TeV = '_BH_HL_tct5otrdB2_20MeV'

tag_crab_HL = '_crabcf_tct5inrdb1_20MeV'
#tag_crab_HL = '_crabcf_tct5inrdb1_modTAN_20MeV'

tag_BH_6p5TeV = '_BH_6500GeV_haloB1_20MeV'
tag_BH_6p5TeV = '_BH_6500GeV_haloB2_20MeV'
tag_BG_6p5TeV = '_BG_6500GeV_flat_20GeV_bs'
# ................................................................................................
# -- ALSO SET ENERGY CUT
EnCut = '2.e-2'
#EnCut = '20.'
# ------------------------------------------------------------------------------------------------
length_LHC = 26658.8832
IPs = [
 ("IP1",        0.000000  ),      
 ("IP2",     3332.436584  ),      
 ("IP3",     6664.720800  ),      
 ("IP4",     9997.005016  ),      
 ("IP5",    13329.289233  ),      
 ("IP6",    16661.725816  ),      
 ("IP7",    19994.162400  ),      
 ("IP8",    23315.378983  ),      
]

# --------------------------------------------------------------------------------
def doRebin(hist,rbf):

    hist_rebinned = hist.Clone(hist.GetName()+"rebinned")
    # must be rad hist!
    if not hist_rebinned.GetName().count("Rad"):
        print "is it really a rad histogram??"
        sys.exit()
    else:
        print "rebinning", hist.GetName()

        
    # take out normalisation by binarea
    nbins = hist.GetNbinsX()
    print "rebinning ", hist.GetName(), "with ", nbins 
    for bin in range(1,nbins+1):
        binArea = math.pi*(hist.GetBinLowEdge(bin+1)**2 -hist.GetBinLowEdge(bin)**2)
        hist_rebinned.SetBinContent(bin,hist.GetBinContent(bin) * binArea)
        hist_rebinned.SetBinError(bin,hist.GetBinError(bin) * binArea)

    # rebin
    hist_rebinned.Rebin(rbf)

    # take back in normalisation by new binarea
    nbins = hist_rebinned.GetNbinsX()
    print "rebinned ", hist_rebinned.GetName(), ". new nbin= ", nbins 
    for bin in range(1,nbins+1):
        binArea = math.pi*(hist_rebinned.GetBinLowEdge(bin+1)**2 -hist_rebinned.GetBinLowEdge(bin)**2)
        hist_rebinned.SetBinContent(bin,hist.GetBinContent(bin)/binArea)
        hist_rebinned.SetBinError(bin,hist.GetBinError(bin)/binArea)

    # re-scale as bin content is already normalised independent of binning!
    hist_rebinned.Scale(1./rbf)

    
    return hist_rebinned
# --------------------------------------------------------------------------------
def mylabel(font):

    mylabel = TLatex()
    mylabel.SetNDC()
    mylabel.SetTextSize(0.05);    
    mylabel.SetTextFont(font)
    mylabel.SetTextColor(1)

    return mylabel

def mean(vec):
    meanVal = 0.
    N = len(vec)
    for n in vec:
        meanVal += n

    meanVal*=1.
    if N:
        meanVal /= N
    return meanVal

def stddev(vec):

    meanVal = mean(vec)
    N = len(vec)
    stddev = 0.
    for n in vec:
        stddev += (meanVal - n)**2

    if N > 1.:
        stddev = math.sqrt(stddev/(N-1))

    return stddev

# ------------------------------------------------------------------------------------------------
# first two numbers correspond to warm sections (ie element 0 and 1) if value is inbetween second and third number (ie between element 1 and 2 of the list) it's considered to be in a cold sector)

warm = [0.0,22.5365,54.853,152.489,172.1655,192.39999999999998,199.48469999999998,224.3,3095.454284,3155.628584,3167.740084,3188.4330840000002,3211.4445840000003,3263.867584,3309.9000840000003,3354.9740840000004,3401.005584,3453.4285840000002,3476.440084,3494.065584,3505.885284,3568.318584,6405.4088,6457.9138,6468.7785,6859.513800000001,6870.3785,6923.5338,9735.907016000001,9824.730516000001,9830.832016,9861.730516,9878.732016,9939.985516,9950.548016,10043.462016,10054.024516,10115.278016,10132.279516,10163.970516,10170.072016,10257.603016,13104.989233,13129.804533,13136.889233,13157.123733,13176.800233,13271.647233,13306.752733,13351.825733,13386.931233000001,13481.778233000001,13501.454732999999,13522.784533,13529.869233,13554.684533,16394.637816,16450.871316,16456.972816,16487.271316000002,16493.372816,16830.871316,16836.972815999998,16867.271316,16873.372816,16928.294816,19734.8504,19760.6997,19771.5644,20217.9087,20228.773400000002,20252.9744,23089.979683999998,23138.576984,23150.396684,23171.375484,23194.386984,23246.809984,23292.842484,23337.915484,23383.947984,23436.370984,23459.382483999998,23480.082484,23492.193984,23553.115984,26433.4879,26458.3032,26465.387899999998,26486.7177,26506.3942,26601.2412,26636.346700000002,26658.883199999997]

def addCol(fileName, colNumber):

    n = 0
    with open(fileName) as mf:
        for line in mf:

            try:
                n += float(line.split()[colNumber])

            except ValueError:    
                pass

    return n


def file_len(fname):

    if fname.endswith('gz'):
        i = 0
        f = gzip.open(fname,'r')
        for line in f:
           i += 1
        return i
    else:
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

def sum_npart(fname,index):
    # fname = file 
    # index = colum number that indicates particle number
    # all header strings are skipped 

    npart = []
    with open(fname) as f:
        for line in f:

            try:
                ipart = float(line.split()[index]) 
                
                if ipart not in npart:
                    npart += [ipart]

            except ValueError:
                pass
    return sum(npart)


def count_npart(fname,index):
    # fname = file 
    # index = colum number that indicates particle number
    npart = []
    with open(fname) as f:
        for line in f:
            try:
                ipart = float(line.split()[index]) 
                if ipart not in npart:
                    npart += [float(ipart)]
            except ValueError:
                pass

    return len(npart)
# ----------------------------------------------------------------------------
def getBeam(tag):
    
    Beam, beam, beamn = 'B2','b2', '2'
    if tag.count('B1') or tag.count('b1'):
        Beam, beam, beamn = 'B1','b1', '1' 

    return Beam, beam, beamn
# ----------------------------------------------------------------------------
def rename(fullpattern, suppresspattern):

    # remove suppresspattern from fullpattern

    return fullpattern.split(suppresspattern)[0]+ fullpattern.split(suppresspattern)[-1]
# ----------------------------------------------------------------------------
def checkSameOutput():
# Feb 2015  
  # returns the directories in which some of the result files are missing


  rundirs_f1 = []
  rundirs_f2 = []

  pattern  = 'LPI'

  direct1 = 'twin_H5_NewScatt_TCT_4TeV_B1hHalo_trajectories/'
  cmd = 'ls -1 ' + direct1 + 'run_*/'+pattern+'* >| ' + direct1 + 'tmp.f1'
  os.system(cmd)

  direct2 = 'twin_NewScatt_TCT_4TeV_B1hHalo_trajectories/'
  cmd = 'ls -1 ' + direct2 + 'run_*/'+pattern+'* >| ' + direct2 + 'tmp.f2'
  os.system(cmd)

  fname1 = direct1 + 'tmp.f1'
  with open(fname1) as mf:
    for line in mf:
      # get the run dir number
      rundirs_f1 += [int(line.split('run_')[1].split('/'+pattern)[0])]


  fname2 = direct2 + 'tmp.f2'
  with open(fname2) as mf:
    for line in mf:
      # get the run dir number
      rundirs_f2 += [int(line.split('run_')[1].split('/'+pattern)[0])]
  # ................................................................................
  present1, missing1 = [], []
  for f2 in rundirs_f2:
    if f2 not in rundirs_f1: missing1 += [f2]
    else:                    present1 += [f2]

  print len(missing1),' missing directories in ', direct1
  # ................................................................................
  present2, missing2 = [], []
  for f1 in rundirs_f1: 
    if f1 not in rundirs_f2: missing2 += [f1]
    else:                    present2 += [f1]

  print len(missing2),' missing directories in ', direct2
  # ................................................................................

  cmd = 'rm ' + direct1 + 'tmp*'
  #os.system(cmd)
  cmd = 'rm ' + direct2 + 'tmp*'
  #os.system(cmd)

  # format is list of int
  return missing1, missing2
# ----------------------------------------------------------------------------

def stringDateToTimeStamp(stringTime, format):

    # format can be "%Y-%m-%d %H:%M:%S"
    st_tup = time.strptime(stringTime, format)
    ts = time.mktime(st_tup)
    # to re-convert to string use time.ctime(ts)
    return ts

# ----------------------------------------------------------------------------
def createDictFromRow(fileName):
    debug = 0
    dList = []
    with open(fileName) as mf:

        for line in mf:

            dictkey = line.split()[0]

            restofline = line.split(dictkey)[-1]
            if debug: print "will have", len(restofline.split()), "elements for each key"

            restoflineList = [ i for i in restofline.split()]
            dList += [(dictkey, restoflineList)]

    return dict(dList)

# ----------------------------------------------------------------------------

def collDict(collsummary):
    # -- needs a coll_summary_jdfsijdhf.dat file -- #
    # returns a dictionary of collsummary file with collimator name as key
    # header is 
    # 1=icoll 	 2=collname 	 3=nimp 	 4=nabs 	 5=imp_av 	 6=imp_sig 	

    collList = []
    with open(collsummary) as cs:
        for line in cs:
            if line.count("#"): continue
            line = line.rstrip()
            collname = line.split()[1]
            collInfo = line.split()

            collList += [[collname, collInfo]]
            #print collList[-1]

    return dict(collList)
# ----------------------------------------------------------------------------
def collgapsDict(collgaps):
    # -- needs a collgaps.dat file -- #
    # returns a dictionary of collgaps content with collimator name as key
    # header is 
    # #0 ID #1 name #2 angle[rad] #3 betax[m] #4 betay[m] #5 halfgap[m] #6 Material # 7 Length[m] # 8 sigx[m] # 9 sigy[m] # 10 tilt1[rad] #11 tilt2[rad] #12 nsig

    collList = []
    with open(collgaps) as cg:
        for line in cg:
            if line.count("#"): continue
            line = line.rstrip()
            collname = line.split()[1]
            collInfo = line.split()

            collList += [[collname, collInfo]]
            #print collList[-1]

    return dict(collList)
# ----------------------------------------------------------------------------
def makeTGraph(xList, yList, color, mStyle):

    """ returns TGraph of x, y """
    gr = TGraph()
    np = len(xList) - 1  # remove title element
    gr.Set(np)

    gr.SetMarkerStyle(mStyle)
    gr.SetLineWidth(1)
    gr.SetLineColor(color)
    gr.SetMarkerColor(color)

    for i in range(len(xList)):
        x=float(xList[i])
        y=float(yList[i])
        #if i<10:print x, y
        gr.SetPoint(i, x, y)

    return gr
# ----------------------------------------------------------------------------
def makeTH1F(xList, yList, hname, nbins, xmin, xmax, color, mStyle):

    """ returns TH1F of x, y """
    hist = TH1F(hname, hname, nbins, xmin, xmax)
    # TH1F(hname, hname, len(axis)-1, array('d', axis) )
    # store sum of squares of weights 
    hist.Sumw2()

    hist.SetMarkerStyle(mStyle)
    hist.SetLineWidth(1)
    hist.SetLineColor(color)
    hist.SetMarkerColor(color)

    for i in range(1,len(xList)-1):
        x=float(xList[i+1])
        y=float(yList[i+1])
        #print x, y
        hist.Fill(x,y)

    return hist
# ----------------------------------------------------------------------------
def getListFromColumn(colList, fname):

    cnt = 0
    with open(fname) as mf:

        for line in mf:            

            lineCol = line.split()

            if cnt == 0:

                # -- list of lists for each desired column in file
                content = [ [] for i in range(len(colList)) ]

                cnt += 1

                #print('Created list for ', len(colList), 'columns')


            for i,c in enumerate(colList):

                #print('Filling colum', c, 'into list', content[i])
                try:
                    content[i] += [float(lineCol[c])]
                except:
                    print 'skipping filling of ....', lineCol[c]

    return content
