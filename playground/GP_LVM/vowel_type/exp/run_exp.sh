#!/bin/csh

set base_path = "/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/02_Tonal_part_projection_exp/"

echo "$base_path""log_exp_tone_all.txt"

/usr/local/bin/python -u ./run_exp.py $base_path >! "$base_path""log_exp_tone_all.txt"

