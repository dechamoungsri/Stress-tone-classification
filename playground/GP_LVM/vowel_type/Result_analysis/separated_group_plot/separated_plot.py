
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../')
sys.path.append('../../../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/')

from tool_box.util.utility import Utility
from tool_box.plotting.horizontal_histogram.Horizontal_Histogram import HorizontalHistogram
from tool_box.plotting.scatter.scatter_plotting import GP_LVM_Scatter

from DataModel.Syllables.Syllable import Syllable
from DataModel.Syllables.SyllableDatabaseManagement import SyllableDatabaseManagement

import traceback
import numpy as np
import os

from Unsupervised_learning.DBSCAN_interface import DBSCAN_executioner

def plot_result(model, data_object, out_file_path):

        data = model.X.mean

        y, name_index, tone, stress, syllable_short_long_type, syllable_positions, phonemes, syllable_type = data_object.get_GP_LVM_training_data(
            Syllable.TRAINING_FEATURE_POLYNOMIAL_2_DEGREE_VOICE, 
            dur_position=[1,2] ,
            num_sampling=25)

        # print syllable_type
        # print model.X.mean
        x = []
        y = []

        input_sensitivity = model.input_sensitivity()
        print input_sensitivity

        index = Utility.get_input_sensitivity(input_sensitivity, 2)
        print index

        data = np.array(data)
        stress = np.array(stress)

        labels_true = np.arange(len(stress), dtype=int)
        labels_true[stress == 'Stress'] = 1
        labels_true[stress == 'Unstress'] = 0

        new_label = []
        for idx, t in enumerate(tone):
            if (labels_true[idx] == 1):
                if (t in [0,1]) :
                    new_label.append(1)
                elif (t in [2]) :
                    new_label.append(2)
                else :
                    new_label.append(3)
            else:
                new_label.append(0)

        try:
            DBSCAN_executioner.run(
                data, 
                new_label, 
                os.path.dirname(outpath), 
                [index[0], index[1]], 
                input_sensitivity, 
                stress_only=False,
                stress_list=labels_true)
            # Kmeans_executioner.run(data, labels_true, os.path.dirname(outpath), [index[0], index[1]], input_sensitivity)
        except:
            print 'Error at path : {}'.format(outpath)
            traceback.print_exc()

def perform_unsupervised(out_file_path, base_path_list, data_object_path):

    model_path = '{}/GP_model.npy'.format(base_path_list)

    import os.path
    if not os.path.isfile(model_path) : return

    data_object = data_object_path

    plot_result(
        Utility.load_obj(model_path), 
        Utility.load_obj(data_object), 
        out_file_path)

def plot_type(plot_type, out_file_path, base_path_list, data_object_path, perform_unsupervised):

    model_path = '{}/GP_model.npy'.format(base_path_list)

    import os.path
    if not os.path.isfile(model_path) : return

    data_object = data_object_path

    # model = Utility.load_obj(model_path)
    # data = model.X.mean
    # means = np.array(data)

    GP_LVM_Scatter.plot_scatter(
        Utility.load_obj(model_path), 
        Utility.load_obj(data_object), 
        out_file_path, 
        label_type=plot_type, perform_unsupervised=False)

    # sys.exit()

    pass

if __name__ == '__main__':

    base_data_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/Tonal_object/remove_all_silence_file/'

    base_path_list = [
       '/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/06_Tonal_part_projection_noise_reduction-250-iters-opt/'
        ]

    vowel_type = ['vvv', 'vvvn','vvvsg']
    #['v', 'vv','vn', 'vvn', 'vsg', 'vvsg']

    input_dims = [10]

    name_in_figure = 'LABEL_TYPE_STRESS'

    for syst in base_path_list:
        # for v in ['vvv']:
        for v in Utility.list_file(syst):
            if '.' in v : continue
            for dims in input_dims:
                delta_path = '{}/{}/input_dims_{}'.format(syst, v, dims)
                for d in ['delta-True_delta-delta-True'] : #Utility.list_file(delta_path):
                    if d.startswith('.'): continue
                    for tone in Utility.list_file('{}/{}/'.format(delta_path, d)):
                        if tone.startswith('.'): continue
                        # if '01234' not in tone: continue
                        tone_path = '{}/{}/{}/'.format(delta_path, d, tone)
                        print tone_path
                        object_data = '{}/{}/syllable_object_{}.pickle'.format(base_data_path, v, tone.split('_')[len(tone.split('_'))-1])
                        print object_data
                        outpath = '{}/{}.eps'.format(tone_path, name_in_figure)
                        print outpath
                        
                        name_index = Utility.load_obj('{}/Y.npy'.format(tone_path))
                        # print name_index 
                        # print len(name_index)

                        # plot_type(
                        #     GP_LVM_Scatter.LABEL_TYPE_STRESS, 
                        #     outpath, 
                        #     tone_path, 
                        #     object_data,
                        #     perform_unsupervised=True)
                        # print 'plot_type'

                        perform_unsupervised(outpath, tone_path, object_data)

                        # plot_type(
                        #     GP_LVM_Scatter.LABEL_TYPE_STRESS_AND_SPLIT_TONE, 
                        #     outpath, 
                        #     tone_path, 
                        #     object_data,
                        #     perform_unsupervised=False)
                        # sys.exit()

    pass




