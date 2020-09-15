import os
from typing import List
from ..utils import append_file

def get_all_data(directory) -> List[str]:
    """
    Returns a list of all datai/ folders inside directory.
    """
    data_dirs = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory,f)) 
                                                     and (f.startswith('data') and len(f)!=4 and f[4:].isnumeric())]
    data_dirs.sort()
    return [os.path.join(directory, f) for f in data_dirs]

def get_all_files(directory):
    """
    Returns lists of paths and names all files in directory
    """
    names = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    paths = [os.path.join(directory,f) for f in names]
    return paths, names    

def make_std_fs(path):
    """
    Makes file structure for standard dataset, in the path directory; if it doesn't already exist.
    """
    assert os.path.split(path)[1].startswith('data'), '\"path\" must correspond to \"data/\" folder of standard file structure'

    if not os.path.isdir(path) :
        os.makedirs(path)
    mono_path = os.path.join(path, 'mono')
    para_path = os.path.join(path, 'para')
    if not os.path.idir(mono_path) :
        os.makedirs(mono_path)
    if not os.path.isdir(para_path) :
        os.makedirs(para_path)
     
def next_available(directory, append: bool=False):
    """
    Returns next available folder in the directory to store joining of data to.
    If append is true, then returns directory/data/, always
    """
    path = os.path.join(directory, 'data')
    if not os.path.isdir(path) or append :
        make_std_fs(path)
        return path
    i=0
    while(True) :
        path = os.path.join(directory,'data-join-'+str(i))
        if not os.path.isdir(path) :
            make_std_fs(path)
            return path
        i=i+1


def joiner(directory, std_folders_lis: List[str]=None, delete_old: bool=False) -> None:
    """
    Joins all data in datai/ or data/ standard dataset folders in the directory and stores in data/ folder.
    If std_folders_lis is provided, the folders in std_folders_lis are joined and put in directory/data/ or in directory/data-join-i/ .
    The files are appended to each other, in the order provided in std_folder_lis or in ascending order of i, for datai/. 
    """
    assert os.path.isdir(directory)
    
    #Setting source and target folders
    if std_folders_lis is None :
        std_folders_lis = get_all_data(directory)
        tgt_dir = next_available(directory, append=True)
    else :
        tgt_dir = next_available(directory)
    
    for src_path in std_folders_lis :
        
        src_file_paths, src_file_names = get_all_files(os.path.join(src_path, 'mono'))+get_all_files(os.path.join(src_path, 'para'))
        
        for src_file in src_file_paths :
            
            base, filename = os.path.split(src_file)
            base, mono_para = os.path.split(base)
            tgt_file = os.path.join(tgt_dir, mono_para, filename)
            append_file(src_file, tgt_file)    