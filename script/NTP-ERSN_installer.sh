#!/bin/bash

# MAJ
#echo "UPGRADE IN PROGRESS..."
#sudo apt-get update
#sudo apt-get dist-upgrade
#sudo apt-get upgrade
#echo "UPGRADE COMPLETED !"


conda create -n py3k anaconda python=3.8
echo "--- installing the prerequisistes"  
# Python
sudo apt-get install python3.8
sudo apt-get install python3-tk
echo "Tkinter INSTALLATIO COMPLETED !"
sudo apt-get install python3-pip
pip3 install image
sudo apt-get install gfortran
echo "FORTRAN INSTALLATION COMPLETED !"
sudo apt install python3-numpy
sudo apt-get install python3-opengl
pip3 install matplotlib
 
echo "              *************************************************  "
echo "                         INSTALLATION was COMPLETED              "
echo "              *************************************************  "
echo " "
printf "Press 'CTRL+C' to exit : "
trap "exit" INT
while :
do
    sleep 10000 
done




