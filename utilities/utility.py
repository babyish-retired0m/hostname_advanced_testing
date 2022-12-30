#!/usr/bin/env python3
__version__ = "2.2"
#2.2 def border_msg()

class Clr:
    """Text colors."""
    RST = '\033[39m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    VIOLET = '\033[34m'
    PINK = '\033[35m'
    BLUE = '\033[36m'
    GREY = '\033[37m'
    BLACK2 = '\033[40m'
    RST2 = '\033[49m'
    RED2 = '\033[41m'
    GREEN2 = '\033[42m'
    YELLOW2 = '\033[43m'
    VIOLET2 = '\033[44m'
    PINK2 = '\033[45m'
    BLUE2 = '\033[46m'
    GREY2 = '\033[47m'


def get_pcname(print_result = False):
	from os import environ
	from platform import node
	from socket import gethostname
	n1 = node()
	n2 = gethostname()
	n3 = environ.get("COMPUTERNAME")
	if n1 == n2 == n3:
		pcname = n1
	elif n1 == n2:
		pcname = n1
	elif n1 == n3:
		pcname = n1
	elif n2 == n3:
		pcname = n2
	else:
		pcname = n1
		if print_result: print("Computernames are not equal to each other")
		#raise Exception("Computernames are not equal to each other")
	if pcname.endswith('.local'): return pcname[:pcname.find('.local')]
	else: return pcname


def get_username(print_result = False):
	from os import getlogin
	from getpass import getuser
	#n1=getlogin()
	n1 = '{}'.format(lambda: pwd.getpwuid(os.getuid())[0])
	n2=getuser()
	if n1 == n2: user = n1
	elif n2 == 'root': user = n1
	else: 
		if print_result: print("Username are not equal to each other")
		#raise Exception("Username are not equal to each other")
		user = n2
	return user


def get_currentdirectory():
	from os import getcwd,path
	n1=getcwd() 
	n2=path.expanduser('~')
	if n1 == n2: return '~'
	else: return n1

def print_percents(len_iter, len_list, percents_step = 1):
	len_list_round = 1000 if len_list > 1000 else 100
	percent_len_list = round(len_list_round/len_list, 1)
	percent = len_iter * percent_len_list
	percents_list = list(range(0, 100, percents_step))
	if percent in percents_list:
		print("{0}{2} percents{1}".format(Clr.RED2, Clr.RST2, percents_list[percents_list.index(percent)]))


def print_violet(message): print(Clr.VIOLET + str(message) + Clr.RST)
def print_violet2(message): print(Clr.VIOLET2 + str(message) + Clr.RST2)
def print_pink(message): print(Clr.PINK + str(message) + Clr.RST)
def print_pink2(message): print(Clr.PINK2 + str(message) + Clr.RST2)
def warp_green(message): return(Clr.GREEN + str(message) + Clr.RST)
def print_green(message): print(Clr.GREEN + str(message) + Clr.RST)
def print_green2(message): print(Clr.GREEN2 + str(message) + Clr.RST2)
def warp_yellow(message): return(Clr.YELLOW + str(message) + Clr.RST)
def print_yellow(message): print(Clr.YELLOW + str(message) + Clr.RST)
def print_yellow2(message): print(Clr.YELLOW2 + str(message) + Clr.RST2)

def warp_red(message): return(Clr.RED + str(message) + Clr.RST)
def warp_red2(message): return(Clr.RED2 + str(message) + Clr.RST2)
def print_red(message): print(Clr.RED + str(message) + Clr.RST)
def print_red2(message): print(Clr.RED2 + str(message) + Clr.RST2)

def warp_grey(message): return(Clr.GREY + str(message) + Clr.RST)
def print_grey(message): print(Clr.GREY + str(message) + Clr.RST)
def print_grey2(message): print(Clr.GREY2 + str(message) + Clr.RST2)

def warp_blue(message): return(Clr.BLUE + str(message) + Clr.RST)
def warp_blue2(message): return(Clr.BLUE2 + str(message) + Clr.RST2)
def print_blue(message): print(Clr.BLUE + str(message) + Clr.RST)
def print_blue2(message): print(Clr.BLUE2 + str(message) + Clr.RST2)


def get_time_unix(): 
	import time
	return time.time()


def get_time_local():
	import time
	return time.localtime()


def get_say(say):
	import os
	# for macOS
	if get_say_check_operating_system() == 'darwin':
		os.system('say ' + say)
	else: pyttsx3.say(say)


def get_say_check_operating_system():
	my_os = get_detect_operating_system()
	if my_os == 'linux' or my_os == 'win32' or my_os == 'cygwin' or my_os == 'aix':
		get_check_package('pyttsx3')
	return my_os


def get_detect_operating_system(print_result = False):
	"""
	# SOLUTION 1 
	# platform.sys executes at the run time
	import platform
	my_os = platform.system()
	print("OS in my system : ",my_os)
	"""

	"""
	# SOLUTION 2
	# sys.platform executes at the compile time.
	'linux'   for Linux
	`win32`   for Windows(Win32)
	'cygwin'  for Windows(cygwin)
	'darwin'  for macOS
	'aix'     for AIX
	"""
	import sys
	my_os = sys.platform
	if print_result: print("OS in my system :", my_os)
	return my_os.lower()


def get_check_package(package_name = None):	
	try: exec('import package_name')
	except ImportError:
		import os
		print(warp_red2('pip3 install ' + package_name))
		if os.system('pip3 install ' + package_name) is False:
			raise SystemExit(warp_red2('pip3 install ' + package_name))


def border_msg(message):
	# Solution 1
	# """Print the message in the box."""
	# #row = len(ord(message))
	# row = len(message)
	# #print('row = len(message)',row)
	# row_len = 60
	# row = row_len if row < row_len else row
	# ###row_len_result = int(row / 4)
	# row_len_result = int(row)
	# #print('row',row,'row_len_result',row_len_result)
	# ###i = ''.join([(row_len_result - 2) * ' '])
	# i = ''.join([(row_len_result) * ' '])
	# h = ''.join(['+'] + ['-' * row] + ['+'])
	# result = h + '\n' + '|' + i + message + i + '|' + '\n' + h
	# print(result)

	# Solution 2
	row = len(message)
	warp = int(row / 4)
	msg_warp = ''.join([warp * ' '])
	msg_border = ''.join(['+'] + [warp * '-'] + ['-' * row] + [warp * '-'] + ['+'])
	result = msg_border + '\n' + '|' + msg_warp + message + msg_warp + '|' + '\n' + msg_border
	print(result)




if __name__ == '__main__':
	import os
	print(getusername() + '@' + getpcname(), getcurrentdirectory(), '% ')
	#print(os.path.expanduser('~'))