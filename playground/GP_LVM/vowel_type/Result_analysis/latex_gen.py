
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../')
sys.path.append('../../../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/')

from tool_box.util.utility import Utility
from tool_box.plotting.horizontal_histogram.Horizontal_Histogram import HorizontalHistogram
from tool_box.plotting.scatter.scatter_plotting import GP_LVM_Scatter
from tool_box.Latex_tool.latext_tool import Latext_Tool
import numpy as np

if __name__ == '__main__':

    base_data_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/Tonal_object/remove_all_silence_file/'

    base_path_list = [
       '/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/06_Tonal_part_projection_noise_reduction-250-iters-opt/'
        ]

    vowel_type = ['vvv', 'vvvn','vvvsg']
    #['v', 'vv','vn', 'vvn', 'vsg', 'vvsg']

    input_dims = [10]

    # /work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/06_Tonal_part_projection_noise_reduction-250-iters-opt/vvvn/input_dims_10/delta-True_delta-delta-False/BGP_LVM_Tone_0/stress_unstress_clustering.pdf 

    deltas = [
        [False, False],
        [True, False],
        [True, True]
    ]

    name_in_figure = 'LABEL_TYPE_STRESS'

    outpath = '/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/06_Tonal_part_projection_noise_reduction-250-iters-opt/'
    for syst in base_path_list:
        for v in vowel_type:
            for dims in input_dims:
                dims_path = '{}/{}/input_dims_{}'.format(syst, v, dims)

                tone_on_delta = [[],[],[],[],[]]
                caption_on_delta = [[],[],[],[],[]]

                for idx, d in enumerate(deltas):
                    deltas_path = '{}/delta-{}_delta-delta-{}/'.format(dims_path, d[0], d[1])
                    for tone in ['0', '1', '2', '3', '4']:#Utility.list_file('{}/{}/'.format(delta_path, d)):
                        # tone_figure_path = '{}/BGP_LVM_Tone_{}/stress_unstress_clustering_kmeans.eps'.format(deltas_path, tone)
                        tone_figure_path = '{}/BGP_LVM_Tone_{}/stress_unstress_clustering_lengthscale.eps'.format(deltas_path, tone)
                        # tone_figure_path = '{}/BGP_LVM_Tone_{}/LABEL_TYPE_STRESS.eps'.format(deltas_path, tone)
                        import os.path
                        if os.path.isfile(tone_figure_path) :
                            # print tone_figure_path
                            tone_on_delta[int(tone)].append(tone_figure_path)
                            caption_on_delta[int(tone)].append('Tone : {}, {}, {}'.format(tone, d[0], d[1]))
                        else :
                            print tone_figure_path

                latext_out_file = '{}/{}.tex'.format(outpath, v)
                # latext_out_file = '{}/{}_kmeans.tex'.format(outpath, v)
                # latext_out_file = '{}/{}_manual_labeling.tex'.format(outpath, v)

                Latext_Tool.plot_all_data(tone_on_delta, caption_on_delta, latext_out_file)

    pass