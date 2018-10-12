#!usr/bin/python
# -*- coding: utf-8 -*-
import os
import os.path
import sys
import subprocess
import tkFileDialog
import tkMessageBox
import shutil
from Tkinter import *
import matplotlib.pyplot as plt
import numpy as np
import json
import matplotlib.patches as mpatch
#from playsound import 
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def new1(self):
        self.nregion  = int(self.ent0[1].get())
        self.nmat     = int(self.ent0[2].get())
        self.tab1 = [0]*self.nregion   
        if  self.nregion == 0:
            tkMessageBox.showwarning("Warning", "Enter the Total Number of Regions")
        elif self.nmat == 0:
            tkMessageBox.showwarning("Warning", "Enter the number of materials")
        elif self.nmat > self.nregion:
            tkMessageBox.showwarning("Warning", "the number of materials must not exceed the number of regions")
        else:
            self.newWindow = Toplevel()
            self.newWindow.grab_set()
            self.newWindow.focus_set()
            self.newWindow.columnconfigure(0, weight=1)
            self.newWindow.rowconfigure(3, weight=1)
            self.newWindow.resizable(True,True)
            if  self.nregion <= 4:
                self.newWindow.geometry("432x238+550+250")
            self.newWindow.title("Parameters input")
            Frame01 = LabelFrame(self.newWindow, text="Size for each Region per [cm]",
                                 font=("Helvetica", 10), fg='blue',bg=self.boutton)
            Frame01.grid(row=0,column=0,sticky=NSEW)
            if len(self.tab1) > len(self.Delta):
                self.Delta = [0]*self.nregion
            self.lab2 = [0]*100
            self.ent2 = [0]*100
            self.lab2[0] = Label(Frame01, width=10, text="Size" ,anchor='w',bg=self.boutton)
            self.lab2[0].grid(row=1, column=0,sticky=NSEW)
            for i in range(self.nregion):
                self.lab2[i+1] = Label(Frame01, width=10, text="Region %s" %(i+1),anchor='w',bg=self.boutton)
                self.lab2[i+1].grid(row=0, column=i+1,sticky=NSEW)
                self.ent2[i+1] = Entry(Frame01, width=10)
                self.ent2[i+1].grid(row=1, column=i+1,sticky=NSEW)
                self.ent2[i+1].delete(0,'end')
                self.ent2[i+1].insert(0,self.Delta[i])

            Frame02 = LabelFrame(self.newWindow, text="Number of fine meshes per Region",
                                 font=("Helvetica", 10), fg='blue',bg=self.boutton)
            Frame02.grid(row=1,column=0,sticky=NSEW)
            if len(self.tab1) > len(self.NFMR):
                self.NFMR = [0]*self.nregion
            self.lab3 = [0]*100
            self.ent3 = [0]*100
            self.lab3[0] = Label(Frame02, width=10, text="NFMR" ,anchor='w',bg=self.boutton)
            self.lab3[0].grid(row=1, column=0,sticky=NSEW)
            for i in range(self.nregion):
                self.lab3[i+1] = Label(Frame02, width=10, text="Region %s" %(i+1),anchor='w',bg=self.boutton)
                self.lab3[i+1].grid(row=0, column=i+1,sticky=NSEW)
                self.ent3[i+1] = Entry(Frame02, width=10)
                self.ent3[i+1].grid(row=1, column=i+1,sticky=NSEW)
                self.ent3[i+1].delete(0,'end')
                self.ent3[i+1].insert(0,self.NFMR[i])

            Frame03 = LabelFrame(self.newWindow, text="Which material fills each region",
                                 font=("Helvetica", 10), fg='blue',bg=self.boutton)
            Frame03.grid(row=2,column=0,sticky=NSEW)
            if len(self.tab1) > len(self.REGMAT):
                self.REGMAT = [0]*self.nregion
            self.lab4 = [0]*100
            self.ent4 = [0]*100
            self.lab4[0] = Label(Frame03, width=10, text="Materials" ,anchor='w',bg=self.boutton)
            self.lab4[0].grid(row=1, column=0,sticky=NSEW)
            for i in range(self.nregion):
                self.lab4[i+1] = Label(Frame03, width=10, text="Region %s" %(i+1),anchor='w',bg=self.boutton)
                self.lab4[i+1].grid(row=0, column=i+1,sticky=NSEW)
                self.ent4[i+1] = Entry(Frame03, width=10)
                self.ent4[i+1].grid(row=1, column=i+1,sticky=NSEW)
                self.ent4[i+1].delete(0,'end')
                self.ent4[i+1].insert(0,self.REGMAT[i])

            Frame04 = LabelFrame(self.newWindow,font=("Helvetica", 10), fg='blue',bg=self.boutton)
            Frame04.grid(row=3,column=0,sticky=NSEW)
            self.bouton = Button(Frame04,text="Save", font='Times',command=self.save1)
            self.bouton.config(bg='white', fg='black', relief='raised',borderwidth=4)
            self.bouton.grid(row =0, column =0,columnspan=1,sticky=NSEW)
            
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def new2(self):
        self.ngroup = int(self.ent0[0].get())
        self.nmat   = int(self.ent0[2].get())
        self.tab2  = [[0]*self.ngroup]*self.nmat
        if  self.ngroup == 0:
            tkMessageBox.showwarning("Warning", "Enter the number of energy group")
        elif self.nmat == 0:
            tkMessageBox.showwarning("Warning", "Enter the number of materials")
        else:
            self.newWindow = Toplevel()
            self.newWindow.grab_set()
            self.newWindow.focus_set()
            self.newWindow.columnconfigure(0, weight=1)
            self.newWindow.rowconfigure(0, weight=1)
            self.newWindow.resizable(True,True)
            if  self.nmat <= 3:
                if  self.ngroup <= 4:
                    self.newWindow.geometry("432x180+550+250")
            self.newWindow.title("Parameters input")
            Frame01 = LabelFrame(self.newWindow, text="Total Cross Section (SigT)",
                                 font=("Helvetica", 10), fg='blue',bg=self.boutton)
            Frame01.grid(columnspan=self.ngroup+1,rowspan=self.nmat+1,sticky=NSEW)
            if np.size(self.tab2) > np.size(self.SigT): 
                self.Vect1  = [0]*self.ngroup*self.nmat

            self.lab5 = [0]*self.ngroup*self.nmat
            self.ent5 = [0]*self.ngroup*self.nmat
            m = 0
            for j in range(self.nmat):
                self.lab5[j] = Label(Frame01, width=10, text="Material %s" %(j+1),anchor='w',bg=self.boutton)
                self.lab5[j].grid(row=j+1, column=0,sticky=NSEW)
                for i in range(self.ngroup):
                    self.lab5[i] = Label(Frame01, width=10, text="G %s" %(i+1),anchor='w',bg=self.boutton)
                    self.lab5[i].grid(row=0, column=i+1,sticky=NSEW)
                    self.ent5[m] = Entry(Frame01, width=10)
                    self.ent5[m].grid(row=j+1, column=i+1,sticky=NSEW)
                    self.ent5[m].delete(0,'end')
                    self.ent5[m].insert(0,self.Vect1[m])
                    m=m+1
            
            self.bouton = Button(Frame01,text="Save", font='Times',command=self.save2)
            self.bouton.config(bg='white', fg='black', relief='raised',borderwidth=4)
            self.bouton.grid(row =j+2, column =0,columnspan=1,pady = 20 ,sticky=NSEW)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def new3(self):
        self.ngroup = int(self.ent0[0].get())
        self.nmat   = int(self.ent0[2].get())
        self.tab3  = [[0]*self.ngroup]*self.nmat
        if  self.ngroup == 0:
            tkMessageBox.showwarning("Warning", "Enter the number of energy groups")
        elif self.nmat == 0:
            tkMessageBox.showwarning("Warning", "Enter the number of materials")
        else:
            self.newWindow = Toplevel()
            self.newWindow.grab_set()
            self.newWindow.focus_set()
            self.newWindow.columnconfigure(0, weight=1)
            self.newWindow.rowconfigure(0, weight=1)
            self.newWindow.resizable(True,True)
            if  self.nmat <= 3:
                if  self.ngroup <= 4:
                    self.newWindow.geometry("432x180+550+250")
            self.newWindow.title("Parameters input")
            Frame01 = LabelFrame(self.newWindow, text="NuFission Cross Section (NuSigF)", 
                                 font=("Helvetica", 10),fg='blue',bg=self.boutton)
            Frame01.grid(columnspan=self.ngroup+1,rowspan=self.nmat+1,sticky=NSEW)
            if np.size(self.tab3) > np.size(self.NuSigF): 
                self.Vect2  = [0]*self.ngroup*self.nmat

            self.lab6 = [0]*self.ngroup*self.nmat
            self.ent6 = [0]*self.ngroup*self.nmat
            m = 0
            for j in range(self.nmat):
                self.lab6[j] = Label(Frame01, width=10, text="Material %s" %(j+1),anchor='w',bg=self.boutton)
                self.lab6[j].grid(row=j+1, column=0,sticky=NSEW)
                for i in range(self.ngroup):
                    self.lab6[i] = Label(Frame01, width=10, text="G %s" %(i+1),anchor='w',bg=self.boutton)
                    self.lab6[i].grid(row=0, column=i+1,sticky=NSEW)
                    self.ent6[m] = Entry(Frame01, width=10)
                    self.ent6[m].grid(row=j+1, column=i+1,sticky=NSEW)
                    self.ent6[m].delete(0,'end')
                    self.ent6[m].insert(0,self.Vect2[m])
                    m+=1
 
            self.bouton = Button(Frame01,text="Save", font='Times',command=self.save3)
            self.bouton.config(bg='white', fg='black', relief='raised',borderwidth=4)
            self.bouton.grid(row =j+2, column =0,columnspan=1,pady = 20 ,sticky=NSEW)

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def new4(self):
        self.ngroup = int(self.ent0[0].get())
        self.nmat   = int(self.ent0[2].get())
        self.order   = int(self.ent0[4].get())
        self.tab4  = [[[[0]*self.ngroup]*self.ngroup]*self.nmat]*(self.order+1)
        if  self.ngroup == 0:
            tkMessageBox.showwarning("Warning", "Enter the number of energy groups")
        elif self.nmat == 0:
            tkMessageBox.showwarning("Warning", "Enter the number of materials")
        else:
            self.newWindow = Toplevel()
            self.newWindow.grab_set()
            self.newWindow.focus_set()
            self.newWindow.columnconfigure(0, weight=1)
            self.newWindow.rowconfigure(0, weight=1)
            self.newWindow.resizable(True,True)
            if  self.order <=0 :
                if self.nmat <=1:
                    if  self.ngroup <= 2:
                        self.newWindow.geometry("488x200+550+250")
            self.newWindow.title("Parameters input")
            Frame01 = LabelFrame(self.newWindow, text="Scatter Cross Section (SigS)",
                                 font=("Helvetica", 10), fg='blue',bg=self.boutton)
            Frame01.grid(sticky=NSEW)
            if np.size(self.tab4) > np.size(self.SigS): 
                self.Vect3  = [0]*self.ngroup*self.ngroup*self.nmat*(self.order+1)

            self.lab = [0]*self.ngroup*self.ngroup*self.nmat*(self.order+1)
            self.ent7 = [0]*self.ngroup*self.ngroup*self.nmat*(self.order+1)
            m1 =  0
            m  =  0
            for i in range(self.nmat):
                self.lab[m] = Label(Frame01, width=17, text="Material %s" %(i+1),anchor='w',bg=self.boutton)
                self.lab[m].grid(row=m1, column=0,sticky=NSEW)

                for k in range(self.ngroup):
                    self.lab[k] = Label(Frame01, width=10, text="G %s" %(k+1),anchor='w',bg=self.boutton)
                    self.lab[k].grid(row=1+m1, column=k+2,sticky=NSEW)

                for l in range(self.order+1):
                    self.lab[l] = Label(Frame01, width=10, text="Legendre Order L = %s" %(l),anchor='w',bg=self.boutton)
                    self.lab[l].grid(row=1+m1, column=0,sticky=NSEW)

                    for j in range(self.ngroup):
                        self.lab[j] = Label(Frame01, width=10, text="G %s" %(j+1),anchor='w',bg=self.boutton)
                        self.lab[j].grid(row=m1+2, column=1,sticky=NSEW)

                        for n in range(self.ngroup):
                            self.ent7[m] = Entry(Frame01, width=10)
                            self.ent7[m].grid(row=m1+2, column=n+2,sticky=NSEW)
                            self.ent7[m].delete(0,'end')
                            self.ent7[m].insert(0,self.Vect3[m])
                            m = m + 1


                        m1 = 1+m1 
                    m1 = 1+m1  
                m1 = 1+m1 
            self.bouton = Button(Frame01,text="Save", font='Times',command=self.save4)
            self.bouton.config(bg='white', fg='black', relief='raised',borderwidth=4)
            self.bouton.grid(row =m1, column =0,columnspan=1,pady = 20 ,sticky=NSEW)   

