
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
from DataModel.Syllables.SyllableDatabaseManagement import SyllableDatabaseManagement

import numpy as np
import matplotlib.pyplot as plt
import re

if __name__ == '__main__':

    # target_file = '/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/playground/ANN/09b_500_iters/3dim_all.txt'
    target_file = '/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/playground/ANN/10_tone_classification/ann_tone_compare_fold_data_save.txt'
    # target_file = '/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/playground/ANN/09_stress_classification/ann_vvv_vvvn_vvvsg_0_1_2_3_4.txt'
    # target_file = '/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/playground/ANN/09_stress_classification/no_use_input_sensitivoty.txt'
    # pattern = re.compile(r"""(?P<start>.+)\s(?P<end>.+)\s.+\-(?P<curphone>.+)\+.+/A:.+""",re.VERBOSE)
    # match = re.match(pattern, line)
    # if match:
       
    #    phone = match.group('curphone')

    data_detail = re.compile(r"""Vowel\s:\s(?P<vvv>.+),\sDelta\s:\s(?P<delta>.+),\sTone\s:\s(?P<tone>.+)""",re.VERBOSE)
    # ann_out_path = re.compile(r"""ANN\soutpath\s.+input_dims_(?P<dims>.+)/delta-False_delta-delta-False/.+""",re.VERBOSE)
    ann_out_path = re.compile(r"""ANN\soutpath\s.+Tonal_projection/10_tone_classification//(?P<vvv_type>.+)/input_dims_(?P<dims>.+)/delta-False_delta-delta-False/.+""",re.VERBOSE)

    number_of_training = re.compile(r"""Number\sof\straining\spatterns:\s\s(?P<num_trn>.+)""",re.VERBOSE)
    input_output_dims = re.compile(r"""Input\sand\soutput\sdimensions: \s(?P<input>.+)\s(?P<output>.+)""",re.VERBOSE)

    plain_data = []
    latent_data = []

    printing_info = [0,1,2]

    # out result
    out_result = dict()
    out_result['real'] = []

    # dims_run = ['3']
    dims_run = ['3', 'No_3', '5', 'No_5', '10', 'No_10']

    for d in dims_run:
        out_result[d] = ''

    lines = Utility.read_file_line_by_line(target_file)
    for idx, line in enumerate(lines):
        if '------------Start-----------' in line:
            plain_data = []
            latent_data = []
            printing_info = [0,1,2]
            if len(out_result['real']) == 0:
                print '------------Start-----------'
            pass
        elif '------------End-----------' in line:
            plain_data = np.array(plain_data).astype(np.float)
            latent_data = np.array(latent_data).astype(np.float)
            # print plain_data
            # print dims

            # out_result['real'].append(np.mean(plain_data))
            out_result['real'].append(plain_data)
            out_result[dims] = np.mean(latent_data)

            if len(out_result['real']) == len(dims_run):
                print out_result['real']
                for p in printing_info:
                    print p
                # print 'Real score : {}'.format(np.mean(out_result['real']))
                # print np.mean(out_result['real'])
                print("%.2f" % (np.mean(out_result['real'])*100))
                for d in dims_run:
                    print d
                for idx, d in enumerate(dims_run):
                    # print 'N_Dim : {}, score : {}'.format(d, out_result[d])
                    # print out_result[d]
                    # print out_result
                    print("%.2f" % (out_result[d]*100))
                print '------------End-----------'
                out_result['real'] = []
                for d in dims_run:
                    out_result[d] = ''
                # break
        elif re.match(data_detail, line):
            # print Utility.trim(line)
            printing_info[0] = Utility.trim(line)
            pass
        elif re.match(ann_out_path, line):
            match = re.match(ann_out_path, line)
            dims = match.group('dims')
            vvv_type = match.group('vvv_type')
            # print dims, vvv_type
            if 'No_duration' in vvv_type:
                vvv_type = 'No'
                dims = '{}_{}'.format(vvv_type, dims)
            # print dims
            # print 'N dims : {}'.format(dims)
            # printing_info[0] = dims
        elif re.match(number_of_training, line):
            match = re.match(number_of_training, line)
            num_trn = match.group('num_trn')
            # print 'Nunber of training data : {}'.format(num_trn)
            printing_info[1] = 'Nunber of training data : {}'.format(num_trn)
        elif re.match(input_output_dims, line):
            match = re.match(input_output_dims, line)
            inputs = match.group('input')
            outputs = match.group('output')
            # print 'Input dims : {}, Output dims : {}'.format(inputs, outputs)
            printing_info[2] = 'Input dims : {}, Output dims : {}'.format(inputs, outputs)
        elif 'Plain' in line:
            for ii in range(idx+1, len(lines)):
                if 'Accuracy : ' in lines[ii]:
                    tar = lines[ii].split(' ')
                    plain_data.append( Utility.trim(tar[2]) )
                    break
        elif 'Latent' in line:
            for ii in range(idx+1, len(lines)):
                if 'Accuracy : ' in lines[ii]:
                    tar = lines[ii].split(' ')
                    latent_data.append( Utility.trim(tar[2]) )
                    break

    pass
