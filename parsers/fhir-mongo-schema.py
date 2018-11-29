
# coding: utf-8

# In[1]:


import sys
import os
from os import path
from os import walk

import re
import json


# ## Flatten

# In[2]:


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

# In[3]:


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

# In[4]:


class ContentReader():
    
    def __init__(self, filename_paths,  destination_path):
        self.filename_paths = filename_paths
        self.destination_path = destination_path
        
    def get_data(self):
        data = []
        index = 0
        for filename_path in self.filename_paths:
            
            print('remaining files: ', len(self.filename_paths) - index)
            
            resource = ReadJSON().read(filename_path)
            
            destination_path = '%s/%s' % (self.destination_path, resource['resourceType'] )

            resource_id = resource['id'].split('-')[0]
            
            if resource['resourceType'] != 'Patient':
                patient_id = resource['subject']['reference']
                resource['patientId'] = patient_id.split(sep="/")[-1]
            
            f = open(destination_path + '/' + resource_id + '.' + resource['resourceType'] + '.json', 'w')
            f.write(json.dumps(resource))
            print('writing: ', resource_id)
            f.close()
            index += 1

        return data


# ## File Open

# In[5]:


class ReadJSON():
    
    @staticmethod
    def read(file_path):
        with open(file_path) as f:
            d = json.load(f)
        return d


# ## Print Flatten FHIR JSON

# In[6]:


root_dir='../'
data_dir='../data'

input_data_dir = data_dir + '/fhir-json/9rows'
input_data_folders = ['DiagnosticReport','Patient','Condition']


output_directory = root_dir + 'output/fhir-json-mongodb/9rows'

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