def new5(self):
        self.ngroup = int(self.ent0[0].get())
        self.nmat   = int(self.ent0[2].get())
        self.tab5  = [[0]*self.ngroup]*self.nmat
        if  self.ngroup == 0:
            tkMessageBox.showwarning("Warning", "Enter the number of energy groups")
        elif self.nmat == 0:
            tkMessageBox.showwarning("Warning", "Enter the number of materials")
        else:
            self.newWindow = Toplevel()
            self.newWindow.grab_set()
            self.newWindow.focus_set()
            self.newWindow.columnconfigure(0, weight=1)
            self.newWindow.rowconfigure(0, weight=1)
            self.newWindow.resizable(True,True)
            if  self.nmat <= 3:
                if  self.ngroup <= 4:
                    self.newWindow.geometry("432x180+550+250")
            self.newWindow.title("Parameters input")
            Frame01 = LabelFrame(self.newWindow, text="Density Function for Neutrons (Chi)",
                                font=("Helvetica", 10), fg='blue',bg=self.boutton)
            Frame01.grid(sticky=NSEW)
            if np.size(self.tab5) > np.size(self.Chi): 
                self.Vect4  = [0]*self.ngroup*self.nmat
           
            self.lab = [0]*100
            self.ent8 = [0]*100
            m = 0
            for j in range(self.nmat):
                self.lab[j] = Label(Frame01, width=10, text="Material %s" %(j+1),anchor='w',bg=self.boutton)
                self.lab[j].grid(row=j+1, column=0,sticky=NSEW)
                for i in range(self.ngroup):
                    self.lab[i] = Label(Frame01, width=10, text="G %s" %(i+1),anchor='w',bg=self.boutton)
                    self.lab[i].grid(row=0, column=i+1,sticky=NSEW)
                    self.ent8[m] = Entry(Frame01, width=10)
                    self.ent8[m].grid(row=j+1, column=i+1,sticky=NSEW)
                    self.ent8[m].delete(0,'end')
                    self.ent8[m].insert(0,self.Vect4[m])
                    m+=1
 
            self.bouton = Button(Frame01,text="Save", font='Times',command=self.save5)
            self.bouton.config(bg='white', fg='black', relief='raised',borderwidth=4)
            self.bouton.grid(row =j+2, column =0,columnspan=1,pady = 20 ,sticky=NSEW)

