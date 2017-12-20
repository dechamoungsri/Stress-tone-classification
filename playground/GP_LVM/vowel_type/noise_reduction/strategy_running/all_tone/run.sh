#!/bin/csh

set base_path = "/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/05_Tonal_part_projection_noise_reduction/"

set log = "$base_path""log.txt"

/usr/local/bin/python -u ./run.py $base_path >! "$log"

