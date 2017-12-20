
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../')
sys.path.append('../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/')
import matplotlib.mlab as mlab
from tool_box.util.utility import Utility
import scipy.stats as stats
from DataModel.Syllables.Syllable import Syllable
from scipy.fftpack import dct

import numpy as np
import matplotlib.pyplot as plt

import re

from tool_box.Latex_tool.latext_tool import Latext_Tool

def find_group(tone, v ,name):

    # if 'n' in v:
    #     v = 'vvvn'
    # elif 'sg' in v:
    #     v = 'vvvsg'
    # else:
    #     v = 'vvv'

    group_path = '/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/06_Tonal_part_projection_noise_reduction-250-iters-opt/{}/input_dims_10/delta-True_delta-delta-True/BGP_LVM_Tone_{}/'.format(v, tone)

    name_index = np.array(Utility.load_obj('{}/name_index.npy'.format(group_path)))
    label = np.array(Utility.load_obj('{}/clustered_label.npy'.format(group_path)))

    # print name
    # print name_index

    if '.' in name:
        print name

    if len(label[name_index==name]) == 0:
        print name
        return 3
    return label[name_index==name][0]

    pass

def run(main_fig_path, out_path):
    vowel_type = ['v', 'vv', 'vn', 'vvn', 'vsg', 'vvsg']
    # vowel_type = ['v', 'vv', 'vn', 'vvn', 'vsg', 'vvsg']
    tones = ['0','1','2','3','4']

    # vowel_type = ['vv']
    # tones = ['1']

    c = dict()
    c[-1] = 'black'
    c[0] = 'blue'
    c[1] = 'red'
    c[2] = 'green'
    c[3] = 'yellow'

    fig_per_line = 4

    syllable_lists = dict()
    # for v in vowel_type:
    for v in ['vvv', 'vvvn', 'vvvsg']:
        for t in tones:

            if v == 'vvv':
                vv = ['v', 'vv']
            elif v == 'vvvn':
                vv = ['vn', 'vvn']
            elif v == 'vvvsg':
                vv = ['vsg', 'vvsg']
            else:
                print 'wtf'

            dire = '{}/{}/'.format(out_path, v)
            Utility.make_directory(dire)
            latext_out_file = '{}/stress-list_vowel-type-{}_Tone-{}.tex'.format(dire, v, t)

            for vi in vv:
                path = '{}/{}/{}/'.format(main_fig_path, vi, t)
                files = Utility.list_file(path)
                file_list = []
                # print files
                for f in files:
                    # tscsd_manual_f17_22_tone_3_dur_15.025_syl_n-aa-m^_stress_0

                    if f.startswith('.'): continue

                    pattern = re.compile(r"""(?P<name>.+)_tone.+dur_(?P<dur>.+)_syl.+_stress_(?P<stress>.+).eps""",re.VERBOSE)
                    match = re.match(pattern, f)
                    # print match
                    if match:
                        dur = float(match.group('dur'))

                        stress = 'Unstress'
                        if int(match.group('stress')) == 1:
                            stress = 'Stress'

                        file_list.append(('{}/{}'.format(path, f), dur, stress, match.group('name')))

                    else :
                        print f

            Utility.sort_by_index(file_list, 1)
            # print file_list

            eps_list = []
            caption_list = []

            temp_eps = []
            temp_cap = []

            for fi in file_list:
                file_path = fi[0]
                dur = fi[1]
                stress = fi[2]
                name = fi[3]

                group = find_group(t, v, name)
                color = c[group]
                # if group != 0:
                #     print v, t
                #     print group, color
                # print '\\textcolor{{{}}}{{{}}}'.format(color,name)
                name = name.replace('_', '\_')
# {\color{red} Panda }
                temp_eps.append(file_path)
                temp_cap.append('{{\color{{{}}} {} }}'.format(color,name))

                if fig_per_line == len(temp_eps):
                    eps_list.append(temp_eps)
                    caption_list.append(temp_cap)

                    temp_eps = []
                    temp_cap = []

            eps_list.append(temp_eps)
            caption_list.append(temp_cap)

            # print len(eps_list)
            if len(eps_list) == 1 : continue
            Latext_Tool.plot_all_data(eps_list, caption_list, latext_out_file)

        pass

if __name__ == '__main__':

    main_fig_path = '/work/w13/decha/Inter_speech_2016_workplace/Fix_stress_label/'

    # out_path = '/work/w13/decha/Inter_speech_2016_workplace/Fix_stress_label/Latex_files_stress_only/'
    out_path = '/work/w13/decha/Inter_speech_2016_workplace/Fix_stress_label/Latex_files/'
    

    run(main_fig_path, out_path)
    
    pass
