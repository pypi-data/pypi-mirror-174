from genericpath import exists
from re import U
import sys, os
import os.path
from os import path
from os.path import exists
import shutil
from exceptions import *
from config import *
from pathlib import Path


class AutomaticFolderCreation(object):
    # This variable is made globally as so it can be used by the creatingFolders function
    global variable_list
    variable_list =[]

    def __init__(self, full_dictionary):
        self.full_dictionary = full_dictionary
    
    # This function is used to store variable of the directory we will be sorting at, recieved from the determine_location.py module
    # Used and stored here and kept at runtime
    def variable_holder(self, variable):
        try:
            self.user_location=variable
            variable_list.append(self.user_location)
            print(variable_list)
        except Exception:
            print('---Something is not right ---')

    #This function creates the folder based on the mame given at self.full_dictionary 
    # it does so by doing some string manipulations
    def creatingFolders(self):
        here=variable_list[0]
        os.chdir(here)
        created_folders = []
        try:
            for ending in self.full_dictionary:
                
                folder_name = ending
                
                if '.' in folder_name:
                    
                    folder_name=folder_name.replace(".", "")
                    
                
                
                if ending == 'other':
                    self.MoveFoldersIntoFolders(folder_name)

                if exists(folder_name):
                    print(folder_name, " already exists, skipping")
                    self.MoveFilesIntofolder(folder_name)
                else:
                    os.mkdir(folder_name)
                    self.MoveFilesIntofolder(folder_name)
                    
                created_folders.append(folder_name)

        except Exception:
            print('couldnt create folder')
            
    # This function deals with moving of files into folders

    def MoveFilesIntofolder(self, foldername):
        self.foldername=foldername
        orig_name="."+self.foldername
        file_to_move_list=self.full_dictionary.get(orig_name)

        try:
            if file_to_move_list is  not None:
                for file in file_to_move_list:
                    if os.path.exists(foldername+"/"+file) == False:
                        shutil.move(file, foldername)
                        
                    else:
                        print(file, 'is already present in ', foldername)
            else:
                print("The list of files is a nonetype hence mostly, the extension has no \
                        extensions needing it at the moment")
        except Exception:
            print('file will not move')

    # This will move folders into folders, normally based on the other 
    
    
    def MoveFoldersIntoFolders(self, folder_name):
        try:    
            if os.path.exists('other')== False:
                os.mkdir('other')
            file_to_move_list=self.full_dictionary.get(folder_name)
            if file_to_move_list is not None:
                for file in file_to_move_list:
                    if os.path.exists(folder_name+"/"+file) == False:
                        shutil.move(file, "other")
                    else:
                        print(file, " already exists within", folder_name)
        except Exception:
            print('File did not move')