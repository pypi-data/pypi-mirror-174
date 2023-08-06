import sys, getopt
from os import execv, path
from tabnanny import check
from exceptions import *
import gather_files
import default_folders


class WhereToSortFiles(object):
    
    def location_of_folder_creation(self,  location):
        user_location=location[0]
        #Simple input questions for user to answer
        location_question = input('do you want to organise folders in your current location, which is {}: yes or no:--> ' .format(user_location))
        try:
            if location_question.lower() == 'no':
                while True:
                    try:
                        user_location = input('where do you want the files saved? eg /Users/ :--> ')
                        if not path.exists(user_location):
                            print('the path you entered does not exist')

                            raise PathDoesNotExist
                        else:
                            user_location=user_location
                            something ={"test_variable":"ValueHere"}

                            #Sends the location/directory of where sorting will occur to the defualt_folders.py module to be stored there and used
                            #Runtime and to be kept there-




                            default_folders.AutomaticFolderCreation(something).variable_holder(user_location)

                            #Sends information to the gather_files.py module where it will determine what type of files are stationed in direction
                            f = gather_files
                            b=f.ListingGivenDirectory(user_location)
                            b.files_in_path()
                            break
                    except Exception:
                        print('the specifid path does not exit')

            elif location_question.lower() == 'yes':
                #determining what location file is at
                print('the user_location is', user_location)
                check_user_location = path.exists(user_location)
                if check_user_location:
                    print(check_user_location)
                    #For some strange reason it requires the use of a dictionary as an argument... investigate why?
                    something ={"test_variable":"ValueHere"}
                    default_folders.AutomaticFolderCreation(something).variable_holder(user_location)
                    f = gather_files
                    b=f.ListingGivenDirectory(user_location)
                    b.files_in_path()


            else:
                print('Your answer was neither yes or no :(')
            something ={"test_variable":"ValueHere"}
            default_folders.AutomaticFolderCreation(something).variable_holder(user_location)
        except Exception:
            print('---something is not right ---')
        

# a.location_of_folder_creation("/Users/emmanuelagyapong/Documents/tests_files")


# def main(cli_argument):
#     print(cli_argument)
#     WhereToSortFiles().location_of_folder_creation(cli_argument)

def main():
    print('Emmanuel it works here')
    
if __name__ == '__main__':
   #main(sys.argv[1:])
   main()
   
  
   

