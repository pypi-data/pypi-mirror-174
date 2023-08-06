class Error(Exception):
    '''This is the base class for the exception'''
    pass

class PathDoesNotExist(Error):
    '''The path they have inputted does not exist'''
    pass 


class   NotAFolder(Error):
    '''Specified folder is not a folder'''
    pass

class IndexIsOutOfBound(Error):   
    '''There is not enough index in the list'''
    pass

class FileWillNotMove(Error):
    '''File will not move for whatever reason'''
    pass
class VariableDoesNotExit(Error):
    '''variable not found'''
    pass

class CouldNotCreateFolder(Error):
    '''couldnt create folder'''
    pass

class FolderWillNotMove(Error):
    '''Folder will not move'''
    pass

class NothingInPathSelected(Error):
    '''from the selected path, there doesnt appear to be anything'''
    pass

