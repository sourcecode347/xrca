# Python 3 XRCA Coded By Baz(AKA SourceCode347)
# Author : SourceCode347
# Website : sourcecode347.com
# http://patorjk.com/software/taag/#p=display&h=3&v=3&f=Epic&t=X%20RCA
# Requirements
# pip install pycryptodome
# pip install termcolor
# pip install colorama
logo='''
            _______ _______ _______ 
|\     /|  (  ____ (  ____ (  ___  )
( \   / )  | (    )| (    \| (   ) |
 \ (_) /   | (____)| |     | (___) |
  ) _ (    |     __| |     |  ___  |
 / ( ) \   | (\ (  | |     | (   ) |
( /   \ )  | ) \ \_| (____/| )   ( |
|/     \|  |/   \__(_______|/     \|
                                                                        
Coded By Baz'''
from termcolor import colored
import time,datetime,codecs
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import colorama
colorama.init()
while True:
	print (colored(logo,"blue"))
	print()
	print (colored("Exit                     : 0","green",attrs=['bold']))
	print (colored("Generate Keys            : 1","green",attrs=['bold']))
	print (colored("Encrypt - Decrypt (text) : 2","green",attrs=['bold']))
	print()
	#choice=input(colored("Enter Your Choice : ","blue",attrs=['bold']))
	choice=input("Enter Your Choice : ")
	if choice=="0":
		break
	if choice=="1":
		#pname=str(input(colored("Enter Public Key file name (ex. public.pem) : ","blue",attrs=['bold'])))
		pname=str(input("Enter Public Key file name (ex. public.pem) : "))
		key = RSA.generate(8192)
		f = open(pname, 'wb')
		f.write(key.publickey().exportKey('PEM'))
		f.close()
		tnow =	datetime.datetime.now()
		current_time =	tnow.strftime("%H:%M:%S")
		print("["+colored(current_time,"blue")+"] "+colored("Public Key Generated As : ","grey",attrs=['bold'])+pname)
		#prname=str(input(colored("Enter Private Key file name (ex. private.pem) : ","blue",attrs=['bold'])))
		prname=str(input("Enter Private Key file name (ex. private.pem) : "))
		f = open(prname, 'wb')
		f.write(key.exportKey('PEM'))
		f.close()
		tnow =	datetime.datetime.now()
		current_time =	tnow.strftime("%H:%M:%S")
		print("["+colored(current_time,"blue")+"] "+colored("Private Key Generated As : ","grey",attrs=['bold'])+prname)
	if choice=="2":
		while True:
			print()
			print (colored("Back    : 0","green",attrs=['bold']))
			print (colored("Encrypt : 1","green",attrs=['bold']))
			print (colored("Decrypt : 2","green",attrs=['bold']))
			print()
			#xchoice=input(colored("Enter Your Choice : ","blue",attrs=['bold']))
			xchoice=input("Enter Your Choice : ")
			if xchoice=="0":
				break
			if xchoice=="1":
				#pname=str(input(colored("Enter file path of Public Key (ex. public.pem) : ","blue",attrs=['bold'])))
				pname=str(input("Enter file path of Public Key (ex. public.pem) : "))
				file_out=open("encrypted_data.bin", "wb")
				f = open(pname, 'rb')
				key = RSA.importKey(f.read())
				session_key = get_random_bytes(16)
				xmessage=str(input("Type Your Message : "))
				cipher_rsa = PKCS1_OAEP.new(key)
				enc_session_key = cipher_rsa.encrypt(session_key)
				# Encrypt the data with the AES session key
				cipher_aes = AES.new(session_key, AES.MODE_EAX)
				ciphertext, tag = cipher_aes.encrypt_and_digest(xmessage.encode())
				[ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]
				file_out.close()
				enx=""
				print(colored("#"*80,"blue"))
				file_in = str(open("encrypted_data.bin", "rb").read())
				print(file_in[2:-1])
				print(colored("#"*80,"blue"))
			if xchoice=="2":
				#xmessage=(input(colored("Enter Encrypted Message : ","blue",attrs=['bold'])))
				xmessage=(input("Enter Encrypted Message : "))
				#xmessage=xmessage.replace("(b'","").replace("',)","")
				#print(codecs.encode(xmessage.encode().decode('unicode_escape'),"raw_unicode_escape"))
				xmessage=codecs.encode(xmessage.encode().decode('unicode_escape'),"raw_unicode_escape")
				#prname=str(input(colored("Enter file path of Private Key (ex. private.pem) : ","blue",attrs=['bold'])))
				file_in=open("decrypted_data.bin", "wb")
				file_in.write(xmessage)
				file_in.close()
				file_in = open("decrypted_data.bin", "rb")
				prname=str(input("Enter file path of Private Key (ex. private.pem) : "))
				f1 = open(prname, 'rb')
				key1 = RSA.importKey(f1.read())
				enc_session_key, nonce, tag, ciphertext = \
					[ file_in.read(x) for x in (key1.size_in_bytes(), 16, 16, -1) ]
				cipher_rsa = PKCS1_OAEP.new(key1)
				session_key = cipher_rsa.decrypt(enc_session_key)
				cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
				data = cipher_aes.decrypt_and_verify(ciphertext, tag)
				print(colored("#"*80,"blue"))
				print(data.decode("utf-8"))
				print(colored("#"*80,"blue"))
