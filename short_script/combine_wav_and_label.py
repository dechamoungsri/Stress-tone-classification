
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

import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    wav_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_data/Manual_labeling_stress_unstress/raw/wav/tsc/sd/'
    label_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_data/Manual_labeling_stress_unstress/raw/label/'

    outpath = '/work/w13/decha/Inter_speech_2016_workplace/Fix_stress_label/wavfile_working/'

    start_set, end_set = 'a', 'h'

    for sett in Utility.char_range(start_set, end_set):
        set_path = '{}/{}/'.format(wav_path, sett)

        setout = '{}/{}/'.format(outpath, sett)
        Utility.make_directory(setout)

        for f in Utility.list_file(set_path):
            if f.startswith('.'): continue

            basename = f.split('.')[0]
            print basename

            wav_file = '{}/{}/{}'.format(wav_path, sett, f)
            label_file = '{}/{}/{}.lab'.format(label_path, sett, basename)

            out = []
            count = 0
            for line in Utility.read_file_line_by_line(label_file):
                spl = line.split(' ')

                if  ('-sil+' in line) | ('-pau+' in line) :
                    out.append('{} {} {}'.format(spl[0], spl[1], 'sil'))
                else :
                    count+=1
                    out.append('{} {} {}'.format(spl[0], spl[1], count))
            
            dest_wav = '{}/{}/{}'.format(outpath, sett, f)
            dest_label = '{}/{}/{}.lab'.format(outpath, sett, basename)

            Utility.copyFile(wav_file, dest_wav)
            Utility.write_to_file_line_by_line(dest_label, out)

    pass
