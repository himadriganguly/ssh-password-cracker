# Dictionary Based SSH Password Cracker In Python

This application is developed just for learning and educational purpose only.

*Note:- Don't use it for any illegal purpose.


## Requirements

1. Python3

2. python-nmap package [**https://pypi.python.org/pypi/python-nmap**](https://pypi.python.org/pypi/python-nmap)

3. pexpect [**https://pypi.python.org/pypi/pexpect/**](https://pypi.python.org/pypi/pexpect/)

4. Nmap to be installed on system


## Usage

	python sshDictionaryAttack.py -h
	
	usage: SSH Dictionary Based Attack [-h] host user passwordFile

	positional arguments:
  		host          Host IP address for the SSH server
  		user          Username for the SSH connection
  		passwordFile  Password file to be used as the dictionary

		optional arguments:
  			-h, --help    show this help message and exit

To get the help menu

	python sshDictionaryAttack.py 127.0.0.1 testuser password_file.txt

It will first check if the `SSH port 22` is open using `Nmap` and if it is open then it will try to enter into `SSH terminal` using the `username` provide and with all the combination of `password` from the `password file`.


## Contribute

If you have any idea you want to implement or think that there is a better way to implement any part of the code please create a fork and I will do my best to merge appropriately. Thank you.

Hope you will like the application.
