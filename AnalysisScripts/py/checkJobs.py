#!/usr/bin/python
#
# 
# script to check the output of lxbatch jobs
#
# R Kwee, July 2013

njobs = 5000
import os, math, subprocess
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-d", "--direct", dest="direct", type="string",
                  help="directory with run_ folders, if resubmit is used indicate the full path!!")
parser.add_option("-r", "--run", dest="doRun", type="int",
                  help="0 or 1 for not running or running, only used in resubmit")

(options, args) = parser.parse_args()
direct = options.direct
doRun = options.doRun
if not direct.endswith('/'):
  direct += '/'
resultfiles = 'LPI*'
resultfiles = '*fort.30*'

if resultfiles.count('LPI'): doIndex = 1
else: doIndex = 0
# ------------------------------------------
cmd = 'pwd'
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
myStdOut = process.stdout.read()
thispath = myStdOut.split()[0] + '/'

def getDirs(pattern):

  cmd = 'for i in `ls -d '+direct+pattern+'`; do echo $i; done'
  process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
  myStdOut = process.stdout.read()
  mydirs= myStdOut.split()
  return mydirs
# ------------------------------------------ 
def checkOutput():
  # ---
  # check if output has been produced
  # ---

  rundirs = []
  missing = []
  alldirs = []

  # all rundirs without path which have job finish sign
  mydirs = getDirs("run_*/job*sh")

  for md in mydirs:
    alldirs += [md.split('/')[-2]]
  print len(alldirs)," dirs with submitted jobs"

  # get rundirs with resultfile
  mydirs = getDirs("run_*/" + resultfiles)
  for md in mydirs:
    rundirs += [md.split("/")[-2]]
  print len(rundirs),"directories with results"

  for a in alldirs:
    if a not in rundirs:
      missing += [a]

  print 'counted', len(missing), 'missing dirs', missing

  action(missing,'ls -lrt',1)
  return missing, thispath
  # ---------

def resubmit(doRun, missing):
    cnt = 0
    notcnt = 0

    mailOpt = '-u Regina.Kwee@gmail.com -R "rusage[pool=16000]" '
    mailOpt = '-u Regina.Kwee@gmail.com '
    queuename = '1nw'
    fullpath = ''

    if thispath not in direct: fullpath = thispath + direct
    else: fullpath = direct

    # missing contains "run_" string
    for r in missing:

      index = '_' + r.split("_")[-1]
      if not doIndex: index = ''
      run_job_fname = fullpath + r +'/job'+index+'.sh'

      cmd = 'bsub '+mailOpt+' -q ' + queuename + ' < ' + run_job_fname

      if doRun:        
        print cmd    
        os.system(cmd)
        cmdS = 'sleep 2'
        os.system(cmdS)

        cnt += 1
      else:
        print cmd
        notcnt += 1

    if doRun: print 'counted ', cnt, 'submitted jobs'
    else: print 'would have submitted', notcnt, 'jobs'

# ------------------------------------------

def checkNfiles():

  # returns the directories in which some of the result files are missing

  rundirs_f1 = []
  rundirs_f2 = []

  f1Pattern  = 'LPI'
  f2Pattern  = 'impacts_r'

  cmd = 'ls -1 ' + direct + 'run_*/'+f1Pattern+'* >| ' + direct + 'tmp.f1'
  os.system(cmd)

  cmd = 'ls -1 ' + direct + 'run_*/'+f2Pattern+'* >| ' + direct + 'tmp.f2'
  os.system(cmd)

  fname1 = direct + 'tmp.f1'

  with open(fname1) as mf:
    for line in mf:
      # get the run dir number
      rundirs_f1 += [int(line.split('run_')[1].split('/'+f1Pattern)[0])]


  fname2 = direct + 'tmp.f2'

  with open(fname2) as mf:
    for line in mf:
      # get the run dir number
      rundirs_f2 += [int(line.split('run_')[1].split('/'+f2Pattern)[0])]

  missing = []
  cnt     = 0
  for f2 in rundirs_f2:

    if f2 not in rundirs_f1:

      cnt += 1

      missing += [f2]

  print 'directories in which some result files are missing in ' + fname1, missing
  action(missing,'ls -lrt',1)
  # ................................................................................
  missing = []
  cnt     = 0
  for f1 in rundirs_f1:

    if f1 not in rundirs_f2:

      cnt += 1

      missing += [f1]

  print 'directories in which some result files are missing in ' + fname2, missing

  action(missing,'ls -lrt',1)

  cmd = 'rm ' + direct + 'tmp*'
  os.system(cmd)

# -------------------------------------------------------------------------------------
def checkSameOutput():

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
  present2, missing2 = []
  for f2 in rundirs_f2:
    if f2 not in rundirs_f1: missing2 += [f2]
    else:                    present2 += [f2]

  print len(missing),' missing directories in ', direct1, missing1
  # ................................................................................
  present1, missing1 = [], []
  for f1 in rundirs_f1: 
    if f1 not in rundirs_f2: missing1 += [f1]
    else:                    present1 += [f1]

  print len(missing),' missing directories in ', direct2, missing2
  # ................................................................................

  cmd = 'rm ' + direct1 + 'tmp*'
  os.system(cmd)
  cmd = 'rm ' + direct2 + 'tmp*'
  os.system(cmd)

  # format is list of int
  return missing1, missing2
# -------------------------------------------------------------------------------------

def makeListofGoodFiles(direct, missing):

  pass  


# -------------------------------------------------------------------------------------

def action(missing,actionType,doAction):

  # remove them, they are faulty

  for m in missing:

    index = str(m)

    if len(index) < 5:
        index = '0'*(5-len(str(m)))+str(m)

        mdir = direct + 'run_' + index

        cmd = actionType + ' ' + mdir

        print cmd

        if doAction:
          os.system(cmd)

# -------------------------------------------------------------------------------------
if __name__ == "__main__":

  #checkSameOutput()
  cmd = 'date'
  os.system(cmd)

  missing, thispath = checkOutput()

  cmd = 'date'
  os.system(cmd)

  resubmit(doRun, missing)
  #checkNfiles()
  
  cmd = 'date'
  os.system(cmd)
