#!/bin/csh

set base_path = "/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/03_Tonal_part_projection_dct/"

set log = "$base_path""log_run_all_every.txt"

/usr/local/bin/python -u ./run_dct.py $base_path >! $log

