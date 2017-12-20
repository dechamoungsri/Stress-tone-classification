
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

def add_data_object():

    obj = Utility.load_obj('/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/mix_object/current_version/all_vowel_type/syllable_object_01234.pickle')

    name_index = Utility.load_obj('/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/11_missing_data/all_vowel_type/input_dims_10/delta-True_delta-delta-True/BayesianGPLVMMiniBatch_Missing_Tone_01234/name_index.npy')
    name_index = np.array(name_index)

    model = Utility.load_obj('/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/11_missing_data/all_vowel_type/input_dims_10/delta-True_delta-delta-True/BayesianGPLVMMiniBatch_Missing_Tone_01234/GP_model.npy')

    data = np.array(model.X.mean)
    print data.shape

    for syl in obj.syllables_list:
        name = syl.name_index
        if 'gpr' not in name: continue

        name_position = np.where(name_index == name)
        # print name_position
        latent_data = data[name_position][0]
        # print latent_data
        syl.set_latent_for_single_space(latent_data)
        # print syl.single_space_latent
        # sys.exit()
    Utility.save_obj(obj, '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/mix_object/current_version/all_vowel_type/syllable_object_01234.pickle')

def gen_json_data():
    outpath = '/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/playground/generate_json/latent_data/'
    obj = Utility.load_obj('/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/mix_object/current_version/all_vowel_type/syllable_object_01234.pickle')
    start_set, end_set = 'a', 'j'
    base_path = '/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/playground/list_file_for_preceeding_suceeding/list_gpr_file/'
    for sett in Utility.char_range(start_set, end_set):
        set_path = '{}/{}/'.format(base_path, sett)

        for f in Utility.list_file(set_path):
            if f.startswith('.'): continue

            file_path = '{}/{}'.format(set_path, f)
            out_list = []
            for line in Utility.read_file_line_by_line(file_path):
                name = Utility.trim(line)
                # "duration" "syllable_context"
                duration = ''
                syllable_context = ''

                d = dict()

                if name == 'sil':
                    syllable_context = 'sil-sil-sil-x'
                    duration = [0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0, 0.0]
                elif name == 'pau':
                    syllable_context = 'pau-pau-pau-x'
                    duration = [0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0, 0.0]
                else:
                    syl = obj.get_syllable_by_name_index(name)
                    syllable_context = '{}-{}-{}-{}'.format(syl.consonant, syl.vowel, syl.final_consonant, syl.tone)
                    duration = syl.single_space_latent.tolist()

                d['duration'] = duration
                d['syllable_context'] = syllable_context
                out_list.append(d)

            outfile_path = '{}/tscsd{}.json'.format(outpath, f)
            Utility.save_json(outfile_path, out_list)


if __name__ == '__main__':

    # add_data_object()
    gen_json_data()

    pass

