#!/usr/bin/python
#
# May 2013, rkwee
# -----------------------------------------------------------------------------------
# from optparse import OptionParser

# parser = OptionParser()
# parser.add_option("-p", dest="path", type="string",
#                   help="put path of dir with result files")
# parser.add_option("-t", dest="tag", type="string",
#                   help="tag of files, eg _nominal ")
# parser.add_option("-z", dest="doZoom", type="int",
#                   help="if do zooms")

# (options, args) = parser.parse_args()

# tag  = options.tag
# path = options.path
# doZoom = options.doZoom

## -------------------------------------------------------------------------------
import ROOT, sys, glob, os
from ROOT import *
import helpers, gzip
from helpers import *
## -------------------------------------------------------------------------------
def lossmap(path,tag,doZoom,doPrint):

    print ' losses on collmator Danieles script'

    debug = False


    if not path.endswith('/'):
        path += '/'


    # path  = workpath + 'HL-LHC-Collimation/AnalysisScripts/C/danielesExample/forRegina/'

    # f1    = path + 'LPI_BLP_out.s_total.dat'
    # f2    = path + 'coll_summary_cleaned.dat'
    # f3    = path + 'CollPositions.V6503.cry.dat'
    # f4    = path + 'FirstImpacts.dat_total.dat'

    # path  = '/afs/cern.ch/work/r/rkwee/public/sixtrack_example/clean_input/' 
    # f1    = path + 'LPI_BLP_out.s'
    # f2    = path + 'coll_summary.dat'
    # f3    = path + 'CollPositions.b1.dat'
    # f4    = path + 'FirstImpacts.dat'

    # path  = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/oldExe/'
    f1    = path + 'LPI_BLP_out'+tag+'.s'
    f2    = path + 'coll_summary'+tag+'.dat'
    f3    = helpers.source_dir + 'CollPositions.b1.dat'
    f4    = path + 'FirstImpacts'+tag+'.dat.gz'

    cmd = "perl -pi -e 's/\\0/ /g' " + f1
    print cmd
    os.system(cmd)             

    #check_npart(path,'_merged')
    #return

    rel = tag
    XurMin, XurMax = 0., length_LHC

    if doZoom:
        XurMin, XurMax = 18e3, 22e3
        rel = tag + '_zoom'

    YurMin, YurMax = 3.2e-9, 3.


    # loss positions
    losses = []
   
    with open(f1) as myfile:
        
        for line in myfile:
            
            line  = line.rstrip()
            
            losses += [float(line.split()[2])]


    names_sum, nabs, length = [],[],[]
    
    with open(f2) as myfile:
        for line in myfile:
            
            line = line.rstrip()
            
            if line.count("nabs"):
                continue

            names_sum  += [ line.split()[1] ]
            nabs   += [ float(line.split()[3]) ]
            length += [ float(line.split()[6]) ]


    names_pos, coll_pos = [],[]
    
    with open(f3) as myfile:

        for line in myfile:

            line = line.rstrip()

            if line.count("Pos"):
                continue

            names_pos  += [ line.split()[1] ]
            coll_pos   += [ float(line.split()[2]) ]


    # -- plot 

    cv = TCanvas( 'cv' + tag, 'cv' + tag, 1200, 700)
    #cv.SetRightMargin(0.12)

    # -- the number of lines in FirstImpact-1 (for header) is the total number of particles hitting a collimator
    maxval = file_len(f4)-1
    tcs = tag.split('_')[-1]

    if doPrint:
        print '('+tcs+', ' + str(maxval) + ')'

    nbins, xmin, xmax = 10*length_LHC,0., length_LHC

    coll_loss = TH1F("coll_loss" + tag,"coll_loss" + tag,nbins, xmin, xmax)
    cold_loss = TH1F("cold_loss" + tag,"cold_loss" + tag,nbins, xmin, xmax)
    warm_loss = TH1F("warm_loss" + tag,"warm_loss" + tag,nbins, xmin, xmax)

    xtitle = 's [m]'
    ytitle = "Cleaning inefficiency #eta"

    coll_loss.SetLineColor(kBlack)
    warm_loss.SetLineColor(kOrange)
    cold_loss.SetLineColor(kBlue)

    meter  = range(10)
    n_warm = len(warm)
    k_warm = [2*k for k in range(n_warm/2)]

    f1_nlines = len(losses)
    f2_nlines = len(names_sum)
    f3_nlines = len(names_pos)

    # -- cold and warm losses for 10th of 1 meter
    for j in range(10):                                                                                                              
        for i in range(f1_nlines):
            for k in k_warm:
                
                if losses[i] >= warm[k] and losses[i] <= warm[k+1]:
                    warm_loss.Fill(losses[i])                                                                   
                if k<n_warm-1 and losses[i] >= warm[k+1] and losses[i] <= warm[k+2]:
                    cold_loss.Fill(losses[i])                                                 

    # -- losses on collimator
    # f2_nlines = 0 
    for i in range(f2_nlines):

        for j in range(f3_nlines):

            if names_sum[i] == names_pos[j]:

                kval = int(nabs[i]/length[i])
                
                for k in range(kval):
                    
                    coll_loss.Fill(coll_pos[j])                


    #pad_l.SetLogy(1)
    coll_loss.GetXaxis().SetTitleOffset(.9)
    coll_loss.GetYaxis().SetTitleOffset(1.06)
    coll_loss.GetXaxis().SetTitle(xtitle)
    coll_loss.GetYaxis().SetTitle(ytitle)
    coll_loss.Scale(1.0/maxval)
    cold_loss.Scale(1.0/maxval)
    warm_loss.Scale(1.0/maxval)
    coll_loss.GetXaxis().SetRangeUser(XurMin, XurMax)
    coll_loss.GetYaxis().SetRangeUser(YurMin, YurMax)

    coll_loss.Draw('hist')
    cold_loss.Draw('samehist')
    warm_loss.Draw('samehist')

    lh = []
    # YurMin = 3.2e-9
    lhRange  = [3e-9+i*1e-9 for i in range(3,7)]
    lhRange += [i*1.e-8 for i in range(1,11)]
    lhRange += [i*1.e-7 for i in range(1,11)]
    lhRange += [i*1.e-6 for i in range(1,11)]
    lhRange += [i*1.e-5 for i in range(1,11)]
    lhRange += [i*1.e-4 for i in range(1,11)]
    lhRange += [i*1.e-3 for i in range(1,11)]
    lhRange += [i*1.e-2 for i in range(1,11)]
    lhRange += [i*1.e-1 for i in range(1,11)]
    lhRange += [i*1. for i in range(1,int(YurMax))]

    for i in lhRange:

        lh += [TLine()]
        lh[-1].SetLineStyle(1)
        lh[-1].SetLineColor(kGray)
        lh[-1].DrawLine(XurMin,i,XurMax,i)


    lv = []
    lvRange = [1000*i for i in range(0,int(length_LHC*1e-3))]
    for s in lvRange:

        if s > XurMin and s < XurMax:
            lv += [TLine()]
            lv[-1].SetLineStyle(1)
            lv[-1].SetLineColor(kGray)
            lv[-1].DrawLine(s,YurMin,s,YurMax)


    # lx, ly = TLine(),TLine()
    # lx.SetLineWidth(2)
    # lx.SetLineStyle(3)
    # lx.DrawLine(XurMin,1,XurMax,1)

    coll_loss.Draw('same')
    cold_loss.Draw('same')
    warm_loss.Draw('same')

    gPad.RedrawAxis()

    x1, y1, x2, y2 = 0.18, 0.78, 0.42, 0.9
    thelegend = TLegend( x1, y1, x2, y2)
    thelegend.SetFillColor(0)
    thelegend.SetLineColor(0)
    thelegend.SetTextSize(0.035)
    thelegend.SetShadowColor(10)
    thelegend.AddEntry(coll_loss,'losses on collimators', "L")
    thelegend.AddEntry(cold_loss,'cold losses', "L")
    thelegend.AddEntry(warm_loss,'warm losses', "L")
    thelegend.Draw()

    lab = mylabel(60)
    lab.DrawLatex(x1, y1-0.1, tcs)

    #gPad.SetRightMargin(1.2)
    #gStyle.SetStatX(0.9)
    #gStyle.SetStatY(0.95)
    gPad.SetGrid(0,1)
    gPad.SetLogy(1)

    pname  = wwwpath
    pname += 'scan/losses'+rel+'.png'

    print('saving file as' + pname ) 

    cv.Print(pname)

    #return cv
    return coll_loss, cold_loss, warm_loss

