
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('../../')

from tool_box.util.utility import Utility
from tool_box.plotting.histogram.histogram import VerticalHistogram

from tool_box.Latex_tool.latext_tool import Latext_Tool

import numpy as np

def run_export_input_sensitivity(system_paths, tones):

    for path in system_paths:
        for tone in tones:
            target_path = '{}/Tone_{}/'.format(path,tone)

            model = Utility.load_obj('{}/GP_model.npy'.format(target_path))
            input_sensitivity = model.input_sensitivity()

            data = model.X.mean
            data_object = np.array(data)

            input_sensitive_path = '{}/input_sentivity.npy'.format(target_path)
            data_object_path = '{}/data_object.npy'.format(target_path)
            
            Utility.save_obj(input_sensitivity, input_sensitive_path)
            Utility.save_obj(data_object, data_object_path)

def run_plot_input_sensitivity(system_paths, tones):

    for path in system_paths:
        for tone in tones:
            target_path = '{}/Tone_{}/'.format(path,tone)
            input_sensitivity = Utility.load_obj('{}/input_sentivity.npy'.format(target_path))
            print target_path
            # print input_sensitivity
            # print map(str, range(len(input_sensitivity)))
            VerticalHistogram.plot(input_sensitivity, range(len(input_sensitivity)), 'Tone '.format(tone), '{}/input_sensitivity.eps'.format(target_path))

    pass

def run_gen_latex(system_paths, tones, captions, target, output_file):

    figure_array = []
    caption_array = []

    for i, path in enumerate(system_paths):

        fig = []
        cap = []

        for tone in tones:
            target_path = '{}/Tone_{}/{}.eps'.format(path,tone,target)
            fig.append(target_path)
            cap.append('{}, T: {}'.format(captions[i], tone))

        figure_array.append(fig)
        caption_array.append(cap)

    # outpath = '/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/Inter_speech_2016/temporary_output/analysis_of_inputsensitivity/input_sensitivity.tex'
    outpath = '{}_{}.tex'.format(output_file, target)
    Latext_Tool.plot_all_data(figure_array, caption_array, outpath)

    pass

if __name__ == '__main__':

    system_paths = [
        # '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/01_manual_labeling_object/BGP_LVM/',
        # '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/02_delta_delta-delta/BGP_LVM/',
        # '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/03_delta/BGP_LVM/',
        # '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/04_no_delta/BGP_LVM/',
        # '/work/w13/decha/Inter_speech_2016_workplace/Data/05_missing_data_no_delta/BGP_LVM/',
        # '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/06_02_with_3-dimentionality/BGP_LVM/',
        # '/work/w13/decha/Inter_speech_2016_workplace/Data/07a_missing_data_no_delta/BayesianGPLVMMiniBatch_Missing/',
        '/work/w13/decha/Inter_speech_2016_workplace/Data/07a-5dims_missing_data_no_delta/BayesianGPLVMMiniBatch_Missing/',
        # '/work/w13/decha/Inter_speech_2016_workplace/Data/07b_missing_data_delta/BayesianGPLVMMiniBatch_Missing/',
        '/work/w13/decha/Inter_speech_2016_workplace/Data/07b-5dims_missing_data_delta/BayesianGPLVMMiniBatch_Missing/',
        # '/work/w13/decha/Inter_speech_2016_workplace/Data/07c_missing_data_delta_deltadelta/BayesianGPLVMMiniBatch_Missing/',
        '/work/w13/decha/Inter_speech_2016_workplace/Data/07c-5dims_missing_data_delta_deltadelta/BayesianGPLVMMiniBatch_Missing/',
        '/work/w13/decha/Inter_speech_2016_workplace/Data/08a-5dims_BayesianGPLVMMiniBatch_data_no_delta/BayesianGPLVMMiniBatch/',
        '/work/w13/decha/Inter_speech_2016_workplace/Data/08b-5dims_BayesianGPLVMMiniBatch_data_delta/BayesianGPLVMMiniBatch/',
        '/work/w13/decha/Inter_speech_2016_workplace/Data/08c-5dims_BayesianGPLVMMiniBatch_data_delta_deltadelta/BayesianGPLVMMiniBatch/'
        ]

    system_paths = [
        '/work/w13/decha/Inter_speech_2016_workplace/Data/07a-5dims_missing_data_no_delta/BayesianGPLVMMiniBatch_Missing/',
        '/work/w13/decha/Inter_speech_2016_workplace/Data/08a-5dims_BayesianGPLVMMiniBatch_data_no_delta/BayesianGPLVMMiniBatch/',
        '/work/w13/decha/Inter_speech_2016_workplace/Data/07b-5dims_missing_data_delta/BayesianGPLVMMiniBatch_Missing/',
        '/work/w13/decha/Inter_speech_2016_workplace/Data/08b-5dims_BayesianGPLVMMiniBatch_data_delta/BayesianGPLVMMiniBatch/',
        '/work/w13/decha/Inter_speech_2016_workplace/Data/07c-5dims_missing_data_delta_deltadelta/BayesianGPLVMMiniBatch_Missing/',
        '/work/w13/decha/Inter_speech_2016_workplace/Data/08c-5dims_BayesianGPLVMMiniBatch_data_delta_deltadelta/BayesianGPLVMMiniBatch/'
        ]


    captions = [
        # '01',
        # '02',
        # '03',
        # '04',
        # '05',
        # '06',
        # '07a',
        '07a5',
        # '07b',
        '07b5',
        # '07c',
        '07c5',
        '08a5',
        '08b5',
        '08c5'
        ]

    captions = [
        '07a5',
        '08a5',
        '07b5',
        '08b5',
        '07c5',
        '08c5'
        ]

    tones = [
        '0',
        '1',
        '2',
        '3',
        '4',
        '01234'
        ]

    # run_export_input_sensitivity(system_paths, tones)
    # run_plot_input_sensitivity(system_paths, tones)

    output_file = '/home/h1/decha/Dropbox/Inter_speech_2016/temporary_output/analysis_of_inputsensitivity/08_07_abc_5dims'

    run_gen_latex(system_paths, tones,captions,'input_sensitivity',output_file)
    run_gen_latex(system_paths, tones,captions,'stress_unstress_plot',output_file)

    # system_names = ['02_delta_delta-delta','03_delta','04_no_delta','05_missing_data_no_delta','06_02_with_3-dimentionality']
    # latex_gen(system_names)

    pass