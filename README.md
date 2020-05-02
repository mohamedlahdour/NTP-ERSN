# Neutron Transport Package NTP-ERSN

In this project we develop a package NTP-ERSN to solve a neutron transport equation.


NTP-ERSN (Neutron Transport Package-Equipe de la Radiation et des systèmes nucleaires), is an open-source code, developed at the Abdelmalek Essaadi University, Tetouan, Morocco, written by FORTRAN90 for educational purposes to solve the equation of multi-group neutron transport in steady-state using a deterministic approach [Lahdour et al., 2019a](https://doi.org/10.1016/j.apradiso.2018.12.004) such as:


Neutron Transport Package NTP-ERSN(Open Neutron Transport Package from the Radiations and Nuclear Systems Group), is an open-source code written in FORTRAN90 for a pedagogical purpose to solve the steady-state multigroup neutron transport equation using either:

* Collision Probability Method (CP) in One-Dimensional cartesian geometry. 
* Discrete Ordinate Method (SN) in One-Dimensional cartesian geometry. 
* Method of Characteristics (MOC) in One-Dimensional cartesian geometry. 

The code, including the graphical user interface is developed and maintained by Mohamed LAHDOUR (PhD student) and Prof. Tarek EL BARDOUNI from University Abdelmalek Essaadi Tetouan Morocco .

You could contact Mohamed Lahdour : mohamedlahdour@gmail.com or mlahdour@uae.ac.ma

The directory structure of NTP-ERSN
=============

        cd NTP-ERSN/app/sources

This directory contains NTP-ERSN source files written in FORTRAN90 such as:

* TRANSPORT_1D_CP.F90 (for the pollision probablity method),
* TRANSPORT_1D_SN.F90 (for the discrete ordinate method),
* TRANSPORT_1D_MOC.F90 (for the method of characteristics)

        cd NTP-ERSN/app

This directory contains the modules generated by f2py namely CP1D.so, SlabSN.so and SlabMOC.so which will be imported by python as modules.

        cd NTP-ERSN

This directory contains the python files for Graphical User Interface (GUI)

Quick Install Guide
=============

This quick install guide outlines the basic steps needed to install NTP-ERSN on your computer.

If you do not wish to follow these steps, the [NTP-ERSN/app/script](https://github.com/mohamedlahdour/NTP-ERSN/tree/master/script) directory is provided with a script [NTP-ERSN_installer.sh](https://github.com/mohamedlahdour/NTP-ERSN/tree/master/script) to download the prerequisites automatically.

Installing on Linux
-------------------

1. If you are using Ubuntu 18.10 or newer, open a terminal in a GNU/Linux box then install gfortran with the following commands:

        sudo apt-get update
        sudo apt-get install gfortran

2. You need to install numpy (F2PY) and matplotlib library ... to run the package OpenNTP:

        sudo apt-get install python-pip
        sudo apt-get install python-numpy
        sudo apt-get install python-imaging-tk
        sudo apt-get install python-opengl
        pip install numpy matplotlib
        pip install pygame
        pip install pygmyplot
        pip install image


3. You need to install Tkinter on Ubuntu with python to run the GUI:

        sudo apt-get install python-tk 

4. Install the **NTP-ERSN** package

        git clone  https://github.com/mohamedlahdour/NTP-ERSN.git

5. Import the **NTP-ERSN** and run the package in the following way:
    
         cd NTP-ERSN
    
* If you want to use it through a graphical interface:

         $ python gui.py

* If you want to use it through a command prompt (Terminal):

        $ python main.py

User's Guide
============

1. Graphical User Interface
--------------------------

A graphical user interface written in Python programing language has been developed to simplify the use of package **NTP-ERSN**.
After starting the software by typing the following command line in a terminal:

         cd NTP-ERSN
         $ python gui.py

A main window (GUI) of the package **NTP-ERSN** an Ubuntu Linux machine will be displayed as in Figure bellow.

![Image 0](https://github.com/mohamedlahdour/NTP-ERSN/tree/master/doc/_images/gui1.png)

This software is a free software; you can redistribute it and / or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version. For the complete text of the license see the GPL-web page.
