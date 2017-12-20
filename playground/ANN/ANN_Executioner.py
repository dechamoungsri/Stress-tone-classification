
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
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn import preprocessing
from sklearn.preprocessing import scale

import random

class ANN_Executioner_Helper(object):
    
    @staticmethod
    def get_latent_data(base_path, names, label_feature, use_input_sensitivity=False, normalize=False):

        model = Utility.load_obj('{}/GP_model.npy'.format(base_path))
        input_sensitivity = model.input_sensitivity()

        latent_data = np.array(Utility.load_obj('{}/GP_model.npy'.format(base_path)).X.mean)
        name_index = np.array(Utility.load_obj('{}/name_index.npy'.format(base_path)))

        latent_Y = []
        for n in names:
            ind = np.where(name_index==n)
            latent_Y.append(latent_data[ind][0])

        if len(latent_Y) != len(names):
            print 'Un equal data : {}'.format(base_path) 
            sys.exit()

        latent_Y = np.array(latent_Y)

        print 'Get input sent {}'.format(input_sensitivity)

        if not use_input_sensitivity: 
            input_sensitivity = None

        data = ANN_Executioner_Helper.get_ClassificationDataSet(latent_Y, label_feature, normalize=normalize, input_sensitivity=input_sensitivity)
        return data

    @staticmethod
    def get_ClassificationDataSet(Y, label_feature, normalize=True, input_sensitivity=None):
        # print Y[:,25]
        if normalize:
            for r in range(len(Y[0])):
                if input_sensitivity is not None:
                    Y[:,r] = preprocessing.normalize(Y[:,r].reshape(1, -1) * input_sensitivity[r])
                    # Y[:,r] = scale(Y[:,r] * input_sensitivity[r])
                else:    
                    Y[:,r] = preprocessing.normalize(Y[:,r].reshape(1, -1))
                    # Y[:,r] = scale(Y[:,r])
                # Y[:,r] = Y[:,r] - np.mean(Y[:,r])

        # print Y[:,25], np.mean(Y[:,25]), max(Y[:,25]), min(Y[:,25])
        # sys.exit()

        print np.var(Y)

        alldata = ClassificationDataSet(len(Y[0]), 1, nb_classes=len(set(label_feature)))
        for a, yyy in enumerate(Y):
            alldata.addSample(Y[a], label_feature[a])

        alldata._convertToOneOfMany( )

        return alldata

    @staticmethod 
    def get_data_from_obj(syl_obj, feature_key, dur_position,
                    delta_bool=True, delta2_bool=True, num_sampling=50, get_only_stress='1',
                    stress_unstress_must_equal=False, get_only_manual_data=True):
        Y, names, tone, stress, syllable_short_long_type,syllalbe_position, phoneme, syllable_type = syl_obj.get_GP_LVM_training_data(
            feature_key=feature_key,
            dur_position=dur_position,
            delta_bool=delta_bool,
            delta2_bool=delta2_bool,
            num_sampling=num_sampling, 
            get_only_stress=get_only_stress,
            get_only_manual_data=get_only_manual_data)

        out = dict()
        out['Y'] = np.array(Y)
        out['name_index'] = np.array(names)
        out['tone'] = np.array(tone)
        out['stress'] = np.array(stress)

        out['stress'][out['stress']=='Stress'] = 1
        out['stress'][out['stress']=='Unstress'] = 0

        if stress_unstress_must_equal:

            stress_index = np.where(out['stress']=='1')[0]
            unstress_index = np.where(out['stress']=='0')[0]

            picked_stress = random.sample(unstress_index, int(2.0*float(len(stress_index))) ) 
            picked_stress = np.append(stress_index, picked_stress)

            # np.random.shuffle(picked_stress)

            print len(stress_index), len(unstress_index), len(picked_stress)

            out['stress'] = out['stress'][picked_stress]
            out['Y'] = out['Y'][picked_stress]
            out['name_index'] = out['name_index'][picked_stress]
            out['tone'] = out['tone'][picked_stress]

            return out

        else:
            return out

    @staticmethod
    def get_train_and_test_fold(fold_object_path, number_of_fold, tst_fold):
        syls_trn, syls_tst = [], []
        
        test_fold_path = '{}{}.pickle'.format(fold_object_path, tst_fold)
        syls_tst = Utility.load_obj(test_fold_path).syllables_list

        train_fold_path = []
        for j in range(number_of_fold):
            if j==tst_fold : continue
            fold_path = '{}{}.pickle'.format(fold_object_path, j)
            syls_trn+= Utility.load_obj(fold_path).syllables_list

        return ( SyllableDatabaseManagement(syllable_list=syls_trn), SyllableDatabaseManagement(syllable_list=syls_tst) )

    @staticmethod
    def run_nn(trndata, tstdata, outpath, name, fold):
        fnn = buildNetwork(trndata.indim, 20, trndata.outdim, hiddenclass=TanhLayer, bias=True)

        trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1, weightdecay=0.01)

        acc = 0.0

        real_obj = []
        predicted_obj = []

        # for i in range(5):
        for i in range(50):
            trainer.trainEpochs( 1 )
            trnresult = percentError( trainer.testOnClassData(),
                                      trndata['class'] )
            tstresult = percentError( trainer.testOnClassData(
                   dataset=tstdata ), tstdata['class'] )
            # print "epoch: %4d" % trainer.totalepochs, \
            #           "  train error: %5.2f%%" % trnresult, \
            #           "  test error: %5.2f%%" % tstresult
            predicted = np.array( trainer.testOnClassData(dataset=tstdata) )
            real = np.array( tstdata['class'][:,0] )
            # print real
            if (accuracy_score(real, predicted) > acc) & (0 != len(np.where(predicted==1)[0])):
                real_obj = real
                predicted_obj = predicted
                acc = accuracy_score(real, predicted) 

        Utility.save_obj(real_obj, '{}/{}_fold_{}_real.npy'.format(outpath, name, fold))
        Utility.save_obj(predicted_obj, '{}/{}_fold_{}_predicted.npy'.format(outpath, name, fold))
        print 'Accuracy : {}'.format(acc)
        return acc

    @staticmethod
    def run_nn_train_until_convergence(trndata, tstdata, outpath, name, fold):

        print 'Train data'
        print trndata.indim, trndata.outdim

        fnn = buildNetwork(trndata.indim, 20, trndata.outdim, hiddenclass=TanhLayer, bias=True)

        trainer = BackpropTrainer( fnn, dataset=trndata, weightdecay=0.001)

        acc = 0.0
        tag = 'No acc'
        real_obj = []
        predicted_obj = []
        for i in range(10):
            trainer.trainEpochs( 5 )
            # trainer.trainUntilConvergence()
            trnresult = percentError( trainer.testOnClassData(),
                                      trndata['class'] )
            tstresult = percentError( trainer.testOnClassData(
                   dataset=tstdata ), tstdata['class'] )
            print "epoch: %4d" % trainer.totalepochs, \
                      "  train error: %5.2f%%" % trnresult, \
                      "  test error: %5.2f%%" % tstresult
            predicted = np.array( trainer.testOnClassData(dataset=tstdata) )
            real = np.array( tstdata['class'][:,0] )

            real_obj = real
            predicted_obj = predicted

        Utility.save_obj(real_obj, '{}/{}_fold_{}_real.npy'.format(outpath, name, fold))
        Utility.save_obj(predicted_obj, '{}/{}_fold_{}_predicted.npy'.format(outpath, name, fold))
        # print tag
        print 'Accuracy : {}'.format( acc )
        print 'Precision : {}'.format( precision_score(real_obj, predicted_obj, average=None) )
        print 'Recall : {}'.format( recall_score(real_obj, predicted_obj, average=None) )
        print 'F-1 : {}'.format( f1_score(real_obj, predicted_obj, average=None) )
        return acc

    @staticmethod
    def run_nn_train_until_convergence2(trndata, tstdata, outpath, name, fold):

        print 'Train data'
        print trndata.indim, trndata.outdim

        fnn = buildNetwork(trndata.indim, 20, trndata.outdim, hiddenclass=TanhLayer, bias=True)

        trainer = BackpropTrainer( fnn, dataset=trndata, weightdecay=0.006)

        acc = 0.0
        tag = 'No acc'
        real_obj = []
        predicted_obj = []
        for i in range(10):
            trainer.trainEpochs( 5 )
            # trainer.trainUntilConvergence()
            trnresult = percentError( trainer.testOnClassData(),
                                      trndata['class'] )
            tstresult = percentError( trainer.testOnClassData(
                   dataset=tstdata ), tstdata['class'] )
            print "epoch: %4d" % trainer.totalepochs, \
                      "  train error: %5.2f%%" % trnresult, \
                      "  test error: %5.2f%%" % tstresult
            predicted = np.array( trainer.testOnClassData(dataset=tstdata) )
            real = np.array( tstdata['class'][:,0] )

            real_obj = real
            predicted_obj = predicted

        Utility.save_obj(real_obj, '{}/{}_fold_{}_real.npy'.format(outpath, name, fold))
        Utility.save_obj(predicted_obj, '{}/{}_fold_{}_predicted.npy'.format(outpath, name, fold))
        # print tag
        print 'Accuracy : {}'.format( acc )
        print 'Precision : {}'.format( precision_score(real_obj, predicted_obj, average=None) )
        print 'Recall : {}'.format( recall_score(real_obj, predicted_obj, average=None) )
        print 'F-1 : {}'.format( f1_score(real_obj, predicted_obj, average=None) )
        return acc

    @staticmethod
    def run_nn_train_tone_classification(trndata, tstdata, outpath, name, fold):

        print 'run_nn_train_tone_classification'

        fnn = buildNetwork(trndata.indim, 20, trndata.outdim, hiddenclass=TanhLayer, bias=True)

        trainer = BackpropTrainer( fnn, dataset=trndata, weightdecay=0.006)
        # trainer = BackpropTrainer( fnn, dataset=trndata, verbose=True)

        acc = 0.0
        tag = 'No acc'
        real_obj = []
        predicted_obj = []

        class_recog = 0

        for i in range(100):
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
            # print real
            # if (accuracy_score(real, predicted) > acc) & (0 != len(np.where(predicted==1)[0])):
            if ( len(set(predicted)) >= class_recog):
                class_recog = len(set(predicted))
                print 'Tone num : {}'.format(set(predicted))
                tag = "Add acc when epoch: %4d" % trainer.totalepochs
                real_obj = real
                predicted_obj = predicted
                acc = accuracy_score(real, predicted) 
            # else:
            #     print predicted

        Utility.save_obj(real_obj, '{}/{}_fold_{}_real.npy'.format(outpath, name, fold))
        Utility.save_obj(predicted_obj, '{}/{}_fold_{}_predicted.npy'.format(outpath, name, fold))
        print tag
        print 'Accuracy : {}'.format( acc )
        print 'Precision : {}'.format( precision_score(real_obj, predicted_obj, average=None) )
        print 'Recall : {}'.format( recall_score(real_obj, predicted_obj, average=None) )
        print 'F-1 : {}'.format( f1_score(real_obj, predicted_obj, average=None) )
        return acc

    @staticmethod
    def run_nn_train_playground(trndata, tstdata, outpath, name, fold):
        # fnn = buildNetwork(trndata.indim, 20, trndata.outdim, hiddenclass=TanhLayer, bias=False)

        # trainer = BackpropTrainer( fnn, dataset=trndata, weightdecay=0.01)
        # trainer = BackpropTrainer( fnn, dataset=trndata, verbose=True)

        fnn = buildNetwork(trndata.indim, 20, trndata.outdim, hiddenclass=TanhLayer, bias=False)

        trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.0, weightdecay=0.0075)

        acc = 0.0
        tag = 'No acc'
        real_obj = []
        predicted_obj = []

        for i in range(10):
            trainer.trainEpochs( 2 )
            trnresult = percentError( trainer.testOnClassData(),
                                      trndata['class'] )
            tstresult = percentError( trainer.testOnClassData(
                   dataset=tstdata ), tstdata['class'] )
            # print "epoch: %4d" % trainer.totalepochs, \
            #           "  train error: %5.2f%%" % trnresult, \
            #           "  test error: %5.2f%%" % tstresult
            predicted = np.array( trainer.testOnClassData(dataset=tstdata) )
            real = np.array( tstdata['class'][:,0] )
            # print real
            # if (accuracy_score(real, predicted) > acc) & (0 != len(np.where(predicted==1)[0])):
            if (0 != len(np.where(predicted==1)[0])):
                tag = "Add acc when epoch: %4d" % trainer.totalepochs
                real_obj = real
                predicted_obj = predicted
                acc = accuracy_score(real, predicted) 

        Utility.save_obj(real_obj, '{}/{}_fold_{}_real.npy'.format(outpath, name, fold))
        Utility.save_obj(predicted_obj, '{}/{}_fold_{}_predicted.npy'.format(outpath, name, fold))
        print tag
        print 'Accuracy : {}'.format( acc )
        print 'Precision : {}'.format( precision_score(real_obj, predicted_obj, average=None) )
        print 'Recall : {}'.format( recall_score(real_obj, predicted_obj, average=None) )
        print 'F-1 : {}'.format( f1_score(real_obj, predicted_obj, average=None) )
        return acc

