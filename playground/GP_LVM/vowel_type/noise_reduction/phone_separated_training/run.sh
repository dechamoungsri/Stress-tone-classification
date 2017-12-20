#!/bin/csh

set base_path = "/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/04_Tonal_part_projection_phone_separated/"

set log = "$base_path""log.txt"

/usr/local/bin/python -u ./run.py $base_path >! "$log"

