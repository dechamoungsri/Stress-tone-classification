
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../')
sys.path.append('../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/pybrain-master/')

from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from pybrain.structure import TanhLayer

import matplotlib.mlab as mlab
from tool_box.util.utility import Utility
import scipy.stats as stats
from DataModel.Syllables.Syllable import Syllable
from DataModel.Syllables.SyllableDatabaseManagement import SyllableDatabaseManagement
from ANN_Executioner import ANN_Executioner_Helper

import numpy as np
import matplotlib.pyplot as plt
# from sklearn.metrics import accuracy_score
# from sklearn import preprocessing

import itertools


def run_latent_data(base_path, trn_data, tst_data, outpath, name, fold):

    trndata = ANN_Executioner_Helper.get_latent_data(base_path, trn_data['name_index'], trn_data['stress'], use_input_sensitivity=True, normalize=True)
    tstdata = ANN_Executioner_Helper.get_latent_data(base_path, tst_data['name_index'], tst_data['stress'], use_input_sensitivity=True, normalize=True)

    ANN_Executioner_Helper.run_nn_train_until_convergence(trndata, tstdata, outpath, name, fold)

    pass

def run(fold_object_path, number_of_fold, outpath, feature, duration, delta_bool, delta2_bool, latent_data_path):

    print 'Start at Fold object path : {}'.format(fold_object_path)
    for i in range(number_of_fold):
        trn_obj, tst_obj = ANN_Executioner_Helper.get_train_and_test_fold(fold_object_path, number_of_fold, i)

        trn_data = ANN_Executioner_Helper.get_data_from_obj(trn_obj, feature, duration, get_only_stress=None, stress_unstress_must_equal=False)
        tst_data = ANN_Executioner_Helper.get_data_from_obj(tst_obj, feature, duration, get_only_stress=None, stress_unstress_must_equal=False)

        trn_data_set = ANN_Executioner_Helper.get_ClassificationDataSet(trn_data['Y'], trn_data['stress'], normalize=True)
        tst_data_set = ANN_Executioner_Helper.get_ClassificationDataSet(tst_data['Y'], tst_data['stress'], normalize=True)

        print "Number of training patterns: ", len(trn_data_set)
        print "Input and output dimensions: ", trn_data_set.indim, trn_data_set.outdim

        print 'Plain data : '
        # ANN_Executioner_Helper.run_nn(trn_data_set, tst_data_set, outpath, 'Plain_data', i)
        ANN_Executioner_Helper.run_nn_train_until_convergence2(trn_data_set, tst_data_set, outpath, 'Plain_data', i)
        print 'Latent data : '
        # run_latent_data(latent_data_path, trn_data, tst_data, outpath, 'Latent_data', i)
        print 

def run_add_and_non_duration(out_base, vowel, d, tone, feature_name, num_dims):

    for n in num_dims:

        print '------------Start-----------'

        print 'Vowel : {}, Delta : {}, Tone : {}'.format(vowel, d, tone)

        base_path = '{}/{}/input_dims_{}/delta-{}_delta-delta-{}/BGP_LVM_Tone_{}/'.format(out_base, vowel, n, d[0], d[1] ,tone)
        syllable_object = '{}/{}/syllable_object_{}_fold/syllable_object_{}_3-fold_'.format(object_base, vowel, tone, tone)
        outpath = '{}/{}/input_dims_{}/delta-{}_delta-delta-{}/BGP_LVM_Tone_{}/feed_forword_ann/{}/'.format(out_base, vowel, n, d[0], d[1] ,tone, feature_name)

        print 'ANN outpath : {}'.format(outpath)
        print 'Syllable object : {}'.format(syllable_object)

        Utility.make_directory(outpath)
        run(syllable_object, fold, outpath, feature, [1,2], d[0], d[1], base_path)

        print '------------End-----------'

if __name__ == '__main__':

    vowel_type = [ 'vvv', 'vvvn', 'vvvsg']
    tones = ['0', '1', '2', '3', '4']

    features_type = [Syllable.Training_feature_tonal_part_raw_remove_head_tail_interpolated]

    fold = 3

    import os
    print os.environ['HOST']

    object_base = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/mix_object/current_version/'
    out_base = '/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/09_25lf0_to_compare_with_ann/'

    for i, j in itertools.product(range(len(vowel_type)), range(len(tones))):
        vowel = vowel_type[i]
        tone = tones[j]

        from time import gmtime, strftime
        print strftime("%Y-%m-%d %H:%M:%S", gmtime())

        deltas = [
            [True, True],
        ]

        for d in deltas:

            for feature in features_type:
                run_add_and_non_duration(out_base, vowel, d, tone, '50lf0_real_til_0_0065', [10])

    pass
