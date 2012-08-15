#!/usr/bin/env python3
"""
Converts between numID (01,02,67) and alphaID (01,A1,df,jk,{l,etc)
"""

import sys
import math
import re
import os

FREQUENCYSNAPSHOT_MAX = 836
TIMESNAPSHOT_MAX = 439
PROBE_MAX = 439
#MODEFILTEREDPROBE_MAX = 43
MODEFILTEREDPROBE_MAX = 118

# TODO: Check the limits of the different numbering systems

def numID_to_alphaID_FrequencySnapshot(numID, snap_plane = 'x', probe_ident = '_id_', snap_time_number = 0):
  '''
  Converts numeric IDs to alpha IDs used by Bristol FDTD 2003

  return values:
  filename, alphaID, pair

  examples:
  26 -> z
  26+27 -> a{

  MAXIMUM NUMBER OF SNAPSHOTS: 32767 (=(2^8)*(2^8)/2 -1)
  MAXIMUM NUMBER OF SNAPSHOTS BEFORE RETURN to aa: 6938 = 26+256*27
  MAXIMUM NUMBER OF SNAPSHOTS BEFORE DUPLICATE IDs: 4508 = 26+(6-(ord('a')-1)+256)*27+1 (6=character before non-printable bell character)
  MAXIMUM NUMBER OF SNAPSHOTS BEFORE ENTERING DANGER AREA (non-printable characters): 836 = 26+(126-(ord('a')-1))*27
  '''

  if numID<1 or numID>FREQUENCYSNAPSHOT_MAX:
    print('ERROR: numID must be between 1 and '+str(FREQUENCYSNAPSHOT_MAX)+' or else you will suffer death by monkeys!!!', file=sys.stderr)
    sys.exit(-1)
  
  if snap_time_number<0 or snap_time_number>99:
    print('ERROR: snap_time_number must be between 0 and 99 or else you will suffer death by monkeys!!!', file=sys.stderr)
    sys.exit(-1)

  #snap_time_number = mod(snap_time_number,100);
  ilo = snap_time_number%10 # gets the 10^0 digit from snap_time_number
  ihi = snap_time_number//10 # gets the 10^1 digit from snap_time_number
  
  if numID<27:
    alphaID = chr(numID + ord('a')-1)
  else:
    alphaID = chr(numID//27 + ord('a')-1) + chr(numID%27 + ord('a'))

  filename = snap_plane + alphaID + probe_ident + chr(ihi + ord('0')) + chr(ilo + ord('0')) + '.prn'
  pair = str(numID) + ':' + alphaID
  
  return filename, alphaID, pair

def numID_to_alphaID_TimeSnapshot(numID, snap_plane = 'x', probe_ident = '_id_', snap_time_number = 0):
  '''
  Converts numeric IDs to alpha IDs used by Bristol FDTD 2003

  return values:
  filename, alphaID, pair
  
  examples:
  99 -> 99
  100 -> :0
  '''

  if numID<1 or numID>TIMESNAPSHOT_MAX:
    print('ERROR: numID must be between 1 and '+str(TIMESNAPSHOT_MAX)+' or else you will suffer death by monkeys!!!', file=sys.stderr)
    sys.exit(-1)
  
  if snap_time_number<0 or snap_time_number>99:
    print('ERROR: snap_time_number must be between 0 and 99 or else you will suffer death by monkeys!!!', file=sys.stderr)
    sys.exit(-1)

  ilo = snap_time_number%10
  ihi = snap_time_number//10

  if numID<10:
    alphaID = chr(numID + ord('0'))
  else:
    alphaID = chr((numID//10) + ord('0')) + chr((numID%10) + ord('0'))

  filename = snap_plane + alphaID + probe_ident + chr(ihi + ord('0')) + chr(ilo + ord('0')) + '.prn'
  pair = str(numID) + ':' + alphaID
  
  return filename, alphaID, pair

def numID_to_alphaID_Probe(numID, probe_ident = '_id_'):
  '''
  Converts numeric IDs to alpha IDs used by Bristol FDTD 2003

  return values:
  filename, alphaID, pair
  
  examples:
  99 -> 99
  100 -> :0
  '''

  if numID<1 or numID>PROBE_MAX:
    print('ERROR: numID must be between 1 and '+str(PROBE_MAX)+' or else you will suffer death by monkeys!!!', file=sys.stderr)
    sys.exit(-1)

  ilo = numID%10
  ihi = numID//10

  alphaID = chr(ihi + ord('0')) + chr(ilo + ord('0'))
  filename = 'p' + alphaID + probe_ident + '.prn'

  pair = str(numID) + ':' + alphaID
  
  return filename, alphaID, pair

def numID_to_alphaID_ModeFilteredProbe(numID, probe_ident = '_id_'):
  '''
  Converts numeric IDs to alpha IDs used by Bristol FDTD 2003

  return values:
  filename, alphaID, pair
  
  examples:
  9 -> 9
  10 -> :
  '''

  if numID<1 or numID>MODEFILTEREDPROBE_MAX:
    print('ERROR: numID must be between 1 and '+str(MODEFILTEREDPROBE_MAX)+' or else you will suffer death by monkeys!!!', file=sys.stderr)
    sys.exit(-1)

  alphaID = chr(numID + ord('0'));
  filename = 'i' + alphaID + probe_ident + '00.prn';

  pair = str(numID) + ':' + alphaID
  
  return filename, alphaID, pair

def alphaID_to_numID(alphaID_or_filename, expected_object_type=None, probe_ident=None):
  '''
  Converts alpha IDs used by Bristol FDTD 2003 to numeric IDs
  
  return values:
  numID, snap_plane, probe_ident, snap_time_number, fixed_filename, object_type

  examples:
  z -> 26
  a{ -> 26+27
  99 -> 99
  :0 -> 100
  '''
  
  # default values
  numID = None
  snap_plane = None
  snap_time_number = None
  alphaID = None
  object_type = None  
  fixed_filename = None

  if not isinstance(alphaID_or_filename, str):
    print('ERROR: alphaID_or_filename should be a string.', file=sys.stderr)
    sys.exit(-1)
  
  (directory,basename) = os.path.split(alphaID_or_filename)
    
  pattern_alphaID_fsnap = re.compile(r"^([a-z\{\|\}~][a-z\{]|[a-z])$")
  pattern_filename_fsnap = re.compile(r"^([xyz])([a-z\{\|\}~][a-z\{]|[a-z])(.*)(\d\d)\.prn$")
  m_alphaID_fsnap = pattern_alphaID_fsnap.match(basename)
  m_filename_fsnap = pattern_filename_fsnap.match(basename)

  pattern_alphaID_tsnap = re.compile(r"^([1-9A-Z:;<=>?@[]\d|\d)$")
  pattern_filename_tsnap = re.compile(r"^([xyz])([1-9A-Z:;<=>?@[]\d|\d)(.*)(\d\d)\.prn$")
  m_alphaID_tsnap = pattern_alphaID_tsnap.match(basename)
  m_filename_tsnap = pattern_filename_tsnap.match(basename)

  pattern_alphaID_probe = re.compile(r"^([0-9A-Z:;<=>?@[]\d)$")
  pattern_filename_probe = re.compile(r"^p([0-9A-Z:;<=>?@[]\d)(.*)\.prn$")
  m_alphaID_probe = pattern_alphaID_probe.match(basename)
  m_filename_probe = pattern_filename_probe.match(basename)

  #pattern_alphaID_mfprobe = re.compile(r"^([1-9A-Z:;<=>?@[])$")
  #pattern_filename_mfprobe = re.compile(r"^i([1-9A-Z:;<=>?@[])(.*)00\.prn$")
  
  #pattern_mfprobe = r"([1-9A-Z:;<=>?@[\]\\^_`a-z{|}~\x7f\x80])"
  
  pattern_mfprobe = r"([0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0¡¢£¤¥¦])"
  pattern_alphaID_mfprobe = re.compile(r"^"+pattern_mfprobe+r"$")
  #pattern_filename_mfprobe = re.compile(r"^i([0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0¡¢£¤¥¦])(.*)00\.prn$")
  pattern_filename_mfprobe = re.compile(r"^i"+pattern_mfprobe+r"(.*)00\.prn$")
  m_alphaID_mfprobe = pattern_alphaID_mfprobe.match(basename)
  m_filename_mfprobe = pattern_filename_mfprobe.match(basename)
  
  if m_alphaID_fsnap and (expected_object_type is None or expected_object_type=='fsnap'):
    alphaID = m_alphaID_fsnap.group(1)
    object_type = 'fsnap'
  elif m_alphaID_tsnap:
    alphaID = m_alphaID_tsnap.group(1)
    object_type = 'probe or tsnap or mfprobe'
  elif m_alphaID_probe:
    alphaID = m_alphaID_probe.group(1)
    object_type = 'probe or tsnap or mfprobe'
  elif m_alphaID_mfprobe:
    alphaID = m_alphaID_mfprobe.group(1)
    object_type = 'probe or tsnap or mfprobe'
  elif m_filename_fsnap:
    snap_plane = m_filename_fsnap.group(1)
    alphaID = m_filename_fsnap.group(2)
    probe_ident = m_filename_fsnap.group(3)
    snap_time_number = int(m_filename_fsnap.group(4))
    object_type = 'fsnap'
  elif m_filename_tsnap:
    snap_plane = m_filename_tsnap.group(1)
    alphaID = m_filename_tsnap.group(2)
    probe_ident = m_filename_tsnap.group(3)
    snap_time_number = int(m_filename_tsnap.group(4))
    object_type = 'tsnap'
  elif m_filename_probe:
    alphaID = m_filename_probe.group(1)
    probe_ident = m_filename_probe.group(2)
    object_type = 'probe'
  elif m_filename_mfprobe:
    alphaID = m_filename_mfprobe.group(1)
    probe_ident = m_filename_mfprobe.group(2)
    object_type = 'mfprobe'
  else:
    print('ERROR: All matches failed : basename = ' + basename, file=sys.stderr)

  if alphaID:
    
    if object_type == 'fsnap':
      
      if len(alphaID) == 1:
        numID = ord(alphaID) - ord('a') + 1
      elif len(alphaID) == 2:
        numID = 27*(ord(alphaID[0]) - ord('a') + 1) + (ord(alphaID[1]) - ord('a'))
      else:
        print('ERROR: alphaID is not of length 1 or 2: alphaID = ' + alphaID, file=sys.stderr)
      if not (snap_plane is None or numID is None or probe_ident is None or snap_time_number is None):
        fixed_filename = os.path.join(directory, 'fsnap_' + snap_plane + "%03d"%numID + probe_ident + "%02d"%snap_time_number + '.prn')

    elif object_type == 'tsnap':
      if len(alphaID) == 1:
        numID = ord(alphaID[0])-ord('0')
      else:
        numID = 10*(ord(alphaID[0])-ord('0')) + (ord(alphaID[1])-ord('0'))
      if not (snap_plane is None or numID is None or probe_ident is None or snap_time_number is None):
        fixed_filename = os.path.join(directory, 'tsnap_' + snap_plane + "%03d"%numID + probe_ident + "%02d"%snap_time_number + '.prn')

    elif object_type == 'probe':
      numID = 10*(ord(alphaID[0])-ord('0')) + (ord(alphaID[1])-ord('0'))
      if not (numID is None or probe_ident is None):
        fixed_filename = os.path.join(directory, 'p' + "%03d"%numID + probe_ident + '.prn')

    elif object_type == 'mfprobe':
      numID = (ord(alphaID[0])-ord('0'))
      if not (numID is None or probe_ident is None):
        fixed_filename = os.path.join(directory, 'mfprobe_i' + "%03d"%numID + probe_ident + '00.prn')

    elif object_type == 'probe or tsnap or mfprobe':
      if len(alphaID) == 1:
        numID = ord(alphaID[0])-ord('0')
      else:
        numID = 10*(ord(alphaID[0])-ord('0')) + (ord(alphaID[1])-ord('0'))

    else:
      print('ERROR: Unknown object type for basename = ' + basename+' and alphaID = '+str(alphaID), file=sys.stderr)
      
  else:
    print('ERROR: alphaID not found for basename = ' + basename, file=sys.stderr)
      
  return numID, snap_plane, probe_ident, snap_time_number, fixed_filename, object_type
  
def FrequencySnapshotID_Test():
  N = FREQUENCYSNAPSHOT_MAX
  for i in range(N):
    numID_in = i+1
    
    print('numID_to_alphaID_FrequencySnapshot(numID_in) check')
    filename_in, alphaID, pair = numID_to_alphaID_FrequencySnapshot(numID_in)
    print((filename_in, alphaID, pair))
    
    print('alphaID_to_numID(alphaID) check')
    numID_out, snap_plane, probe_ident, snap_time_number, fixed_filename, object_type = alphaID_to_numID(alphaID)
    print((numID_out, snap_plane, probe_ident, snap_time_number, fixed_filename, object_type))
    if numID_out != numID_in:
      sys.exit(-1)

    print('alphaID_to_numID(filename_in) check')
    numID_out, snap_plane, probe_ident, snap_time_number, fixed_filename, object_type = alphaID_to_numID(filename_in)
    print((numID_out, snap_plane, probe_ident, snap_time_number, fixed_filename, object_type))
    if numID_out != numID_in:
      sys.exit(-1)
  return
  
def TimeSnapshotID_Test():
  N = TIMESNAPSHOT_MAX
  for i in range(N):
    numID_in = i+1
    
    print('numID_to_alphaID_TimeSnapshot(numID_in) check')
    filename_in, alphaID, pair = numID_to_alphaID_TimeSnapshot(numID_in)
    print((filename_in, alphaID, pair))
    
    print('alphaID_to_numID(alphaID) check')
    numID_out, snap_plane, probe_ident, snap_time_number, fixed_filename, object_type = alphaID_to_numID(alphaID)
    print((numID_out, snap_plane, probe_ident, snap_time_number, fixed_filename, object_type))
    if numID_out != numID_in:
      sys.exit(-1)

    print('alphaID_to_numID(filename_in) check')
    numID_out, snap_plane, probe_ident, snap_time_number, fixed_filename, object_type = alphaID_to_numID(filename_in)
    print((numID_out, snap_plane, probe_ident, snap_time_number, fixed_filename, object_type))
    if numID_out != numID_in:
      sys.exit(-1)
  return
  
def ProbeID_Test():
  N = PROBE_MAX
  for i in range(N):
    numID_in = i+1
    
    print('numID_to_alphaID_Probe(numID_in) check')
    filename_in, alphaID, pair = numID_to_alphaID_Probe(numID_in)
    print((filename_in, alphaID, pair))
    
    print('alphaID_to_numID(alphaID) check')
    numID_out, snap_plane, probe_ident, snap_time_number, fixed_filename, object_type = alphaID_to_numID(alphaID)
    print((numID_out, snap_plane, probe_ident, snap_time_number, fixed_filename, object_type))
    if numID_out != numID_in:
      sys.exit(-1)

    print('alphaID_to_numID(filename_in) check')
    numID_out, snap_plane, probe_ident, snap_time_number, fixed_filename, object_type = alphaID_to_numID(filename_in)
    print((numID_out, snap_plane, probe_ident, snap_time_number, fixed_filename, object_type))
    if numID_out != numID_in:
      sys.exit(-1)
  return

def ModeFilteredProbeID_Test():
  N = MODEFILTEREDPROBE_MAX
  for i in range(N):
    numID_in = i+1
    
    print('numID_to_alphaID_ModeFilteredProbe(numID_in) check')
    filename_in, alphaID, pair = numID_to_alphaID_ModeFilteredProbe(numID_in)
    print((filename_in, alphaID, pair))
    
    print('alphaID_to_numID(alphaID) check')
    numID_out, snap_plane, ModeFilteredProbe_ident, snap_time_number, fixed_filename, object_type = alphaID_to_numID(alphaID,'mfprobe')
    print((numID_out, snap_plane, ModeFilteredProbe_ident, snap_time_number, fixed_filename, object_type))
    if numID_out != numID_in:
      sys.exit(-1)

    print('alphaID_to_numID(filename_in) check')
    numID_out, snap_plane, ModeFilteredProbe_ident, snap_time_number, fixed_filename, object_type = alphaID_to_numID(filename_in)
    print((numID_out, snap_plane, ModeFilteredProbe_ident, snap_time_number, fixed_filename, object_type))
    if numID_out != numID_in:
      sys.exit(-1)
  return

def FrequencySnapshotID_List():
  N = FREQUENCYSNAPSHOT_MAX
  for i in range(N):
    numID_in = i+1
    filename_in, alphaID, pair = numID_to_alphaID_FrequencySnapshot(numID_in)
    print(pair)
  return
  
def TimeSnapshotID_List():
  N = TIMESNAPSHOT_MAX
  for i in range(N):
    numID_in = i+1
    filename_in, alphaID, pair = numID_to_alphaID_TimeSnapshot(numID_in)
    print(pair)
  return
  
def ProbeID_List():
  N = PROBE_MAX
  for i in range(N):
    numID_in = i+1
    filename_in, alphaID, pair = numID_to_alphaID_Probe(numID_in)
    print(pair)
  return

def ModeFilteredProbeID_List():
  N = MODEFILTEREDPROBE_MAX
  for i in range(N):
    numID_in = i+1
    filename_in, alphaID, pair = numID_to_alphaID_ModeFilteredProbe(numID_in)
    print(pair)
  return
  
def main():
  
  FrequencySnapshotID_List()
  TimeSnapshotID_List()
  ProbeID_List()
  ModeFilteredProbeID_List()
  
  FrequencySnapshotID_Test()
  TimeSnapshotID_Test()
  ProbeID_Test()
  ModeFilteredProbeID_Test()
  
  return

if __name__ == "__main__":
  main()
