# this module make paths for store and retrieve documents

import os

def make_store_path(parameter_1,parameter2):
    # in construction
    return path_store

def make_rpath_documents(path_db):  # path to fisic db
    ''' Make paths to each file for each announcement in each country
        and transfor these files from pdf to txt.
    '''

    for root, dirs, files in os.walk(path_db):

        for _root, _dirs, _files in os.walk(root):
            if files:
                for _file in _files
                    # join _root with _file and transform pdf to txt!
                    # print somet flag...
        
        return 'work done for %s country ' % dirs