def save1(self):
        del self.Delta[:]
        del self.REGMAT[:]
        del self.NFMR[:] 
        for i in range(self.nregion):
            self.Delta.append(eval(self.ent2[i+1].get()))
            self.NFMR.append(eval(self.ent3[i+1].get()))
            self.REGMAT.append(eval(self.ent4[i+1].get()))
        self.newWindow.destroy()

def save2(self):
    m=0
    self.SigT = []
    for i in range(self.nmat):
        self.SigT.append([])
        for j in range(self.ngroup):
            self.SigT[i].append(eval(self.ent5[m].get())) 
            m+=1
    m = 0
    for i in range(self.nmat):
        for j in range(self.ngroup):
            self.Vect1[m] = eval(self.ent5[m].get())
            m +=1
    self.newWindow.destroy()

def save3(self):
    m=0
    self.NuSigF  = []
    for i in range(self.nmat):
        self.NuSigF.append([])
        for j in range(self.ngroup):
            self.NuSigF[i].append(eval(self.ent6[m].get())) 
            m+=1
    m=0
    for i in range(self.nmat):
        for j in range(self.ngroup):
            self.Vect2[m] = eval(self.ent6[m].get())
            m +=1
    self.newWindow.destroy()
def save4(self):
    self.order   = int(self.ent0[4].get())
    self.SigS = []
    m=0
    for i in range(self.nmat):
        self.SigS.append([])
        for l in range(self.order+1):
            self.SigS[i].append([])
            for j in range(self.ngroup):
                self.SigS[i][l].append([])
                for n in range(self.ngroup):
                    self.SigS[i][l][j].append(eval(self.ent7[m].get()))
                    m+=1

    m = 0
    for i in range(self.nmat):
        for l in range(self.order+1):
            for j in range(self.ngroup):
                for n in range(self.ngroup):
                    self.Vect3[m] = eval(self.ent7[m].get())
                    m +=1
    self.newWindow.destroy()

