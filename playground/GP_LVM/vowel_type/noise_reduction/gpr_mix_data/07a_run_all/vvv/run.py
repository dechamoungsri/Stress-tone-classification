
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../')
sys.path.append('../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/')
import matplotlib.mlab as mlab
from tool_box.util.utility import Utility

from DataModel.Syllables.Syllable import Syllable
from DataModel.Syllables.SyllableDatabaseManagement import SyllableDatabaseManagement

from GP_LVM_Tool.latent_variable_model_training import Latent_variable_model_Training

import numpy as np

def run_command(feature_type, missing_data, data_object_base_path_name, base_out_path, input_dims, tone_list, dur_position, num_sampling, d1, d2):
    
    deltas = [
        [d1, d2]
    ]

    output_name_paths = []

    for i, d in enumerate(deltas):
        outp = '{}/input_dims_{}/delta-{}_delta-delta-{}/'.format(base_out_path, input_dims, d[0], d[1])
        output_name_paths.append(outp)

    print 'Missing Data : {}'.format(missing_data)
    print 'Inducing points : 10 percent'

    for idx, output_name in enumerate(output_name_paths):

        delta_bool=deltas[idx][0]
        delta2_bool=deltas[idx][1]

        if missing_data:
            method_name = 'BayesianGPLVMMiniBatch_Missing'
        else :
            method_name = 'BGP_LVM'

        for tone in tone_list:

            print 'Delta : {}, Delta-Dealta : {}'.format(delta_bool, delta2_bool)

            data_object_path = '{}{}.pickle'.format(data_object_base_path_name, tone)

            print 'data path ',data_object_path

            syllable_management = Utility.load_obj(data_object_path)

            if len(syllable_management.syllables_list) == 0:
                print 'No syllable in this object database : {}'.format(tone)
                print '-----------------------------------------------------------------'
                continue

            print 'Syllable all : {} Syllables'.format(len(syllable_management.syllables_list))

            output_path = '{}/{}_Tone_{}/'.format(output_name, method_name, tone)

            Utility.make_directory(output_path)

            print output_path

            print 'Feature Key : {}'.format(feature_type)

            Y_full, names, tone, stress,syllable_short_long_type,syllalbe_position, phoneme, syllable_type = syllable_management.get_GP_LVM_training_data(
            feature_key=feature_type,
            dur_position=dur_position,
            delta_bool=delta_bool, delta2_bool=delta2_bool,
            missing_data=missing_data, num_sampling=num_sampling,)

            print 'Y full : {}'.format(np.array(Y_full).shape)

            Y, names, tone, stress,syllable_short_long_type,syllalbe_position, phoneme, syllable_type = syllable_management.get_GP_LVM_training_data(
            feature_key=feature_type,
            dur_position=dur_position,
            delta_bool=delta_bool, delta2_bool=delta2_bool,
            missing_data=missing_data, num_sampling=num_sampling,
            no_short_duration=True, 
            get_only_stress=False, exp=False, subtract_typical_contour=False, non_unlabelled_stress=False,get_only_gpr_data=False)

            Latent_variable_model_Training.execute_Bayesian_GPLVM_training_with_Y_names(
                Y, 
                names, 
                input_dims, 
                output_path, 
                missing_data=False,
                max_iters=500,
                num_inducing=10,
                BayesianGPLVMMiniBatch=False)

    pass

if __name__ == '__main__':

    print sys.argv

    base_path = sys.argv[1] #'/home/h1/decha/Dropbox/Inter_speech_2016/workspace/01_Tonal_part_projection/'

    print base_path

    import os
    print os.environ['HOST']

    object_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/mix_object/current_version/'

    deltas = [
        # [True, False],
        [True, True],
        # [False, False],
    ]

    for d in deltas:
        for v_type in ['vvv']:
            print 'Vowel type : {}'.format(v_type)
            data_object_base_path_name = '{}/{}/syllable_object_'.format(object_path, v_type)
            base_vowel_type_path = '{}/{}/'.format(base_path, v_type)

            feature_type =  Syllable.Training_feature_tonal_part_raw_remove_head_tail_interpolated
            print feature_type

            run_command(
                feature_type=feature_type, 
                missing_data=False, 
                data_object_base_path_name=data_object_base_path_name, 
                base_out_path=base_vowel_type_path, 
                input_dims=10, 
                tone_list=['4'], 
                dur_position=[1,2],
                num_sampling=50,
                d1=d[0],
                d2=d[1])

            # sys.exit()

    pass
