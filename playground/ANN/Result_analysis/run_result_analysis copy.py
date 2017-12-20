
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

def match_process(target_file):

    dim = ''
    vvv = ''
    dur = ''
    name = ''

    data_detail = re.compile(r"""Vowel\s:\s(?P<vvv>.+),\sDelta\s:\s(?P<delta>.+),\sTone\s:\s(?P<tone>.+)""",re.VERBOSE)
    ann_out_path = re.compile(r"""ANN\soutpath\s.+input_dims_(?P<dims>.+)/delta-False_delta-delta-False/.+""",re.VERBOSE)

    number_of_training = re.compile(r"""Number\sof\straining\spatterns:\s\s(?P<num_trn>.+)""",re.VERBOSE)
    input_output_dims = re.compile(r"""Input\sand\soutput\sdimensions: \s(?P<input>.+)\s(?P<output>.+)""",re.VERBOSE)

    lines = Utility.read_file_line_by_line(target_file)
    for idx, line in enumerate(lines):
        if '------------Start-----------' in line:
            dim = ''
            vvv = ''
            dur = ''
            name = ''
            pass
        elif '------------End-----------' in line:

            pass
        elif re.match(data_detail, line):
            # print Utility.trim(line)
            match = re.match(data_detail, line)
            vvv = match.group('vvv')
            if 'No_duration' in vvv:
                dur = 'NoDur'
                vvv = vvv.split('No_duration_')[1]
            else :
                dur = 'Dur'
            pass
        elif re.match(ann_out_path, line):
            match = re.match(ann_out_path, line)
            dim = match.group('dims')
            # print dims
            name = '{}_{}_{}'.format(dim, vvv, dur)
            # print name
            pass
        elif re.match(number_of_training, line):
            match = re.match(number_of_training, line)
            num_trn = match.group('num_trn')
            o = 'Nunber of training data : {}'.format(num_trn)
            printing_info[name].append(o)
        elif re.match(input_output_dims, line):
            match = re.match(input_output_dims, line)
            inputs = match.group('input')
            outputs = match.group('output')
            # print 'Input dims : {}, Output dims : {}'.format(inputs, outputs)
            # printing_info[2] = 'Input dims : {}, Output dims : {}'.format(inputs, outputs)
            o = 'Input dims : {}, Output dims : {}'.format(inputs, outputs)
            printing_info[name].append(o)
        elif 'Plain' in line:
            for ii in range(idx+1, len(lines)):
                if 'Accuracy : ' in lines[ii]:
                    tar = lines[ii].split(' ')
                    # plain_data.append( Utility.trim(tar[2]) )
                    real = 'real_{}_{}'.format( vvv, dur)
                    out_dict[real].append(Utility.trim(tar[2]))
                    break
        elif 'Latent' in line:
            for ii in range(idx+1, len(lines)):
                if 'Accuracy : ' in lines[ii]:
                    tar = lines[ii].split(' ')
                    # latent_data.append( Utility.trim(tar[2]) )
                    out_dict[name].append( Utility.trim(tar[2]) )
                    break
    pass

if __name__ == '__main__':

    target_file = '/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/playground/ANN/10_tone_classification/ann_tone_compare_fold_data_save.txt'

    dims = ['real', '3', '5', '10']
    vowel_type = ['vvv', 'vvvn', 'vvvsg', 'all_vowel_type']
    dur = ['Dur', 'NoDur']

    out_dict = dict()
    printing_info = dict()
    for d in dims:
        for v in vowel_type:
            for du in dur:
                name = '{}_{}_{}'.format(d, v, du)
                # print name
                out_dict[name] = []
                printing_info[name] = []

    match_process(target_file)

    for du in dur:
        method = ''
        print_list = []
        for v in vowel_type:
            for d in dims:
                name = '{}_{}_{}'.format(d, v, du)
                # print name
                method = method + ' , ' + name
                print_list.append(np.mean( np.array(out_dict[name]).astype(np.float) ))
                # print out_dict[name]
        print method
        for p in print_list:
            print("%.2f" % ( p*100))


    pass
