#!/usr/bin/env python3

import sys
import re
import subprocess
import getpass
import os

# TODO: Finish this

def parseQstatFullOutput(qstat_full_output):


  job_list = []

  pattern_job = re.compile("Job Id: (?P<jobId>.*?)\n(?P<jobDetails>.*?)\n\n",re.DOTALL)
  for job_blob in pattern_job.finditer(qstat_full_output):
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

  if len(sys.argv)>1:
    with open(sys.argv[1], 'r') as f:
      qstat_full_output = f.read()
  else:
    qstat_process = subprocess.Popen(['qstat','-f'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return_code = qstat_process.wait()
    (qstat_full_output, qstat_stderr) = qstat_process.communicate()

  job_list = parseQstatFullOutput(qstat_full_output)

  for job in job_list:
    if getpass.getuser() in job['Job_Owner']:
      #print(job['Job_Name'])
      #print(job['jobId'])
      #print(job['submit_args'].split()[-1])
      
      if 'Variable_List' in job.keys():
        variable_dict = dict([i.split('=',1) for i in job['Variable_List'].split(',')])
        #print(variable_dict['JOBDIR'])
        #print(variable_dict)
        #print(variable_dict['PBS_O_WORKDIR'])
        
      script_path = os.path.join(variable_dict['PBS_O_WORKDIR'],job['submit_args'].split()[-1])
      print(job['jobId'] + ' -> ' + script_path + ' job_state=' + job['job_state'])
    
  print('Number of jobs = '+str(len(job_list)))

  return
  
if __name__ == "__main__":
  '''
  qstat wrapper
  '''
  main()
