#!/bin/csh

echo start

set base_path = "/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/11_missing_data/"

set log = "$base_path""log_missing_data_234.txt"
# set log = "$base_path""log_vvvsg_allvowel_tone_1_2_3_4_01234.txt"

/usr/local/bin/python -u ./run.py $base_path >! "$log"

