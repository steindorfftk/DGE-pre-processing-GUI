from tkinter import *
from tkinter import ttk
import sys
from time import sleep
import os

root = Tk()

class TextRedirector:
	def __init__(self, text_widget):
		self.text_widget = text_widget
	def write(self, message):
		self.text_widget.insert(END, message)
		self.text_widget.see(END) 
	def flush(self):
		self.text_widget.update_idletasks()

class Application():
	def __init__(self):
		self.root = root
		self.screen()
		self.screenFrames()
		self.frame1()
		self.frame2()
		root.mainloop()
	def screen(self):
		self.root.title("NBioinfo's DGE pre processing")	
		self.root.configure(background='#ADD8E6')
		self.root.geometry('800x600')
		self.root.resizable(True,True)
		self.root.maxsize(width=1200,height = 900)
		self.root.minsize(width=400,height = 300)		
	def screenFrames(self):
		self.frame_1 = Frame(self.root,bd=4,bg='#FFFFFF',highlightbackground='#a7a7a7',highlightthickness=2)
		self.frame_1.place(relx=0.03 ,rely=0.04,relwidth=0.4,relheight=0.39)
		self.frame_2 = Frame(self.root,bd=4,bg='#FFFFFF',highlightbackground='#a7a7a7',highlightthickness=2)
		self.frame_2.place(relx=0.46 ,rely=0.04,relwidth=0.51,relheight=0.39)
		self.frame_3 = Frame(self.root,bd=4,bg='#FFFFFF',highlightbackground='#a7a7a7',highlightthickness=2)
		self.frame_3.place(relx=0.03 ,rely=0.46,relwidth=0.94,relheight=0.5)
		self.outputText = Text(self.frame_3,wrap='word',font=('Arial',9))
		self.outputText.pack(fill=BOTH, expand=True)
		sys.stdout = TextRedirector(self.outputText)
	def frame1(self):
		self.lb_sra = Label(self.frame_1, text="SRA Accession List:",bg='#FFFFFF',font=('Arial',11))
		self.lb_sra.place(relx=0.01,rely=0.01)
		self.sra_text = Text(self.frame_1,wrap="word",font=('Arial',9))
		self.sra_text.place(relx=0.01,rely=0.11,relwidth=0.98, relheight=0.88)	
		scrollbar = Scrollbar(self.frame_1, command=self.sra_text.yview)
		scrollbar.place(relx=0.96, rely=0.11, relheight=0.88)
		self.sra_text.config(yscrollcommand=scrollbar.set)
	def frame2(self):
		listOrganisms = ["Homo sapiens","Mus musculus"]
		self.verbose = BooleanVar()
		self.lowmemory = BooleanVar()
		self.runButton = Button(self.frame_2,text='Run',font=('Arial',13),command=self.on_button_click)
		self.runButton.place(relx=0.7,rely=0.85,relwidth=0.3,relheight=0.15)
		self.optLabel = Label(self.frame_2, text="Options:",bg='#FFFFFF',font=('Arial',11))
		self.optLabel.place(relx=0.01,rely=0.01)
		self.orgLabel = Label(self.frame_2, text="Organism",bg='#FFFFFF',font=('Arial',10))
		self.orgLabel.place(relx=0.04,rely=0.16)
		self.orgSelector = ttk.Combobox(self.frame_2,values=listOrganisms,font=('Arial',10))
		self.orgSelector.place(relx=0.25,rely=0.16)
		self.verboseLabel = Label(self.frame_2, text="Verbose",bg='#FFFFFF',font=('Arial',10))
		self.verboseLabel.place(relx=0.04,rely=0.32)
		self.verboseButton = Checkbutton(self.frame_2,text="",variable=self.verbose,onvalue=True,offvalue=False,bg='#FFFFFF')
		self.verboseButton.place(relx=0.25,rely=0.32)
		self.verboseButton.select()
		self.lowmemoryLabel = Label(self.frame_2, text="Low memory",bg='#FFFFFF',font=('Arial',10))
		self.lowmemoryLabel.place(relx=0.04,rely=0.48)
		self.lowmemoryButton = Checkbutton(self.frame_2,text="",variable=self.lowmemory,onvalue=True,offvalue=False,bg='#FFFFFF')
		self.lowmemoryButton.place(relx=0.25,rely=0.48)
		self.lowmemoryButton.select()
	def get_list(self):
		input_sra = self.sra_text.get("1.0", "end-1c")
		input_path = 'input/SraAccList.txt'
		with open(input_path, 'w') as text:
			text.write(input_sra)
		self.accession_list = []
		with open('input/SraAccList.txt', 'r') as texto:
			for line in texto:
				linha = line.split()
				self.accession_list.append(linha[0])	
	def run_sra(self):
		self.done_check = []
		print('Downloading SRA data...')
		os.system('prefetch --option-file input/SraAccList.txt ')
		sleep(10)
		if self.verbos == True:
			isdone = True
			prefetch_done = os.listdir('temporary/sratoolkit/sra')
			for file in prefetch_done:
				self.done_check.append(file[:-4])
			for acc in self.accession_list:
				if acc not in self.done_check:
					isdone = False
			if isdone == True:
				self.outputText.delete(1.0,END)
				print('Done!\n')
			else:
				self.outputText.delete(1.0,END)
				print('Error downloading one or more SRA files')
	
	def on_button_click(self):
		self.outputText.delete(1.0,END)
		self.organism = self.orgSelector.get()
		self.verbos = self.verbose.get()
		self.lowmemor = self.lowmemory.get()
		self.get_list()
		self.run_sra()


		
Application()



