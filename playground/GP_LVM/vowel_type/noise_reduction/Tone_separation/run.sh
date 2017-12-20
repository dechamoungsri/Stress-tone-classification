#!/bin/csh

set base_path = "/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/08_Tona_separation/"

set log = "$base_path""log_01234_all_vowel_type_tone.txt"

/usr/local/bin/python -u ./run.py $base_path >! "$log"

