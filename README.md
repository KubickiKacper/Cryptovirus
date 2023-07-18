# Cryptovirus
For Educational Purposes Only!

This is coding part of my thesis called "Design and implementation of malware for security testing".

First stage of attack is using exe file of ransomware by victim. Virus connects with API to generate RSA keys, store them in database and get public key. Every pair of keys is generated separately for every attack.
Then malware creates AES key to encrypt every possible file in system. Time of encryption depends of number of files and their size.
If encryption completes, AES key will be encrypted by RSA key and stored in the directory created during attack containing list of encrypted files, RSA key and encrypted AES key.
Next step is ransom request:

![OknoInformujaceOAtaku](https://github.com/KubickiKacper/Cryptovirus/assets/82718318/053e65b2-faec-44fa-867d-2134b6ffb694)

If victim pay, he will have opportunity to decrypt his files, otherwise, decryption keys stored in database would be deleted in 72 hours by TTL mechanism of MongoDB.
After sending victim's BTC address of payment, he needs to use decryption button. Ransomware will get RSA private key, to decrypt AES key, and decrypt all files in PC.
All the files will be deleted, if decryption completes.
This is not end of attack yet.
Software will download keylogger from the server and store it in C:\ProgramData\Microsoft\Windows\StartMenu\Programs\StartUp directory, which files will be executed with every system start up.
Keylogger grather up to 50 chars and sends them to server and save to txt file called like IP of victim machine. 

VirusTotal test:
![RezultatTestu](https://github.com/KubickiKacper/Cryptovirus/assets/82718318/56351b0a-de46-4f41-a831-dcc30fa19bdc)
