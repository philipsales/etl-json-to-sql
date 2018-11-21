#!/usr/bin/env python
# coding: utf-8

# In[10]:


import sys
import os
from os import path
from os import walk

import re

import pandas as pd
import json
import logging
from pandas.io.json import json_normalize 
import subprocess



# ## Flatten

# In[3]:


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
            
    
    return result


# In[4]:


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

# In[58]:


class FileIterator:
    
    def __init__(self, input_root, input_folders, max_count):
        self.input_data_dir = input_root
        self.input_folders = input_folders
        self.max_item = max_count
        
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
                    
                    if index <= self.max_item:
                        counter = 'remaining files %i out of %i' % ( ((self.max_item) - index), (self.max_item) )
                        print(counter)
                        if not filename.endswith(('.json~', '.swp', '-checkpoint.json')):
                            print('valid file: ',filename)
                            path_db_workload_files.append(root + '/' + filename)
                            index+=1
                        if ''.join(dirs) != '.ipynb_checkpoints':
                            pass
                    else:
                        break


        return path_db_workload_files


# ## Filecontent reader

# In[14]:


class ContentReaderJSON():
    
    def __init__(self, filename_paths):
        self.filename_paths = filename_paths
        
    def get_data(self):
        data = []
        for filename_path in self.filename_paths:
            
            json = ReadJSON()
            data.append(json.read(filename_path))

        return data


# In[75]:


class ContentReader():
    
    def __init__(self, filename_paths,  destination_path):
        self.filename_paths = filename_paths
        self.destination_path = destination_path
        
    def get_data(self):
        data = []
        index = 0
        for filename_path in self.filename_paths:
            counter = 'remaining files %i out of %i' % ( (len(self.filename_paths) - index), len(self.filename_paths) )
            print(counter)
            print('filename: ', filename_path)

            '''
            cmd = "cp %s %s" % (filename_path, self.destination_path)
            result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
            result.stdout
            print(cmd)
            index += 1

            
            '''
            read_json = ReadJSON()
            #resource = read_json.read(filename_path)
            resource = read_json.read(filename_path, self.destination_path)
            '''
            
            destination_path = '%s/%s' % (self.destination_path, resource['resourcetype'] )

            resource_id = resource['id'].split('-')[0]
            
            f = open(destination_path + '/' + resource_id + '.' + resource['resourcetype'] + '.json', 'w')
            f.write(json.dumps(resource))
            print('writing: ',resource['id'])
            f.close()
            '''
            index += 1
            
            #data.append(read_json.read(filename_path))
            

        return data


# ## File Open

# In[7]:


class ReadJSON():
    
    @staticmethod
    def read(file_path, destination_dir):
        resource = ''

        with open(file_path) as f:
            try:
                resource = json.load(f)

            except ValueError as e: 
                print('INVALIDE JSON') 

            destination_path = '%s/%s' % (destination_dir, resource['resourceType'] )

            #resource_id = resource['id'].split('-')[0]
            resource_id = resource['id']
            
            flatten_resource = flattenDict(resource)
            json_resource = json.dumps(flatten_resource)

            f = open(destination_path + '/' + resource_id + '.' + resource['resourceType'] + '.json', 'w')

            try:
                f.write(json_resource)
                #f.write(json.dumps(resource))
                print('writing: ',resource['id'])
            except TypeError:
                print("Unable to serialize the object")

            f.close()

        #return flattenDict(d)
        return resource 

class ReadJSONORIG():
    
    @staticmethod
    def read(file_path):
        with open(file_path) as f:
            d = json.load(f)
        #return flattenDict(d)
        return d


# ## Print Flatten FHIR JSON

# In[19]:


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


# In[ ]:


class MakeResult():

    @staticmethod
    def outputs(self):      
        for resource in self.data:
           
            destination_path = self.destination_path + '/' + resource['resourcetype']
            #print('destination: ' ,destination_path)
            id = resource['id'].split('-')[0]
     
            f = open(destination_path + '/' + id + '.' + resource['resourcetype'] + '.json', 'w')
            f.write(json.dumps(resource))
            f.flush()
            f.close()
        return


# In[76]:


root_dir='/root/etl-json-to-sql/'
data_dir='/root/data'

input_data_folders = ['Patient']
input_data_dir = data_dir + '/json/1M'

output_directory = data_dir + '/json-cassandra/1M'
max_count = 1000000 

directory = MakeDirectory(output_directory)
directory.create_dir(input_data_folders)
    
files = FileIterator(input_data_dir, input_data_folders, max_count)
input_dirpaths = files.iterate_filenames()

data = []
files = ContentReader(input_dirpaths, output_directory)
data = files.get_data()

#result = MakeResult(data, input_dirpaths, output_directory)
#result.outputs()

#TODO OPTIMIZE array 
#TODO OPTIMIZE DYNAMIC FIELDS DDL GENERATOR

