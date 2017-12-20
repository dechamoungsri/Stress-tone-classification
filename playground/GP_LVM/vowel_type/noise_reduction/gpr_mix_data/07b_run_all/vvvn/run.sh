#!/bin/csh

echo start

set base_path = "/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/07b_07a_manual/"

set log = "$base_path""log_vvvn_tone_01234.txt"

/usr/local/bin/python -u ./run.py $base_path >! "$log"

