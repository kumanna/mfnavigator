#!/bin/sh

while read i;do
    AMFINAME=$(echo $i|awk 'BEGIN { FS = ":" } {print $1 }')
    MFNAME=$(echo $i|awk 'BEGIN { FS = ":" } {print $2 }')
    python3 manage.py importnavs --amcid $2 --amfinumber $AMFINAME --mfname "\"$MFNAME\"" --navfile $3
done < $1
