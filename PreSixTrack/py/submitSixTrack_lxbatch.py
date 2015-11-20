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
import os, stat, sys, random
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
parser.add_option("-t", dest="tag", type="string",
                  help="put name of TCS as in collDB, otherwise ignore (tcs is any appendix to CollDB*.data<tag>")
parser.add_option("-o", dest="opticstag", type="string",
                  help="put extension of optics tag, otherwise ignore")

(options, args) = parser.parse_args()

njobs = options.njobs
queuename = options.queuename
npacks = options.npacks
run_dir = options.run_dir
ckey = options.ckey
tag = options.tag
opticstag = options.opticstag

#tag  = '.'+ run_dir.split('7TeVPostLS1_')[-1]

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
gitpath    = '/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/SixTrackConfig/'
commonsource = sourcepath + 'common/'



# assume all exectutables are in sourcepath + 'common/'
cList  = [[ '3.5TeVExample',    [sourcepath + '3.5TeVExample/'   ,'SixTrack_4411_coll_gfortran_O4', '3500000' ]]]
cList += [[ '3.5TeVOldExe',     [sourcepath + '3.5TeVOldExe/'    ,'SixTrackwColl'                 , '3500000' ]]]
cList += [[ '7TeV_hHaloB1',     [sourcepath + 'NewColl7TeVB1/'   ,'SixTrack_4446_coll_gfortran_O4', '7000000' ]]]
cList += [[ '7TeV_hHaloB2',     [sourcepath + 'NewColl7TeVB2/'   ,'SixTrack_4446_coll_gfortran_O4', '7000000' ]]]
cList += [[ '7TeV_vHaloB1',     [sourcepath + 'NewColl7TeVB1/'   ,'SixTrack_4446_coll_gfortran_O4', '7000000' ]]]
cList += [[ '7TeV_vHaloB2',     [sourcepath + 'NewColl7TeVB2/'   ,'SixTrack_4446_coll_gfortran_O4', '7000000' ]]]
cList += [[ '4TeV_vHaloB2',     [sourcepath + 'TCT_4TeV_60cm/b2/','SixTrack_4518_cernlib_coll_gfortran_O4', '4000000' ]]]
cList += [[ '4TeV_hHaloB2',     [sourcepath + 'TCT_4TeV_60cm/b2/','SixTrack_4518_cernlib_coll_gfortran_O4', '4000000' ]]]
cList += [[ '4TeV_vHaloB1',     [sourcepath + 'TCT_4TeV_60cm/b1/','SixTrack_4518_cernlib_coll_gfortran_O4', '4000000' ]]]
cList += [[ '4TeV_hHaloB1',     [sourcepath + 'TCT_4TeV_60cm/b1/','SixTrack_4518_cernlib_coll_gfortran_O4', '4000000' ]]]
cList += [[ 'NewScatt_4TeV_hHaloB1', [gitpath + '4TeV/TCThaloStudies/b1/','SixTrack_4518_cernlib_coll_h5_gfortran_O4', '4000000' ]]]
cList += [[ 'NewScatt_4TeV_vHaloB1', [gitpath + '4TeV/TCThaloStudies/b1/','SixTrack_4518_cernlib_coll_h5_gfortran_O4', '4000000' ]]]
cList += [[ 'NewScatt_4TeV_hHaloB2', [gitpath + '4TeV/TCThaloStudies/b2/','SixTrack_4518_cernlib_coll_h5_gfortran_O4', '4000000' ]]]
cList += [[ 'NewScatt_4TeV_vHaloB2', [gitpath + '4TeV/TCThaloStudies/b2/','SixTrack_4518_cernlib_coll_h5_gfortran_O4', '4000000' ]]]

cList += [[ 'HL_TCT_hHaloB1_h5',[sourcepath + 'HL_TCT_7TeV/b1/'  ,'SixTrack_4518_cernlib_coll_h5_gfortran_O4', '7000000' ]]]
cList += [[ 'HL_TCT_vHaloB1_h5',[sourcepath + 'HL_TCT_7TeV/b1/'  ,'SixTrack_4518_cernlib_coll_h5_gfortran_O4', '7000000' ]]]
cList += [[ 'HL_TCT_hHaloB2_h5',[gitpath + '7TeV/hilumiLHC/TCThaloStudies_relaxedCollSettings/b2/' ,'SixTrack_4518_cernlib_coll_h5_gfortran_O4', '7000000' ]]]
cList += [[ 'HL_TCT_vHaloB2_h5',[gitpath + '7TeV/hilumiLHC/TCThaloStudies_relaxedCollSettings/b2/' ,'SixTrack_4518_cernlib_coll_h5_gfortran_O4', '7000000' ]]]

