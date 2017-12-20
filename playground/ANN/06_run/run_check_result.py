
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

from sklearn.metrics import f1_score

def cal_F1(tones, vowel, m, base, types):

    real = np.array( [] )
    predicted = np.array( [] )

    for v in vowel:
        for t in tones:
            path = '{}/{}/input_dims_10/delta-True_delta-delta-True/BGP_LVM_Tone_{}/feed_forword_ann/{}/'.format(base, v, t, m)
            for fold in range(3):
                real_obj = Utility.load_obj( '{}/{}_data_fold_{}_real.npy'.format(path, types, fold) )
                real = np.append(real, real_obj)

                predicted_obj = Utility.load_obj( '{}/{}_data_fold_{}_predicted.npy'.format(path, types,fold) )
                predicted = np.append(predicted, predicted_obj)

    print tones, m
    print f1_score(real, predicted, average=None) 

    pass

if __name__ == '__main__':

     # Plain_data_fold_2_predicted.npy
     # /work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/09_25lf0_to_compare_with_ann/vvvsg/input_dims_10/delta-True_delta-delta-True/BGP_LVM_Tone_4/feed_forword_ann/50lf0_til_0_001/Plain_data_fold_2_real.npy
     # /work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/09_25lf0_to_compare_with_ann/vvvsg/input_dims_10/delta-True_delta-delta-True/BGP_LVM_Tone_4/feed_forword_ann/50lf0_til_coverage/Plain_data_fold_2_real.npy
# Latent_data_fold_2_real.npy
    base = '/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/09_25lf0_to_compare_with_ann/'

    tone_list = [['0'], ['1'], ['2'], ['3'], ['4'], ['0', '1', '2', '3', '4'] ]
    vowel = ['vvv', 'vvvn', 'vvvsg']

    method = ['50lf0_real_til_0_006']

    for m in method:
        for tones in tone_list:
            cal_F1(tones, vowel, m, base, 'Plain')
            print '--------------------------'

    base = '/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/06_Tonal_part_projection_noise_reduction-250-iters-opt/'

    method = ['50lf0_latent_til_0_006']

    for m in method:
        for tones in tone_list:
            cal_F1(tones, vowel, m, base, 'Latent')
            print '--------------------------'

    pass
