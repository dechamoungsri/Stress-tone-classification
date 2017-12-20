
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

if __name__ == '__main__':


    syl_object_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/01_manual_labeling_object/syllable_all.pickle'
    syllable_management = Utility.load_obj(syl_object_path)

    for tone in [0,1,2,3,4,'01234']:

        all_vowel_syl = []
        vowel_type = ['v', 'vv', 'vn', 'vvn', 'vsg', 'vvsg']

        vowel_type_dict = dict()
        for v in vowel_type:
            vowel_type_dict[v] = []

        for syl in syllable_management.syllables_list:

            # y = syl.get_Y_features(Syllable.Training_feature_tonal_part_raw_remove_head_tail_interpolated, num_sampling=50,delta_bool=True, delta2_bool=True, exp=True)
            
            if syl.is_un_voice_tonal_file: continue

            if tone == '01234':
                all_vowel_syl.append(syl)
                vowel_type_dict[syl.get_vowel_length_type()].append(syl)
            else:
                if tone != syl.tone: continue
                all_vowel_syl.append(syl)
                vowel_type_dict[syl.get_vowel_length_type()].append(syl)

        print tone
        base_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/Tonal_object/remove_all_silence_file/'
        Utility.save_obj(SyllableDatabaseManagement(syllable_list=all_vowel_syl), '{}/{}/syllable_object_{}.pickle'.format(base_path, 'all_vowel_type', tone))
        for v in vowel_type:
            Utility.save_obj(SyllableDatabaseManagement(syllable_list=vowel_type_dict[v]), '{}/{}/syllable_object_{}.pickle'.format(base_path, v, tone))
            print v, len(vowel_type_dict[v])


    pass
