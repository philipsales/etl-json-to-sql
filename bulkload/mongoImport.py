#!/usr/bin/env python
# coding: utf-8

# In[11]:
import sys
from os import path
from os import walk
import re
import pandas as pd
import json
import logging
import subprocess


# In[14]:
class FileIterator:

    def __init__(self, input_root, input_folders, max_item):
        self.input_data_dir = input_root
        self.input_folders = input_folders
        self.max_item = max_item 
        
    def iterate_filenames(self):
        resources = self.__iterate_dirfiles()
        files = self.__iterate_file(resources)
        return files
        
    def __iterate_dirfiles(self):
        path_files = []
        file_names = self.input_folders

        for item in file_names:
            path_files.append(input_data_dir + '/' + item)
        return path_files
    
    def __iterate_file(self, path_dbs):
        path_db_workload_files = []     
        for path_db in path_dbs:
            for root, dirs, files in walk(path_db):  
                index = 0;
                for filename in files:
                    print('remaining files: ', len(files)-index)

                    if index < self.max_item:
                        if not filename.endswith(('.json~', '.swp')):
                            print('valid file: ',filename)
                            path_db_workload_files.append(root + '/' + filename)
                            index += 1
                        if ''.join(dirs) != '.ipynb_checkpoints':
                            pass
                    else:
                        break
                    
        return path_db_workload_files



# In[15]:


class ContentReader():
    
    def __init__(self, filename_paths):
        self.filename_paths = filename_paths
        
    def get_data(self):
        data = []
        for filename_path in self.filename_paths:
            
            json = ReadJSON()
            data.append(json.read(filename_path))

        return data


# In[9]:


class ReadJSON():
    
    @staticmethod
    def read(file_path):
        with open(file_path) as f:
            d = json.load(f)
        return d


# In[121]:


class MongoImport():
    
    @staticmethod
    def insert_all(dir_paths):
        database = 'ycsb'
        index = 0
        result = ''

        for path in dir_paths:
            print('remaining files: ', len(dir_paths)-index)
            filename = path.split('/')[-1]
            collection = filename.split('.')[-2].lower()

            try:
                cmd = "mongoimport --db %s --collection %s --type json --file '%s'" % (database, collection, path)
                result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
                result.stdout
                index += 1
            except Exception as e:
                print(e)
                result = e

        return result



# In[120]:

root_dir='/root/etl-json-to-sql/'
data_dir='/root/data'

input_data_folders = ['Patient']
input_data_dir = data_dir + '/json/1M'
max_count = 1000000


files = FileIterator(input_data_dir, input_data_folders, max_count)
input_dirpaths = files.iterate_filenames()

result = MongoImport.insert_all(input_dirpaths)

