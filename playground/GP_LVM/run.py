
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../')

from tool_box.util.utility import Utility

from DataModel.Syllables.SyllableDatabaseManagement import SyllableDatabaseManagement
from DataModel.Syllables.Syllable import Syllable
from GP_LVM_Tool.latent_variable_model_training import Latent_variable_model_Training


def run_for_missing_data():

    dropbox_path = '/home/h1/decha/Dropbox/'

    output_name = '05_missing_data_no_delta'
    
    delta_bool=False
    delta2_bool=False

    input_dims = 3

    for tone in ['01234']:
        print 'Delta : {}, Delta-Dealta : {}'.format(delta_bool, delta2_bool)
        print 'Missing data'

        data_object_path = '{}/Inter_speech_2016/Syllable_object/01_manual_labeling_object/syllable_{}.pickle'.format(dropbox_path,tone)
        if tone is '01234':
            data_object_path = '{}/Inter_speech_2016/Syllable_object/01_manual_labeling_object/syllable_all.pickle'.format(dropbox_path)

        syllable_management = Utility.load_obj(data_object_path)

        output_path = '{}/Inter_speech_2016/Syllable_object/{}/BGP_LVM/Tone_{}/'.format(dropbox_path,output_name,tone)

        print output_path

        Latent_variable_model_Training.execute_Bayesian_GPLVM_training(
            syllable_management, 
            Syllable.MISSING_VALUES, 
            input_dims, 
            output_path,
            delta_bool=delta_bool,
            delta2_bool=delta2_bool,
            missing_data=True)

        pass

    pass

def run_for_voice_data():

    dropbox_path = '/home/h1/decha/Dropbox/'

    output_name,delta_bool,delta2_bool = '02_delta_delta-delta', True, True
    # output_name,delta_bool,delta2_bool = '03_delta',  True, False
    # output_name,delta_bool,delta2_bool = '04_no_delta',  False, False
    input_dims = 3

    for tone in ['0','1','2','3','4', '01234']:
    # for tone in ['01234']:

        print 'Running Tone : {}'.format(tone)

        if tone is '01234':
            data_object_path = '{}/Inter_speech_2016/Syllable_object/01_manual_labeling_object/syllable_all.pickle'.format(dropbox_path)
            syllable_management = Utility.load_obj(data_object_path)
        else :
            data_object_path = '{}/Inter_speech_2016/Syllable_object/01_manual_labeling_object/syllable_{}.pickle'.format(dropbox_path,tone)
            syllable_management = Utility.load_obj(data_object_path)

        print 'Delta : {}, Delta-Dealta : {}'.format(delta_bool, delta2_bool)
        output_path = '{}/Inter_speech_2016/Syllable_object/{}/BGP_LVM/{}_dimentionality/Tone_{}/'.format(dropbox_path,output_name,input_dims,tone)

        print output_path

        Latent_variable_model_Training.execute_Bayesian_GPLVM_training(
            syllable_management, 
            Syllable.TRAINING_FEATURE_POLYNOMIAL_2_DEGREE_VOICE, 
            input_dims, 
            output_path,
            delta_bool=delta_bool,
            delta2_bool=delta2_bool)

    pass

def run_for_missing_data_with_delta_and_interpolate(max_iters):

    dropbox_path = '/home/h1/decha/Dropbox/'

    # output_name = '05_missing_data_no_delta'
    
    # output_name_paths = [
    #     '/work/w13/decha/Inter_speech_2016_workplace/Data/07a_missing_data_no_delta/',
    #     '/work/w13/decha/Inter_speech_2016_workplace/Data/07b_missing_data_delta/',
    #     '/work/w13/decha/Inter_speech_2016_workplace/Data/07c_missing_data_delta_deltadelta/'
    #     ]

    output_name_paths = [
        # '/work/w13/decha/Inter_speech_2016_workplace/Data/07_max_iters_{}/07a-5dims_BayesianGPLVMMiniBatch_data_no_delta/'.format(max_iters) ,
        # '/work/w13/decha/Inter_speech_2016_workplace/Data/07_max_iters_{}/07b-5dims_BayesianGPLVMMiniBatch_data_delta/'.format(max_iters) ,
        '/work/w13/decha/Inter_speech_2016_workplace/Data/07_max_iters_{}/07c-5dims_BayesianGPLVMMiniBatch_data_delta_deltadelta/'.format(max_iters)
        ]

    missing_data = True
    subtract_typical_contour = False

    print 'Missing Data : {}'.format(missing_data)

    deltas = [
        # [False, False],
        # [True, False],
        [True, True]
    ]

    # input_dims = 3
    input_dims = 5

    for idx, output_name in enumerate(output_name_paths):

        delta_bool=deltas[idx][0]
        delta2_bool=deltas[idx][1]

        if missing_data:
            method_name = 'BayesianGPLVMMiniBatch_Missing'
        else :
            method_name = 'BGP_LVM'

        # for tone in ['0','1','2','3','4','01234']:
        for tone in ['01234']:
            print 'Delta : {}, Delta-Dealta : {}'.format(delta_bool, delta2_bool)
            print 'Missing data'

            data_object_path = '{}/Inter_speech_2016/Syllable_object/01_manual_labeling_object/syllable_{}.pickle'.format(dropbox_path,tone)
            if tone is '01234':
                data_object_path = '{}/Inter_speech_2016/Syllable_object/01_manual_labeling_object/syllable_all.pickle'.format(dropbox_path)

            syllable_management = Utility.load_obj(data_object_path)

            output_path = '{}/{}/Tone_{}/'.format(output_name, method_name, tone)

            Utility.make_directory(output_path)

            print output_path

            Latent_variable_model_Training.execute_Bayesian_GPLVM_training(
                syllable_management, 
                # Syllable.TRAINING_FEATURE_POLYNOMIAL_2_DEGREE, 
                Syllable.TRAINING_FEATURE_POLYNOMIAL_2_DEGREE_VOICE, 
                input_dims, 
                output_path,
                subtract_typical_contour=subtract_typical_contour,
                delta_bool=delta_bool,
                delta2_bool=delta2_bool,
                missing_data=missing_data,
                max_iters=max_iters)

    pass

if __name__ == '__main__':

    for iters in [100, 200, 300, 400, 500]:
        run_for_missing_data_with_delta_and_interpolate(iters)

    # run_for_missing_data()
    # sys.exit()
    # pass

    # run_for_voice_data()
    # sys.exit()
    pass

        # syl_index = 751
        # name_index = syllable_management.syllables_list[syl_index].name_index
        # figure_out_path = '/home/h1/decha/Dropbox/Inter_speech_2016/temporary_output/{}_delta_delta.eps'.format(name_index)

        # syllable_management.get_Y_features(
        #     syllable_management.syllables_list[syl_index], 
        #     Syllable.TRAINING_FEATURE_POLYNOMIAL_2_DEGREE_VOICE, 
        #     delta_bool=True, delta2_bool=True, subtract_means=True ,output=figure_out_path)

        # y, names = syllable_management.get_GP_LVM_training_data(
        #     Syllable.TRAINING_FEATURE_POLYNOMIAL_2_DEGREE_VOICE,
        #     delta_bool=True,
        #     delta2_bool=True)