

import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../')
sys.path.append('../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/')
import matplotlib.mlab as mlab
from tool_box.util.utility import Utility

from DataModel.Syllables.Syllable import Syllable

if __name__ == '__main__':

    mono_label = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_data/Manual_labeling_stress_unstress/raw/mono/tsc/sd/b/tscsd_stust_b03.lab'
    full_label = '/home/h1/decha/data/TrainingData/label/Stress-labeling/full_stress_addtime/nc_th_1_118_18_2.lab'

    mono = Utility.read_file_line_by_line(mono_label)
    full = Utility.read_file_line_by_line(full_label)

    outfile = []

    for i in range(len(full)):
        spl = full[i].split(' ')
        mon_spl = mono[i+1].split(' ')

        out = '{} {} {}'.format(mon_spl[0], mon_spl[1], spl[2].strip())
        print out
        outfile.append(out)

    # Utility.write_to_file_line_by_line(full_label, outfile)

    pass


# mono_label = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_data/Manual_labeling_stress_unstress/raw/mono/tsc/sd/'

# full_label = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_data/Manual_labeling_stress_unstress/raw/label_phone/tsc/sd/'

# start_set, end_set = 'a', 'h'

# for sett in Utility.char_range(start_set, end_set):
#     set_path = '{}/{}/'.format(mono_label, sett)
#     for f in Utility.list_file(set_path):
#         if f.startswith('.') : continue
#         file_path = '{}/{}'.format(set_path, f)
#         mono = Utility.read_file_line_by_line(file_path)

#         full_file = '{}/{}/{}'.format(full_label, sett, f)
#         # print full_file
#         full = Utility.read_file_line_by_line(full_file)

#         if len(full) != len(mono):
#             print f
