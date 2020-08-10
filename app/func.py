#!usr/bin/python3
# -*- coding: utf-8 -*-
import os
import os.path
import sys
import subprocess
from tkinter import filedialog
from tkinter import messagebox
import shutil
from tkinter import ttk 
from tkinter import *
import matplotlib.pyplot as plt
import numpy 
import numpy as np
import json
import matplotlib.patches as mpatch
import matplotlib.patches as mpatches
import matplotlib.mlab as mlab
import shlex
from threading import Thread
from queue import Queue, Empty
#from playsound import 
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def new1(self):
    self.nmat = int(self.ent0[1].get())
    self.np   = int(self.ent0[2].get())
    self.nx   = int(self.ent0[3].get())
    self.nxa  = int(self.ent0[4].get())
    self.na   = int(self.ent0[5].get())

    M00 = open('app/link/script01.py', "r" ).read() 
    if M00 == 'Pin Cell':
        if  self.nmat == 0:
            messagebox.showwarning("Warning", "Enter Enter the materials number")
        elif self.np == 0:
            messagebox.showwarning("Warning", "Enter the pin cells number")
        elif self.nx == 0:
            messagebox.showwarning("Warning", "Enter the x mesh pin cell number \n"+
                                     "(Each pin cell is approximated by a x cartesian grid)")
        elif self.np != 0 and self.nx != 0 and self.nmat != 0:

            self.newWindow = Toplevel()
            self.newWindow.grab_set()
            self.newWindow.focus_set()
            self.newWindow.columnconfigure(0, weight=1)
            self.newWindow.rowconfigure(3, weight=1)
            self.newWindow.resizable(True,True)
            self.newWindow.title("Parameters input")
            tabControl = ttk.Notebook(self.newWindow) 
            tab = [0]*self.np
            labelframe = [0]*self.np
            self.lab1 = [0]*self.nx*self.np
            self.ent1 = [0]*self.nx*self.np
            self.lab2 = [0]*self.nx*self.np
            self.ent2 = [0]*self.nx*self.np
            self.lab3 = [0]*self.nx*self.np
            self.ent3 = [0]*self.nx*self.np
            self.Delta = [0]*self.nx*self.np
            self.NFMR = [0]*self.nx*self.np
            self.REGMAT = [0]*self.nx*self.np
            m1=0;m2=0;m3=0
            for i in range(self.np):
                tab[i] = ttk.Frame(tabControl) 
                tabControl.add(tab[i], text ="Pin Cell %s" %(i+1)) 
                tabControl.pack(expand = 1, fill ="both") 
                labelframe[i] = LabelFrame(tab[i], text="Size for each region per [cm]",fg='blue')  
                labelframe[i].pack(fill="both", expand="yes")  
                for j in range(self.nx):
                    self.lab1[j] = Label(labelframe[i], text="X %s" %(j+1),anchor="center")
                    self.lab1[j].grid(row=0, column=j+1,sticky=NSEW)
                    self.ent1[m1] = Entry(labelframe[i], width=10)
                    self.ent1[m1].grid(row=1, column=j+1,sticky=NSEW)
                    self.ent1[m1].delete(0,'end') 
                    self.ent1[m1].insert(0,self.Delta[m1])
                    m1+=1

                labelframe[i] = LabelFrame(tab[i], text="Which material fills each region",fg='blue')  
                labelframe[i].pack(fill="both", expand="yes") 

                for j in range(self.nx):
                    self.lab2[j] = Label(labelframe[i], text="X %s" %(j+1),anchor="center")
                    self.lab2[j].grid(row=0, column=j+1,sticky=NSEW)
                    self.ent2[m2] = Entry(labelframe[i], width=10)
                    self.ent2[m2].grid(row=1, column=j+1,sticky=NSEW)
                    self.ent2[m2].delete(0,'end') 
                    self.ent2[m2].insert(0,self.REGMAT[m2])
                    m2+=1

                labelframe[i] = LabelFrame(tab[i], text="Number of fine meshes per region",fg='blue')  
                labelframe[i].pack(fill="both", expand="yes") 

                for j in range(self.nx):
                    self.lab3[j] = Label(labelframe[i], text="X %s" %(j+1),anchor="center")
                    self.lab3[j].grid(row=0, column=j+1,sticky=NSEW)
                    self.ent3[m3] = Entry(labelframe[i], width=10)
                    self.ent3[m3].grid(row=1, column=j+1,sticky=NSEW)
                    self.ent3[m3].delete(0,'end') 
                    self.ent3[m3].insert(0,self.NFMR[m3])
                    m3+=1
            self.bouton = ttk.Button(self.newWindow,text="Save and Close", style='BW.TButton', command=self.save1)
            self.bouton.pack(fill="x", expand="yes")
 
    elif M00 == 'Assembly':
        if  self.na  == 0:
            messagebox.showwarning("Warning", "Enter the assemblies number")
        elif  self.nxa  == 0:
            messagebox.showwarning("Warning", "Enter the x mesh assembly number \n"+
                                       "(Each assembly contains a set of pin cells)")
        elif self.na != 0 and self.nxa !=0:
            self.newWindow = Toplevel()
            self.newWindow.grab_set()
            self.newWindow.focus_set()
            self.newWindow.columnconfigure(0, weight=1)
            self.newWindow.rowconfigure(3, weight=1)
            self.newWindow.resizable(True,True)
            self.newWindow.title("Parameters input")
            tabControl = ttk.Notebook(self.newWindow) 
            tab = [0]*self.na
            labelframe = [0]*self.na
            self.lab4 = [0]*100
            self.ent4 = [0]*100
            self.assm  = [0]*self.nxa*self.na
            m=0
            for i in range(self.na):
                tab[i] = ttk.Frame(tabControl) 
                tabControl.add(tab[i], text ="Assembly %s" %(i+1)) 
                tabControl.pack(expand = 1, fill ="both")

                labelframe[i] = LabelFrame(tab[i], text="Which pin cells fill the assembly lattice",fg='blue')  
                labelframe[i].pack(fill="both", expand="yes") 

                for j in range(self.nxa):
                    self.lab4[m] = Label(labelframe[i], text="%s" %(j+1),anchor="center")
                    self.lab4[m].grid(row=0, column=j+1,sticky=NSEW)
                    self.ent4[m] = Entry(labelframe[i], width=10)
                    self.ent4[m].grid(row=1, column=j+1,sticky=NSEW)
                    self.ent4[m].delete(0,'end') 
                    self.ent4[m].insert(0,self.assm[m])
                    m+=1

            self.bouton = ttk.Button(self.newWindow,text="Save and Close", style='BW.TButton', command=self.save2)
            self.bouton.pack(fill="x", expand="yes") 
    elif M00 == 'Core':
        if self.na == 0:
            messagebox.showwarning("Warning", "Enter the assemblies number")
        elif self.na != 0:
            self.newWindow = Toplevel()
            self.newWindow.grab_set()
            self.newWindow.focus_set()
            self.newWindow.columnconfigure(0, weight=1)
            self.newWindow.rowconfigure(3, weight=1)
            self.newWindow.resizable(True,True)
            self.newWindow.title("Parameters input")
            self.lab5 = [0]*100
            self.ent5 = [0]*100
            self.core = [0]*self.na
            
            labelframe = LabelFrame(self.newWindow, text="Which ssembly lattices fill the core geometry",fg='blue')  
            labelframe.pack(fill="both", expand="yes") 

            for j in range(self.na):
                self.lab5[j] = Label(labelframe, text="%s" %(j+1),anchor="center")
                self.lab5[j].grid(row=0, column=j+1,sticky=NSEW)
                self.ent5[j] = Entry(labelframe, width=10)
                self.ent5[j].grid(row=1, column=j+1,sticky=NSEW)
                self.ent5[j].delete(0,'end') 
                self.ent5[j].insert(0,self.core[j])

            self.bouton = ttk.Button(self.newWindow,text="Save and Close", style='BW.TButton', command=self.save3)
            self.bouton.pack(fill="x", expand="yes") 

  
            
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def new2(self):
    self.ng    = int(self.ent0[0].get())
    self.nmat  = int(self.ent0[1].get())
    self.order = int(self.ent0[8].get())+1
    M00 = open('app/link/script02.py', "r" ).read() 
    if M00 == 'TotalXS':
        if  self.ng == 0:
            messagebox.showwarning("Warning", "Enter the number of energy group")
        elif self.nmat == 0:
            messagebox.showwarning("Warning", "Enter the number of materials")
        else:
            self.newWindow = Toplevel()
            self.newWindow.grab_set()
            self.newWindow.focus_set()
            self.newWindow.columnconfigure(0, weight=1)
            self.newWindow.rowconfigure(0, weight=1)
            self.newWindow.resizable(True,True)
            self.newWindow.title("Parameters input")
            labelframe = LabelFrame(self.newWindow, text="Total Cross Section (SigT)",fg='blue')  
            labelframe.pack(fill="both", expand="yes") 
            self.SigT = [0]*self.ng*self.nmat
            self.lab6 = [0]*self.ng*self.nmat
            self.ent6 = [0]*self.ng*self.nmat
            m = 0
            for j in range(self.nmat):
                self.lab6[j] = Label(labelframe, width=10, text="Material %s" %(j+1),anchor='center')
                self.lab6[j].grid(row=j+1, column=0,sticky=NSEW)
                for i in range(self.ng):
                    self.lab6[i] = Label(labelframe, width=10, text="G %s" %(i+1),anchor='center')
                    self.lab6[i].grid(row=0, column=i+1,sticky=NSEW)
                    self.ent6[m] = Entry(labelframe, width=10)
                    self.ent6[m].grid(row=j+1, column=i+1,sticky=NSEW)
                    self.ent6[m].delete(0,'end')
                    self.ent6[m].insert(0,self.SigT[m])
                    m+=1
            self.bouton = ttk.Button(self.newWindow,text="Save and Close", style='BW.TButton', command=self.save4)
            self.bouton.pack(fill="x", expand="yes") 

    elif M00 == 'FissionXS':
        if  self.ng == 0:
            messagebox.showwarning("Warning", "Enter the number of energy group")
        elif self.nmat == 0:
            messagebox.showwarning("Warning", "Enter the number of materials")
        else:
            self.newWindow = Toplevel()
            self.newWindow.grab_set()
            self.newWindow.focus_set()
            self.newWindow.columnconfigure(0, weight=1)
            self.newWindow.rowconfigure(0, weight=1)
            self.newWindow.resizable(True,True)
            self.newWindow.title("Parameters input")
            labelframe = LabelFrame(self.newWindow, text="Total Cross Section (SigF)",fg='blue')  
            labelframe.pack(fill="both", expand="yes") 
            self.SigF  = [0]*self.ng*self.nmat
            self.lab7 = [0]*self.ng*self.nmat
            self.ent7 = [0]*self.ng*self.nmat
            m = 0
            for j in range(self.nmat):
                self.lab7[j] = Label(labelframe, width=10, text="Material %s" %(j+1),anchor='center')
                self.lab7[j].grid(row=j+1, column=0,sticky=NSEW)
                for i in range(self.ng):
                    self.lab7[i] = Label(labelframe, width=10, text="G %s" %(i+1),anchor='center')
                    self.lab7[i].grid(row=0, column=i+1,sticky=NSEW)
                    self.ent7[m] = Entry(labelframe, width=10)
                    self.ent7[m].grid(row=j+1, column=i+1,sticky=NSEW)
                    self.ent7[m].delete(0,'end')
                    self.ent7[m].insert(0,self.SigF[m])
                    m+=1
            self.bouton = ttk.Button(self.newWindow,text="Save and Close", style='BW.TButton', command=self.save5)
            self.bouton.pack(fill="x", expand="yes") 

    elif M00 == 'NuFissionXS':
        if  self.ng == 0:
            messagebox.showwarning("Warning", "Enter the number of energy group")
        elif self.nmat == 0:
            messagebox.showwarning("Warning", "Enter the number of materials")
        else:
            self.newWindow = Toplevel()
            self.newWindow.grab_set()
            self.newWindow.focus_set()
            self.newWindow.columnconfigure(0, weight=1)
            self.newWindow.rowconfigure(0, weight=1)
            self.newWindow.resizable(True,True)
            self.newWindow.title("Parameters input")
            labelframe = LabelFrame(self.newWindow, text="Total Cross Section (NuSigF)",fg='blue')  
            labelframe.pack(fill="both", expand="yes") 

            self.lab8 = [0]*self.ng*self.nmat
            self.ent8 = [0]*self.ng*self.nmat
            self.NuSigF  = [0]*self.ng*self.nmat
            m = 0
            for j in range(self.nmat):
                self.lab8[j] = Label(labelframe, width=10, text="Material %s" %(j+1),anchor='center')
                self.lab8[j].grid(row=j+1, column=0,sticky=NSEW)
                for i in range(self.ng):
                    self.lab8[i] = Label(labelframe, width=10, text="G %s" %(i+1),anchor='center')
                    self.lab8[i].grid(row=0, column=i+1,sticky=NSEW)
                    self.ent8[m] = Entry(labelframe, width=10)
                    self.ent8[m].grid(row=j+1, column=i+1,sticky=NSEW)
                    self.ent8[m].delete(0,'end')
                    self.ent8[m].insert(0,self.NuSigF[m])
                    m=m+1
            self.bouton = ttk.Button(self.newWindow,text="Save and Close", style='BW.TButton', command=self.save6)
            self.bouton.pack(fill="x", expand="yes") 

    elif M00 == 'ScatterMatrixXS':
        if  self.ng == 0:
            messagebox.showwarning("Warning", "Enter the number of energy group")
        elif self.nmat == 0:
            messagebox.showwarning("Warning", "Enter the number of materials")
        else:
            self.newWindow = Toplevel()
            self.newWindow.grab_set()
            self.newWindow.focus_set()
            self.newWindow.columnconfigure(0, weight=1)
            self.newWindow.rowconfigure(0, weight=1)
            self.newWindow.resizable(True,True)
            self.newWindow.title("Parameters input")
            self.lab9 = [0]*self.ng*self.nmat*self.ng*self.order
            self.ent9 = [0]*self.ng*self.nmat*self.ng*self.order
            self.SigS  = [0]*self.ng*self.nmat*self.ng*self.order
            labelframe = LabelFrame(self.newWindow, text="Scatter Matrix Cross Section (SigS)",fg='blue')  
            labelframe.pack(fill="both", expand="yes") 

            tabControl = ttk.Notebook(labelframe)
            tab2 = [0]*self.nmat
            labelframe = [0]*self.order
            m2= 0
            for j in range(self.nmat):
                tab2[j] = ttk.Frame(tabControl) 
                tabControl.add(tab2[j], text ="Material %s" %(j+1)) 
                tabControl.pack(expand = 1, fill ="both") 
                for i in range(self.order):
                    labelframe[i] = LabelFrame(tab2[j], text="Legender Order L= %s" %(i),fg='blue')  
                    labelframe[i].pack(fill="both", expand="yes") 
                    m = 0
                    for k in range(self.ng):
                        self.lab9[k] = Label(labelframe[i], width=10, text="G %s" %(k+1),anchor='center')
                        self.lab9[k].grid(row=1, column=k+1,sticky=NSEW)
                        m1=0
                        for n in range(self.ng):
                            self.lab9[m2] = Label(labelframe[i], width=10, text="G %s" %(n+1),anchor='center')
                            self.lab9[m2].grid(row=m1+2, column=0, sticky=NSEW)
                            self.ent9[m2] = Entry(labelframe[i], width=10)
                            self.ent9[m2].grid(row=m1+2, column=m+1, sticky=NSEW)
                            self.ent9[m2].delete(0,'end')
                            self.ent9[m2].insert(0,self.SigS[m2])
                            m1+=1
                            m2+=1 
                        m+=1
                    m1+=1
            self.bouton = ttk.Button(self.newWindow,text="Save and Close", style='BW.TButton', command=self.save7)
            self.bouton.pack(fill="x", expand="yes") 

    elif M00 == 'ChiXS':
        if  self.ng == 0:
            messagebox.showwarning("Warning", "Enter the number of energy group")
        elif self.nmat == 0:
            messagebox.showwarning("Warning", "Enter the number of materials")
        else:
            self.newWindow = Toplevel()
            self.newWindow.grab_set()
            self.newWindow.focus_set()
            self.newWindow.columnconfigure(0, weight=1)
            self.newWindow.rowconfigure(0, weight=1)
            self.newWindow.resizable(True,True)
            self.newWindow.title("Parameters input")
            labelframe = LabelFrame(self.newWindow, text="Density Function for Neutrons (Chi)",fg='blue')  
            labelframe.pack(fill="both", expand="yes") 

            self.lab10 = [0]*self.ng*self.nmat
            self.ent10 = [0]*self.ng*self.nmat
            self.Chi  = [0]*self.ng*self.nmat
            m = 0
            for j in range(self.nmat):
                self.lab10[j] = Label(labelframe, width=10, text="Material %s" %(j+1),anchor='center')
                self.lab10[j].grid(row=j+1, column=0,sticky=NSEW)
                for i in range(self.ng):
                    self.lab10[i] = Label(labelframe, width=10, text="G %s" %(i+1),anchor='center')
                    self.lab10[i].grid(row=0, column=i+1,sticky=NSEW)
                    self.ent10[m] = Entry(labelframe, width=10)
                    self.ent10[m].grid(row=j+1, column=i+1,sticky=NSEW)
                    self.ent10[m].delete(0,'end')
                    self.ent10[m].insert(0,self.Chi[m])
                    m=m+1
            self.bouton = ttk.Button(self.newWindow,text="Save and Close", style='BW.TButton', command=self.save8)
            self.bouton.pack(fill="x", expand="yes") 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def save1(self):
    m=0
    self.Delta  = []
    self.REGMAT = []
    self.NFMR   = [] 
    for i in range(self.np):
        self.Delta.append([])
        self.REGMAT.append([])
        self.NFMR.append([])
        for j in range(self.nx):
            self.Delta[i].append(eval(self.ent1[m].get()))
            self.REGMAT[i].append(eval(self.ent2[m].get()))
            self.NFMR[i].append(eval(self.ent3[m].get()))
            m+=1
    self.newWindow.destroy()

