#!/bin/sh

MFLIST=$(sed 's/^\(......\).*/\1/' $1)

for i in $MFLIST; do
    echo -n "$i: "
    grep "$i" $2|tail -1|awk 'BEGIN { FS = ";" } { print $NF }';
done
