#!/usr/bin/python
#
# this is a script to submit fluka jobs to lxbatch
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
# 2013, September
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
parser.add_option("-c", dest="ncycles", type="string",
                  help="put number of cycles")
parser.add_option("-e", dest="nevents", type="string",
                  help="put number of events")
parser.add_option("-k", dest="ckey", type="string",
                  help="put key dictionary (similar as or same run_dir)")

(options, args) = parser.parse_args()

njobs = options.njobs
queuename = options.queuename
ncycles = options.ncycles
nevents = options.nevents
if not nevents.count('.'): nevents += "."
run_dir = options.run_dir
ckey = options.ckey

# use the agruments
#njobs=10
#queuename='8nh'
#ncycles='50'
doTest=0
doRun=0
showInfo=1
mailOpt = '-u Regina.Kwee@gmail.com'
# -----------------------------------------------------------
gitpath    = '/afs/cern.ch/work/r/rkwee/HL-LHC/LHC-Collimation/FlukaRoutines/'
sourcepath = '/afs/cern.ch/work/r/rkwee/HL-LHC/runs/sourcedirs/'
projectpath= "/afs/cern.ch/project/lhc_mib/"
commonsource = sourcepath + 'common/'

# assume all exectutables are in sourcepath + 'common/'

cList  = [['fluka_4TeV_haloB2',   [sourcepath + 'TCT_4TeV_60cm/fluka/','slc6Exe/ir1_4TeV_shscript.exe', '*fort.6*', 'RANDOMIZ       1.0  9875214.', '']]]
cList += [['fluka_4TeV_haloB1_20MeV',   [sourcepath + 'TCT_4TeV_60cm/fluka/','newExe/my.exe', '*fort.6*', 'RANDOMIZ       1.0  9875214.', '']]]
cList += [['fluka_HL_TCT_haloB2', [sourcepath + 'HL_TCT_7TeV/fluka/'  ,'exe_tct_impacts_myexe_new/mynew.exe', '*fort.*','RANDOMIZ         1.0  9875214.','']]]

cList += [['fl_HL_TCT5LOUT_rdB1', [sourcepath + 'HL_TCT_7TeV/fluka/hybrid/'  ,'withStuprf/hybridHL.exe', '*fort.30','RANDOMIZ         1.0  1822551.','tct5otrd']]]
cList += [['fl_HL_TCT5IN_rdB1',    [sourcepath + 'HL_TCT_7TeV/fluka/hybrid/','withStuprf/hybridHL.exe', '*fort.30','RANDOMIZ         1.0  1822551.','tct5inrd']]]
cList += [['fl_HL_TCT5IN_rdB2',    [sourcepath + 'HL_TCT_7TeV/fluka/hybrid/','withStuprf/hybridHL.exe', '*fort.30','RANDOMIZ         1.0  1822551.','tcinrdb2']]]
cList += [['fl_HL_TCT5LOUT_rdB2',    [sourcepath + 'HL_TCT_7TeV/fluka/hybrid/','withStuprf/hybridHL.exe', '*fort.30','RANDOMIZ         1.0  1822551.','tcotrdb2']]]
cList += [['fluka_6.5TeV_haloB1_20MeV', [gitpath + '6.5TeV/','hybridHL.exe', '*fort.30', 'RANDOMIZ       1.0  9875214.', 'HALOB1']]]
cList += [['fluka_6.5TeV_haloB2_20MeV', [gitpath + '6.5TeV/','hybridHL.exe', '*fort.30 *fort.*6*', 'RANDOMIZ       1.0  9875214.', 'HALOB2']]]
cList += [['fl_HL_crabfailB1',    [sourcepath + 'HL_TCT_7TeV/fluka/hybrid/','withStuprf/hybridHL.exe', '*fort.30','RANDOMIZ         1.0  1822551.','crabcfb1']]]
cList += [['fl_4TeV_BGcreateTrj_20MeV',  [gitpath + '4TeV/','sourceINICON/ini1.exe', '*fort.89','RANDOMIZ         1.0  9875214.','ICON*']]]
cList += [['fl_6.5TeV_BGcreateTrj_20MeV',[projectpath + 'beamgas/6500GeV_beamsize/checkTrajectory6500GeV/inicon1/','ini.exe', '*fort.89','RANDOMIZ       1.0  9875214.','']]]
cList += [['fl_4TeV_BG_20MeV',    [gitpath + '4TeV/','beamgas/sourceBeamGasCorr/bg_4TeV.exe', '*fort.67 *fort.91','RANDOMIZ         1.0  9875214.','BGASA']]] # correction was in the writing out
cList += [['fl_6.5TeV_BG_20MeV', [gitpath + '6.5TeV/','beamgas/sourceBG/BG.exe', '*fort.67 *fort.91','RANDOMIZ         1.0  9875214.','BGASB']]] 


cDict = dict(cList)
try:
    source_dir  = cDict[ckey][0]
except KeyError:
    print('KeyError, possible keys are:', cDict.keys())
    sys.exit()

