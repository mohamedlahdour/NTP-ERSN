#!/bin/bash

# MAJ
#echo "UPGRADE IN PROGRESS..."
#sudo apt-get update
#sudo apt-get dist-upgrade
#sudo apt-get upgrade
#echo "UPGRADE COMPLETED !"

echo "--- installing the must-have pre-requisites"  
# Python
sudo apt-get install python-tk
echo "Tkinter INSTALL COMPLETED !"
sudo apt-get install python-pip
pip install pygmyplot
pip install image
sudo apt-get install gfortran
echo "FORTRAN INSTALL COMPLETED !"
sudo apt install python-numpy
pip install pygame
sudo apt-get install python-opengl
sudo apt-get install python-matplotlib
 
echo "              *************************************************  "
echo "                       INSTALL COMPLETED WITH SUCCES             "
echo "              *************************************************  "
echo " "
printf "Press 'CTRL+C' to exit : "
trap "exit" INT
while :
do
    sleep 10000 
done




