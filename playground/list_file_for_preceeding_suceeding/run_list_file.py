
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

def gen_file_list():

    outpath = '/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/playground/list_file_for_preceeding_suceeding/list_gpr_file/'

    label_path = '/work/w2/decha/Data/GPR_data/label/03_GPR_syllable_level/full/tsc/sd/'
    start_set = 'a'
    end_set = 'j'

    for sett in Utility.char_range(start_set, end_set):
        set_path = '{}/{}/'.format(label_path, sett)

        out_set_path = '{}/{}/'.format(outpath, sett)
        Utility.make_directory(out_set_path)

        for f in Utility.list_file(set_path):
            if f.startswith('.'): continue
            file_path = '{}/{}'.format(set_path, f)
            count = 0
            # print f
            file_number = f[6] + f[7]

            out_list = []

            for line in Utility.read_file_line_by_line(file_path):
                # print Utility.trim(line)
                out = ''
                if 'sil-sil+sil/A:' in line:
                    out = 'sil'
                elif 'pau-pau+pau/A:' in line:
                    out = 'pau'
                else:
                    count += 1
                    out = 'tscsd_gpr_{}{}_{}'.format(sett, file_number, count)
                # print out
                out_list.append(out)

            if len(out_list) != len(Utility.read_file_line_by_line(file_path)):
                print file_path

            out_file_name = '{}/{}{}.lab'.format(out_set_path, sett, file_number)
            # print out_file_name

            Utility.write_to_file_line_by_line(out_file_name, out_list)

def set_pre_suc():
    tones = ['01234']

    name_list_path = '/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/playground/list_file_for_preceeding_suceeding/list_gpr_file/'

    for t in tones:
        path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/mix_object/current_version/all_vowel_type/syllable_object_{}.pickle'.format(t)
        print path

        syl_management = Utility.load_obj(path)
        for syl in syl_management.syllables_list:
            if 'manual' in syl.name_index: continue

            name = syl.name_index.split('_')
            file_tar = '{}/{}/{}.lab'.format(name_list_path, name[2][0], name[2])
            list_file = Utility.read_file_line_by_line(file_tar)
            for idx, l in enumerate(list_file):
                f = Utility.trim(l)
                if f == syl.name_index:
                    # print '--------------------'
                    preceeding = Utility.trim(list_file[idx-1])
                    # print f
                    succeeding = Utility.trim(list_file[idx+1])
                    # print '--------------------'
                    syl.set_preceeding_succeeding_name_index(preceeding, succeeding)

            # sys.exit()

        Utility.save_obj(syl_management, path)

if __name__ == '__main__':
    # tscsd_gpr_a01_1
    tones = ['01234']

    name_list_path = '/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/playground/list_file_for_preceeding_suceeding/list_gpr_file/'

    for t in tones:
        path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/mix_object/current_version/all_vowel_type/syllable_object_{}.pickle'.format(t)
        print path

        syl_management = Utility.load_obj(path)

        for syl in syl_management.syllables_list:
            if 'manual' in syl.name_index: continue

            print syl.preceeding_name, syl.name_index, syl.succeeding_name


    # object_syl = Utility.load_obj('/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/mix_object/current_version/all_vowel_type/syllable_object_01234.pickle')

    # print object_syl.syllables_list[0].name_index
           # sys.exit()
    pass
