#!/bin/csh

echo start

set base_path = "/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/12_missing_data_all/"

set log = "$base_path""log_missing_vvvn_data.txt"
# set log = "$base_path""log_vvvsg_allvowel_tone_1_2_3_4_01234.txt"

/usr/local/bin/python -u ./run_vvvn.py $base_path >! "$log"

