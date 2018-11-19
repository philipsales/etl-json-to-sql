
# coding: utf-8

# In[7]:
import sys
import os
import json


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


input_path = "/root/data/1M/patient"
input_filename = "1.Patient.ndjson"
input_dir = input_path + '/' + input_filename

print('INPUT DIR: ',input_dir)

output_filename = input_filename.split('.')[1]
output_dir = "/root/etl-json-to-sql/output/fhir-json/1M/" + output_filename + '/'

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

