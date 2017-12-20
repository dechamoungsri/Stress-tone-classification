
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

import numpy as np
import matplotlib.pyplot as plt

def add_feature(syllables_object):
    
    for syl in syllables_object.syllables_list:
        syl.gen_separated_vowel_final_consonant()

    pass

if __name__ == '__main__':

    base = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/Tonal_object/remove_all_silence_file/'

    vowel_type = ['all_vowel_type', 'v', 'vv', 'vn', 'vvn', 'vsg', 'vvsg']
    tones = ['0', '1', '2', '3', '4', '01234']

    out = '/home/h1/decha/Dropbox/Inter_speech_2016/temporary_output/'

    for v in vowel_type:
        for t in tones:
            print v, t 
            base_path = '{}/{}/syllable_object_{}.pickle'.format(base,v,t)
            syl_obj = Utility.load_obj(base_path)
            # add_feature(syl_obj)
            # Utility.save_obj(syl_obj, base_path)

            if len(syl_obj.syllables_list) != 0:
                tar = syl_obj.syllables_list[0]
                print tar.consonant, tar.vowel, tar.final_consonant, tar.tone
                tar.plot_by_phoneme('{}/{}_{}_by_phone.pdf'.format(out, v, t) )
            else :
                print v, t ,'is None'
            # syl_obj.syllables_list[0].plot_by_phoneme('{}/{}_{}_by_phone.pdf'.format(out, v, t) )
            # sys.exit()

    pass

