
# coding: utf-8

# In[2]:


import sys
from os import path
from os import walk
import re
import pandas as pd
import json
import logging
import subprocess


# In[3]:


#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

#logging.basicConfig
fh = logging.FileHandler('logs_cassandra_dump.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

'''
#For streaming only
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
'''

logger.info('This is a test log message.')


# In[4]:


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
                    
                    if index < self.max_item:
                        
                        if not filename.endswith(('.json~', '.swp', '-checkpoint.json')):
                            print('valid file: ',filename)
                            path_db_workload_files.append(root + '/' + filename)
                            index+=1
                            
                        if ''.join(dirs) != '.ipynb_checkpoints':
                            pass
                    else:
                        break

        
        return path_db_workload_files


# In[5]:


class ContentReaderJSON():
    
    def __init__(self, filename_paths):
        self.filename_paths = filename_paths
        
    def get_data(self):
        data = []
        for filename_path in self.filename_paths:
            
            json = ReadJSON()
            #data.append(json.read(filename_path))

        return data


# In[6]:


class ContentReader():
    
    def __init__(self, filename_paths):
        self.filename_paths = filename_paths
        
    def get_data(self):
        data = []
        tmp = ''
        index = 0
        
        for filename_path in self.filename_paths:
            
            read_json = ReadJSON()
            data = read_json.read(filename_path)
            database = 'ycsb'
            table = 'patient'
            
            print('remaining files: ', len(self.filename_paths)-index)
            
            try:
                cmd = '''cqlsh localhost 9042 -e 'INSERT INTO %s.%s JSON '"'"'%s'"'"';' ''' % (database, table, json.dumps(data))
                result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode != 0:
                    print("error item:  ", data['id'])
                    print("error code: ", result.stderr)
                    print(cmd)
                else:
                    print("inserting:  ", data['id'])
                    result.stdout
                    index += 1
                   
            except Exception as e:
                print(e)
                result = e
        return result
            #data.append(json.read(filename_path))

        return data


# In[7]:


class ReadJSON():
    
    @staticmethod
    def read(file_path):
        with open(file_path) as f:
            d = json.load(f)
        return d


# In[8]:


class CassandraImport():
    
    @staticmethod
    def insert_all(data):
        database = 'ycsb'

        index = 0

        for item in data:
            
            print('remaining files: ', len(data)-index)
            
            try:

                cmd = '''cqlsh localhost 9042 -e 'INSERT INTO ycsb.patient JSON '"'"'%s'"'"';' ''' % json.dumps(item)
                result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode != 0:
                    print("error item:  ", item['id'])
                    print("error code: ", result.stderr)
                    print(cmd)
                else:
                    print("inserting:  ", item['id'])
                    result.stdout
                    index += 1
                   
            except Exception as e:
                print(e)
                result = e
        return result


# In[11]:


root_dir = '../'

input_data_folders = ['Patient']
input_data_dir = root_dir + 'output/fhir-json-cassandra/9rows'
max_count = 100

files = FileIterator(input_data_dir, input_data_folders, max_count)
input_dirpaths = files.iterate_filenames()

data = []
files = ContentReader(input_dirpaths)
data = files.get_data()

#result = CassandraImport.insert_all(data)

