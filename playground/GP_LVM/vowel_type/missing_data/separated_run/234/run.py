
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

def run_command(feature_type, data_object_base_path_name, base_out_path, input_dims, tone_list, dur_position, num_sampling, d1, d2, missing_data):
    
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

            output_path = '{}/{}_Tone_{}/'.format(output_name, method_name, tone)

            Utility.make_directory(output_path)

            print output_path

            try: 
                Latent_variable_model_Training.execute_Bayesian_GPLVM_training(
                    syllable_management, 
                    feature_type, 
                    input_dims, 
                    output_path,
                    num_sampling=num_sampling,
                    dur_position=dur_position,
                    delta_bool=delta_bool,
                    delta2_bool=delta2_bool,
                    num_inducing=100,
                    max_iters=100,
                    BayesianGPLVMMiniBatch=True,
                    get_only_gpr_data=True)
            except:
                print 'Tone : {}, Vowel : {}'.format(tone, output_name_paths)

    pass

if __name__ == '__main__':

    print sys.argv

    base_path = sys.argv[1] #'/home/h1/decha/Dropbox/Inter_speech_2016/workspace/01_Tonal_part_projection/'

    print base_path

    import os
    print os.environ['HOST']

    object_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/mix_object/current_version/'

    deltas = [
        [True, True],
    ]

    for indims in [10]:
    # for indims in [3]:
        
        for d in deltas:
            for v_type in ['all_vowel_type']:
                print 'Vowel type : {}'.format(v_type)
                data_object_base_path_name = '{}/{}/syllable_object_'.format(object_path, v_type)
                base_vowel_type_path = '{}/{}/'.format(base_path, v_type)

                feature_type =  Syllable.TRAINING_RAW_DATA
                print feature_type

                run_command(
                    feature_type=feature_type, 
                    data_object_base_path_name=data_object_base_path_name, 
                    base_out_path=base_vowel_type_path, 
                    input_dims=indims, 
                    # tone_list=['01234'], 
                    tone_list=['2','3','4'], 
                    dur_position=[0,1,2],
                    num_sampling=25,
                    d1=d[0],
                    d2=d[1],
                    missing_data=True)

    pass
