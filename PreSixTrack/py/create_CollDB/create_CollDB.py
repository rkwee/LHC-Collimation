#script by amarsili@cern.ch

from CollDB_inputs import *
from math import pi
from datetime import datetime
import coll_lists
import os
 
def read_twiss(filename):
  '''takes a twiss "filename" and extracts all collimators and their positions'''
  f = open(filename)
  translate_cast = {'s':str, 'le':float} #changes given types into python casting functions
  res = []
  for line in f:
    if "@" in line: continue #get rid of header
    if line[0] == "*": names = line.split()[1:] #names
    elif line[0]=="$": 
      given_cast = line.split()[1:]
      cast = [translate_cast[x[1:]] for x in given_cast] #list of same length as line with casting function
    else:
      els = line.split()
      res.append([cast[i](x.strip('"')) for i, x in enumerate(els)]) #strips element of " and apply adapted cast
  f.close()  
  return res, names
#

def make_valuedict(valist, name_column, column):
  '''takes a list of lines (usually from one of the read functions), a name_column (int) and a column number
  name_column is the number of the column containing the names (keys of the dict)
  column is the number of the column contain the values
  returns a dictionary where key = entry at position name_column, value = value at position column 
  TIP: column can be names.index('S')'''
  
  #return dict( [(l[name_column], l[column]) for l in valist] ) # too magical
  valuedict = {}
  for l in valist:
    valuedict[l[name_column]] = l[column]
  return valuedict
#

def make_listdict(res, names):
  '''changes the structure of the object'''
  listdict = {}
  for i, name in enumerate(names):
    listdict[name] = []
    for t in res:
      try: listdict[name].append(t[i])
      except IndexError: print "Error: list not complete, pb at tuple #"+str(res.index(t))+":\n"+str(t)
  return listdict
#

#class collimator(str):
  #'''collimator object. Like a string with more attributes, mainly from hard-coded dictionary'''
  
  #def __new__(cls, value):
    #obj = str.__new__(cls, value.upper())
    #return obj
  ##  
  
class collimator:
  '''collimator object. Attributes mainly from hard-coded dictionary
  name kept as attribute Name'''
  def __init__(self, s):
    self.Name = s.upper()
    self.Beam = self.beam()
    self.Type = self.Name.split('.')[0]
    self.IR = self.ir()
    self.Tilt = 0.
    self.BetaX = 'BetaX'
    self.BetaY = 'BetaY'
    self.S = 0.
    try:
      self.Material = material[self.Type]
      self.Length = length[self.Type]
    except KeyError:
      raise KeyError, "Type of collimator ("+self.Type+") not existing, probably not installed."
    try: self.Angle = angle[self.Name]
    except KeyError: raise KeyError, "Angle for collimator ("+self.Name+") not found!"
    #self.O = hand_get_setting(self, SettingDict)
  #
  
  def __repr__(self):
    return self.Name
  #
  def beam(self):
    if "B1" in self.Name:
      return 1
    elif "B2" in self.Name:
      return 2
    else: return 0
  #
  def ir(self):
    cell = self.Name.split('.')[1]
    return int(cell[-1])
  #
  def get_setting(self, SettingDict):
    self.O = hand_get_setting(self, SettingDict)
#

def make_SetDict(setting_file):
  '''makes setting dict. from setting file'''
  SetDict = {}
  try: 
    f = open(setting_file) #running locally
  except IOError:
    f = open(os.environ['PYTHONPATH']+'Scripts/'+setting_file) #platform-wide
  for line in f:
    if line.split() and line[0] != '#':
      try: key, value = line.split()
      except ValueError: raise ValueError, "The structure of the setting file is wrong: "+line
      SetDict[key] = value
  f.close()
  return SetDict
#  

def make_SetDict_fort3(fort3):
  sec, ter = read_fort3(fort3)
  SettingDict = match_settings(settings_sec, sec)
  SettingDict.update(match_settings(settings_ter, ter))
  return SettingDict
#

