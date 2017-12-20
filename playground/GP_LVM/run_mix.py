
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../')

from tool_box.util.utility import Utility

from DataModel.Syllables.SyllableDatabaseManagement import SyllableDatabaseManagement
from DataModel.Syllables.Syllable import Syllable
from GP_LVM_Tool.latent_variable_model_training import Latent_variable_model_Training

def mix_two_data_base():
    stress_manual_object_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/01_manual_labeling_object/syllable_all.pickle'

    stress_object = Utility.load_obj(stress_manual_object_path)
    syl_list_stress = stress_object.syllables_list

    print len(syl_list_stress)

    syl_list = []

    for syl in syl_list_stress:
        spl = syl.name_index.split('_')
        if (spl[2][0] in ['a','b','c','d']):
            # print syl.name_index
            syl_list.append(syl)

    print len(syl_list)

    gpr_object_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/gpr_syllable_obj/Syllable_object_a_to_d.pickle'
    gpr_object = Utility.load_obj(gpr_object_path)
    gpr_syl_list = gpr_object.syllables_list

    for syl in gpr_syl_list:
        spl = syl.name_index.split('_')
        if (spl[2][0] in ['a','b','c','d']):
            # print syl.name_index
            syl_list.append(syl)

    print len(syl_list)

    syl_obj = SyllableDatabaseManagement(syllable_list=syl_list)
    syl_obj.dump('/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/mix_syllable_obj/mix_syllable_all.pickle')

    for tone in [0,1,2,3,4]:
        tone_obj = SyllableDatabaseManagement(syllable_list=(syl_obj.get_tone_n_syllable(tone)))
        tone_obj.dump('/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/mix_syllable_obj/mix_syllable_{}.pickle'.format(tone))

def run_for_mix(input_dims):

    dropbox_path = '/home/h1/decha/Dropbox/'

    missing_data = True
    subtract_typical_contour = False

    deltas = [
        [False, False],
        [True, False],
        [True, True]
    ]

    print 'This running aims to show the unlabelled data on the labeled data in distribution.'
    print 'Do not use subtract contour'

    data_object = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/mix_syllable_obj/mix_syllable_'

    output_name_paths = [
        '/work/w13/decha/Inter_speech_2016_workplace/mix-projection-addtional/02_mix_a-{}dims_data_no_delta_missing_data_No-subtract_typical_contour/'.format(input_dims),
        '/work/w13/decha/Inter_speech_2016_workplace/mix-projection-addtional/02_mix_b-{}dims_data_delta-{}_delta-delta-{}_missing_data_No-subtract_typical_contour/'.format(input_dims,deltas[1][0],deltas[1][1]),
        '/work/w13/decha/Inter_speech_2016_workplace/mix-projection-addtional/02_mix_c-{}dims_data_delta-{}_delta-delta-{}_missing_data_No-subtract_typical_contour/'.format(input_dims,deltas[2][0],deltas[2][1]),
        ]

    print 'Missing Data : {}'.format(missing_data)
    print 'Subtract_typical_contour : {}'.format(subtract_typical_contour)

    for idx, output_name in enumerate(output_name_paths):

        delta_bool=deltas[idx][0]
        delta2_bool=deltas[idx][1]

        if missing_data:
            method_name = 'BayesianGPLVMMiniBatch_Missing'
        else :
            method_name = 'BGP_LVM'

        for tone in ['0','1','2','3','4','01234']:
        # for tone in ['01234']:

            print 'Delta : {}, Delta-Dealta : {}'.format(delta_bool, delta2_bool)
            print 'Missing data'

            data_object_path = '{}{}.pickle'.format(data_object, tone)

            if tone is '01234':

                data_object_path = '{}all.pickle'.format(data_object)

            print data_object_path

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

    # mix_two_data_base()

    #epsilon
    # for input_dims in [10]:
    #     run_for_mix(input_dims)

    #Beta
    for input_dims in [10]:
        run_for_mix(input_dims)

    pass
