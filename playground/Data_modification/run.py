
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

def add_stress(sil_list, database):

    for syl in database.syllables_list:
        name_index = syl.name_index
        # print name_index
        if name_index in sil_list:
            syl.stress_manual = '1'
            # if syl.duration < 45:
                # print name_index, syl.duration

    pass

if __name__ == '__main__':

    vowel_type = ['vvv', 'vvvn', 'vvvsg', 'all_vowel_type']
    tones = ['0', '1', '2', '3', '4', '01234']

    sil_list = Utility.load_obj('/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/gpr_syllable_obj/gpr_followed_by_sil_list.npy')

    for v in vowel_type:
        for t in tones:
            count = 0
            print v, t
            base = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/mix_object/{}/syllable_object_{}.pickle'.format(v, t)
            obj = Utility.load_obj(base)
            # add_stress(sil_list, obj)

            # Utility.save_obj(obj, base)

            for syl in obj.syllables_list:
                if syl.name_index in sil_list:
                    # print syl.name_index, syl.stress_manual
                    count += 1

            print count

            # sys.exit()
    pass
