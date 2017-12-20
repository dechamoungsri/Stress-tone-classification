
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

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score

import itertools

def get_training_object(train_list, feature):
    syl_list = []
    for t in train_list:
        syl_obj = Utility.load_obj(t)
        syl_list+=syl_obj.syllables_list
    syllable_management_object = SyllableDatabaseManagement(syllable_list=syl_list)
    Y, names, tone, stress, syllable_short_long_type,syllalbe_position, phoneme, syllable_type = syllable_management_object.get_GP_LVM_training_data(
            feature_key=feature,
            dur_position=[1,2],
            delta_bool=True,
            delta2_bool=True,
            num_sampling=50)

    stress = np.array(stress)
    stress[stress=='Stress'] = 1
    stress[stress=='Unstress'] = 0

    label_feature = stress
    alldata = ClassificationDataSet(len(Y[0]), 1, nb_classes=len(set(label_feature)))
    for idx, yyy in enumerate(Y):

        alldata.addSample(yyy, label_feature[idx])

    alldata._convertToOneOfMany( )

    return alldata

def run(fold_object_path, number_of_fold, outpath, feature):

    for i in range(number_of_fold):
        test_fold_path = '{}{}.pickle'.format(fold_object_path, i)
        # print test_fold_path

        train_fold_path = []
        for j in range(number_of_fold):
            if j==i : continue
            fold_path = '{}{}.pickle'.format(fold_object_path, j)
            train_fold_path.append(fold_path)
        # print train_fold_path

        trndata = get_training_object(train_fold_path, feature)
        # print trndata

        tstdata = get_training_object([test_fold_path], feature)
        # print tstdata

        print "Number of training patterns: ", len(trndata)
        print "Input and output dimensions: ", trndata.indim, trndata.outdim
        print "First sample (input, target, class):"

        fnn = buildNetwork(trndata.indim, 20, trndata.outdim, hiddenclass=TanhLayer, bias=False)

        trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1, weightdecay=0.01)

        acc = 0.0

        for i in range(50):
            trainer.trainEpochs( 1 )
            trnresult = percentError( trainer.testOnClassData(),
                                      trndata['class'] )
            tstresult = percentError( trainer.testOnClassData(
                   dataset=tstdata ), tstdata['class'] )
            print "epoch: %4d" % trainer.totalepochs, \
                      "  train error: %5.2f%%" % trnresult, \
                      "  test error: %5.2f%%" % tstresult
            predicted = np.array( trainer.testOnClassData(dataset=tstdata) )
            real = np.array( tstdata['class'][:,0] )

            # print real, predicted

            # predicted = predicted[real==1]
            # real = real[real==1]

            print len(predicted), len(real)

            print f1_score(predicted, real, average=None)

            # if accuracy_score(real, predicted) > acc:
            #     acc = accuracy_score(real, predicted) 

        print f1_score(predicted, real, average=None)

        # trainer.trainUntilConvergence()
        # trnresult = percentError( trainer.testOnClassData(),
        #                       trndata['class'] )
        # tstresult = percentError( trainer.testOnClassData(
        #    dataset=tstdata ), tstdata['class'] )
        # print "epoch: %4d" % trainer.totalepochs, \
        #   "  train error: %5.2f%%" % trnresult, \
        #   "  test error: %5.2f%%" % tstresult

        print '---------------------------------'
        # sys.exit()

    pass

if __name__ == '__main__':

    vowel_type = ['vvv', 'vvvn', 'vvvsg']
    # vowel_type = ['vvvn', 'vvvsg']
    tones = ['0', '1', '2', '3', '4']
    # tones = ['0']

    features_type = [Syllable.Training_feature_tonal_part_raw_remove_head_tail_interpolated]

    fold = 3

    object_base = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/Tonal_object/remove_all_silence_file/'
    out_base = '/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/06_Tonal_part_projection_noise_reduction-250-iters-opt/'

    for i, j in itertools.product(range(len(vowel_type)), range(len(tones))):
        vowel = vowel_type[i]
        tone = tones[j]

        for feature in features_type:
            syllable_object = '{}/{}/syllable_object_{}_fold/syllable_object_{}_3-fold_'.format(object_base, vowel, tone, tone)
            print syllable_object

            outpath = '{}/{}/input_dims_10/delta-True_delta-delta-True/BGP_LVM_Tone_{}/feed_forword_ann/{}/'.format(out_base, vowel, tone, '150-lf0_duration')
            print outpath

            Utility.make_directory(outpath)
            run(syllable_object, fold, outpath, feature)

        # sys.exit()

    pass
