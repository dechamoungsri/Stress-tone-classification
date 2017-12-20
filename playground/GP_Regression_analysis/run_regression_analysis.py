
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../')

from GP_LVM_Tool.gp_regression_tool import GPModelByGPy
from tool_box.util.utility import Utility
from DataModel.Syllables.Syllable import Syllable

import numpy as np
import matplotlib.pyplot as plt

def run(main_path, syllable_management_path):
    # main_path = '/work/w13/decha/Inter_speech_2016_workplace/Data/07c-5dims_missing_data_delta_deltadelta/BayesianGPLVMMiniBatch_Missing/Tone_4/'

    # syllable_management_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/01_manual_labeling_object/syllable_4.pickle'

    model_path = '{}/GP_model.npy'.format(main_path)
    outpath = '{}/GP2dRegression.npy'.format(main_path)

    model = Utility.load_obj(model_path)

    data = model.X.mean

    x = []

    input_sensitivity = model.input_sensitivity()
    print input_sensitivity

    index = Utility.get_input_sensitivity(input_sensitivity, 2)
    print index

    for i in range(len(data)):
        x.append([data[i,index[0]], data[i,index[1]]])

    x = np.array(x)

    syllable_management = Utility.load_obj(syllable_management_path)
    y, name_index, tone, stress, syllable_short_long_type, syllable_positions, phonemes, syllable_type = syllable_management.get_GP_LVM_training_data(Syllable.TRAINING_FEATURE_POLYNOMIAL_2_DEGREE_VOICE, subtract_typical_contour=False)

    y = np.array(y)
    # print y[:,50]
    y = y[:,50]
    y = y[np.newaxis].T
    print y.shape

    GPModelByGPy.execute_training(x, y, outpath)

    pass

def analysis(main_path):
    # main_path = '/work/w13/decha/Inter_speech_2016_workplace/Data/07c-5dims_missing_data_delta_deltadelta/BayesianGPLVMMiniBatch_Missing/Tone_4/'
    gpmodel = Utility.load_obj('{}/GP2dRegression.npy'.format(main_path))

    model_path = '{}/GP_model.npy'.format(main_path)
    model = Utility.load_obj(model_path)
    data = model.X.mean

    x = []

    input_sensitivity = model.input_sensitivity()
    print input_sensitivity

    index = Utility.get_input_sensitivity(input_sensitivity, 2)
    print index

    for i in range(len(data)):
        x.append([data[i,index[0]], data[i,index[1]]])

    x = np.array(x)

    y = np.array(gpmodel.predict(x)[0])
    print y.shape

    plt.clf()
    plt.scatter(x[:,0], x[:,1], c=y, cmap='gray')
    plt.savefig('{}/gpregression.pdf'.format(main_path))
    pass

if __name__ == '__main__':

    for t in ['0','1','2','3','4','01234']:

        main = '/work/w13/decha/Inter_speech_2016_workplace/Data/07c-5dims_missing_data_delta_deltadelta/BayesianGPLVMMiniBatch_Missing/Tone_{}/'.format(t)

        if t == '01234': t = 'all'
        manage = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/01_manual_labeling_object/syllable_{}.pickle'.format(t)

        run(main, manage)
        analysis(main)
    pass
