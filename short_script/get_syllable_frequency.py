import sys
sys.path.append('../')
sys.path.append('../../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')


import re
import operator

from tool_box.util.utility import Utility

object_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/mix_syllable_obj/mix_syllable_all.pickle'

syllable_object = Utility.load_obj(object_path)

freq = dict()

for syl in syllable_object.syllables_list:
    phoneme = syl.get_syllable_phoneme()
    if phoneme in freq:
        freq[phoneme]+= 1
    else : 
        freq[phoneme] =1

sorted_freq = sorted(freq.items(), key=operator.itemgetter(1))

for s in sorted_freq:
    sys.stdout.write('\'{}\','.format(s[0]))
