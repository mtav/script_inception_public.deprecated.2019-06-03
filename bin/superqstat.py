#!/usr/bin/env python3

import sys
import re

# TODO: Finish this

def parseFile(infile):

  QFILE = infile
  with open(QFILE, 'r') as f:
    # read the whole file as one string
    fulltext = f.read()

  pattern_job = re.compile("Job Id: (?P<jobId>.*?)\n(?P<jobDetails>.*?)\n\n",re.DOTALL)

  job_blob_iterator = pattern_job.finditer(fulltext)
  Njobs = sum(1 for _ in job_blob_iterator)
  print('Number of jobs = '+str(Njobs))
  
  job_blob_iterator = pattern_job.finditer(fulltext)
  job_blob = job_blob_iterator.__next__()

  #print(job_blob.groupdict())
  print(job_blob.groupdict()['jobId'])
  job_details = job_blob.groupdict()['jobDetails']
  #print(job_details)
  
  job_details = job_details.replace('\n\t','')
  #print(job_details)

  pattern_jobitems = re.compile("\s*(?P<key>.*)\s*=\s*(?P<value>.*)\s*")
  job_items_iterator = pattern_jobitems.finditer(job_details)

  #job_item = job_items_iterator.__next__()
  #print(job_item.groupdict())
  
  for job_item in job_items_iterator:
    print(job_item.groupdict())
  
  #for job_blob in job_blob_iterator:
    #print(job_blob)
  
  return

def main():
  parseFile(sys.argv[1])
  return
  
if __name__ == "__main__":
  '''
  qstat wrapper
  '''
  main()
