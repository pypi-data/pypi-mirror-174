from operator import index
import os
import default_folders

class TypeOfFile:
    ''' this module determins the type of file and puts it into a dictionary'''
    
    def __init__(self, list_of_file_ending, list_of_folders):
        self.file_ending=list_of_file_ending
        self.list_of_folders=list_of_folders
    
    def determine_file_extension(self):
        global extensionandfile
        global extensiondictionary
        extensionandfile = {'other'}

        extensiondictionary={}
        #This for loop is used to determine whether the variables have 1 fullstop 
        # if not then it will go into the complex_file-ending function for further analysis
        try:
            for file in self.file_ending: 
                if '.' in file  and file.count('.')<=1:
                    point=file.index('.')
                    extensionandfile.add(file[point:])
                    #print(extensionandfile)
                else:

                    print(file, 'has a complex extension possible due to mutiple fullstops')
                    self.complex_file_endings(file)
                    
            # This part seperate what is a folder and what is a file by the file extension and 
            # adds it to a list table of some sort
            # there may be a situation where theres is a file with no file extension 
            temp_list = []
            folder_list =[]
            for ending in extensionandfile:
                for file in self.file_ending:
                    if ending in file:
                        temp_list.append(file)
                    
                    if os.path.isdir(file):
                        folder_list.append(file)
                    else:
                        print(file, 'its not directory')


                extensiondictionary[ending]=temp_list.copy()
                extensiondictionary['other']=self.list_of_folders.copy()
                temp_list.clear()
                folder_list.clear()
            print(extensionandfile)
            
            
            default_folders.AutomaticFolderCreation(extensiondictionary).creatingFolders()
            
        except Exception:
            print('---Something does appear right---')

    # This function sorts out any file with multiple fullstops in folder
    def complex_file_endings(self, filename):
        
        self.filename_list = list(filename)
        
        
        try:
            for i in self.filename_list:
                
                if i == "." and self.filename_list.count(".")>1:
                    
                    self.filename_list.remove(i)
                    
                
                if i=="." and self.filename_list.count(".")==1:
                    indexof=self.filename_list.index(i)
                    res = self.filename_list[indexof:]
                    
                    #this stage takes thename of the file with only one fullstop in it and tries to 
                    # make list and then concatenate them together and then add it to the 
                    # extensionandfile which is what is used later to determine how to move files
                    
                    n=""
                    if res:
                        for i in res:
                            n+=""+i

                    extensionandfile.add(n)
                    break
        except Exception:
            print('---Something is not write ---')
         