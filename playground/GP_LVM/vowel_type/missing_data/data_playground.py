
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

    syllable_object = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/mix_object/current_version/all_vowel_type/syllable_object_01234.pickle'

    syllable_object = Utility.load_obj(syllable_object)

    syl = syllable_object.syllables_list[0]

    print syl.raw_data
    print syl.get_raw_with_missing_value(25, True, True)
    print len(syl.get_raw_with_missing_value(25, True, True))

    pass
