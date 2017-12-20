
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

def gen_database(v, t, data_obj, outpath):

    obj = Utility.load_obj(data_obj)

    out_obj = '{}/syllable_object_{}.pickle'.format(outpath, t)

    out_list = []

    for syl in obj.syllables_list:
        if v[0] == 'all_vowel_type':
            if t == '01234':
                out_list.append(syl)
            elif syl.tone == int(t): 
                out_list.append(syl)
        elif syl.get_vowel_length_type() in v:
            if t == '01234':
                out_list.append(syl)
            elif syl.tone == int(t): 
                out_list.append(syl)

    print out_obj

    Utility.save_obj(SyllableDatabaseManagement(syllable_list=out_list), out_obj)

    pass

def check(v, t, obj_path):
    print obj_path
    obj = Utility.load_obj(obj_path)
    print '------------------------------------------'
    print v, t
    for syl in obj.syllables_list:
        print syl.get_vowel_length_type(), syl.tone

    pass

if __name__ == '__main__':

    base_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/gpr_syllable_obj/'

    data_obj = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/gpr_syllable_obj/Syllable_object.pickle'

    tone = ['0', '1', '2', '3', '4', '01234']
    # tone = ['0', '1', '2', '3', '4']
    # vowel_type = [['v', 'vv']]
    vowel_type = [['v', 'vv'], ['vn', 'vvn'], ['vsg', 'vvsg'], ['all_vowel_type']]

    for v in vowel_type:

        if len(v) == 2:
            vowel = 'v' + v[1]
        else:
            vowel = v[0]

        vowel_path = '{}/{}'.format(base_path, vowel)
        print vowel_path
        Utility.make_directory(vowel_path)
        for t in tone:
            # gen_database(v, t, data_obj, vowel_path)

            out_obj = '{}/syllable_object_{}.pickle'.format(vowel_path, t)
            check(v, t, out_obj)

    pass