def save2(self):
    m=0
    self.assm = []
    for i in range(self.na):
        self.assm.append([])
        for j in range(self.nxa):
            self.assm[i].append(eval(self.ent4[m].get()))
            m+=1
    self.newWindow.destroy()

def save3(self):
    self.core  = []
    for i in range(self.na):
        self.core.append(eval(self.ent5[i].get()))
    self.newWindow.destroy()

def save4(self):
    m=0
    self.SigT = []
    for i in range(self.nmat):
        self.SigT.append([])
        for j in range(self.ng):
            self.SigT[i].append(eval(self.ent6[m].get())) 
            m+=1
    self.newWindow.destroy()

def save5(self):
    m=0
    self.SigF  = []
    for i in range(self.nmat):
        self.SigF.append([])
        for j in range(self.ng):
            self.SigF[i].append(eval(self.ent7[m].get())) 
            m+=1
    self.newWindow.destroy()

def save6(self):
    m=0
    self.NuSigF  = []
    for i in range(self.nmat):
        self.NuSigF.append([])
        for j in range(self.ng):
            self.NuSigF[i].append(eval(self.ent8[m].get())) 
            m+=1
    self.newWindow.destroy()

def save7(self):
    self.order   = int(self.ent0[8].get())
    self.SigS = []
    m=0
    for i in range(self.nmat):
        self.SigS.append([])
        for l in range(self.order+1):
            self.SigS[i].append([])
            for j in range(self.ng):
                self.SigS[i][l].append([])
                for n in range(self.ng):
                    self.SigS[i][l][j].append(eval(self.ent9[m].get()))
                    m+=1
    self.newWindow.destroy()

