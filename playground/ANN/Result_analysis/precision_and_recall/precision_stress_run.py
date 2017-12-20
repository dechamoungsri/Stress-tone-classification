
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

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

def get_data_from_prefix_suffix(path, prefix, suffix, fold):

    data = np.array([])

    for i in range(fold):
        object_path = '{}/{}{}{}'.format(path, prefix, i, suffix)
        # print object_path
        obj = Utility.load_obj(object_path)
        data = np.append(data, obj)

    # print data, len(data)
    return data

def cal_all_comparison(real, pred):

    precis = precision_score(real, pred, average=None)  
    recall = recall_score(real, pred, average=None)
    f1 = f1_score(real, pred, average=None)

    # print 'Precis : {}'.format(precis)
    # print 'Recal : {}'.format(recall)
    # print 'F1 : {}'.format(f1)

    return (precis, recall, f1)

    pass

def cal_precision_recall__f1_score(path, fold, v, t, dim):

    real_object = get_data_from_prefix_suffix(path, 'Plain_data_fold_', '_real.npy', fold) 
    predicted_plain_data = get_data_from_prefix_suffix(path, 'Plain_data_fold_', '_predicted.npy', fold) 
    predicted_latent_data = get_data_from_prefix_suffix(path, 'Latent_data_fold_', '_predicted.npy', fold) 

    vowel['{}_{}_{}'.format(t, dim, 'real')] = np.append(vowel['{}_{}_{}'.format(t, dim, 'real')], real_object)
    vowel['{}_{}_{}'.format(t, dim, 'raw')] = np.append(vowel['{}_{}_{}'.format(t, dim, 'raw')], predicted_plain_data)
    vowel['{}_{}_{}'.format(t, dim, 'latent')] = np.append(vowel['{}_{}_{}'.format(t, dim, 'latent')], predicted_latent_data)

    # if 0 == len(np.where(predicted_plain_data==1)[0]):
    #     print np.where(predicted_plain_data==1)

    print 'Plain data'
    precis, recall, f1 = cal_all_comparison(real_object, predicted_plain_data)

    result['{}_{}_{}_{}_{}'.format(v, t, dim, 'un', 'raw')] = f1[0]
    result['{}_{}_{}_{}_{}'.format(v, t, dim, 'st', 'raw')] = f1[1]

    print 'Latent data'
    precis, recall, f1 = cal_all_comparison(real_object, predicted_latent_data)

    result['{}_{}_{}_{}_{}'.format(v, t, dim, 'un', 'latent')] = f1[0]
    result['{}_{}_{}_{}_{}'.format(v, t, dim, 'st', 'latent')] = f1[1]

    # sys.exit()

if __name__ == '__main__':

    # base_path = '/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/09_25lf0_to_compare_with_ann/all_vowel_type/input_dims_3/delta-False_delta-delta-False/BGP_LVM_Tone_01234/feed_forword_ann/25lf0/Latent_data_fold_0_predicted.npy'
# /work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/09_25lf0_to_compare_with_ann/vvv/input_dims_3/delta-False_delta-delta-False/BGP_LVM_Tone_01234/feed_forword_ann/25lf0_50b_iters_ann/Latent_data_fold_2_predicted.npy
    base_path = '/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/09_25lf0_to_compare_with_ann/'

    # base_path = '/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/09b_25lf0_fix_some_500_max_iters/'

    # vowel_type = ['vvv', 'vvvn', 'vvvsg', 'all_vowel_type']
    vowel_type = ['vvv', 'vvvn', 'vvvsg']
    # vowel_type = ['vvv']
    input_dims = ['3', '5', '10']
    tones = ['0', '1', '2', '3', '4', '01234']

    ann_type = '25lf0'

    number_of_fold = 3

    result = dict()

    for v in vowel_type:
        for t in tones:
            for dim in input_dims:
                for s in ['un', 'st']:
                    for data in ['raw', 'latent']:
                        result['{}_{}_{}_{}_{}'.format(v, t, dim, s, data)] = -1

    vowel = dict()
    for t in tones:
        for dim in input_dims:
            for data in ['raw', 'latent', 'real']:
                vowel['{}_{}_{}'.format(t, dim, data)] = np.array([])

    for v in vowel_type:
        for t in tones:
            for dim in input_dims:
                ann_path = '{}/{}/input_dims_{}/delta-False_delta-delta-False/BGP_LVM_Tone_{}/feed_forword_ann/{}/'.format(base_path, v, dim, t, ann_type)
                print '--------------------------------------Start----------------------------------------'
                print 'Vowel : {}, Dim : {}, Tone : {}'.format(v, dim, t)
                try:
                    cal_precision_recall__f1_score(ann_path, number_of_fold, v, t, dim)
                except: 
                    print 'Error'
                    print ann_path
                print '---------------------------------------End------------------------------------------'

    for v in vowel_type:
        for dim in input_dims:
            for data in ['raw', 'latent']:
                for s in ['un', 'st']:
                    print s
                    tone_line = ''
                    for t in tones:
                        p = result['{}_{}_{}_{}_{}'.format(v, t, dim, s, data)] 
                        p = '{:.2%}'.format(p)
                        # p = '{}_{}_{}_{}_{}'.format(v, t, dim, s, data)
                        tone_line = tone_line + p + ','
                    print tone_line

    for s, ss in enumerate(['un', 'st']):
        for data in ['raw', 'latent']:
            for dim in input_dims:
                tone_line = ''
                for t in tones:

                    print '{}_{}_{}_{}'.format(t, dim, s, data)

                    real = vowel['{}_{}_{}'.format(t, dim, 'real')]
                    dat = vowel['{}_{}_{}'.format(t, dim, data)]

                    print real
                    print dat, len(np.where(dat==1)[0])

                    precis, recall, f1 = cal_all_comparison(real, dat)

                    p = f1[s]
                    p = '{:.2%}'.format(p)
                    # p = '{}_{}_{}_{}'.format(t, dim, s, data)
                    tone_line = tone_line + p + ','
                print tone_line

    pass