cList += [[ 'HL_TCT_hHaloB1_h5_nomSett',[gitpath + '7TeV/hilumiLHC/TCThaloStudies_nominalCollSettings/b1/' ,'SixTrack_4518_cernlib_coll_h5_gfortran_O4', '7000000' ]]]
cList += [[ 'HL_TCT_vHaloB1_h5_nomSett',[gitpath + '7TeV/hilumiLHC/TCThaloStudies_nominalCollSettings/b1/' ,'SixTrack_4518_cernlib_coll_h5_gfortran_O4', '7000000' ]]]
cList += [[ 'HL_TCT_ccf_h5_nomSett',[gitpath + '7TeV/hilumiLHC/TCThaloStudies_relaxedCollSettings/b1/' ,'SixTrack_4518_cernlib_coll_h5_gfortran_O4', '7000000' ]]]

cList += [[ '4TeV_vHaloB1_h5',  [sourcepath + 'TCT_4TeV_60cm/b1/','SixTrack_4518_cernlib_coll_h5_gfortran_O4', '4000000' ]]]
cList += [[ '4TeV_hHaloB1_h5',  [sourcepath + 'TCT_4TeV_60cm/b1/','SixTrack_4518_cernlib_coll_h5_gfortran_O4', '4000000' ]]]
cList += [[ '4TeV_vHaloB2_h5',  [sourcepath + 'TCT_4TeV_60cm/b2/','SixTrack_4518_cernlib_coll_h5_gfortran_O4', '4000000' ]]]
cList += [[ '4TeV_hHaloB2_h5',  [sourcepath + 'TCT_4TeV_60cm/b2/','SixTrack_4518_cernlib_coll_h5_gfortran_O4', '4000000' ]]]
cList += [[ '6.5TeV_hHaloB1_h5',[gitpath + '6.5TeV/MED800/B1/','SixTrack_4518_cernlib_coll_h5_gfortran_O4', '6500000' ]]]
cList += [[ '6.5TeV_vHaloB1_h5',[gitpath + '6.5TeV/MED800/B1/','SixTrack_4518_cernlib_coll_h5_gfortran_O4', '6500000' ]]]
cList += [[ '6.5TeV_hHaloB2_h5',[gitpath + '6.5TeV/MED800/B2/','SixTrack_4518_cernlib_coll_h5_gfortran_O4', '6500000' ]]]
cList += [[ '6.5TeV_vHaloB2_h5',[gitpath + '6.5TeV/MED800/B2/','SixTrack_4518_cernlib_coll_h5_gfortran_O4', '6500000' ]]]

cList += [[ '4TeV_pencilB1_h5',  [gitpath + '4TeV/TCThaloStudies/b1/','SixTrack_4518_cernlib_coll_h5_gfortran_O4', '4000000' ]]]
cList += [[ '4TeV_pencilB2_h5',  [gitpath + '4TeV/TCThaloStudies/b2/','SixTrack_4518_cernlib_coll_h5_gfortran_O4', '4000000' ]]]

cDict = dict(cList)

try:
    source_dir  = cDict[ckey][0]
except KeyError:
    print('KeyError, possible keys are:', cDict.keys())
    sys.exit()

afsRunMain  = "/afs/cern.ch/work/r/rkwee/HL-LHC/runs/"
afsRunMain  = "/afs/cern.ch/project/lhc_mib/bgChecks2/"

afs_run_dir = afsRunMain + run_dir + '/'
loc_run_dir = run_dir.split('/')[-1] + '/'
energy      = cDict[ckey][2]
haloType    = ''
doH5        = False
if ckey.count('vHalo'): haloType = 'vHalo/'
if ckey.count('hHalo'): haloType = 'hHalo/'
if ckey.count('pencil'): haloType = 'pencil/'
if cDict[ckey][1].count('h5') or cDict[ckey][1].count('H5'): doH5 = True

if doH5: print "=" * 22, "running h5 format ", "="*22
else: print "=" * 22, "running traditional format ", "="*22
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
fort2       = source_dir +'fort.2' + opticstag
fort3       = thissource + haloType + 'fort.3'
collDB      = thissource +'CollDB_V6.503_lowb_st.'+beam+'.data' + tag
collPos     = source_dir +'CollPositions.'+beam+'.dat'
apertfile   = source_dir +'allapert.' + beam
surveyfile  = source_dir +'SurveyWithCrossing_XP_lowb_'+beam+'.dat'
beamlossExe = commonsource +'beamLossPattern'
reserveDS   = ' -R "rusage[pool=14000]" '
reserveDS   = ''
h5dumpExe   = "/afs/cern.ch/user/r/rkwee/public/hdf5/hdf5-1.8.14/bin/h5dump"

if not doH5:
    beamlossExe = commonsource +'BeamLossPattern_2005-04-30_gcc2.9'
    reserveDS   = ' -R "rusage[pool=30000]" '

cleanIneExe = commonsource +'CleanInelastic_2013-08-19b'
cleanColExe = commonsource +'CleanCollScatter_2014.09.10'
cleancoll   = commonsource +'correct_coll_summary.sh'

if ckey.count('HL'):# and ckey.count('nomSett'): 
    collDB = source_dir +'CollDB.ats.11t.'+beam + tag

