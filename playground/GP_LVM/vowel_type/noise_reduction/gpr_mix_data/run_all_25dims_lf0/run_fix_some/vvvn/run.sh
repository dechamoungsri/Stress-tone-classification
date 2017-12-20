#!/bin/csh

echo start

set base_path = "/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/09b_25lf0_fix_some_500_max_iters/"

set log = "$base_path""log_vvvn_all_tone_dims_5_10.txt"
# set log = "$base_path""log_vvvsg_allvowel_tone_1_2_3_4_01234.txt"

/usr/local/bin/python -u ./run.py $base_path >! "$log"

