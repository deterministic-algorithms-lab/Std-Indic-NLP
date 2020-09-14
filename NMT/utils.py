import os

#Joins all datai/ standard dataset folders in the directory
def joiner(directory, delete_old: bool) -> None :
    assert os.path.isdir(directory)