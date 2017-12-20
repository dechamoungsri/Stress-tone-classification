
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

    dur_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_level_prediction/01_single_space/testrun/out/tsc/a-i/speech_param/a-i/demo/seed-00/M-1024/B-1024/num_iters-5/dur/param_mean/tscsdj02.npy'


    obj = np.load(dur_path)
    # print obj

    json = '/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/playground/generate_json/latent_data/tscsdj02.lab.json'
    np.set_printoptions(precision=3)
    json = Utility.load_json(json)
    for idx, j in enumerate(json):
        d = np.array(j['duration'])
        print d
        print obj[idx]
        print '---------------------------'

    pass
