
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

def run_command(feature_type, missing_data, data_object_base_path_name, base_out_path, input_dims, tone_list, dur_position):
    
    deltas = [
        [False, False],
        [True, False],
        [True, True]
    ]

    output_name_paths = []

    for i, d in enumerate(deltas):
        outp = '{}/input_dims_{}/{}_delta-{}_delta-delta-{}/'.format(base_out_path, input_dims, Utility.fill_zero(i+1,2), d[0], d[1])
        output_name_paths.append(outp)

    print 'Missing Data : {}'.format(missing_data)

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

            num_inducing = int(0.1 * len(syllable_management.syllables_list))
            print 'num_inducing : ', num_inducing

            output_path = '{}/{}_Tone_{}/'.format(output_name, method_name, tone)

            Utility.make_directory(output_path)

            print output_path

            Latent_variable_model_Training.execute_Bayesian_GPLVM_training(
                syllable_management, 
                feature_type, 
                input_dims, 
                output_path,
                dur_position=dur_position,
                subtract_typical_contour=False,
                exp=False,
                delta_bool=delta_bool,
                delta2_bool=delta2_bool,
                missing_data=missing_data,
                num_inducing=num_inducing)

    pass

if __name__ == '__main__':

    print sys.argv

    base_path = sys.argv[1] #'/home/h1/decha/Dropbox/Inter_speech_2016/workspace/01_Tonal_part_projection/'

    print base_path

    object_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/Tonal_object/remove_all_silence_file/'

    # for v_type in ['all_vowel_type', 'v', 'vv','vn', 'vvn', 'vsg', 'vvsg']:
    # for v_type in ['v', 'vv','vn', 'vvn', 'vsg', 'vvsg']:
    for v_type in ['all_vowel_type']:
        print 'Vowel type : {}'.format(v_type)
        data_object_base_path_name = '{}/{}/syllable_object_'.format(object_path, v_type)
        base_vowel_type_path = '{}/{}/'.format(base_path, v_type)
        run_command(
            feature_type=Syllable.Training_feature_tonal_part_raw_remove_head_tail_interpolated, 
            missing_data=False, 
            data_object_base_path_name=data_object_base_path_name, 
            base_out_path=base_vowel_type_path, 
            input_dims=10, 
            # tone_list=[0,1,2,3,4], 
            tone_list=['01234'], 
            dur_position=[1,2])

    pass
