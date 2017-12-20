#!/bin/csh

echo start

set base_path = "/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/14_missing_data_no_consonant_50dims/"

set log = "$base_path""log_missing_vvv_vvvn_vvvsg_data.txt"
# set log = "$base_path""log_vvvsg_allvowel_tone_1_2_3_4_01234.txt"

/usr/local/bin/python -u ./run_vvv_vvvn_vvvsg.py $base_path >! "$log"

