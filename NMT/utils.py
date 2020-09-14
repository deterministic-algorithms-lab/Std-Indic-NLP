import os

def joiner(directory, delete_old: bool) -> None :
    '''
    Joins all datai/ standard dataset folders in the directory
    '''
    assert os.path.isdir(directory)