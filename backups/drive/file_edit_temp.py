from shutil import copy as shutil_copy
from shutil import move as shutil_move
from os import path, makedirs

def _test_folder(location, location_is_file=True) -> None:
    print("_test_folder location", location)
    folder = location
    if location_is_file:
        print(1, location.rfind("\\"))
        if location.rfind("\\") > -1:
            print(3)
            folder = location[0:location.rfind("\\")]
        elif location.rfind("/") > -1:
            print(4)
            folder = location[0:location.rfind("/")]
    else:
        print(2)
    print("folder", folder)
    if not path.exists(folder): 
        makedirs(folder)

def copy(source: str, destination: str) -> None:
    """
    Copies a file from source to destination.
    """
    _test_folder(destination)
    shutil_copy(source, destination)
    return

def move(source: str, destination: str) -> None:
    """
    Moves a file from source to destination.
    """
    _test_folder(destination)
    shutil_move(source, destination)
    return

def read(location: str, codec = "", split = True) -> list[str]: # utf-8-sig
    """
    Opens a file and reads the contents into a list of strings (or a single tring, if split is False). The file is then closed.
    
    codec can be used to change the encoding with which the file is read. Leave as "" for default.
    """
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
    """
    Creates a file, or overwrites it if it already exists, and writes the data to it.
    
    codec can be used to change the encoding with which the file is read. Leave as "" for default.
    """
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
