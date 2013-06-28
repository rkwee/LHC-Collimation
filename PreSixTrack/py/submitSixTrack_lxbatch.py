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

njobs=10
queuename='8nh'
npacks='50'
doRun=1
showInfo=0
# -----------------------------------------------------------
afsRunMain  = "/afs/cern.ch/work/r/rkwee/HL-LHC/runs/"
run_dir     = "exampleRuns/"
source_dir  = "/afs/cern.ch/work/r/rkwee/public/sixtrack_example/clean_input/save/"
afs_run_dir = afsRunMain + run_dir
# -----------------------------------------------------------

if not os.path.exists(afs_run_dir):
    print 'making dir', afs_run_dir
    os.mkdir(afs_run_dir)

# prepare runfiles: these files should be present in source_dir

sixtrackExe = 'SixTrack_4411_coll_gfortran_O4'
fort2       = 'fort.2'
fort3       = 'fort.3'
collDB      = 'CollDB_V6.503_lowb_st.b1.data'
collPos     = 'CollPositions.b1.dat'
apertfile   = 'allapert.b1'
surveyfile  = 'SurveyWithCrossing_XP_lowb.dat'
beamlossExe = 'BeamLossPattern_2005-04-30_gcc2.9'
cleanIneExe = 'CleanInelastic'
cleancoll   = 'correct_coll_summary.sh'

inputFiles  = [sixtrackExe,beamlossExe,cleanIneExe,fort2,collDB,collPos,apertfile,surveyfile,cleancoll]

# -----------------------------------------------------------

occupiedDirs = []

for subdir in os.listdir(afs_run_dir):
    if showInfo:
        print "cheking", subdir
    if os.path.isdir(afs_run_dir+subdir):
        occupiedDirs += [int(subdir.split('_')[-1])]

startjob = 0
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

    # for each job create a subdir
    subdir = afs_run_dir + 'run_' + str(job) + '/'
    
    os.mkdir(subdir)

    print('Changing to rundir ' + subdir)
    os.chdir(subdir)
    
    # write a job script

    run_job_fname = subdir + 'job_'+str(job)+'.sh'
    run_job = open(run_job_fname,'w')
    run_job.write('#!/bin/bash\n\n')

    run_job.write('mkdir ' + run_dir +'\n')
    run_job.write('mkdir ' + run_dir +'run_' + str(job)+ '\n')
    run_job.write('cd ' + run_dir + 'run_'+ str(job) +'\n')

    # copy the inputfiles
    for inpfile in inputFiles:
        
        inpfile = source_dir + inpfile

        # copy to the local, randomly attributed path on the lxbatch
        cmd =  'cp ' + inpfile + ' . \n'
        run_job.write(cmd)

    # now fort3 file
    cmd = "sed 's\\100 3500000\\" + npacks + " 3500000\\' " + source_dir+fort3 + " > " + fort3 + '\n'
    run_job.write(cmd)

    run_job.write('./' +sixtrackExe + ' >| screenout\n' ) 
    run_job.write('./' +beamlossExe + ' lowb tracks2.dat BLP_out ' + apertfile  + '\n')
    run_job.write('./' +cleanIneExe + ' FLUKA_impacts.dat LPI_BLP_out.s '+ collPos + ' coll_summary.dat\n')
    run_job.write('./' + cleancoll + '\n')

    # copy back
    cmd = 'cp amplitude.dat efficiency.dat coll_summary.dat screen* survival.dat LP* FLUKA* FirstImpacts.dat sigmasettings.out impacts* ' + subdir
    #cmd = "cp * " + subdir + "\n"
    run_job.write(cmd)

    run_job.close()

    # make it executable 
    cmd = 'chmod 755 ' + run_job_fname
    os.system(cmd)

    # submit to batch
    cmd = 'bsub -q ' + queuename + ' -R "rusage[pool=30000]" < ' + run_job_fname
    print cmd

    if doRun:        
        os.system(cmd)
    
# -----------------------------------------------------------

cnt = len(newrange)
if doRun:
    print "submitted", cnt, "jobs"
else:
    print "would have submitted", cnt, "jobs"