def save5(self):
    m=0
    self.Chi  = []
    for i in range(self.nmat):
        self.Chi.append([])
        for j in range(self.ngroup):
            self.Chi[i].append(eval(self.ent8[m].get())) 
            m+=1
    m = 0
    for i in range(self.nmat):
        for j in range(self.ngroup):
            self.Vect4[m] = eval(self.ent8[m].get())
            m +=1
    self.newWindow.destroy()
###### Drow geometry   <>
def Draw(self):
        filename = open('app/link/script.py', "r" ).read()
        with open(filename) as json_data:
            data = json.load(json_data)
            l = data['data']['parameter']['Size of each region [cm]']
            self.nmat = data['data']['parameter']['Total number of Materials']
            self.nregion = data['data']['parameter']['Total number of regions'] 
            self.regmat = data['data']['parameter']['Which material fills each region']
        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        width = [0]
        som = [0]
        for i in range(self.nregion):
          width.append(l[i])
          som.append(sum(width))
        rectangles = []
        red_patch = []
        m = som[0]

        for n in range(self.nregion):
          rectangles.append(mpatch.Rectangle((som[n],-5), abs(som[n+1])-abs(som[n]), 10))
        colr = ['#00ffff',"yellow",'g','r',"Green","Grey",'b', 'y', 'r', 'c', 'm', 'y', 'k', 'w'] 
        i=0
        for r in rectangles:
            ax.add_artist(r) 
            r.set_facecolor(color=colr[self.regmat[i]-1])
            rx, ry = r.get_xy()
            cx = rx + r.get_width()/2.0
            cy = ry + r.get_height()/2.0
            i=i+1
        for i in range(self.nmat):
            red_patch.append(mpatch.Patch(color=colr[i], label="Mat %s" %(i+1)))

        ax.set_ylim((-10, 10))
        ax.set_xlim((min(som), max(som)))
        ax.set_xlabel('X [cm]')
        ax.set_title('Color by Materials') 
        plt.legend(handles=red_patch)
        plt.show()

