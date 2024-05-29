# BTC-offline-ad
# Made by Alfonso Davila
# pip install bip_utils

import platform
import multiprocessing
import os
import sys
import time

from bip_utils import (
	Bip39WordsNum, Bip39Languages, Bip39MnemonicGenerator, Bip39MnemonicValidator, Bip39SeedGenerator,
	Bip44, Bip44Coins, Bip44Changes, Bip84, Bip84Coins, Bip32Slip10Secp256k1
)

import binascii

DATABASE = r'database/2_4_2023/'

def bip(num):
	mnemonic = Bip39MnemonicGenerator(Bip39Languages.ENGLISH).FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
	#print(mnemonic)
	return str(mnemonic)

def passw():
	return '123456'

def generate_address_X(bip, mnemonic, passphrase, lenght):
	if mnemonic :
		#print(mnemonic)
		seed_bytes = Bip39SeedGenerator(mnemonic).Generate(passphrase)
	else :
		seed_bytes = os.urandom(lenght)
	if bip == 84:
		bipXx_mst_ctx = Bip84.FromSeed(seed_bytes, Bip84Coins.BITCOIN)	
	else :
		# Derive the master BIP44 key from the seed bytes.
		bipXx_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
	# Derive account 0 for Bitcoin: m/44'/0'/0'.
	bip44_acc_ctx = bipXx_mst_ctx.Purpose().Coin().Account(0)
	# Derive the external chain: m/44'/0'/0'/0
	bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
	# Derive the first address of the external chain: m/44'/0'/0'/0/0
	bip44_addr_ctx = bip44_chg_ctx.AddressIndex(0)
	bip44_addr = bip44_addr_ctx.PublicKey().ToAddress()
	bip44_addr_priv = bip44_addr_ctx.PrivateKey().ToWif()
	#print(bip44_addr)
	return [bip44_addr, bip44_addr_priv]

def main(database, args):
	while True:
		mnemonic = bip(12)
		passph = passw()

		address_44 = generate_address_X(44, mnemonic, '', '')
		address_84 = generate_address_X(84, mnemonic, '', '')
		address_44_p = generate_address_X(44, mnemonic, passph, '')
		address_84_p = generate_address_X(84, mnemonic, passph, '')
		address_44_ = address_44[0]
		address_84_ = address_84[0]
		address_44_p_ = address_44_p[0]
		address_84_p_ = address_84_p[0]

		address_44_16 = generate_address_X(44, '', '', 16)
		address_84_16 = generate_address_X(84, '', '', 16)
		address_44_32 = generate_address_X(44, '', '', 32)
		address_84_32 = generate_address_X(84, '', '', 32)
		address_44_16_ = address_44_16[0]
		address_84_16_ = address_84_16[0]
		address_44_32_ = address_44_32[0]
		address_84_32_ = address_84_32[0]


		#print(address_44_)
		#print(address_84_)
		#print(address_44_p_)
		#print(address_84_p_)

		#print(address_44_16_)
		#print(address_84_16_)
		#print(address_44_32_)
		#print(address_84_32_)
		
		#address_84_ = '12QZ1csen8h26qevyAujtog5TZG35BSUUk'
		#print(mnemonic + '\n' + address_44_ + '\n' + address_84_)
		if args['verbose']:
			print(address_44_)
		if (address_44_[-args['substring']:] in database) or (address_84_[-args['substring']:] in database) or (address_44_p_[-args['substring']:] in database) or (address_84_p_[-args['substring']:] in database) or (address_44_16_[-args['substring']:] in database) or (address_84_16_[-args['substring']:] in database) or (address_44_32_[-args['substring']:] in database) or (address_84_32_[-args['substring']:] in database):
			for filename in os.listdir(DATABASE):
				with open(DATABASE + filename) as file:
					file_read = file.read()
					if (address_44_ in file_read) or (address_84_ in file_read) or (address_44_p_ in file_read) or (address_84_p_ in file_read) or (address_44_16_ in file_read) or (address_84_16_ in file_read) or (address_44_32_ in file_read) or (address_84_32_ in file_read):
						with open('found.txt', 'a') as plutus:
							#plutus.write('hex private key: ' + str(private_key) + '\n' +
							#             'WIF private key: ' + str(private_key_to_wif(private_key)) + '\n'
							#             'public key: ' + str(public_key) + '\n' +
							#             'uncompressed address: ' + str(address) + '\n\n')
							plutus.write('mnemonic:   '+str(mnemonic)+ '\n'+
								"address bip44: " + str(address_44[0]) + "\n" +
								"WIF private key: " + str(address_44[1]) + "\n" +
								"address bip84: " + str(address_84[0]) + "\n" +
								"WIF private key: " + str(address_84[1]) + "\n" +
								"passphrase: " + str(passph) + "\n" +
								"address bip44: " + str(address_44_p[0]) + "\n" +
								"WIF private key: " + str(address_44_p[1]) + "\n" +
								"address bip84 pass: " + str(address_84_p[0]) + "\n" +
								"WIF private key: " + str(address_84_p[1]) + 

								"16bit & 32bit: " + str(passph) + "\n" +
								"address bip44 16bit: " + str(address_44_16[0]) + "\n" +
								"WIF private key: " + str(address_44_16[1]) + "\n" +
								"address bip84 16bit: " + str(address_84_16[0]) + "\n" +
								"WIF private key: " + str(address_84_16[1]) + "\n" +
								"address bip44 32bit: " + str(address_44_32[0]) + "\n" +
								"WIF private key: " + str(address_44_32[1]) + "\n" +
								"address bip84 32bit: " + str(address_84_32[0]) + "\n" +
								"WIF private key: " + str(address_84_32[1]) + "\n" +

								"\n\n")                                 
							plutus.close()
						break

