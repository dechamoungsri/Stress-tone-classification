
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

    base_path = '/work/w2/decha/Data/GPR_data/label/09_stress_manual_labeling/utt/tsc/sd/'

    set_dict = dict()

    start_set, end_set = 'a', 'h'

    for sett in Utility.char_range(start_set, end_set):
        set_path = '{}/{}/'.format(base_path, sett)

        count = 0

        for f in Utility.list_file(set_path):
            if f.startswith('.'): continue
            file_path = '{}/{}'.format(set_path, f)
            for line in Utility.read_file_line_by_line(file_path):
                if 'stress: 1' in line:
                    count+=1

        set_dict[sett] = count

    for key in set_dict:
        print key, set_dict[key]

    pass
