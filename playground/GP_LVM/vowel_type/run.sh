#!/bin/csh

set base_path = "/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/01_Tonal_part_projection/"

set log = "$base_path""log_run_tone_separated2.txt"

/usr/local/bin/python -u ./run.py $base_path >! "$log"

