#!/bin/csh

set base_path = "/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/06_Tonal_part_projection_noise_reduction-250-iters-opt/"

set log = "$base_path""log_separated_tone.txt"

/usr/local/bin/python -u ./run.py $base_path >! "$log"

