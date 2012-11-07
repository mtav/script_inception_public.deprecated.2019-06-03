#!/usr/bin/env python3

import sys
import re

# TODO: Finish this

def parseFile(QFILE):

  with open(QFILE, 'r') as f:
    # read the whole file as one string
    fulltext = f.read()

  job_list = []

  pattern_job = re.compile("Job Id: (?P<jobId>.*?)\n(?P<jobDetails>.*?)\n\n",re.DOTALL)
  for job_blob in pattern_job.finditer(fulltext):
    job_dict = {}

    job_id = job_blob.groupdict()['jobId']
    job_details = job_blob.groupdict()['jobDetails']
  
    job_dict['jobId'] = job_id
    
    job_details = job_details.replace('\n\t','')

    pattern_jobitems = re.compile("\s*(?P<key>.*?)\s*=\s*(?P<value>.*)\s*")
    for job_item in pattern_jobitems.finditer(job_details):
      key = job_item.groupdict()['key']
      value = job_item.groupdict()['value']
      job_dict[key]=value
    
    job_list.append(job_dict)
  
  return(job_list)

def main():
  job_list = parseFile(sys.argv[1])

  #for job in job_list:
    #print(job['Job_Name'])
    
  print('Number of jobs = '+str(len(job_list)))

  return
  
if __name__ == "__main__":
  '''
  qstat wrapper
  '''
  main()
