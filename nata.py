#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
try:
	from grab import Grab
	from Tkinter import *
	import ttk
	import logging
	import re
	import shutil
	import threading
except(ImportError):
	print "\nTo use this script you need (grab, python-lxml, python-lxml-dbg ) modules."\
			"\nRead the top intro for instructions.\n"
	a = raw_input('Do you want install it [Y/n]? ')
	if a == 'y' or a == 'Y':
		os.system('sudo aptitude install python-pip python-lxml python-lxml-dbg python-tk && sudo pip install grab')
		sys.exit(1)
	else:
		sys.exit(1)
_run = False
i  = 0

def run():
	print '\nRunning ...'
	threading.Thread(target=main).start()
	
def stop():
	global _run
	print '\nQuit'
	_run = False
	tk.destroy()
	sys.exit(0)
	
#MAIN
def main():
	
	global _run
	_run = True
	count  = 0
	url = 'http://www.natashaclub.com/'
	url_s = 'https://www.natashaclub.com/search_result.php?p_per_page=1000&photos_only=on&online_only=on&Sex=female&LookingFor=male&DateOfBirth_start=18&DateOfBirth_end=75&Region[]=3&Region[]=4&Region[]=7&Country[]=179&CityST=0&City=&&page='
    
	g = Grab()
	
	g.setup(hammer_mode=True, hammer_timeouts=((20, 30), (60, 90), (150, 200)))
	g.setup(follow_refresh=True)
	
	if log.get() == True:
		print 'makin log dir'
		lb["text"] = 'makin log dir'
		try:
			os.mkdir('log')
			g.setup(log_dir='log')
			logger = logging.getLogger('grab')
			logger.addHandler(logging.StreamHandler())
			logger.setLevel(logging.DEBUG)
			g.setup(debug_post='True')
		except Exception:
			shutil.rmtree('log')
			os.mkdir('log')
			g.setup(log_dir='log')
			#sys.exit('[!] unable to delete log directory')

	g.go(url)
	g.set_input('ID', ladyId.get())
	g.set_input('Password', ladyPas.get())
	g.set_input('rememberme', '1')
	g.submit()
	g.dump_cookies('cookies')
	
	g.go(url)
	if g.search(u'Member Menu'):
		print 'Authorization complete ...'
		lb["text"] = 'Authorization complete ...'
	else:
		print "\033[31m\t[!]Invalid login\033[0m"
		lb['text'] = '[!]Invalid login'
		_run = False
		sys.exit()


	g.go(url_s)
	list = g.doc.select('//a[contains(@href, "&&page=")]/@href')[13].text()
	page = re.findall('(\d+)', list)[8]
	page = int(page)
	for i in range(page+1):
		if _run:
			
			g.go(url_s + repr(i))
			
			list2 = g.doc.select('//a[contains(@href, "vkiss.php?sendto=")]/@href').text_list()
			for item in list2:
				if _run:
					try:
						
						g.go(url + item)
						if g.search(u'Virtual smile NOT sent'):
							print 'Virtual smile NOT sent'
							lb["text"] = 'Virtual smile NOT sent'
							if g.search(u"Sorry, but you've reached your limit for today."):
								print "\033[31m\t[+]Sorry, but you've reached your limit for today.\033[0m"
								lb['text'] = "Sorry, but you've reached your limit for today."
								_run = False
								sys.exit()
						
						else:
							text =  '\033[32m[+] Виртуальная улыбка была отправлена : ', re.findall('(\d+)', item), '\033[0m'
							print text
							lb["text"] = text
							count()
					except Exception:
						print _run
def count():
	global i
	i  = i +1  	
	lb1["text"] = i				

if __name__ == '__main__':
	tk = Tk()
	tk.geometry('450x80')
	tk.title('www.natashaclub.com')

	lb = ttk.Label(tk, text='ID:PASS :').place(x = 0, y = 5)
	ladyId = ttk.Entry(tk)
	ladyId.insert(0,'Melon__Fruit')
	ladyId.place(x = 60, y = 5)

	ladyPas = ttk.Entry(tk)
	ladyPas.insert(0,'1156tree')
	ladyPas.place(x = 200, y = 5)

	exitBtn = ttk.Button(tk, text = 'run',command=run)
	exitBtn.place(x = 180, y = 30)
	
	runBtn = ttk.Button(tk, text = 'exit',command=stop)
	runBtn.place(x = 280, y = 30)
	
	log = BooleanVar()
	logBtn = ttk.Checkbutton(tk, text='Enable logging',variable=log, onvalue=True, offvalue=False)
	logBtn.place(x = 5, y = 30)
	
	lb = ttk.Label(tk, text="Waiting for user activity ...")
	lb.pack(side = 'bottom', fill = 'x')
	
	lb1 = ttk.Label(tk, text='kiss' , font="Arial 25 bold")
	lb1.pack(side = 'right', padx = 10,)

	tk.mainloop()