def hand_get_setting(col, SettingDict):
  if col.Type == 'TCP' and col.IR == 3: o = SettingDict['NSIG_TCP3']
  elif col.Type == 'TCP' and col.IR == 7: o = SettingDict['NSIG_TCP7']
  elif col.Type == 'TCSG' and col.IR == 3: o = SettingDict['NSIG_TCSG3']
  elif col.Type == 'TCSG' and col.IR == 7: o = SettingDict['NSIG_TCSG7']
  elif col.Type == 'TCSG' and col.IR == 6: o = SettingDict['NSIG_TCSTCDQ']
  elif col.Type == 'TCLA' and col.IR == 3: o = SettingDict['NSIG_TCLA3']
  elif col.Type == 'TCLA' and col.IR == 7: o = SettingDict['NSIG_TCLA7']
  elif col.Type == 'TCLP': o = SettingDict['NSIG_TCLP']
  elif col.Type == 'TCLD': o = SettingDict['NSIG_TCRYO']
  elif 'TCLI' in col.Type: o = SettingDict['NSIG_TCLI']
  elif 'TCDQ' in col.Type: o = SettingDict['NSIG_TCDQ']
  elif col.Type == 'TDI': o = SettingDict['NSIG_TDI']
  elif 'TCTH' in col.Type and col.IR == 1: o = SettingDict['NSIG_TCTH1']
  elif 'TCTH' in col.Type and col.IR == 2: o = SettingDict['NSIG_TCTH2']
  elif 'TCTH' in col.Type and col.IR == 5: o = SettingDict['NSIG_TCTH5']
  elif 'TCTH' in col.Type and col.IR == 8: o = SettingDict['NSIG_TCTH8']
  elif 'TCTV' in col.Type and col.IR == 1: o = SettingDict['NSIG_TCTV1']
  elif 'TCTV' in col.Type and col.IR == 2: o = SettingDict['NSIG_TCTV2']
  elif 'TCTV' in col.Type and col.IR == 5: o = SettingDict['NSIG_TCTV5']
  elif 'TCTV' in col.Type and col.IR == 8: o = SettingDict['NSIG_TCTV8']
  elif "NSIG_"+col.Type in SettingDict: o = SettingDict["NSIG_"+col.Type]
  else: 
    print "Opening for collimator ("+str(col)+") not found, set to 999."
    return 999.
  return float(o)
#

def match_settings(Types, values):
  SettingDict = {}
  for i in range(min(len(Types), len(values))):
    SettingDict[Types[i]] = values[i]
  return SettingDict
#
  
def read_collDB(filename, line_index = 7):
  '''prints specific line for each collimator'''
  f = open(filename)
  i = 0
  for line in f:
    if line[0] == 'T': 
      i = 0
      collimator = line.strip()
    if i == line_index: 
      print collimator, float(line)
    i += 1
  f.close()
#

def read_fort3(filename):
  '''gets the settings in sigma from correct line of fort.3'''
  f = open(filename)
  collimation = False
  i = 0
  for line in f:
    if "COLLIMATION" in line: collimation = True
    if collimation:
      i += 1
      if i == 5: #setting of primary and secondaries
	sec = line.split()
      if i == 6: #setting of tertiaries
	ter = line.split()
  return sec, ter
#

def print_all(cols):
  print 'Name\t\tPosition\tSetting\tLength\tMaterial\tBetaX\tBetaY\t\tAngle'
  for c in cols:
    print c, '\t', c.S, '\t', c.O, '\t', c.Length, '\t', c.Material, '\t', c.BetaX, '\t', c.BetaY, '\t', c.Angle


def write_CollDB(cols,  name = "CollDB"):
  '''function that writes the COllDB file in the proper style'''
  #get current time & date in proper form
  now = datetime.now().isoformat(' ').split('.')[0]
  header = '# Database for cleaning insertion collimators'
  cols.sort(key = lambda x:x.S)
  
  f = open(name, 'w')
  #f.write(header)
  print >> f, header
  print '# Created by script at '+now
  #print '# settings (in sigma) from ' + fort3
  #print '# position and beta from ' + twiss
  print '# /!\ can be edited by hand of course'
  print >> f, len(cols)
  for c in cols:
    print >> f, '#'
    print >> f, c
    print >> f, str(c).lower()
    print >> f, '  ', c.O
    print >> f, c.Material
    print >> f, c.Length
    print >> f, c.Angle
    print >> f, c.Tilt
    print >> f, '  ', c.BetaX
    print >> f, '  ', c.BetaY
  #
  f.close()
  print name, "written."
#

def write_CollPositions(cols, positions, filename = 'CollPositions.b1.dat'):
  f = open(filename, 'w')
  f.write("%Ind           Name   Pos[m]\n")
  for i, c in enumerate(cols):
    f.write('% 4i'%(i+1)) #index, formated to take 4 characters, filling with spaces before
    f.write('% 15s'%c.Name) #expert name, formated to take 15 characters, filling with spaces before
    f.write('% 9.2f'%c.S) #longit. position, formated to take 9 characters (including 2 decimals), filling with spaces before
    f.write('\n')
  f.close()
  print filename, "written."
