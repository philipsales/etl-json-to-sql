
# coding: utf-8

# In[11]:


import sys
import os
from os import path, walk
#from os import path
#from os import walk

import re
import json
from collections import OrderedDict


# ## Flatten

# In[4]:


def flattenDict(d, result=None):
    
    if result is None:
        result = {}
        
    for key, value in list(d.items()):
        value = d[key]
        
        #TODO: OPtimiza strip clean
        if isinstance(value, str):
            value = value.replace("'", ' ')
            
        if isinstance(value, dict):
            value1 = {}
            for keyIn in value:
                value1[".".join([key,keyIn])]=value[keyIn.lower()]
            flattenDict(value1, result)
        elif isinstance(value, (list, tuple)):  
            for indexB, element in enumerate(value):
                if isinstance(element, dict):
                    value1 = {}
                    index = 0
                    for keyIn in element:
                        newkey = ".".join([key,keyIn])        
                        value1[".".join([key,keyIn])]=value[indexB][keyIn]
                        index += 1
                    for keyA in value1:
                        flattenDict(value1, result)   
        else: 
            result[key.lower()]=value

    return OrderedDict(sorted(result.items()))


# In[6]:


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

# In[13]:


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
                        path_db_workload_files.append(root + '/' + filename)
                        index+=1
                    if ''.join(dirs) != '.ipynb_checkpoints':
                        pass

        return path_db_workload_files


# ## Filecontent reader

# In[15]:


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

            resource_id = resource['id']
             
            f = open(destination_path + '/' + resource_id + '.' + resource['resourcetype'] + '.json', 'w')
            f.write(json.dumps(resource))
            print('writing: ', resource_id)
            f.close()
            index += 1

        return data


# ## File Open

# In[24]:


class ReadJSON():
    
    @staticmethod
    def read(file_path):
        new_patient_id = ''
        
        with open(file_path) as f:
            d = json.load(f)
            
            flat_d = flattenDict(d)
            
            #TODO: Create separate Fx
            if flat_d['resourcetype'] != 'Patient':
                new_patient_id = flat_d['subject.reference'].split(sep="/")[-1]
                flat_d.pop('subject.reference', None)
                flat_d['patientid'] = new_patient_id
            
        return flat_d


# In[25]:


root_dir='../'
data_dir='../data'

input_data_folders = ['Patient','Condition','DiagnosticReport']
input_data_dir = data_dir + '/fhir-json/9rows'

output_directory = root_dir + '/output/fhir-json-cassandra/9rows'

directory = MakeDirectory(output_directory)
directory.create_dir(input_data_folders)
    
files = FileIterator(input_data_dir, input_data_folders)
input_dirpaths = files.iterate_filenames()
input_dirpaths

data = []
files = ContentReader(input_dirpaths, output_directory)
data = files.get_data()

#TODO OPTIMIZE array 
#TODO OPTIMIZE DYNAMIC FIELDS DDL GENERATOR

