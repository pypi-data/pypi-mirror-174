from functools import wraps
import os
import glob
import shutil
import time
import re

from exceptions import *


def isDir(dirAddr):
    return not isFile(dirAddr)

def isFile(fileAddr):
    val = fileAddr.strip()
    last = os.path.basename(os.path.normpath(val))
    return "." in last[-4:]

def fileExists(fileAddr):
    if not isFile(fileAddr): raise InvalidFile("This is not a valid file address!")
    return os.path.isfile(fileAddr)

def dirExists(dirAddr):
    if not isDir(dirAddr): raise InvalidDir("This is not a valid dir address!")
    return os.path.isdir(dirAddr)

def getFileExtenssion(fileAddr):
    val = fileAddr.strip()
    last = os.path.basename(os.path.normpath(val))
    if not "." in last[-4:]: raise InvalidFile("This is not a valid file address!")

    return last.split(".")[-1]

def createDir(folder,replace=False):
    if not isDir(folder): raise InvalidDir("this is not a valid dir address!")

    if not dirExists(folder):
        os.mkdir(folder)
    else:
        if replace:
            os.remove(folder)
            os.mkdir(folder)
  

def moveFiles(pattern, folder):
    if not isDir(folder):     raise InvalidDir("this is not a valid dir address!")
    if not dirExists(folder): raise InvalidDir("folder not found!")

    files = glob.glob(pattern)
    for f in files:
        fnm = os.path.basename(f)
        # shutil.copy(f, DIR +  fr'\{folder}.xls')
        shutil.copy(f,f"{folder}/{fnm}")
        os.remove(f)

def clearDir(folder):
    if not isDir(folder):     raise InvalidDir("this is not a valid dir address!")
    if not dirExists(folder): raise InvalidDir("folder not found!")

    files = glob.glob(folder + "\*.*")
    for f in files:
        os.remove(f)

def waitFileFromChrome(pattern,dirr=None,timeout=0):
    start = time.time()
    dirr =  dirr if dirr else fr'c:\Users\{os.getlogin()}\downloads'
    
    while not glob.glob(f"{dirr}\{pattern}"):
        if timeout and time.time() - start > timeout: raise("Timeout downloading the file")
    
    time.sleep(0.5)

    while glob.glob(dirr + "\*.crdownload"):
        time.sleep(0.5)
        if timeout and time.time() - start > timeout: raise("Timeout downloading the file")
    
    list_of_files = glob.glob(f"{dirr}\{pattern}") # * means all if need specific format then *.csv
    return max(list_of_files, key=os.path.getctime)

def renameFile(fl,newName):
    if not isFile(fl):      raise InvalidDir("this is not a valid file address!")
    if not fileExists(fl):  raise InvalidDir("file not found!")

    path = os.path.dirname(os.path.abspath(fl))
    os.rename(fl,f"{path}\{newName}")
    return f"{path}\{newName}"

add1 = "c:/mydir"
add2 = "c:/mydir/myfile.ext"

print(isDir(add1))
print(isDir(add2))

True
False

