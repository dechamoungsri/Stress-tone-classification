#!/bin/csh

set base_path = "/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/01_Tonal_part_projection/"

echo "$base_path""log_run_tone_all.txt"

/usr/local/bin/python -u ./run_tone_all.py $base_path >! "$base_path""log_run_tone_all.txt"