def exit_editor(self):
        if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
            self.root.destroy()
def data_up(self):
        self.ngroup = int(self.ent0[0].get())
        self.nregion  = int(self.ent0[1].get())
        self.nmat   = int(self.ent0[2].get())
        if  self.ngroup == 0:
            tkMessageBox.showwarning("Warning", "Enter the Input Parametres")
        elif self.nregion == 0:
            tkMessageBox.showwarning("Warning", "Enter the Input Parametres")
        elif self.nmat == 0:
            tkMessageBox.showwarning("Warning", "Enter the Input Parametres")   
        else:
            global filename  # 
            filename = open("app/input/input.json",'w')
            open('app/link/script.py', "w" ).write(os.path.abspath(os.path.dirname( __file__)) +'/input/input.json')
            filename.write('{ \n  "data": { \n    "parameter": { \n      "id": 100,')
            filename.write('\n      "Total number of energy groups": '+ self.ent0[0].get() +',')
            filename.write('\n      "Total number of Materials": '+ self.ent0[2].get() +',')
            filename.write('\n      "Total number of regions": '+ self.ent0[1].get() +',')
            filename.write('\n      "Which material fills each region": '+ str(self.REGMAT) +',')
            filename.write('\n      "Size of each region [cm]": '+ str(self.Delta) +',')
            filename.write('\n      "Number of fine meshes": '+ str(self.NFMR) +',')  
            filename.write('\n      "Number of Angular Discretization": '+ self.ent0[3].get() +',')
            filename.write('\n      "The l-order Legendre polynomial": '+ self.ent0[4].get() +',')
            filename.write('\n      "Maximum Number of Iterations": '+ self.ent1[0].get() +',')
            filename.write('\n      "Criterion of Keff convergence": '+ self.ent1[1].get())
            filename.write('\n    }, \n    "materials": [')
            # Ici Boucle
            for i in range(self.nmat):
                filename.write('\n      { \n        "id": '+ str(i+1) +', \n        "name": "material '+ str(i+1) +'",') 
                filename.write('\n        "XSTotal": ' + str(self.SigT[i][:]) +',' + '\n        "XSNuFission": '+ str(self.NuSigF[i][:])+',')
                filename.write('\n        "XSScatter Matrix":'+str(self.SigS[i][:][:][:])+','+ '\n        "XSChi":  '+str(self.Chi[i][:]))
                if i == self.nmat-1:
                    filename.write('\n      }')
                else:
                    filename.write('\n      },')  
            # Fin Boucle
            filename.write('\n    ]  \n  }  \n}') 
            filename.close() 
            self.textPad.delete(1.0,END)     
            fh = open("app/input/input.json","r")        
            self.textPad.insert(1.0,fh.read()) 
            fh.close()
            self.update_line_number()