def save8(self):
    m=0
    self.Chi  = []
    for i in range(self.nmat):
        self.Chi.append([])
        for j in range(self.ng):
            self.Chi[i].append(eval(self.ent10[m].get())) 
            m+=1
    self.newWindow.destroy()
###### Drow geometry   
def Draw(self):
    filename = open('app/link/script.dir', "r" ).read()
    fmm_id = []
    assembly = []
    pin = []
    regmat = []
    nom    = []
    width_x = []
    width_y = []
    with open(filename) as json_data:
        data = json.load(json_data)
        nmat = data['data']['parameter']['Total number of materials']
        npc = data['data']['parameter']['Total number of pin cells']  
        na  = data['data']['parameter']['Total number of assemblies'] 
        core = data['data']['parameter']['Core']

        for i in range(na):
            assembly.append(data['data']['Assemblies'][i]['assembly'])

        for i in range(npc):
            pin.append(data['data']['PinCells'][i]['mat_fill'])

        Height = 1
        width = len(core)*len(pin[0])*len(assembly[0])
        fmm_id =numpy.zeros((width),dtype='i')
        i=0
        for j in range(len(core)):
            for k in range(len(assembly[0])):
                for m in range(len(pin[0])):
                    fmm_id[i] = pin[assembly[core[j]-1][k]-1][m]
                    i+=1
        nx = len(core)
        ny = 1
           
        nxx = len(assembly[0])
        nyy = 1
        NX = nxx*nx
        NY = ny*nyy
        width_x.append(data['data']['PinCells'][0]['width'])
        width_y = [2]
        nx =  len(width_x[0])*NX
        ny =  1
        xcm  = width_x[0]*NX
        ycm  = width_y[0]*NY
        for j in range(nmat):
            nom.append(data['data']['materials'][j]['name'])
        for i in range(npc):
            regmat.append(data['data']['PinCells'][i]['mat_fill'])
        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        widthx = [0]
        widthy = [0]
        somx = [0]
        somy = [0]
        for i in range(nx):
            widthx.append(xcm[i])
            somx.append(sum(widthx))

        widthy = [2.0]
        somy = [2.0]
        ycm = [2.0]
        rectangles = []
        red_patch = []
        mx = somx[0]
        my = somy[0]
            
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.77, box.height])
        for i in range(nx):
            for j in range(ny):
                rectangles.append(mpatch.Rectangle((somx[i],somy[j]), xcm[i], ycm[j],linewidth=0.0,edgecolor='k'))
        colr = colors = ['#ff6666','#ffcc99', '#99ff99', '#66b3ff','#c2c2f0','#ffb3e6', 
                             '#c2c2f0','#ffb3e6', '#c2c2f0','#ffb3e6', '#c2c2f0','#ffb3e6']
        for i in range(nmat):
            red_patch.append(mpatches.Patch(color=colr[i], label=nom[i]))
            
        n=0
        for r in rectangles:
            ax.add_artist(r) 
            r.set_facecolor(color=colr[int(fmm_id[n])-1])

            rx, ry = r.get_xy()
            cx = rx + r.get_width()/2.0
            cy = ry + r.get_height()/2.0
            n+=1

        ax.set_ylim((1,5))
        ax.set_xlim((min(somx), max(somx)))
            #ax.set_xticklabels([])
        ax.set_yticklabels([]) 
        ax.set_xlabel('X [cm]')
            #ax.set_ylabel('Y [cm]')
        ax.set_title('Color by Materials') 
        clb = plt.legend(handles=red_patch,loc='center left',title="Materials",
                         fontsize='small',bbox_to_anchor=(1, 0.5))
        plt.show()

