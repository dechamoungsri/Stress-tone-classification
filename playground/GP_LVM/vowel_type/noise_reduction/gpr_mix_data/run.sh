#!/bin/csh

echo start

set base_path = "/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/06_Tonal_part_projection_noise_reduction-250-iters-opt/"

set log = "$base_path""log_allvowel_tone_0_1_2_3_4.txt"

/usr/local/bin/python -u ./run.py $base_path >! "$log"