afsRunMain  = "/afs/cern.ch/work/r/rkwee/HL-LHC/runs/"
afsRunMain  = "/afs/cern.ch/project/lhc_mib/"

crabfolder  = ''
if ckey.count('crab'): 
    afsRunMain  = "/afs/cern.ch/project/lhc_mib/crabcf/"
    crabfolder  = '/crabcf/'

if ckey.count('4TeV') and ckey.count('createTr'): 
    afsRunMain  = "/afs/cern.ch/project/lhc_mib/beamgas/4TeV_beamsize/createTrajectories/"
elif ckey.count('4TeV') and ckey.count('BG_'): 
    afsRunMain  = "/afs/cern.ch/project/lhc_mib/beamgas/4TeV_beamsize/"
elif ckey.count('6.5TeV') and ckey.count('createTr'): 
    afsRunMain  = "/afs/cern.ch/project/lhc_mib/beamgas/6500GeV_beamsize/checkTrajectory6500GeV/inicon1/"
elif ckey.count('6.5TeV') and ckey.count('BG_'): 
    afsRunMain  = "/afs/cern.ch/project/lhc_mib/beamgas/6500GeV_beamsize/"

run_dir     = run_dir + "/"
afs_run_dir = afsRunMain + run_dir

# -----------------------------------------------------------
beam        = 'b1'
if ckey.count('B2') or ckey.count('b2'):
    beam = 'b2'

thissource  = ''
if showInfo: print("Using thissource " + thissource )
# -----------------------------------------------------------
if not os.path.exists(afs_run_dir):
    print 'making dir', afs_run_dir
    os.mkdir(afs_run_dir)

enCut = ''
if   ckey.count("20MeV"): enCut = "20MeV"
elif ckey.count("20GeV"): enCut = "20GeV"

# prepare runfiles: these files should be present in source_dir
flukaExe    = source_dir + cDict[ckey][1]

# what to copy back
fortfiles  = cDict[ckey][2]

# specific to each inp file the RAND seed string
iniRand    = cDict[ckey][3]

# name of datafile to be replaced in inp file (ONLY done if string to be replace is present!)
tctlosses  = cDict[ckey][4]

if  ckey.count("4TeV"):
    haloData    = source_dir + beam +'/HALO.dat'
    magfile1    = source_dir + 'MB.dat'
    magfile2    = source_dir + 'MBXW.dat'
    magfile3    = source_dir + 'MQTL.dat'
    magfile4    = source_dir + 'MQXA.dat'
    magfile5    = source_dir + 'MQXB.dat'
    magfile6    = source_dir + 'MQYana.dat'
    inpFile     = source_dir + beam + '/ir1_4TeV_settings_from_TWISS_'+enCut + '_' + beam+'.inp'
    if ckey.count('createTr'):
        inpFile     = source_dir + 'beamgas/ir1_4TeV_settings_from_TWISS_'+enCut + '_' + beam+'_orbitDumpICON.inp'
        inputFiles  = [magfile1,magfile2,magfile3,magfile4,magfile5,magfile6,flukaExe, inpFile]
        haloData    = source_dir +'ICON*dat'
        for i in range(1,1001):
            inputFiles += [source_dir +'inicon1/ICON'+str(i)+'.dat']

    elif ckey.count('BG_'):
        haloData    = source_dir + 'beamgas/' + tctlosses+'.dat'
        inpFile     = gitpath + '4TeV/beamgas/ir1_4TeV_settings_from_TWISS_'+enCut + '_' + beam+'.inp'
        inputFiles  = [magfile1,magfile2,magfile3,magfile4,magfile5,magfile6,flukaExe, inpFile,haloData]
    else:
        inputFiles  = [magfile1,magfile2,magfile3,magfile4,magfile5,magfile6,flukaExe, inpFile,haloData]

elif ckey.count("6.5TeV"):
    magfile1    = source_dir + 'MB.dat'
    magfile2    = source_dir + 'MBXW.dat'
    magfile3    = source_dir + 'MQTL.dat'
    magfile4    = source_dir + 'MQXA.dat'
    magfile5    = source_dir + 'MQXB.dat'
    magfile6    = source_dir + 'MQYana.dat'
    inputFiles  = [magfile1,magfile2,magfile3,magfile4,magfile5,magfile6,flukaExe]

    if ckey.count("halo"):
        haloData = source_dir + beam +'/'+ tctlosses+'.dat'
        inpFile  = source_dir + beam + '/ir1_6500GeV_'+beam+'_'+enCut+'.inp'
    elif ckey.count("BG"): 
        haloData = source_dir + 'beamgas/'+ tctlosses+'.dat'
        inpFile  = source_dir + 'beamgas/flat/ir1_6500GeV_'+beam+'_'+enCut+'.inp'
    elif ckey.count('createTr'):
        inpFile  = source_dir + 'ir1_6500GeV_'+beam+'_'+enCut+'_orbitDumpINICON.inp'
        haloData = ''
        for i in range(1,1001):
            inputFiles += [source_dir +'ICON'+str(i)+'.dat']
    else:
        haloData = ''

    inputFiles += [inpFile]
    if haloData: inputFiles+= [haloData]