def exit_editor(self):
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        self.root.destroy()
def data_up(self,event=None):
    self.ng    = int(self.ent0[0].get())
    self.nmat  = int(self.ent0[1].get())
    self.np    = int(self.ent0[2].get())
    self.nx    = int(self.ent0[3].get())
    self.nxa   = int(self.ent0[4].get())
    self.na    = int(self.ent0[5].get())
    self.order = int(self.ent0[8].get())+1
    if self.ng == 0:
        messagebox.showwarning("Warning", "Enter the number of energy group")
    elif self.nmat == 0:
        messagebox.showwarning("Warning", "Enter the number of materials")
    elif self.np == 0:
        messagebox.showwarning("Warning", "Enter the pin cells number")
    elif self.nx == 0:
        messagebox.showwarning("Warning", "Enter the x mesh pin cell number \n"+
                                 "(Each pin cell is approximated by a x cartesian grid)")  
    else:
        global filename  # 
        filename = open("app/input/input.json",'w')
        open('app/link/script.dir', "w" ).write(os.path.abspath(os.path.dirname( __file__)) +'/input/input.json')
        PATH = open(os.getcwd()+'/app/link/script.dir', "r" ).read()
        self.root.title(os.path.basename(PATH) + '- Sotution of the Transport Equation'
            ' by Multigroup Methods')
        filename.write('{ \n  "data": { \n    "parameter": { \n      "id": 100,')
        filename.write('\n      "Total number of energy groups": '+ self.ent0[0].get() +',')
        filename.write('\n      "Total number of materials": '+ self.ent0[1].get() +',')  
        filename.write('\n      "Total number of pin cells": '+ self.ent0[2].get() +',') 
        filename.write('\n      "Total number of assemblies": '+ self.ent0[5].get() +',')
        filename.write('\n      "Total number of active pin cells": '+ self.ent0[7].get() +',') 
        filename.write('\n      "Core": '+ str(self.core) +',')
        filename.write('\n      "Number of angular discretizations": '+ self.ent0[6].get() +',')
        filename.write('\n      "The l-order Legendre polynomial": '+ self.ent0[8].get() +',')
        filename.write('\n      "Maximum number of iterations": '+ self.ent0[9].get() +',')
        filename.write('\n      "Criterion of Keff convergence": '+ self.ent0[10].get())
        filename.write('\n    }, \n    "Assemblies": [')
        # loop on assembly
        for i in range(self.na):
            filename.write('\n      { \n        "id": '+ str(i+1) +', \n        "name": "Assembly '+ str(i+1) +'",') 
            filename.write('\n        "assembly": ' + str(self.assm[i]))
            if i == self.na-1:
                filename.write('\n      }')
            else:
                filename.write('\n      },') 
        filename.write('\n ], \n    "PinCells": [') 
        # loop on pin cell
        for i in range(self.np):
            filename.write('\n      { \n        "id": '+ str(i+1) +', \n        "name": "PinCell '+ str(i+1) +'",') 
            filename.write('\n        "width": ' + str(self.Delta[i])+',')
            filename.write('\n        "mat_fill": ' + str(self.REGMAT[i])+',')
            filename.write('\n        "fine_mesh": ' + str(self.NFMR[i]))
            if i == self.np-1:
                filename.write('\n      }')
            else:
                filename.write('\n      },') 
        filename.write('\n ], \n    "materials": [') 
        # loop on material
        for i in range(self.nmat):
            filename.write('\n      { \n        "id": '+ str(i+1) +', \n        "name": "material '+ str(i+1) +'",') 
            filename.write('\n        "XSTotal": ' + str(self.SigT[i][:])+',')
            filename.write('\n        "XSFission": ' + str(self.SigF[i][:])+',')
            filename.write('\n        "XSNuFission": ' + str(self.NuSigF[i][:])+',')
            filename.write('\n        "XSScatter Matrix":'+str(self.SigS[i][:][:][:])+',')
            filename.write('\n        "XSChi":  '+str(self.Chi[i][:]))
            if i == self.nmat-1:
                filename.write('\n      }')
            else:
                filename.write('\n      },')  
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
    a1 = Button(t2, text='Find All', underline=0,command=lambda:self.search_for(v.get(), c.get(), self.textPad, t2, e))
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
    filename = filedialog.askopenfilename(defaultextension=".json",
            filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
    open('app/link/script.dir', "w" ).write(str(filename))
    if filename == "": # If no file chosen.
        filename = None # Absence of file.
    else:
        self.root.title(os.path.basename(filename)) # Returning the basename of 'file'
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
       f = filedialog.asksaveasfilename(initialfile='input.json',defaultextension=".json",
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

def select02(self,enent=None):
    self.value02.get()
    open('app/link/script02.py', "w" ).write(self.value02.get())  

def select09(self,enent=None):
    self.value01.get()
    open('app/link/script01.py', "w" ).write(self.value01.get())  

def select10(self,enent=None):
    self.value10.get()
    open('app/link/script10.py', "w" ).write(self.value10.get())

def popup(self,event):
    self.cmenu.tk_popup(event.x_root, event.y_root, 0)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def powerpf(self,enent=None):
    #define plot size in inches (width, height) & resolution(DPI)
    fig = plt.figure(figsize=(5, 4), dpi=100)
    M00 = open('app/link/script00.py', "rb" ).read() 
    if int(M00) == 1:
        data = np.loadtxt('app/Output/PF_CP.H')
    elif int(M00) == 2:
        data = np.loadtxt('app/Output/PF_SN.H')
    elif int(M00) == 3:
        data = np.loadtxt('app/Output/PF_MOC.H')
    else:
        messagebox.showwarning("Warning", "select the calculation method")
    max_columns = 1
    max_rows = len(data)-1      
    y_pos = np.arange(1,max_rows+1,1)
    plt.bar(y_pos, data[1:], align='center',  facecolor='red', alpha=0.5)
    plt.xticks(y_pos)
    if int(M00) == 1:
        plt.title("CP Method")
    elif int(M00) == 2:
        plt.title("SN Method") 
    elif int(M00) == 3:
        plt.title("MOC")    
    plt.xlabel('Pin Cell')
    plt.ylabel('Normalized Pin Power Distribution')
    plt.show()

def plot(self,enent=None):
    #define plot size in inches (width, height) & resolution(DPI)
    fig = plt.figure(figsize=(5, 4), dpi=100)
    M00 = open('app/link/script00.py', "rb" ).read() 
    if int(M00) == 1:
        data = np.loadtxt('app/Output/FLUX_CP.H')
    elif int(M00) == 2:
        data = np.loadtxt('app/Output/FLUX_SN.H')
    elif int(M00) == 3:
        data = np.loadtxt('app/Output/FLUX_MOC.H')
    else:
        messagebox.showwarning("Warning", "select the calculation method")

    if int(len(data)) >= 0:
        matrix = []  
        for line in data:
            matrix.append(line)
        max_columns = len(matrix[0]) - 1
        max_rows = len(matrix)
        x = [matrix[rownum][0] for rownum in range(max_rows)]
        y = [[matrix[rownum][colnum + 1] for rownum in range(max_rows)]for colnum in range(max_columns)]
        p = [0]*max_columns
        name = ['OpenMC','CP','SN','MOC']
        tt = ['g--','o','k:','r']
        for i in range(max_columns):
            #p[i] = plt.plot(x,y[i] ,tt[i],label=name[i])
            p[i] = plt.plot(x,y[i] ,label="Group %s" %(max_columns-i),linewidth=1)
        if int(M00) == 1:
            plt.title("CP Method")
        elif int(M00) == 2:
            plt.title("SN Method") 
        elif int(M00) == 3:
            plt.title("MOC")    
        plt.xlabel('Distance  [cm]')
        #plt.xticks(range(1,52,5))
        plt.ylabel('Normalized Flux')
        plt.legend()
        plt.show()
    else:
        messagebox.showwarning("Warning", "Select More than a Fine Number of Meshes")
def geometry():
    print ('geometry')

def run(event=None):
    cmd = 'python3 main.py'
    proc = subprocess.Popen(shlex.split(cmd), stdout = subprocess.PIPE, stderr=subprocess.PIPE, encoding = 'utf8')
    a = None
    Test = None
    while 1:
        text = proc.stdout.readline()[:-1]
        if type(text) != str or text == '' and proc.poll() != None:
            break
        elif type(text) == str or text == '.':
            Test = str(a)
            print (text)

    if  Test == str(a):
        messagebox.showwarning("Warning", "Running case finished")
    else:
        messagebox.showwarning("Warning", "Check Error")

def compile():
    M00 = open('app/link/script00.py', "r" ).read() 
    if int(M00) == 1:
        if os.path.exists('app/SlabCP.so'):
            os.remove('app/SlabCP.so') 
        cmd = 'f2py3 -c app/sources/TRANSPORT_CP.f90 -m SlabCP'
        proc = subprocess.Popen(shlex.split(cmd), stdout = subprocess.PIPE, stderr=subprocess.PIPE, encoding = 'utf8')
        while 1:
            text = proc.stdout.readline()[:-1]
            if type(text) != str or text == '' and proc.poll() != None: 
                break
 
            elif type(text) == str and len(text) > 6:
                print (text)
        if os.path.exists('SlabCP.cpython-38-x86_64-linux-gnu.so'):
            os.rename('SlabCP.cpython-38-x86_64-linux-gnu.so', 'SlabCP.so')
        shutil.move('SlabCP.so', 'app')

    elif int(M00) == 2:
        if os.path.exists('app/SlabSN.so'):
            os.remove('app/SlabSN.so') 
        cmd = 'f2py3 -c app/sources/TRANSPORT_SN.f90 -m SlabSN'
        proc = subprocess.Popen(shlex.split(cmd), stdout = subprocess.PIPE, stderr=subprocess.PIPE, encoding = 'utf8')
        while 1:
            text = proc.stdout.readline()[:-1]
            if type(text) != str or text == '' and proc.poll() != None: 
                break
 
            elif type(text) == str and len(text) > 6:
                print (text)
        if os.path.exists('SlabSN.cpython-38-x86_64-linux-gnu.so'):
            os.rename('SlabSN.cpython-38-x86_64-linux-gnu.so', 'SlabSN.so')
        shutil.move('SlabSN.so', 'app')

    elif int(M00) == 3:
        if os.path.exists('app/SlabMOC.so'):
            os.remove('app/SlabMOC.so')
        cmd = 'f2py3 -c app/sources/TRANSPORT_MOC.f90 -m SlabMOC'
        proc = subprocess.Popen(shlex.split(cmd), stdout = subprocess.PIPE, stderr=subprocess.PIPE, encoding = 'utf8')
        while 1:
            text = proc.stdout.readline()[:-1]
            if type(text) != str or text == '' and proc.poll() != None: 
                break
 
            elif type(text) == str and len(text) > 6:
                print (text)
        if os.path.exists('SlabMOC.cpython-38-x86_64-linux-gnu.so'):
            os.rename('SlabMOC.cpython-38-x86_64-linux-gnu.so', 'SlabMOC.so')
        shutil.move('SlabMOC.so', 'app')
    else:
        messagebox.showwarning("Warning", "select the calculation method")

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

