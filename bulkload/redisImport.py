#!/usr/bin/env python
# coding: utf-8

# In[158]:
import sys
from os import path
from os import walk
import re
import pandas as pd
import json
import logging
import redis


# In[160]:
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
                index = 0
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


# In[104]:


class ContentReader():
    
    def __init__(self, filename_paths):
        self.filename_paths = filename_paths
        
    def get_data(self):
        data = []
        tmp = ''
        index=0

        pool = redis.ConnectionPool(host='0.0.0.0', port=6379, db=0)
        r = redis.Redis(connection_pool=pool)


        for filename_path in self.filename_paths:
            counter = 'remaining files %i out of %i' % ( (len(self.filename_paths) - index), (len(self.filename_paths)) )
            print(counter)
            index += 1

            read_json = ReadJSON()
            data = read_json.read(filename_path)
            key = data['resourceType'] + ':' + data['id']
            print(key)


            try:
                result = json.loads(r.execute_command('JSON.SET', key, '.', json.dumps(data)))
                print(result)
            except Exception as e:
                print(e)
                result = e



# In[103]:


class ReadJSON():
    
    @staticmethod
    def read(file_path):
        with open(file_path) as f:
            d = json.load(f)
        return d 


# In[162]:


class RedisImport():
    
    @staticmethod
    def insert_all(data):
        index=0
        result = ''

        pool = redis.ConnectionPool(host='0.0.0.0', port=6379, db=0)
        r = redis.Redis(connection_pool=pool)

        key = data['resourceType'] + ':' + data['id']
        print(key)

        try:
            result = json.loads(r.execute_command('JSON.SET', key, '.', json.dumps(data)))
            print('Result: ',result)
        except Exception as e:
            print('Exception error:', e)
            result = e

        return result


# In[163]:

root_dir='/root/etl-json-to-sql/'
data_dir='/root/data'

input_data_folders = ['Patient']
input_data_dir = data_dir + '/json/1M'
max_count = 100000

files = FileIterator(input_data_dir, input_data_folders, max_count)
input_dirpaths = files.iterate_filenames()

files = ContentReader(input_dirpaths)
files.get_data()



# In[ ]:




