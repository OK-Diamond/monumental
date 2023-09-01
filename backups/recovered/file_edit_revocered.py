import shutil
import os

def _test_folder(location, location_is_file=True) -> None:
    '''
    Looks for a folder and creates it if it does not already exist.
    '''
    folder = location
    if location_is_file:
        if location.rfind("/") > -1:
            folder = location[0:location.rfind("/")]
    if not os.path.exists(folder): 
        os.makedirs(folder)
    return

def delete_contents(location: str, del_files: bool = True, del_folders: bool = True) -> None:
    '''
    Location must be a folder.\n
    Deletes all files and folders inside the specified folder, unless the optional parameters specify otherwise.
    '''
    for root, dirs, files in os.walk(location):
        if del_files:
            for f in files:
                os.unlink(os.path.join(root, f))
        if del_folders:
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
    return

def delete(location: str) -> None:
    '''
    Deletes a file or folder.
    '''
    if os.path.isfile(location):
        os.remove(location)
    elif os.path.isdir(location):
        shutil.rmtree(location)
    else:
        print(f"Error: {location} file/folder not found")

def copy(source: str, destination: str) -> None:
    '''
    Copies a file from source to destination.
    '''
    _test_folder(destination)
    shutil.copy(source, destination)
    return

def move(source: str, destination: str) -> None:
    '''
    Moves a file from source to destination.
    '''
    _test_folder(destination)
    shutil.move(source, destination)
    return

def read(location: str, codec = "", split = True) -> list[str]: # utf-8-sig
    '''
    Opens a file and reads the contents into a list of strings (or a single tring, if split is False). The file is then closed.\n
    codec can be used to change the encoding with which the file is read. Leave as "" for default.
    '''
    if codec == "":
        f = open(location, "r")
    else:
        f = open(location, "r", encoding = codec)
    data = f.read()
    if split:
        data = data.split("\n")
    f.close()
    return data

def write(location: str, data: str, codec = "") -> None: # cp1252
    '''
    Creates a file, or overwrites it if it already exists, and writes the data to it.\n
    codec can be used to change the encoding with which the file is read. Leave as "" for default.
    '''
    _test_folder(location)
    if codec == "":
        try:
            f = open(location, "x")
        except:
            f = open(location, "w")
    else:
        try:
            f = open(location, "x", encoding = codec)
        except:
            f = open(location, "w", encoding = codec)
    f.write(data)
    f.close()
    return

def append(location: str, data: str, codec = "") -> None:
    if codec == "":
        f = open(location, "a")
    else:
        f = open(location, "x", encoding = codec)
    f.write(data)
    f.close()
    return
