#!/bin/csh

echo start

set base_path = "/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/09_25lf0_to_compare_with_ann/"

set log = "$base_path""log_vvv_vvvn_tone_0_1_2_3_4_01234_dims_5_10.txt"

/usr/local/bin/python -u ./run.py $base_path >! "$log"
