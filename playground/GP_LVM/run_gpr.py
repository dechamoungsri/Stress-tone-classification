
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../')

from tool_box.util.utility import Utility

from DataModel.Syllables.SyllableDatabaseManagement import SyllableDatabaseManagement
from DataModel.Syllables.Syllable import Syllable
from GP_LVM_Tool.latent_variable_model_training import Latent_variable_model_Training

def run_for_missing_data_with_delta_and_interpolate():

    dropbox_path = '/home/h1/decha/Dropbox/'

    # 01
    output_name_paths = [
        # '/work/w13/decha/Inter_speech_2016_workplace/gpr-projection-additional/01_gpr_a-5dims_BayesianGPLVMMiniBatch_data_no_delta/',
        # '/work/w13/decha/Inter_speech_2016_workplace/gpr-projection-additional/01_gpr_b-5dims_BayesianGPLVMMiniBatch_data_delta/',
        '/work/w13/decha/Inter_speech_2016_workplace/gpr-projection-additional/01_gpr_c-5dims_BayesianGPLVMMiniBatch_data_delta_deltadelta/'
        ]

    missing_data = True
    subtract_typical_contour = True

    # 02
    # subtract_typical_contour = False
    # output_name_paths = [
    #     '/work/w13/decha/Inter_speech_2016_workplace/gpr-projection-additional/02_gpr_a-5dims_BayesianGPLVMMiniBatch_data_no_delta/',
    #     '/work/w13/decha/Inter_speech_2016_workplace/gpr-projection-additional/02_gpr_b-5dims_BayesianGPLVMMiniBatch_data_delta/',
    #     '/work/w13/decha/Inter_speech_2016_workplace/gpr-projection-additional/02_gpr_c-5dims_BayesianGPLVMMiniBatch_data_delta_deltadelta/'
    #     ]

    print 'Missing Data : {}'.format(missing_data)
    print 'Subtract_typical_contour : {}'.format(subtract_typical_contour)
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
        for tone in ['0','1','2','3','4']:
        # for tone in ['01234']:
            print 'Delta : {}, Delta-Dealta : {}'.format(delta_bool, delta2_bool)
            print 'Missing data'

            # data_object_path = '{}/Inter_speech_2016/Syllable_object/01_manual_labeling_object/syllable_{}.pickle'.format(dropbox_path,tone)

            data_object_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/gpr_syllable_obj/Syllable_object_a_to_d_tone_{}.pickle'.format(tone)

            if tone is '01234':
                # data_object_path = '{}/Inter_speech_2016/Syllable_object/01_manual_labeling_object/syllable_all.pickle'.format(dropbox_path)
                data_object_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/gpr_syllable_obj/Syllable_object_a_to_d.pickle'

            syllable_management = Utility.load_obj(data_object_path)

            output_path = '{}/{}/Tone_{}/'.format(output_name, method_name, tone)

            Utility.make_directory(output_path)

            print output_path

            Latent_variable_model_Training.execute_Bayesian_GPLVM_training(
                syllable_management, 
                Syllable.TRAINING_FEATURE_POLYNOMIAL_2_DEGREE_VOICE, 
                input_dims, 
                output_path,
                subtract_typical_contour=subtract_typical_contour,
                delta_bool=delta_bool,
                delta2_bool=delta2_bool,
                missing_data=missing_data)

    pass

if __name__ == '__main__':

    run_for_missing_data_with_delta_and_interpolate()

    pass
# 