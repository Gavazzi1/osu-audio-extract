#!/bin/bash

rm -f *.osz
mkdir -p tmp
rm -f tmp/*
unzip -q "$1"
newdir="$(echo $1 | cut -d'.' -f1)"
mkdir -p "$newdir"

for i in *.osz; do
    unzip -q "$i" -d tmp
    audiofn="$(grep -h AudioFilename tmp/*.osu | head -n 1 | rev | cut -d':' -f1 | rev)"
    audiofn="$(echo "$audiofn" | sed 's/^[ \t]*//;s/[ \t]*$//')"  # remove leading/trailing space
    audiofn="$(echo "$audiofn" | rev | cut -c2- | rev)"  # remove trailing \r

    titleline="$(grep -h Title: tmp/*.osu | head -n 1)"
    songname="${titleline##Title:}"
    songname="$(echo $songname | awk '{$1=$1};1')"
    songname="$(echo $songname | rev | cut -c2- | rev)"
    songname="${songname///}" # remove forward slashes (illegal in linux)

    ext="$(echo $audiofn | rev | cut -d'.' -f1 | rev)"
    echo "$songname - $audiofn"

    cp "tmp/$audiofn" "$newdir/$songname.$ext"

    rm -r tmp
done
rm *.osz
