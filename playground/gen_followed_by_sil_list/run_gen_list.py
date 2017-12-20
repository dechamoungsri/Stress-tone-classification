
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

def run_gen(base_path, start_set, end_set, pattern, outpath):

    out = []

    for sett in Utility.char_range(start_set, end_set):
        set_path = '{}/{}/'.format(base_path, sett)
        for f in Utility.list_file(set_path):
            if f.startswith('.'): continue
            file_path = '{}/{}'.format(set_path, f)
            # print file_path

            count = 0
            # tscsd_gpr_g37_13

            prefix = 'tscsd_gpr'

            lines = Utility.read_file_line_by_line(file_path)

            for idx, line in enumerate(lines):
                # print line
                match = re.match(pattern, line)
                if match:
                   phone = match.group('curphone')
                   # print phone

                   if phone not in ['sil', 'pau']:
                        count+=1
                        # print f
                        name_index = '{}_{}{}_{}'.format(prefix, sett, f[6:8], count)

                        if ( 'sil-sil+sil/A:' in lines[idx+1] ) | ( 'pau-pau+pau/A:' in lines[idx+1] ) :
                            print name_index
                            out.append(name_index)

    print len(out)
    outpath_file = '{}/gpr_followed_by_sil_list.npy'.format(outpath)
    Utility.save_obj(out, outpath_file)

    pass

if __name__ == '__main__':

    base_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Training_data/03_GPR_syllable_level/full_time/tsc/sd/'
    start_set = 'a'
    end_set = 'j'

    outpath = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/gpr_syllable_obj/'

    pattern = re.compile(r"""(?P<start>.+)\s(?P<end>.+)\s.+\-(?P<curphone>.+)\+.+/A:.+""",re.VERBOSE)

    # name_index_path = '/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/07_06with_mix_data/vvv/input_dims_10/delta-True_delta-delta-True/BGP_LVM_Tone_2/name_index.npy'

    # print Utility.load_obj(name_index_path)

    run_gen(base_path, start_set, end_set, pattern, outpath)

    pass
