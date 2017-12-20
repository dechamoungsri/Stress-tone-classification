
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../')
sys.path.append('../../../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/')

from tool_box.util.utility import Utility
from tool_box.plotting.horizontal_histogram.Horizontal_Histogram import HorizontalHistogram
from tool_box.plotting.scatter.scatter_plotting import GP_LVM_Scatter

import numpy as np

def get_stress_unstress(name_index, label_clustered, outpath):

    name_index = np.array(name_index)
    label_clustered = np.array(label_clustered)

    print len(set(label_clustered))

    group_dict = dict()
    
    for g in set(label_clustered):
        group_dict[g] = name_index[label_clustered == g]
        print g, len(group_dict[g])
        # print group_dict[g]
        Utility.save_obj(group_dict[g], '{}/{}.npy'.format(outpath, g))


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
        for v in vowel_type:
            if '.' in v : continue
            for dims in input_dims:
                delta_path = '{}/{}/input_dims_{}/delta-True_delta-delta-True/'.format(syst, v, dims)
                for tone in ['0','1','2','3','4']: #Utility.list_file('{}/'.format(delta_path)):
                    if tone.startswith('.'): continue
                    tone = 'BGP_LVM_Tone_{}'.format(tone)
                    tone_path = '{}/{}/'.format(delta_path, tone)
                    print v
                    print tone
                    print tone_path

                    outpath = '{}/group_list/'.format(tone_path)
                    Utility.make_directory(outpath)

                    object_data = '{}/{}/syllable_object_{}.pickle'.format(base_data_path, v, tone.split('_')[len(tone.split('_'))-1])
                    # print object_data

                    if '01234' in tone: continue

                    name_index = Utility.load_obj('{}/name_index.npy'.format(tone_path))
                    # print name_index

                    label_clustered = Utility.load_obj('{}/clustered_label.npy'.format(tone_path))

                    get_stress_unstress(name_index, label_clustered, outpath)
                    # sys.exit()

    pass