# ------------------------------------------------------------------------------------

def benchmarkEff(rfname,cvName):

    print'opening', rfname

    if not os.path.exists(rfname):
        print 'missing file', rfname
        sys.exit()

    rf    = TFile.Open(rfname)
    pList = rf.Get(cvName).GetListOfPrimitives()

    print 'In', cvName
    for obj in pList:
        if isinstance(obj, TH1):
            print 'found frame histogram', obj.GetName()

# ------------------------------------------------------------------------------------

def check_npart(thispath,appendix):

    index = 1
    
    # l = sum_npart(fname,index)
    #    print("npart of " + fname + " is " + str(l))    

    # ----

    # fname = thispath + "tracks2.dat"
    index = 0
    
    #l = count_npart(fname,index)
    #print("npart of " + fname + " is " + str(l))    

    # ----
    #fname = thispath + "survival"+appendix+".dat"
    #index = 1
    
    #l = count_npart(fname,index)
   
    #print("npart of " + fname + " is " + str(l))    

    # ----
    fname = thispath + "LPI_BLP_out"+appendix+".s"
    index = 1
    
    l = count_npart(fname,index)
   
    print("npart of " + fname + " is " + str(l))    
    # ----

    fname = thispath + "FirstImpacts"+appendix+".dat"
    index = 0
    
    ll = count_npart(fname,index)
    print("npart of " + fname + " is " + str(ll))

# ------------------------------------------------------------------------------------
if __name__ == "__main__":
    gROOT.SetBatch()
    gROOT.Reset()
    gROOT.SetStyle("Plain")
    gROOT.LoadMacro("/afs/cern.ch/user/r/rkwee/scratch0/miScripts/py/AtlasStyle.C")
    gROOT.LoadMacro("/afs/cern.ch/user/r/rkwee/scratch0/miScripts/py/AtlasUtils.C")
    SetAtlasStyle()

    #gStyle.SetOptStat(1000100110)
    gStyle.SetPalette(1)
    gStyle.SetStatX(0.95)
    gStyle.SetStatY(0.95)
    gStyle.SetTitleX(0.1)
    gStyle.SetTitleY(.955)

    gStyle.SetOptStat(0)
    #gStyle.SetCanvasColor(10)
    # gStyle.SetPalette(100,prepPalette())
 
    lossmap(path,tag,doZoom)
  
    print '--- fin ---'
