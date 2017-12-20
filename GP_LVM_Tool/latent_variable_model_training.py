'''
Created on Jan 29, 2016

@author: decha
'''

import sys
sys.path.append('../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

import GPy

from DataModel.Syllables.Syllable import Syllable
from tool_box.util.utility import Utility

import numpy as np

class Latent_variable_model_Training(object):
    '''
    classdocs
    '''

    @staticmethod
    def Bayesian_GPLVM_train(Y,
                             input_dim,
                             kernel=None,
                             num_inducing=100,
                             optimize=True,
                             max_iters=250,
                             verbose=1,
                             missing_data=False,
                             BayesianGPLVMMiniBatch=False):
        
        if num_inducing > 500:
            num_inducing = 500

        print "num_inducing, input_dim, max_iters, missing_data, BayesianGPLVMMiniBatch"
        print num_inducing, input_dim, max_iters, missing_data, BayesianGPLVMMiniBatch

        if kernel is None:
            kernel = GPy.kern.RBF(input_dim , ARD=True)
        
        # print Y[0]

        if BayesianGPLVMMiniBatch:
            print 'BayesianGPLVMMiniBatch'
            from GPy.models.bayesian_gplvm_minibatch import BayesianGPLVMMiniBatch
            m = BayesianGPLVMMiniBatch(Y, input_dim, kernel=kernel, num_inducing=num_inducing, init="PCA", missing_data=True)
        else:
            print 'GPy.models.BayesianGPLVM'
            m = GPy.models.BayesianGPLVM(Y, input_dim, kernel=kernel, num_inducing=num_inducing, init="PCA", missing_data=missing_data)
            # print 'BayesianGPLVMMiniBatch'
            # m = BayesianGPLVMMiniBatch(Y, input_dim, kernel=kernel, num_inducing=num_inducing, init="PCA", missing_data=missing_data)

        if optimize: m.optimize('scg', messages=verbose, max_iters=max_iters)

        return m
        
        pass

    @staticmethod
    def execute_Bayesian_GPLVM_training(
        syllable_management, 
        feature_key, 
        input_dim, 
        output_path, 
        dur_position,
        num_sampling,
        exp=False,
        subtract_typical_contour=False,
        delta_bool=False,
        delta2_bool=False,
        missing_data=False,
        max_iters=250,
        num_inducing=100,
        get_only_stress=None,
        non_unlabelled_stress=False,
        BayesianGPLVMMiniBatch=False,
        get_only_gpr_data=False):

        # Data preparation 
        # Result Extraction and save

        print 'Feature Key : {}'.format(feature_key)

        Utility.make_directory(output_path)

        Y, names, tone, stress,syllable_short_long_type,syllalbe_position, phoneme, syllable_type = syllable_management.get_GP_LVM_training_data(
            feature_key=feature_key,
            dur_position=dur_position,
            exp=exp,
            delta_bool=delta_bool,
            delta2_bool=delta2_bool,
            missing_data=missing_data,
            subtract_typical_contour=subtract_typical_contour,
            num_sampling=num_sampling,
            get_only_stress=get_only_stress, 
            non_unlabelled_stress=non_unlabelled_stress,
            get_only_gpr_data=get_only_gpr_data)
        # print 'Example training data : '
        # print Y[0]

        # sys.exit()
        Utility.save_obj(names, '{}/name_index.npy'.format(output_path))

        Y = np.asarray(Y)
        print 'Y shape :',  Y.shape
        Utility.save_obj(Y, '{}/Y.npy'.format(output_path))

        m = Latent_variable_model_Training.Bayesian_GPLVM_train(Y, input_dim, missing_data=missing_data, max_iters=max_iters, num_inducing=num_inducing, BayesianGPLVMMiniBatch=BayesianGPLVMMiniBatch)
        Utility.save_obj(m, '{}/GP_model.npy'.format(output_path))

    @staticmethod
    def execute_Bayesian_GPLVM_training_with_Y_names(
        Y, 
        names, 
        input_dim, 
        output_path, 
        missing_data=False,
        max_iters=250,
        num_inducing=100,
        BayesianGPLVMMiniBatch=False):

        # Data preparation 
        # Result Extraction and save

        Utility.make_directory(output_path)

        # print 'Example training data : '
        # print Y[0]

        # sys.exit()
        Utility.save_obj(names, '{}/name_index.npy'.format(output_path))

        Y = np.asarray(Y)
        print 'Y shape :',  Y.shape
        Utility.save_obj(Y, '{}/Y.npy'.format(output_path))

        m = Latent_variable_model_Training.Bayesian_GPLVM_train(Y, input_dim, missing_data=missing_data, max_iters=max_iters, num_inducing=num_inducing, BayesianGPLVMMiniBatch=BayesianGPLVMMiniBatch)
        Utility.save_obj(m, '{}/GP_model.npy'.format(output_path))

    def __init__(self, params):
        '''
        Constructor
        '''
        