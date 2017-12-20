
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

    obj = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/Tonal_object/version_5/remove_all_silence_file/vvvsg/syllable_object_1.pickle'

    syl_management = Utility.load_obj(obj)

    mix = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/mix_object/current_version/vvvsg/syllable_object_1.pickle'
    mix_management = Utility.load_obj(mix)

    n_old = []

    for syl in syl_management.syllables_list:
        if syl.stress_manual == '1':
            # print syl.name_index
            n_old.append(syl.name_index)

    n_new = []
    for syl in mix_management.syllables_list:
        if syl.stress_manual == '1':
            if 'manual' in syl.name_index:
            # print syl.name_index
                n_new.append(syl.name_index)

    print len(n_old), len(n_new)

    print n_old
    print n_new

    pass

