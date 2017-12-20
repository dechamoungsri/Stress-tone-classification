
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

def load_fix_list(path):
    out = []
    for f in Utility.list_file(path):
        if f.startswith('.'): continue
        for line in Utility.read_file_line_by_line('{}/{}'.format(path, f)):
            # print Utility.trim(line)
            out.append(Utility.trim(line))

    return out
    pass

def fix():

    base_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/Tonal_object/remove_all_silence_file/'

    fixed_list_path = '/work/w13/decha/Inter_speech_2016_workplace/Fix_stress_label/fix_list/'

    fixed_list = load_fix_list(fixed_list_path)

    fixed_list = np.array(fixed_list)

    for v in Utility.list_file(base_path):
        if v.startswith('.'): continue
        vowel_path = '{}/{}/'.format(base_path, v)
        for tone in Utility.list_file(vowel_path):
            if tone.startswith('.'): continue
            tone_file_path = '{}/{}'.format(vowel_path, tone)
            print tone_file_path
            syl_obj = Utility.load_obj(tone_file_path)

            for syl in syl_obj.syllables_list:
                # print syl.stress_manual
                if syl.name_index in fixed_list:
                    print syl.name_index, syl.stress_manual
                    if syl.stress_manual == 0:
                        syl.stress_manual = 1
                    else :
                        syl.stress_manual = 0
                    # print syl.name_index
            Utility.save_obj(syl_obj, tone_file_path)

    pass

def check_result():

    path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/Tonal_object/remove_all_silence_file//vvvsg//syllable_object_01234.pickle'

    obj = Utility.load_obj(path)
    for syl in obj.syllables_list:
        if syl.name_index == 'tscsd_manual_g37_14':
            print syl.name_index, syl.stress_manual

    pass

if __name__ == '__main__':

    fix()
    # check_result()

    pass
