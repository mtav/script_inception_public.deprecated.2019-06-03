#!/usr/bin/env python3

import sys
import re

# TODO: Finish this

def parseFile(infile):

  #pattern = r""
  #Job Id: (.*)
      #Job_Name = (.*)
      #Job_Owner = (.*)
      #job_state = (.*)
      #queue = (.*)
      #server = (.*)
      #Checkpoint = (.*)
      #ctime = (.*)
      #Error_Path = (.*)
    #/qsub.chr.9.22.e1600362
      #Hold_Types = (.*)
      #Join_Path = (.*)
      #Keep_Files = (.*)
      #Mail_Points = (.*)
      #mtime = (.*)
      #Output_Path = (.*)
    #s/qsub.chr.9.22.o1600362
      #Priority = (.*)
      #qtime = (.*)
      #Rerunable = (.*)
      #Resource_List.nodect = (.*)
      #Resource_List.nodes = (.*)
      #Resource_List.walltime = (.*)
      #etime = (.*)
      #submit_args = (.*)

  QFILE = infile
  with open(QFILE, 'r') as f:
    # read the whole file as one string
    fulltext = f.read()
  
  print(fulltext)
  
  #pattern_objects = re.compile("(?P<Type>\w+)\s*(?P<nameblob>[^{}]+)?{(?P<data>[^{}]*)}",re.DOTALL)
  pattern_objects = re.compile("Job Id: (.*)\n\n",re.DOTALL)
  objects = [m.groupdict() for m in pattern_objects.finditer(fulltext)]

  #entries = []
  ## process objects
  #for i in range(len(objects)):
      #Type = objects[i]['Type']
      #name = ''
      #if 'nameblob' in objects[i].keys():
        ##print objects[i]['nameblob']
        #if objects[i]['nameblob']:
          ##print 'OK'
          #pattern_nameblob = re.compile("\*\*name=(.*)")
          #m = pattern_nameblob.match(objects[i]['nameblob'])
          #if m:
            #name = m.group(1).strip()
        ##else:
          ##print 'NOT OK'
          ##name = ''
      ##else:
        ##print 'NO NAME'
        ##name = ''
      #data = objects[i]['data']
      
      ## convert Type to upper case and strip it
      #Type = Type.upper().strip()
      ## split data by spaces and new lines
      #data = re.split('\s+',data)
      ## remove empty lines from data
      ##data = filter(None, data)
      #data = list(filter(None, data))
      ##print('data = '+str(data))
      
      #entry = Entry()
      #entry.Type = Type
      #entry.name = name
      #entry.data = data
      #entries.append(entry)

  #for line in f:
    #if len(line.strip())>0:
      #tab = line.strip().split('\t')

  return

def main():
  parseFile(sys.argv[1])
  return
  
if __name__ == "__main__":
  '''
  qstat wrapper
  '''
  main()
