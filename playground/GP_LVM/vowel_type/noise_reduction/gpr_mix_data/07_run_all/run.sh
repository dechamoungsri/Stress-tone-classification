#!/bin/csh

echo start

set base_path = "/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/07_06with_mix_data/"

set log = "$base_path""log_allvowel_tone_all_01234.txt"

/usr/local/bin/python -u ./run.py $base_path >! "$log"

