#!/bin/bash
#
# Script     : build.sh
# Usage      : ./build.sh /path/to/input
# Author     : Giuseppe Totaro
# Date       : 08/28/2017 [MM-DD-YYYY]
# Last Edited: 
# Description: This scripts compiles all .java files. 
# Notes      : 
#

if [ ! -e lib/tika-app-1.16.jar ]
then
	echo "Error: this program requires Apache Tika 1.16!"
	echo "Please provide \"tika-app-1.16.jar\" file in the \"lib\" folder and try again."
	exit 1
fi

mkdir -p bin

for file in $(find . -name "*.java" -print)
do
	javac -cp ./:./lib/tika-app-1.16.jar:./lib/junit-4.12.jar:./src -d ./bin ${file}
done
