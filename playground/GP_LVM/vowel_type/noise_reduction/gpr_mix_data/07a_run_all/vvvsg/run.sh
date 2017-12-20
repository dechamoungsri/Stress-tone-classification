#!/bin/csh

echo start

set base_path = "/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/07a_no_too_short/"

set log = "$base_path""log_vvvsg_tone_1.txt"

/usr/local/bin/python -u ./run.py $base_path >! "$log"

