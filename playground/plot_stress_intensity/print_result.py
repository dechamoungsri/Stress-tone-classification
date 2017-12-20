
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

log_file = '/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/playground/GP_LVM/vowel_type/Result_analysis/recogniton_result.txt'

p =  []

for line in Utility.read_file_line_by_line(log_file):

    if '01234' in line: continue

    if 'Label for scan' in line:
        p =  []
        p.append(Utility.trim(line))
    elif 'Accuracy score :' in line:
        # print Utility.trim(line)
        if len(p) == 0:
            continue

        p.append(Utility.trim(line))

        ppp = ''

        for pp in p:
            ppp+=pp +' | '
        print ppp

        # /work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/06_Tonal_part_projection_noise_reduction-250-iters-opt//vvvsg/input_dims_10/delta-True_delta-delta-False/BGP_LVM_Tone_2//LABEL_TYPE_STRESS.eps
    elif 'LABEL_TYPE_STRESS' in line:
        if not 'delta-True_delta-delta-True' in line:
            p = []
            continue
        spl = line.split('delta')
        p.append('{}, {}'.format(spl[1][1:6], spl[3][1:6]))
        # print spl[1][1:6], spl[3][1:6]