elif ckey.count("HL"):

    # HL v1.0
    haloData    = source_dir + beam +'/'+ tctlosses+'.dat'
    # haloData    = source_dir + 'TCTIMPAC.dat'
    magfile1    = source_dir + 'MBXF_150.dat'
    magfile2    = source_dir + 'MQXFv3.dat'
    inpFile     = source_dir + beam + '/hllhc_ir1_'+beam+'_relaxColl_20MeV.inp'
    inputFiles  = [haloData, magfile1,magfile2, inpFile, flukaExe]

    # HYBRID version, HL v1.1 geo and v1.0 collimator 
    haloData    = source_dir + beam +'/'+ tctlosses+'.dat'
    magfile1    = source_dir + 'MBXF.dat'
    magfile2    = source_dir + 'MQXFv3.dat'
    magfile3    = source_dir + 'MQYana.dat'
    inpFile     = source_dir + beam + crabfolder + '/hilumi_ir1_hybrid_'+beam+'_exp_20MeV.inp'
    inputFiles  = [haloData,magfile1,magfile2,magfile3, inpFile, flukaExe]

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
    # simplify
    run_job_fname = subdir + 'job.sh'


    run_job = open(run_job_fname,'w')
    run_job.write('#!/bin/bash\n\n')
    
    run_job.write('export FLUKA=/afs/cern.ch/work/r/rkwee/Fluka/fluka20112clinuxAA/ \n')
    run_job.write('export FLUPRO=/afs/cern.ch/work/r/rkwee/Fluka/fluka20112clinuxAA/ \n')
    
    # run_job.write('export FLUKA=/afs/cern.ch/project/fluka/flukadev/ \n')
    # run_job.write('export FLUPRO=/afs/cern.ch/project/fluka/flukadev/ \n')

    run_job.write('export PATH=${FLUPRO}:${FLUPRO}/flutil:${PATH} \n')

    run_job.write('mkdir ' + run_dir +'\n')
    run_job.write('mkdir ' + run_dir +'run_' + str(index)+ '\n')
    run_job.write('cd ' + run_dir + 'run_'+ str(index) +'\n')

    # copy the inputfiles
    for inpfile in inputFiles:
        # copy to the local, randomly attributed path on the lxbatch
        cmd =  'cp ' + inpfile + ' . \n'
        run_job.write(cmd)

    flukaInp  = inpFile.split('/')[-1]
    flukaInpA = flukaInp + '.l'

    # change name of tct losses file
    sourceline = "linksour"
    newsourceline = tctlosses 
    if ckey.count('createTr'): 
        newsourceline = 'ICON'+ str(job)

    cmd = "sed 's\\" + sourceline + "\\" + newsourceline + "\\' " + flukaInp +  " > "+ flukaInpA + "\n" 
    run_job.write(cmd)

    cmd = "mv " + flukaInpA + " " + flukaInp + " \n"
    run_job.write(cmd)

    # random seed
    nDigits = 7
    rndm = str(random.random()*1e7)
    rndm = rndm[:nDigits]
    if not rndm.count('.'):
      rndm += '.'

    # sed needs new filenames
    flukaInp1 = flukaInp  + '.t'
    flukaInp2 = flukaInp1 + '.tp'

    cmd = "sed 's\\"+iniRand+"\\RANDOMIZ         1.0  "+rndm+"\\' " + inpFile.split('/')[-1] + " > "+ flukaInp1 + "\n"
    run_job.write(cmd)

    # number of events
    cmd = "sed 's\\START     10.0\\START     " + nevents + "\\' " + flukaInp1 + " > "+ flukaInp2+ "\n"
    run_job.write(cmd)

    cmd = "mv " + flukaInp2 + " " + flukaInp + "\n"
    run_job.write(cmd)

    # executable
    cmd = '$FLUPRO/flutil/rfluka -e '+flukaExe.split('/')[-1] +' -M ' + ncycles + ' ' + flukaInp.split('.')[0] + ' \n'
    run_job.write(cmd)

    # gzip log file
    cmd = 'gzip *out \n'
    run_job.write(cmd)

    # gzip inp file
    cmd = 'gzip *.inp \n'
    run_job.write(cmd)
    
    # copy back
    if doTest:
        cmd_copy = "cp * " + subdir
    else:
        cmd_copy = 'cp '+fortfiles+' *inp.gz *out* ' + subdir
        if ckey.count('Traj') : cmd_copy = 'cp '+fortfiles+' *out* ' + subdir

    run_job.write(cmd_copy)

    run_job.close()

    # make it executable 
    cmd = 'chmod 755 ' + run_job_fname
    os.system(cmd)

    # submit to batch
    cmd = 'bsub '+mailOpt+' -q ' + queuename + ' < ' + run_job_fname
    print cmd

    if doRun:        
        os.system(cmd)
        cmd = "sleep 2"
        os.system(cmd)
# -----------------------------------------------------------

cnt = len(newrange)
if doRun:
    print "submitted", cnt, "jobs"
else:
    print "would have submitted", cnt, "jobs"
