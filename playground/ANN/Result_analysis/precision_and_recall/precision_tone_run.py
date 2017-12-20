
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

    return (precis, recall, f1)

    pass

def cal_precision_recall__f1_score(path, fold, v, dim):

    real_object = get_data_from_prefix_suffix(path, 'Plain_data_fold_', '_real.npy', fold) 
    predicted_plain_data = get_data_from_prefix_suffix(path, 'Plain_data_fold_', '_predicted.npy', fold) 
    predicted_latent_data = get_data_from_prefix_suffix(path, 'Latent_data_fold_', '_predicted.npy', fold) 

    # if 0 == len(np.where(predicted_plain_data==1)[0]):
    #     print np.where(predicted_plain_data==1)

    if 'No_duration' in v:
        dur = 'No_duration'
    else :
        dur = 'Duration'

    vowel['{}_{}_{}'.format(dur, dim, 'real')] = np.append(vowel['{}_{}_{}'.format(dur, dim, 'real')], real_object)
    vowel['{}_{}_{}'.format(dur, dim, 'raw')] = np.append(vowel['{}_{}_{}'.format(dur, dim, 'raw')], predicted_plain_data)
    vowel['{}_{}_{}'.format(dur, dim, 'latent')] = np.append(vowel['{}_{}_{}'.format(dur, dim, 'latent')], predicted_latent_data)

    plain_precis, plain_recall, plain_f1 = cal_all_comparison(real_object, predicted_plain_data)
    latent_precis, latent_recall, latent_f1 = cal_all_comparison(real_object, predicted_latent_data)

    print 'Precision score : '
    print plain_precis
    print latent_precis

    print 'Recall score : '
    print plain_recall
    print latent_recall

    print 'F1 score : '
    print plain_f1
    print latent_f1

    result['{}_{}_{}'.format(v, dim, 'raw')] = plain_f1
    result['{}_{}_{}'.format(v, dim, 'latent')] = latent_f1

    # sys.exit()

if __name__ == '__main__':

    # base_path = '/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/09_25lf0_to_compare_with_ann/all_vowel_type/input_dims_3/delta-False_delta-delta-False/BGP_LVM_Tone_01234/feed_forword_ann/25lf0/Latent_data_fold_0_predicted.npy'
# /work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/09_25lf0_to_compare_with_ann/vvv/input_dims_3/delta-False_delta-delta-False/BGP_LVM_Tone_01234/feed_forword_ann/25lf0_50b_iters_ann/Latent_data_fold_2_predicted.npy
    base_path = '/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/10_tone_classification/'

    # base_path = '/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/09b_25lf0_fix_some_500_max_iters/'

    vowel_type = ['vvv', 'No_duration_vvv', 'vvvn', 'No_duration_vvvn', 'vvvsg', 'No_duration_vvvsg', 'all_vowel_type', 'No_duration_all_vowel_type']

    input_dims = ['3', '5', '10']
    tones = ['01234']

    ann_type = '25lf0_fix_b'

    number_of_fold = 3

    result = dict()
    for v in vowel_type:
        for dim in input_dims:
            for data in ['raw', 'latent']:
                result['{}_{}_{}'.format(v, dim, data)] = -1

    vowel = dict()
    for v in ['No_duration', 'Duration']:
        for dim in input_dims:
            for data in ['raw', 'latent', 'real']:
                vowel['{}_{}_{}'.format(v, dim, data)] = np.array([])

    for v in vowel_type:
        for dim in input_dims:
            for t in tones:

                print 'Vowel : {}, Dim : {}, Tone : {}'.format(v, dim, t)

                ann_path = '{}/{}/input_dims_{}/delta-False_delta-delta-False/BGP_LVM_Tone_{}/feed_forword_ann/{}/'.format(base_path, v, dim, t, ann_type)
                # print ann_path
                cal_precision_recall__f1_score(ann_path, number_of_fold, v, dim)

                print '----------------------------------------------------------------------------------------'

    # for v in vowel_type:
    #     for data in ['raw', 'latent']:
    #         for dim in input_dims:
    #             # print '{}_{}_{}'.format(v, dim, data)
    #             tone_line = ''
    #             for f in result['{}_{}_{}'.format(v, dim, data)] :
    #                 p = f
    #                 p = '{:.2%}'.format(p)
    #                 # p = '{}_{}_{}_{}'.format(t, dim, s, data)
    #                 tone_line = tone_line + p + ','
    #             print tone_line

    for v in ['No_duration', 'Duration']:
        for data in ['raw', 'latent']:
            for dim in input_dims:
                # print '{}_{}_{}'.format(v, dim, data)
                real = vowel['{}_{}_{}'.format(v, dim, 'real')] 
                dat = vowel['{}_{}_{}'.format(v, dim, data)]
                precis, recall, f1 = cal_all_comparison(real, dat) 

                tone_line = ''
                for f in f1 :
                    p = f
                    p = '{:.2%}'.format(p)
                    # p = '{}_{}_{}_{}'.format(t, dim, s, data)
                    tone_line = tone_line + p + ','
                print tone_line

    pass
