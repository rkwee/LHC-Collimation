#!/usr/bin/python
#
# this is a script to submit sixtrack jobs to lxbatch
# it needs a source dir with all the input files required for the job
# these are copied to the dir which is allocated randomly by the batch sytem
#
# a copy of the run structure is created on afs
# result files are copied back to that afs structure
#
# this script recognizes the directories already created in the main run_dir
# it will create new subdirs in run_dir counting on top of the exisisting ones
#
# Regina Kwee-Hinzmann
# 2013, June
#
# -----------------------------------------------------------
import os, stat, sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-r", dest="run_dir", type="string",
                  help="put name for run directory")
parser.add_option("-n", dest="njobs", type="int",
                  help="number of jobs")
parser.add_option("-q", dest="queuename", type="string",
                  help="put queuename")
parser.add_option("-p", dest="npacks", type="string",
                  help="put number of packs")
parser.add_option("-k", dest="ckey", type="string",
                  help="put key dictionary (similar as or same run_dir)")
parser.add_option("-t", dest="tcs", type="string",
                  help="put name of TCS as in collDB, otherwise ignore (tcs is any appendix to CollDB*.data<tcs>")

(options, args) = parser.parse_args()

njobs = options.njobs
queuename = options.queuename
npacks = options.npacks
run_dir = options.run_dir
ckey = options.ckey
tcs = options.tcs
#tcs  = '.'+ run_dir.split('7TeVPostLS1_')[-1]

# use the agruments
#njobs=10
#queuename='8nh'
#npacks='50'
doTest=0
doRun=1
showInfo=1
mailOpt = '-u Regina.Kwee@gmail.com'
# -----------------------------------------------------------

sourcepath = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/sourcedirs/'
commonsource = sourcepath + 'common/'

# assume all exectutables are in sourcepath + 'common/'
cList  = [[ '3.5TeVExample',    [sourcepath + '3.5TeVExample/'   ,'SixTrack_4411_coll_gfortran_O4', '3500000' ]]]
cList += [[ '3.5TeVOldExe',     [sourcepath + '3.5TeVOldExe/'    ,'SixTrackwColl'                 , '3500000' ]]]
cList += [[ '7TeV_hHaloB1',     [sourcepath + 'NewColl7TeVB1/'   ,'SixTrack_4446_coll_gfortran_O4', '7000000' ]]]
cList += [[ '7TeV_hHaloB2',     [sourcepath + 'NewColl7TeVB2/'   ,'SixTrack_4446_coll_gfortran_O4', '7000000' ]]]
cList += [[ '7TeV_vHaloB1',     [sourcepath + 'NewColl7TeVB1/'   ,'SixTrack_4446_coll_gfortran_O4', '7000000' ]]]
cList += [[ '7TeV_vHaloB2',     [sourcepath + 'NewColl7TeVB2/'   ,'SixTrack_4446_coll_gfortran_O4', '7000000' ]]]
cList += [[ '4TeV_vHaloB2',     [sourcepath + 'TCT_4TeV_60cm/b2/','SixTrack_4446_coll_gfortran_O4', '4000000' ]]]
cList += [[ '4TeV_hHaloB2',     [sourcepath + 'TCT_4TeV_60cm/b2/','SixTrack_4446_coll_gfortran_O4', '4000000' ]]]
cList += [[ '4TeV_vHaloB1',     [sourcepath + 'TCT_4TeV_60cm/b1/','SixTrack_4446_coll_gfortran_O4', '4000000' ]]]
cList += [[ '4TeV_hHaloB1',     [sourcepath + 'TCT_4TeV_60cm/b1/','SixTrack_4446_coll_gfortran_O4', '4000000' ]]]
cList += [[ 'HL_TCT_hHaloB1',   [sourcepath + 'HL_TCT_7TeV/b1/'  ,'SixTrack_4446_coll_gfortran_O4', '7000000' ]]]
cList += [[ 'HL_TCT_vHaloB1',   [sourcepath + 'HL_TCT_7TeV/b1/'  ,'SixTrack_4446_coll_gfortran_O4', '7000000' ]]]

cDict = dict(cList)

try:
    source_dir  = cDict[ckey][0]
except KeyError:
    print('KeyError, possible keys are:', cDict.keys())
    sys.exit()

afsRunMain  = "/afs/cern.ch/work/r/rkwee/HL-LHC/runs/"
afs_run_dir = afsRunMain + run_dir + '/'
loc_run_dir = run_dir.split('/')[-1] + '/'
energy      = cDict[ckey][2]
haloType    = ''
if ckey.count('vHalo'): haloType = 'vHalo/'
if ckey.count('hHalo'): haloType = 'hHalo/'
# -----------------------------------------------------------
beam        = 'b1'
if source_dir.count('B2') or source_dir.count('b2'):
    beam = 'b2'

if ckey.count('7TeV'): thissource  = sourcepath + 'postLS1/' + beam + '/'
else: thissource  = source_dir

if showInfo: print("Using thissource " + thissource )
# -----------------------------------------------------------
if not os.path.exists(afs_run_dir):
    print 'making dir', afs_run_dir
    os.mkdir(afs_run_dir)

# prepare runfiles: these files should be present in source_dir

