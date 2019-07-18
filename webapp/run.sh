#!/bin/bash
#
# Script     : run.sh
# Usage      : ./run.sh /path/to/to/input
# Author     : Giuseppe Totaro
# Date       : 08/28/2017 [MM-DD-YYYY]
# Last Edited: 
# Description: This scripts runs the StandardsExtractingContentHandler to 
#              extract the standard references from every file in a directory. 
# Notes      : 
#

function usage() {
	echo "Usage: run.sh /path/to/input threshold"
	exit 1
}

INPUT=""
OUTPUT=""
UMLS_USER=""
UMLS_PASS=""
CTAKES_HOME=""

if [ ! -e lib/tika-app-1.16.jar ]
then
	echo "Error: this program requires Apache Tika 1.16!"
	echo "Please provide \"tika-app-1.16.jar\" file in the \"lib\" folder and try again."
	exit 1
fi

if [ $# -lt 2 ]
then
	usage
fi

INPUT="$1"
THRESHOLD="$2"

java -cp ./lib/tika-app-1.16.jar:./bin StandardsExtractor "$INPUT" $THRESHOLD 2> /dev/null
