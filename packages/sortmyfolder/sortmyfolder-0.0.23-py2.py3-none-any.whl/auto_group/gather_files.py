from importlib.metadata import files
import os
import type_of_file
from exceptions import *

class ListingGivenDirectory(object):
    #This module recieves the path so it can change directory into it and work from there
    def __init__(self, path):
        self.path = path
        self.list_of_folders=[]
    #This function takes the list of folders int the directory and converts it into list
    def files_in_path(self):
        try:

            os.chdir(self.path)
            files_found = os.listdir(self.path) 
            print('the files found and to be manipulated are', files_found)
            for files in files_found:
                if os.path.isdir(files) and "." not in files:
                    self.list_of_folders.append(files)

                else:
                    pass
            list_files_found=files_found
            #Sends information containing files found and folders to type_of_file 
            # module 
            a=type_of_file
            b=a.TypeOfFile(list_files_found, self.list_of_folders)
            b.determine_file_extension()

        except Exception:
            print('nothing in selected path')
        