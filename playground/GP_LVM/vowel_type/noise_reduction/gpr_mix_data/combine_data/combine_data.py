
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

    gpr_base_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/gpr_syllable_obj/'
    manual_base_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/Tonal_object/remove_all_silence_file/'

    out = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/mix_object/'

    tone = ['0', '1', '2', '3', '4', '01234']
    # tone = ['0', '1', '2', '3', '4']
    # vowel_type = [['v', 'vv']]
    vowel_type = [ 'vvv', 'vvvn', 'vvvsg', 'all_vowel_type']

    for v in vowel_type:

        for t in tone:
            gpr = Utility.load_obj('{}/{}/syllable_object_{}.pickle'.format(gpr_base_path, v, t))
            manual = Utility.load_obj('{}/{}/syllable_object_{}.pickle'.format(manual_base_path, v, t))
            # mix_syls = gpr.syllables_list + manual.syllables_list

            # mix_out_path = '{}/{}/'.format(out, v)
            # Utility.make_directory(mix_out_path)

            # Utility.save_obj(SyllableDatabaseManagement(syllable_list=mix_syls), '{}/{}/syllable_object_{}.pickle'.format(out, v, t))

            print len(gpr.syllables_list)
            print len(manual.syllables_list)

            print len(Utility.load_obj('{}/{}/syllable_object_{}.pickle'.format(out, v, t)).syllables_list)

    pass