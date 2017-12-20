
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

    base_path = '/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/10_tone_classification/'
    for v in Utility.list_file(base_path):
        if '.' in v : continue
        for dims in Utility.list_file('{}/{}/'.format(base_path, v)):
            if '.' in dims  : continue
            for delta in Utility.list_file('{}/{}/{}/'.format(base_path, v, dims)):
                if '.' in delta  : continue
                for tone in Utility.list_file('{}/{}/{}/{}/'.format(base_path, v, dims, delta)):
                    if '.' in tone  : continue
                    tone_path = '{}/{}/{}/{}/{}/'.format(base_path, v, dims, delta, tone)
                    print tone_path

                    gp_model = '{}/GP_model.npy'.format(tone_path)
                    if Utility.is_file_exist(gp_model):
                        m = Utility.load_obj(gp_model)
                        data = m.X.mean
                        data = np.array(data)
                        # print data
                        Utility.save_obj(data, '{}/readable_gp_model.npy'.format(tone_path))
                        # sys.exit()

    pass
