
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

import collections

def gen_utt(file_path, out_file):

    out_list = []

    phrase, word, syllable, phone = collections.OrderedDict(), collections.OrderedDict(), collections.OrderedDict(), collections.OrderedDict()

    word_index, syllable_index, phone_index = 0, 0, 0

    output_array = []

    lines = Utility.read_file_line_by_line(file_path)
    for line in lines:
        #regex
        pat = re.compile(r"""
            ^(?P<prev_phoneme>.+)-(?P<cur_phoneme>.+)\+(?P<next_phoneme>.+)
            /A:(?P<prev_phone_position>.+)_.+-(?P<cur_phone_position>.+)_.+\+(?P<next_phone_position>.+)_.+
            /B:(?P<prev_tone>.+)-(?P<cur_tone>.+)\+(?P<next_tone>.+)
            /C:(?P<prev_syllable_position>.+)_.+-(?P<cur_syllable_position>.+)_.+\+(?P<next_syllable_position>.+)_.+
            /D:(?P<prev_number_of_phone>.+)-(?P<cur_number_of_phone>.+)\+(?P<next_number_of_phone>.+)
            /E:(?P<prev_word_position>.+)-(?P<cur_word_position>.+)\+(?P<next_word_position>.+)
            /F:.+_(?P<prev_number_of_syllable>.+)-.+_(?P<cur_number_of_syllable>.+)\+.+_(?P<next_number_of_syllable>.+)
            /G:.+_(?P<number_of_syllable_in_sentence>.+)_(?P<number_of_word_in_sentence>.+)
            /H:(?P<prev_word_partofspeech>.+)_.+-(?P<cur_word_partofspeech>.+)_.+\+(?P<next_word_partofspeech>.+)_.+
            /I:(?P<cur_stress>.+)
            ?
            """,
            re.VERBOSE)

        match = re.match(pat, line)
        if match == None:
            raise(UtteranceException('Unmatched context: {:}'.format(line)))

        #Check if pau or sil add new entity
        if (match.group('cur_phoneme') == 'sil') :
            #Phone unit
            od                = collections.OrderedDict()
            od['unit']        = 'phone'
            od['entity']       = match.group('cur_phoneme')
            output_array.append(od)
        elif (match.group('cur_phoneme') == 'pau') : 
            #Phone unit
            od                = collections.OrderedDict()
            od['unit']        = 'phone'
            od['entity']       = match.group('cur_phoneme')
            output_array[len(output_array)-1]['inners'].append(od)
        else :
            # Check if Start of utterance, add new utterance
            if (match.group('cur_word_position') == '1') & (match.group('cur_syllable_position') == '1') & (match.group('cur_phone_position') == '1') :
                #Utterance unit
                od                = collections.OrderedDict()
                od['unit']        = 'utterance'
                od['inners']       = []
                output_array.append(od)
                #print output_array

            # Check if Start of word, add new word
            if (match.group('cur_syllable_position') == '1') & (match.group('cur_phone_position') == '1') :
                #Word unit
                od                = collections.OrderedDict()
                od['unit']        = 'word'

                word_index+=1
                od['word_index']        = word_index

                od['part_of_speech'] = int(match.group('cur_word_partofspeech'))
                od['inners']       = []
                output_array[len(output_array)-1]['inners'].append(od)
                #print "output_array"

            # Check if Start of syllable, add new syllable
            if (match.group('cur_phone_position') == '1') :
                # Tone entity
                od                = collections.OrderedDict()
                od['unit']        = 'syllable'

                syllable_index+=1
                od['syllable_index']        = syllable_index

                od['tone_type'] = int(match.group('cur_tone'))
                od['stress'] = int(match.group('cur_stress'))
                od['inners']       = []         
                word_index = len(output_array[len(output_array)-1]['inners'])
                output_array[len(output_array)-1]['inners'][word_index-1]['inners'].append(od)
                #print output_array

            # Add new phone
            od                = collections.OrderedDict()
            od['unit']        = 'phone'

            phone_index+=1
            od['phone_index']        = phone_index

            od['entity']       = match.group('cur_phoneme') 
            word_index = len(output_array[len(output_array)-1]['inners'])
            syllable_index = len(output_array[len(output_array)-1]['inners'][word_index-1]['inners'])
            output_array[len(output_array)-1]['inners'][word_index-1]['inners'][syllable_index-1]['inners'].append(od)

    # print output_array
    Utility.yaml_save(out_file, output_array)

    pass

if __name__ == '__main__':

    full_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_data/Manual_labeling_stress_unstress/raw/label_phone/tsc/sd/'

    outpath = '/work/w2/decha/Data/GPR_data/label/09_stress_manual_labeling/utt/tsc/sd/'

    start_set, end_set = 'i', 'i'
    for sett in Utility.char_range(start_set, end_set):
        set_path = '{}/{}/'.format(full_path, sett)

        out_set_path = '{}/{}/'.format(outpath, sett)
        Utility.make_directory(out_set_path)

        for f in Utility.list_file(set_path):
            if f.startswith('.'): continue

            base_name = Utility.get_basefilename(f).split('_')[2]

            out_file = '{}/tscsd{}.utt.yaml'.format(out_set_path, base_name)

            file_path = '{}/{}'.format(set_path, f)
            print out_file
            gen_utt(file_path, out_file)
            # for line in Utility.read_file_line_by_line(file_path):
            # sys.exit()
    pass
