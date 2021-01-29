import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
from fang_worm_out_and_in import func_worm
def start(name):
	if type(name)==list:
		os.system('python fang_worm_out_and_in.py')
		for i in name:
			os.system(f"start scrapy crawl {i}")
	else:

		os.system(f"start scrapy crawl {name}")

window = Tk()
window.title("启动爬虫")
# ttk.Button(text = 'paseDate1',command = lambda:start("paseDate1"),width = 60).pack(pady = 10)


ttk.Button(text = 'nostory',command = lambda:start("nostory"),width = 60).pack(pady = 10)

ttk.Button(text = 'xjxf',command = lambda:start("xjxf"),width = 60).pack(pady = 10)

ttk.Button(text = 'fang_worm_out_and_in',command = lambda:os.system('python fang_worm_out_and_in.py'),width = 60).pack(pady = 10)

ttk.Button(text = '启动全部',command = lambda:start(['nostory','xjxf']),width = 60).pack(pady = 10)
mainloop()