sixtrackExe = commonsource +cDict[ckey][1]
fort2       = source_dir +'fort.2'
fort3       = thissource + haloType + 'fort.3'
collDB      = thissource +'CollDB_V6.503_lowb_st.'+beam+'.data' + tcs
collPos     = source_dir +'CollPositions.'+beam+'.dat'
apertfile   = source_dir +'allapert.' + beam
surveyfile  = source_dir +'SurveyWithCrossing_XP_lowb_'+beam+'.dat'
beamlossExe = commonsource +'BeamLossPattern_2005-04-30_gcc2.9'
cleanIneExe = commonsource +'CleanInelastic'
cleancoll   = commonsource +'correct_coll_summary.sh'

if ckey.count('HL'): collDB = source_dir +'CollDB.ats.11t.'+beam + tcs
inputFiles  = [sixtrackExe,beamlossExe,cleanIneExe,fort2,collPos,apertfile,surveyfile,cleancoll]

cnt = 0
for i in inputFiles:

    inpfile = i
    if not os.path.exists(inpfile):
        print('This input file ' + inpfile + ' does not exists!')
        cnt += 1

if cnt:
    print("Missing inputfile(s)! Exiting.")
    sys.exit()

# -----------------------------------------------------------

occupiedDirs = []

for subdir in os.listdir(afs_run_dir):
    if not subdir.startswith('run'): continue

    if showInfo:
        print "checking", subdir
    if os.path.isdir(afs_run_dir+subdir):
        occupiedDirs += [int(subdir.split('_')[-1])]

startjob = -1
if occupiedDirs:
    startjob = max(occupiedDirs)

if showInfo:
    print "occupiedDirs", occupiedDirs
    print("starting in folder run_" + str(startjob))

newrange = range(startjob+1, startjob+njobs+1)

if showInfo:
    print "newrange", newrange
# -----------------------------------------------------------
for job in newrange:

    index = str(job)

    if len(index) < 5:
        index = '0'*(5-len(str(job)))+str(job)

    # for each job create a subdir
    subdir = afs_run_dir + 'run_' + index + '/'
    os.mkdir(subdir)

    print('Changing to rundir ' + subdir)
    os.chdir(subdir)
    
    # write a job script

    run_job_fname = subdir + 'job_'+str(index)+'.sh'
    run_job = open(run_job_fname,'w')
    run_job.write('#!/bin/bash\n\n')

    run_job.write('mkdir ' + loc_run_dir +'\n')
    run_job.write('mkdir ' + loc_run_dir +'run_' + str(index)+ '\n')
    run_job.write('cd ' + loc_run_dir + 'run_'+ str(index) +'\n')

    # copy the inputfiles
    for inpfile in inputFiles:
        
        # copy to the local, randomly attributed path on the lxbatch
        cmd =  'cp ' + inpfile + ' . \n'
        run_job.write(cmd)

    # hardcoded in BeamLossPattern
    cmd = 'cp ' + surveyfile + ' SurveyWithCrossing_XP_lowb.dat \n'
    run_job.write(cmd)

    # collDB
    if len(tcs) > 1:
        cmd =  'cp ' + collDB + ' ' +collDB.split('/')[-1].split(tcs)[0]+ ' \n'
    else:
        cmd =  'cp ' + collDB + ' . \n'
    run_job.write(cmd)

    # now fort3 file
    cmd_npacks = "sed 's\\1 "+energy+"\\" + npacks + " "+energy+"\\' " + fort3 + " > " + fort3.split('/')[-1] + '\n'
    run_job.write(cmd_npacks)

    run_job.write('./'+sixtrackExe.split('/')[-1] + ' >| screenout\n' ) 
    run_job.write('./'+beamlossExe.split('/')[-1] + ' lowb tracks2.dat BLP_out ' + apertfile.split('/')[-1]  + '\n')
    run_job.write("perl -pi -e 's/\\0/ /g' LPI_BLP_out.s" + '\n')
    run_job.write('./'+cleanIneExe.split('/')[-1] + ' FLUKA_impacts.dat LPI_BLP_out.s '+ collPos.split('/')[-1] + ' coll_summary.dat\n')
    run_job.write('./'+cleancoll.split('/')[-1] + '\n')

    # gzip log file
    cmd = 'gzip FirstImpacts.dat \n'
    run_job.write(cmd)

    # copy back
    # cmd_copy = 'cp amplitude.dat efficiency.dat coll_summary.dat screen* survival.dat LP* FLUKA* FirstImpacts.dat sigmasettings.out impacts* ' + subdir
    if doTest:
        cmd_copy = 'cp coll_summary.dat collgaps* screen* LP* FirstImpacts.dat* sigmasettings.out impacts* ' + subdir
        cmd_copy = "cp * " + subdir
    else:
        cmd_copy = 'cp coll_summary.dat LP* FirstImpacts.dat* impacts* ' + subdir

    run_job.write(cmd_copy)

    run_job.close()

    # make it executable 
    cmd = 'chmod 755 ' + run_job_fname
    os.system(cmd)

    # submit to batch
    cmd = 'bsub '+mailOpt+' -q ' + queuename + ' -R "rusage[pool=30000]" < ' + run_job_fname
    print cmd

    if doRun:        
        os.system(cmd)
    
# -----------------------------------------------------------

cnt = len(newrange)
if doRun:
    print "submitted", cnt, "jobs"
else:
    print "would have submitted", cnt, "jobs"
