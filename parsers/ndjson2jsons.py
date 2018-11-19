
# coding: utf-8

# In[7]:


import sys
import os
import pandas as pd
import json
import logging
import pandas_profiling


# In[8]:


class MakeDirectory:
    
    def __init__(self, path):
        self.path = path

    def create_dir(self):
        dirName = self.path
        try:
            os.makedirs(dirName)
            print("Directory " , dirName ,  " Created ") 
        except FileExistsError:
            print("Directory " , dirName ,  " already exists")


# In[9]:


#input_path = "../data/ndjson"
input_path = "../data/ndjson/100/Procedure"
#input_filename = "3.DiagnosticReport.ndjson"
#input_filename = "3.Observation.ndjson"
#input_filename = "5.Procedure.ndjson"
input_filename = "1.Procedure.ndjson"
#input_filename = "2.Patient.ndjson"
input_dir = input_path + '/' + input_filename
print('INPUT DIR: ',input_dir)

output_filename = input_filename.split('.')[1]
#output_dir = "../output/ndjson/" + output_filename + '/'
output_dir = "../output/fhir-json/100/" + output_filename + '/'

directory = MakeDirectory(output_dir)
directory.create_dir()

with open(input_dir) as infile:
    index=0
    for line in infile:
        print(index)
        f = open(output_dir + str(index) + '.' + output_filename + '.json', 'w')
        f.write(line)
        f.close()
        index += 1

