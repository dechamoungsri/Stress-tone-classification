
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../')
sys.path.append('../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/')
import matplotlib.mlab as mlab
from tool_box.util.utility import Utility
import scipy.stats as stats
from DataModel.Syllables.Syllable import Syllable
from DataModel.Syllables.SyllableDatabaseManagement import SyllableDatabaseManagement

import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    # path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/gpr_syllable_obj/Syllable_object.pickle'

    path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/Tonal_object/remove_all_silence_file/all_vowel_type/syllable_object_01234.pickle'

    syls = Utility.load_obj(path)
    tone = [0,0,0,0,0]
    for v in ['v', 'vv', 'vn', 'vvn', 'vsg', 'vvsg'] : 
    # for v in ['v', 'vv'] : 
        print v
        for syl in syls.syllables_list:
            if syl.get_vowel_length_type() == v:
                # if syl.duration > 40:
                if syl.stress_manual == '1':
                    tone[syl.tone]+=1
    for t in tone :
        print t

    pass