inputFiles  = [sixtrackExe,beamlossExe,cleanIneExe,cleanColExe,fort2,collPos,apertfile,cleancoll]

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

    run_job.write('date +"%T %d.%m.%Y %Z" \n')
    run_job.write('mkdir ' + loc_run_dir +'\n')
    run_job.write('mkdir ' + loc_run_dir +'run_' + str(index)+ '\n')
    run_job.write('cd ' + loc_run_dir + 'run_'+ str(index) +'\n')

    # copy the inputfiles
    for inpfile in inputFiles:
        
        # copy to the local, randomly attributed path on the lxbatch
        cmd =  'cp ' + inpfile + ' . \n'
        run_job.write(cmd)

    # fort2 file
    if not fort2.endswith(".2"):
        cmd = "mv fort.2* fort.2\n"
        run_job.write(cmd)

    # hardcoded in BeamLossPattern
    cmd = 'cp ' + surveyfile + ' SurveyWithCrossing_XP_lowb.dat \n'
    run_job.write(cmd)

    # collDB
    if not tag.count("thin") and tag != '':
        cmd = 'cp ' + collDB + ' ' +collDB.split('/')[-1].split(tag)[0]+ ' \n'
    else:
        cmd =  'cp ' + collDB + ' . \n'

    run_job.write(cmd)

    # now fort3 file
    cmd_npacks = "sed 's\\1 "+energy+"\\" + npacks + " "+energy+"\\' " + fort3 + " > " + fort3.split('/')[-1]+'.tmp' + '\n'
    run_job.write(cmd_npacks)

    # fix random number
    rndm = str(random.random()*1e7)
    if rndm.count("."): rndm = rndm.replace('.','')
    rndm = rndm[:7]    

    cmd_rnd = "sed 's\\LSE. .FALSE. 0 .TRU\\LSE. .FALSE. " + str(rndm) +" .TRU\\' " + fort3.split('/')[-1]+'.tmp' + " > " + fort3.split('/')[-1] + '\n'
    run_job.write(cmd_rnd)
    run_job.write('rm ' + fort3.split('/')[-1]+'.tmp\n')

    run_job.write('./'+sixtrackExe.split('/')[-1] + ' >& screenout\n' ) 

    if not doH5:
        run_job.write('./'+beamlossExe.split('/')[-1] + ' lowb tracks2.dat BLP_out ' + apertfile.split('/')[-1]  + '\n')
        run_job.write("perl -pi -e 's/\\0/ /g' LPI_BLP_out.s" + '\n')

    else:
        run_job.write('./'+beamlossExe.split('/')[-1] + ' tracks2.h5 BLP_out ' + apertfile.split('/')[-1] + ' SurveyWithCrossing_XP_lowb.dat' + '\n')

    run_job.write('./'+cleanIneExe.split('/')[-1] + ' FLUKA_impacts.dat LPI_BLP_out.s '+ collPos.split('/')[-1] + ' coll_summary.dat\n')
    run_job.write('./'+cleanColExe.split('/')[-1] + ' Coll_Scatter.dat LPI_BLP_out.s ' + collPos.split('/')[-1] + ' coll_summary.dat\n')
    run_job.write('./'+cleancoll.split('/')[-1] + '\n')

    # gzip log file
    cmd = 'gzip FirstImpacts.dat \n'
    run_job.write(cmd)

    # gzip impacts file
    cmd = 'gzip impacts* \n'
    run_job.write(cmd)

    # gzip impacts file
    cmd = 'gzip Coll_Scatter* \n'
    run_job.write(cmd)

    # gzip impacts file
    cmd = 'ls -lrth tracks2* \n'
    run_job.write(cmd)

    # copy back
    # cmd_copy = 'cp amplitude.dat efficiency.dat coll_summary.dat screen* survival.dat LP* FLUKA* FirstImpacts.dat sigmasettings.out impacts* ' + subdir
    if doTest:
        cmd_copy = 'mv coll_summary.dat collgaps* screen* LP* FirstImpacts.dat* sigmasettings.out impacts* ' + subdir +'\n'
        cmd_copy = "mv * " + subdir +'\n'
    else:
        cmd_copy = 'mv coll_summary.dat LPI* FirstImpacts.dat* impacts_real* Coll_Sc*real* ' + subdir +'\n'

    run_job.write(cmd_copy)
    run_job.write('date +"%T %d.%m.%Y %Z" \n')
    run_job.close()

    # make it executable 
    cmd = 'chmod 755 ' + run_job_fname
    os.system(cmd)

    # submit to batch
    cmd = 'bsub '+mailOpt+' -q ' + queuename + reserveDS + ' < ' + run_job_fname
    print cmd

    if doRun:        
        os.system(cmd)
        if not doH5: cmd = "sleep 4"
        else: cmd = "sleep 2"
        os.system(cmd)
# -----------------------------------------------------------

cnt = len(newrange)
if doRun:
    print "submitted", cnt, "jobs"
else:
    print "would have submitted", cnt, "jobs"