def print_help():
	print('''BTC-Offline 

Speed test: 
execute 'python3 btc-offline-ad.py time', the output will be the time it takes to bruteforce a single address in seconds


By default this program runs with parameters:
python3 btc-offline-ad.py verbose=0 substring=8

verbose: must be 0 or 1. If 1, then every bitcoin address that gets bruteforced will be printed to the terminal. This has the potential to slow the program down. An input of 0 will not print anything to the terminal and the bruteforcing will work silently. By default verbose is 0.

substring: to make the program memory efficient, the entire bitcoin address is not loaded from the database. Only the last <substring> characters are loaded. This significantly reduces the amount of RAM required to run the program. if you still get memory errors then try making this number smaller, by default it is set to 8. This opens us up to getting false positives (empty addresses mistaken as funded) with a probability of 1/(16^<substring>), however it does NOT leave us vulnerable to false negatives (funded addresses being mistaken as empty) so this is an acceptable compromise.

cpu_count: number of cores to run concurrently. More cores = more resource usage but faster bruteforcing. Omit this parameter to run with the maximum number of cores''')
	sys.exit(0)

def timer(args):
	start = time.time()
	mnemonic = bip(12)
	address_44 = generate_address_X(44, mnemonic, '', '')
	address_84 = generate_address_X(84, mnemonic, '', '')
	end = time.time()
	print(str(end - start))
	sys.exit(0)

if __name__ == '__main__':
	args = {
		'verbose': 0,
		'substring': 8,
		'fastecdsa': platform.system() in ['Linux', 'Darwin'],
		'cpu_count': multiprocessing.cpu_count(),
	}
	
	for arg in sys.argv[1:]:
		command = arg.split('=')[0]
		if command == 'help':
			print_help()
		elif command == 'time':
			timer(args)
		elif command == 'cpu_count':
			cpu_count = int(arg.split('=')[1])
			if cpu_count > 0 and cpu_count <= multiprocessing.cpu_count():
				args['cpu_count'] = cpu_count
			else:
				print('invalid input. cpu_count must be greater than 0 and less than or equal to ' + str(multiprocessing.cpu_count()))
				sys.exit(-1)
		elif command == 'verbose':
			verbose = arg.split('=')[1]
			if verbose in ['0', '1']:
				args['verbose'] = verbose
			else:
				print('invalid input. verbose must be 0(false) or 1(true)')
				sys.exit(-1)
		elif command == 'substring':
			substring = int(arg.split('=')[1])
			if substring > 0 and substring < 27:
				args['substring'] = substring
			else:
				print('invalid input. substring must be greater than 0 and less than 27')
				sys.exit(-1)
		else:
			print('invalid input: ' + command  + '\nrun `python3 btc-offline-ad.py help` for help')
			sys.exit(-1)
	
	print('reading database files...')
	database = set()
	for filename in os.listdir(DATABASE):
		with open(DATABASE + filename) as file:
			for address in file:
				address = address.strip()
				database.add(address[-args['substring']:])
	print('DONE')

	print('database size: ' + str(len(database)))
	print('processes spawned: ' + str(args['cpu_count']))
	
	for cpu in range(8): # args['cpu_count']
		multiprocessing.Process(target = main, args = (database, args)).start()
