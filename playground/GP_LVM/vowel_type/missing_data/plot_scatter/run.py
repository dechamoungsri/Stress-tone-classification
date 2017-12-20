
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../')
sys.path.append('../../../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/')

from tool_box.util.utility import Utility
from tool_box.plotting.horizontal_histogram.Horizontal_Histogram import HorizontalHistogram
from tool_box.plotting.scatter.scatter_plotting import GP_LVM_Scatter

import numpy as np

def plot_type(plot_type, out_file_path, base_path_list, data_object_path):

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
        label_type=plot_type, 
        perform_unsupervised=True,
        non_unlabelled_stress=False,
        get_only_gpr_data=False, 
        return_after_dbscan=True)

    # sys.exit()

    pass

if __name__ == '__main__':

    # base_data_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/Tonal_object/remove_all_silence_file/'
    base_data_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/mix_object/current_version/'

    base_path_list = [

        '/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/12_missing_data_all/'
        ]

    vowel_type = ['vvv', 'vvvn', 'vvvsg']
    # vowel_type = ['all_vowel_type']
    #['v', 'vv','vn', 'vvn', 'vsg', 'vvsg']

    input_dims = [10]

    name_in_figure = 'LABEL_TYPE_STRESS_GPR'

    for syst in base_path_list:
        for v in Utility.list_file(syst):
            if '.' in v : continue
            for dims in input_dims:

                delta_path = '{}/{}/input_dims_{}'.format(syst, v, dims)
                for d in Utility.list_file(delta_path):
                    if 'alias' in d : continue
                    if d.startswith('.'): continue
                    for tone in Utility.list_file('{}/{}/'.format(delta_path, d)):
                        if tone.startswith('.'): continue
                        # if '01234' not in tone: continue

                        tone_path = '{}/{}/{}/'.format(delta_path, d, tone)

                        name_index = Utility.load_obj('{}/name_index.npy'.format(tone_path))
                        # print name_index
                        # sys.exit()

                        print 'Label for scan : Tone: {} , Vowel: , {}'.format(tone, v)

                        # print tone_path
                        object_data = '{}/{}/syllable_object_{}.pickle'.format(base_data_path, v, tone.split('_')[len(tone.split('_'))-1])
                        # print object_data
                        outpath = '{}/{}.eps'.format(tone_path, name_in_figure)
                        # print outpath

                        plot_type(
                            GP_LVM_Scatter.LABEL_TYPE_STRESS, 
                            outpath, 
                            tone_path, 
                            object_data)

                        # sys.exit()

    pass