#  

def find_collimators(namelist):
  '''function that extracts collimators names from ["namelist"].
  The collimators are chosen following criteria on their expert names'''
  cols = []
  for c in namelist:
    if c[:3] == "TDI": cols.append(c)
    if c[:2] == "TC" and not c[2] == 'A' and not c[4] == 'M':
      if c.split('.')[0] not in ['TCDD', 'TCDSA', 'TCDSB']: cols.append(c)
  return cols
#

def create_CollDB(twiss_file, setting_file, colllist = [], name = '', fort3 = ''):
  '''create a list of collimators (from [colist] if passed, otherwise from elements in twiss_file) 
  with attributes:
  - settings (in sigma) from "setting_file"
  /!\ if "fort3" is passed, will ignore "setting_file" and get settings from "fort3" instead!
  - position and Beta from "twiss_file"
  writes list in longitudinal order in "name"'''
  if fort3:
    sec, ter = read_fort3(fort3)
    SettingDict = match_settings(settings_sec, sec)
    SettingDict.update(match_settings(settings_ter, ter))
    print "# Settings from", fort3
  else: 
    SettingDict = make_SetDict(setting_file)
    print "# settings from", setting_file
  #  
  twiss, titles = read_twiss(twiss_file)
  print '# position and beta from ' + twiss_file
  #
  ld = make_listdict(twiss, titles)
  twiss_list = find_collimators(ld['NAME'])
  if not colllist:
    colllist = twiss_list
    print "# collimators list from", twiss_file
  else: 
    print "# collimators from given colllist."
    print "# These collimators in twiss file were ignored:"
    for c in twiss_list:
      if c not in colllist: print c
  betaX = make_valuedict(twiss, titles.index('NAME'), titles.index('BETX'))
  betaY = make_valuedict(twiss, titles.index('NAME'), titles.index('BETY'))
  pos = make_valuedict(twiss, titles.index('NAME'), titles.index('S'))
  cols = []
  for x in colllist:
    c = collimator(x)
    #except KeyError: 
      #print "Warning:", x, "could not be created (angle or material unkown), removed from the list."
      #continue
    c.get_setting(SettingDict)
    cols.append(c)
  real_cols = []
  for c in cols:
    try: 
      c.BetaX = betaX[c.Name]
      c.BetaY = betaY[c.Name]
      c.S = pos[c.Name]
      real_cols.append(c)
    except KeyError: print c, "not found in twiss file. Removed from list."
  #
  if not name:
    name = twiss_file[6:-4] # "twiss.blabla.dat" => "blabla"
    write_CollDB(real_cols, "CollDB."+name+'.'+str(c.Beam)) 
  write_CollPositions(real_cols, pos, "CollPositions."+name+'.b'+str(c.Beam)+".dat")
  
  return real_cols
#

if __name__ == '__main__':
  
  pass
  #SetDict = make_SetDict_fort3("../fort.3_4TeV.hor")
  #SetDict = make_SetDict('settings_by_type.4TeV.cfg')
  
  colls = create_CollDB('settings_by_type.4TeV.cfg', '../twiss.thin.as-built.b1.updated.dat', "CollDB_generated_by_script", coll_lists.after_LS1_b1)
  #cols.sort(key = lambda x:x.S)
  #print_all(cols)
  
  #fort3 = "../fort.3_4TeV.hor"
  #sec, ter = read_fort3(fort3)
  #SettingDict = match_settings(settings_sec, sec)
  #SettingDict.update(match_settings(settings_ter, ter))
  
  #cols = [collimator(x) for x in angle]
  
  #twiss_file = '../twiss.thin.as-built.b1.updated.dat'
  #twiss, names = read_twiss(twiss_file)
  #betaX = make_valuedict(twiss, 1, names.index('BETX'))
  #betaY = make_valuedict(twiss, 1, names.index('BETY'))
  #pos = make_valuedict(twiss, 1, names.index('S'))
  #for c in cols:
    #try: 
      #c.BetaX = betaX[c.Name]
      #c.BetaY = betaY[c.Name]
      #c.S = pos[c.Name]
    #except KeyError: print c, "not found in twiss file."
  
  #write_CollDB(cols)
  
  #c = collimator("tcp.6l3.b1")
  #filename = 'CollDB_V6.503_b1_3.5TeV'
  #read_collDB(filename)