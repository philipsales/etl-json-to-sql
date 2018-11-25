
# coding: utf-8

# In[2]:


import sys
import os
from os import path
from os import walk

import re

import pandas as pd
import json
import logging
import pandas_profiling
from pandas.io.json import json_normalize 

from collections import OrderedDict


# ## Get Columns

# In[3]:


with open("../data/fhir-json/2rows/Patient/1.Patient.json") as f:
    d = json.load(f)

awhcuris = json_normalize(d)
address_data = awhcuris.head(31)
address_data.T

data_list = list(address_data)
data_list


# ## Flatten

# In[67]:


def flattenDict(d, result=None):
    
    if result is None:
        result = {}
        
    for key, value in list(d.items()):
        value = d[key]
        
        #TODO: OPtimiza strip clean
        if isinstance(value, str):
            value = value.replace("'", ' ')
    
                
        if isinstance(value, dict):
            #print('THIS IS DICT: ========')
            #print(value)
            value1 = {}
            for keyIn in value:
                #print('DICT keyIn :', keyIn)
                value1[".".join([key,keyIn])]=value[keyIn.lower()]
            flattenDict(value1, result)
        elif isinstance(value, (list, tuple)):  
            #print('THIS IS TUPEL: ', value)
            for indexB, element in enumerate(value):
                if isinstance(element, dict):
                    value1 = {}
                    index = 0
                    for keyIn in element:
                        #print('TUPLES keyIn :', keyIn)
                        #print('key :', key)
                        newkey = ".".join([key,keyIn])        
                        value1[".".join([key,keyIn])]=value[indexB][keyIn]
                        index += 1
                    for keyA in value1:
                        flattenDict(value1, result)   
        else: 
            result[key.lower()]=value
            
            #columns.append(key.lower())
            #print('[key]: ', key)
            
            
            #print('result[key]: ', result[key])
    

    return OrderedDict(sorted(result.items()))


# In[5]:


class MakeDirectory:
    
    def __init__(self, path):
        self.path = path

    def create_dir(self, folders=None):
        dirName = ''
        
        if isinstance(folders, list):
            
            for folder in folders:
                dirName =  self.path + '/' + folder
                try:
                    os.makedirs(dirName)
                    print("Directory " , dirName ,  " Created ") 
                except FileExistsError:
                    print("Directory " , dirName ,  " already exists")
        else:
            os.makedirs(dirName)


# ## Folder directory Iterator

# In[6]:


class FileIterator:
    
    def __init__(self, input_root, input_folders):
        self.input_data_dir = input_root
        self.input_folders = input_folders
        
    def iterate_filenames(self):
        resources = self.__iterate_dirfiles()
        
        files = self.__iterate_file(resources)
        
        return files
        
    def __iterate_dirfiles(self):
        path_files = []
        file_names = self.input_folders

        for file in file_names:
            path_files.append(input_data_dir + '/' + file)
        return path_files
    
    def __iterate_file(self, path_dbs):
        path_db_workload_files = []     
        for path_db in path_dbs:
            for root, dirs, files in walk(path_db): 
                index = 0
                for filename in files:
                    
                    print('remaining files: ', len(files)-index)
                    if not filename.endswith(('.json~', '.swp', '-checkpoint.json')):
                        print('valid file: ',filename)
                        path_db_workload_files.append(root + '/' + filename)
                        index+=1
                    if ''.join(dirs) != '.ipynb_checkpoints':
                        pass

        return path_db_workload_files


# ## Filecontent reader

# In[7]:


class ContentReaderJSON():
    
    def __init__(self, filename_paths):
        self.filename_paths = filename_paths
        
    def get_data(self):
        data = []
        for filename_path in self.filename_paths:
            
            json = ReadJSON()
            data.append(json.read(filename_path))

        return data


# In[8]:


class ContentReader():
    
    def __init__(self, filename_paths,  destination_path):
        self.filename_paths = filename_paths
        self.destination_path = destination_path
        
    def get_data(self):
        data = []
        index = 0
        for filename_path in self.filename_paths:
            
            print('remaining files: ', len(self.filename_paths) - index)
            
            read_json = ReadJSON()
            resource = read_json.read(filename_path)
            
            
            destination_path = '%s/%s' % (self.destination_path, resource['resourcetype'] )

            resource_id = resource['id'].split('-')[0]
            
            
            f = open(destination_path + '/' + resource_id + '.' + resource['resourcetype'] + '.json', 'w')
            f.write(json.dumps(resource))
            print('writing: ', resource_id)
            f.close()
            index += 1
            
            #data.append(read_json.read(filename_path))

        return data


# ## File Open

# In[71]:


class ReadJSON():
    
    @staticmethod
    def read(file_path):
        new_id = ''
        flat_d = ''
        
        with open(file_path) as f:
            d = json.load(f)
            flat_d = flattenDict(d)
            
            new_id = '%s:%s' % (flat_d['resourcetype'], flat_d['id'])
            flat_d['id'] = new_id
            
            if flat_d['resourcetype'] != 'Patient':
                #new_patient_id = 'Patient:%s' % (flat_d['subject.reference'])
                new_patient_id = flat_d['subject.reference'].replace("/", ":")
                flat_d.pop('subject.reference', None)
                flat_d['patientId'] = new_patient_id
            
        return flat_d


# ## Print Flatten FHIR JSON

# In[10]:


class MakeResults():
    def __init__(self, data, source_paths, destination_path):
        self.source_paths = source_paths
        self.data = data
        self.destination_path = destination_path
        
    def outputs(self):      
        for resource in self.data:
           
            destination_path = self.destination_path + '/' + resource['resourcetype']
            #print('destination: ' ,destination_path)
            id = resource['id'].split('-')[0]
     
            f = open(destination_path + '/' + id + '.' + resource['resourcetype'] + '.json', 'w')
            f.write(json.dumps(resource))
            f.close()
        return


# In[11]:


class MakeResult():

    @staticmethod
    def outputs(self):      
        for resource in self.data:
           
            destination_path = self.destination_path + '/' + resource['resourcetype']
            #print('destination: ' ,destination_path)
            id = resource['id'].split('-')[0]
     
            f = open(destination_path + '/' + id + '.' + resource['resourcetype'] + '.json', 'w')
            f.write(json.dumps(resource))
            f.close()
        return


# In[73]:


root_dir='../'
data_dir='../data'

input_data_folders = ['Patient']
input_data_dir = data_dir + '/fhir-json/9rows'

output_directory = root_dir + '/output/fhir-json-redis/9rows'

directory = MakeDirectory(output_directory)
directory.create_dir(input_data_folders)
    
files = FileIterator(input_data_dir, input_data_folders)
input_dirpaths = files.iterate_filenames()
input_dirpaths

data = []
files = ContentReader(input_dirpaths, output_directory)
data = files.get_data()

#result = MakeResult(data, input_dirpaths, output_directory)
#result.outputs()

#TODO OPTIMIZE array 
#TODO OPTIMIZE DYNAMIC FIELDS DDL GENERATOR