def on_find(self,event=None):
        t2 = Toplevel(self.root)
	t2.title('Find')
	t2.geometry('350x65+200+250')
	t2.transient(self.root)
	Label(t2,text="Find All:").grid(row=0, column=0, pady=4, sticky='e')
	v=StringVar()
	e = Entry(t2, width=25, textvariable=v)
	e.grid(row=0, column=1, padx=2, pady=4, sticky='we')
	c=IntVar()
	a0 = Checkbutton(t2, text='Ignore Case', variable=c)
        a0.grid(row=1, column=1, sticky='e', padx=2, pady=2)
	a1 = Button(t2, text='Find All', underline=0,
                    command=lambda:self.search_for(v.get(), c.get(), self.textPad, t2, e))
        a1.grid(row=0, column=2, sticky='e'+'w', padx=2, pady=4)
	def close_search():
		self.textPad.tag_remove('match', '1.0', END)
		t2.destroy()
	t2.protocol('WM_DELETE_WINDOW', close_search)

def new_file(self,event=None):
        global filename
        filename = None
        self.root.title("data")
        self.textPad.delete(1.0, END)
        self.update_line_number()

def open_file(self,event=None):
        global filename
        filename = tkFileDialog.askopenfilename(defaultextension=".json",
                filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
        open('app/link/script.py', "w" ).write(str(filename))
        if filename == "": # If no file chosen.
            filename = None # Absence of file.
        else:
            self.root.title(os.path.basename(filename) + '- Sotution of the Transport Equation'
            ' by Multigroup Methods') # Returning the basename of 'file'
            self.textPad.delete(1.0,END)         
            fh = open(filename,"r")        
            self.textPad.insert(1.0,fh.read()) 
            fh.close()
        self.update_line_number()
##################################################################
def save(self,event=None):
        global filename
        try:
            f = open(filename, 'w')
            letter = self.textPad.get(1.0, 'end')
            f.write(letter)
            f.close()
        except:
            self.save_as()

def save_as(self):
        try:
           # Getting a filename to save the file.
           f = tkFileDialog.asksaveasfilename(initialfile='input.json',defaultextension=".json",
                                    filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
           fh = open(f, 'w')           
           global filename
           filename = f
           textoutput = self.textPad.get(1.0, END)
           fh.write(textoutput)              
           fh.close()                
           self.root.title(os.path.basename(f) + " - Tkeditor") 
        except:
            pass

def undo(self):
        self.textPad.event_generate("<<Undo>>")
        self.update_line_number()
    
def redo(self):
        self.textPad.event_generate("<<Redo>>")
        self.update_line_number()

def cut(self):
        self.textPad.event_generate("<<Cut>>")
        self.update_line_number()
    
def copy(self):
        self.textPad.event_generate("<<Copy>>")
        self.update_line_number()

def paste(self):
        self.textPad.event_generate("<<Paste>>")
        self.update_line_number()
    

def select_all(self,event=None):
	    self.textPad.tag_add('sel', '1.0', 'end')

def search_for(self,needle,cssnstv, textPad, t2,e):
        textPad.tag_remove('match', '1.0', END)
        count =0
        if needle:
                pos = '1.0'
                while True:
                    pos = textPad.search(needle, pos, nocase=cssnstv, stopindex=END)
                    if not pos: break
                    lastpos = '%s+%dc' % (pos, len(needle))
                    textPad.tag_add('match', pos, lastpos)
                    count += 1
                    pos = lastpos
                textPad.tag_config('match', foreground='red', background='yellow')
        e.focus_set()
        t2.title('%d matches found' %count)

def show_info_bar(self):
        val = self.showinbar.get()
        if val:
            self.infobar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')
        elif not val:
            self.infobar.pack_forget()

def update_line_number(self,event=None):
        txt = ''
        if self.showln.get():
            endline, endcolumn = self.textPad.index('end-1c').split('.')
            txt = '\n'.join(map(str, range(1, int(endline))))
        currline, curcolumn = self.textPad.index("insert").split('.')
        self.infobar.config(text='Line: %s | Column: %s'  %(currline,curcolumn) )

def theme(self):
        global bgc,fgc
        val = self.themechoice.get()
        clrs = self.clrschms.get(val)
        fgc, bgc = clrs.split('.')
        fgc, bgc = '#'+fgc, '#'+bgc
        self.textPad.config(bg=bgc, fg=fgc)

def highlight_line(self,interval=100):
        self.textPad.tag_remove("active_line", 1.0, "end")
        self.textPad.tag_add("active_line", "insert linestart", "insert lineend+1c")
        self.textPad.after(interval, toggle_highlight)

def undo_highlight(self):
        self.textPad.tag_remove("active_line", 1.0, "end")

def toggle_highlight(self,event=None):
        val = self.hltln.get()
        self.undo_highlight() if not val else self.highlight_line()

def select00(self):
        self.value00.get()
        open('app/link/script00.py', "w" ).write(self.value00.get()) 
        if  int(self.value00.get())==1:
            self.button[0].config(bg='#00ffff')
       
        else: 
            self.button[0].config(bg='grey76')
            self.ent0[3].config(state=NORMAL) 

def select01(self):
        self.value01.get()
        open('app/link/script01.py', "w" ).write(self.value01.get()) 
        if  int(self.value01.get())==1:
            self.button[1].config(bg='#00ffff')
        else:
            self.button[1].config(bg='grey76')
def select02(self):
        self.value02.get()
        open('app/link/script02.py', "w" ).write(self.value02.get()) 
        if  int(self.value02.get())==1:
            self.button[2].config(bg='#00ffff')
        else:
            self.button[2].config(bg='grey76')
def select03(self):
        self.value03.get()
        open('app/link/script03.py', "w" ).write(self.value03.get())
def select04(self):
        self.value04.get()
        open('app/link/script04.py', "w" ).write(self.value04.get())
def select07(self):
        self.value07.get()
        open('app/link/script07.py', "w" ).write(self.value07.get())
def select08(self):
        self.value08.get()
        open('app/link/script08.py', "w" ).write(self.value08.get())    
def select09(self,enent=None):
        self.value09.get()
        open('app/link/script09.py', "w" ).write(self.value09.get())  
def select10(self,enent=None):
        self.value10.get()
        open('app/link/script10.py', "w" ).write(self.value10.get())

def popup(self,event):
        self.cmenu.tk_popup(event.x_root, event.y_root, 0)


def plot(self,enent=None):
        #define plot size in inches (width, height) & resolution(DPI)
        fig = plt.figure(figsize=(5, 4), dpi=100)
        M00 = open('app/link/script00.py', "rb" ).read() 
        M01 = open('app/link/script01.py', "rb" ).read()
        M02 = open('app/link/script02.py', "rb" ).read()

        if M00 == str(1):
            data = np.loadtxt('app/Output/flux_cp.h')
        elif M01 == str(1):
            data = np.loadtxt('app/Output/flux_sn.h')
        elif M02 == str(1):
            data = np.loadtxt('app/Output/flux_moc.h')
        else:
            tkMessageBox.showwarning("Warning", "select the calculation method")

        if int(len(data)) >= 0:
           
            if M00 != str(0) or M01 != str(0) or M02 != str(0):
                matrix = []  
                for line in data:
                    matrix.append(line)
                max_columns = len(matrix[0]) - 1
                max_rows = len(matrix)
                x = [matrix[rownum][0] for rownum in range(max_rows)]
                y = [[matrix[rownum][colnum + 1] for rownum in range(max_rows)]for colnum in range(max_columns)]
                p = [0]*max_columns
                for i in range(max_columns):
                    key = 'Group', int(i+1)
                    p[i] = plt.plot(x,y[i] ,label="Group %s" %(max_columns-i),linewidth=1)
                #p[i] = plt.plot(x,y[i] ,label="Group %s" %(max_columns-i),marker=".",linewidth=1)
                if M00 == str(1):
                    plt.title("CP Method")
                elif M01 == str(1):
                    plt.title("SN Method") 
                elif M02 == str(1):
                    plt.title("MOC")    
                plt.xlabel('Distance [cm]')
                plt.ylabel('Normalized Flux')
                plt.legend()
                plt.show()
        else:
            tkMessageBox.showwarning("Warning", "Select More than a Fine Number of Meshes")
def geometry():
        print 'geometry'

def run(event=None):
    proc = subprocess.Popen(['python', 'app/python.py'],
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE)
    a = None
    Test = None
    while 1:
        text = proc.stdout.readline()[:-1]
        if type(text) != str or text == '' and proc.poll() != None:
            break
        elif type(text) == str or text == '.':
            Test = str(a)
            print text

    if  Test == str(a):
        tkMessageBox.showwarning("Warning", "Running case finished")
    else:
        tkMessageBox.showwarning("Warning", "Check Error")
         


def compile():
    M00 = open('app/link/script00.py', "r" ).read()  
    M01 = open('app/link/script01.py', "r" ).read()
    M02 = open('app/link/script02.py', "r" ).read()  

    if M00 == str(1):
        if os.path.exists('app/SlabCP.so'):
            os.remove('app/SlabCP.so')
        proc = subprocess.Popen(['f2py','-c','app/sources/TRANSPORT_CP.f90','-m','SlabCP'],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        while 1:
            text = proc.stdout.readline()[:-1]
            if type(text) != str or text == '' and proc.poll() != None: 
                break
 
            elif type(text) == str and len(text) > 6:
                print text
        shutil.move('SlabCP.so', 'app') 
    
    elif M01 == str(1):
        if os.path.exists('app/SlabSN.so'):
            os.remove('app/SlabSN.so') 
        proc = subprocess.Popen(['f2py','-c','app/sources/TRANSPORT_SN.f90','-m','SlabSN'], 
                                        stderr=subprocess.PIPE, 
                                        stdout=subprocess.PIPE)
        while 1:
            text = proc.stdout.readline()[:-1]
            if type(text) != str or text == '' and proc.poll() != None: 
                break
 
            elif type(text) == str and len(text) > 6:
                print text
        shutil.move('SlabSN.so', 'app')

    elif M02 == str(1):
        if os.path.exists('app/SlabMOC.so'):
            os.remove('app/SlabMOC.so')
        proc = subprocess.Popen(['f2py','-c','app/sources/TRANSPORT_MOC.f90','-m','SlabMOC'],
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)
        while 1:
            text = proc.stdout.readline()[:-1]
            if type(text) != str or text == '' and proc.poll() != None: 
                break
 
            elif type(text) == str and len(text) > 6:
                print text
        shutil.move('SlabMOC.so', 'app')
    else:
        tkMessageBox.showwarning("Warning", "select the calculation method")

def about():
        newWindow = Toplevel()
        newWindow.overrideredirect(1)
        newWindow.geometry("500x200+490+290")
        newWindow.config(bg='grey76')
        newWindow.title("Deterministic Code")
        a0 = Label(newWindow, text="NTP-ERSN")
        a0.config(fg='red',bg='grey76',font=("Helvetica", 16,"bold"))
        a0.pack()
        a1 = Label(newWindow, text='Python GUI Programming Using Tkinter')
        a1.config(fg='blue',bg='grey76',font=("Helvetica", 11))
        a1.pack()
        a2 = Label(newWindow, text='This project was developed by Mohamed LAHDOUR'
                                   ' & Tarek EL Bardouni')
        a2.config(fg='black',bg='grey76',font=("Helvetica", 11))
        a2.pack()
        a3 = Label(newWindow,text="Departement of Physics, Laboratory of Radiation"
                                  "& Nuclear Systems")
        a3.config(fg='black',bg='grey76',font=("Helvetica", 11))
        a3.pack()
        a4 = Label(newWindow,text="University Abdelmalek Essaadi, Faculty of sciences"
                                  "Tetouan (Morocco)")
        a4.config(fg='black',bg='grey76',font=("Helvetica", 11))
        a4.pack()
        b1=Button(newWindow,text="close", font='Times',bg='white',command=newWindow.destroy)
        b1.pack(pady=10)
def help_box(event=None):
        newWindow = Toplevel()
        newWindow.overrideredirect(1)
        newWindow.geometry("500x180+490+290")
        newWindow.config(bg='grey76')
        newWindow.title("Help")
        a0 = Label(newWindow, text="NTP-ERSN")
        a0.config(fg='red',bg='grey76',font=("Helvetica", 16,"bold"))
        a0.pack()
        a1 = Label(newWindow, text="For Help Contact Us:")
        a1.config(fg='black',bg='grey76',font=("Helvetica", 11))
        a1.pack()
        a2 = Label(newWindow, text="mlahdour@uae.ac.ma  &  telbardouni@uae.ac.ma")
        a2.config(fg='black',bg='grey76',font=("Helvetica", 11))
        a2.pack()
        b1=Button(newWindow,text="close", font='Times',bg='white',command=newWindow.destroy)
        b1.pack(pady=10)
