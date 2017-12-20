
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

    path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/Tonal_object/remove_all_silence_file/'

    for v in ['v', 'vn', 'vsg']:

        outpath = '{}/vv{}/'.format(path, v)
        Utility.make_directory(outpath)

        for t in ['0','1','2','3','4','01234']:
            vv = 'v' + v
            v_obj = Utility.load_obj('{}/{}/syllable_object_{}.pickle'.format(path, v, t))
            vv_obj = Utility.load_obj('{}/{}/syllable_object_{}.pickle'.format(path, vv, t))

            vvv_obj_list = v_obj.syllables_list + vv_obj.syllables_list
            print 'vv' + v, t, len(vvv_obj_list)
            vvv_obj = SyllableDatabaseManagement(syllable_list=vvv_obj_list)
            Utility.save_obj(vvv_obj, '{}/vv{}/syllable_object_{}.pickle'.format(path, v, t))

    pass
