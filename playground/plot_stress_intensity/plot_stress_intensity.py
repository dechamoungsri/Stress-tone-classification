
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
from sklearn import preprocessing

import numpy as np
import matplotlib.pyplot as plt
import GPy
import re

def plot(lf0_path, label_path, filename, sett, intensity_path):

    lf0 = Utility.read_lf0_into_ascii('{}/{}/{}.lf0'.format(lf0_path, sett, filename))

    lf0[lf0<0] = np.nan

    intense_object = Utility.load_obj(intensity_path)

    xtic_list = []
    intensity_position = []
    syl_ist = []
    count = 0
    # print '{}/{}/{}.lab'.format(label_path, sett, filename)
    for line in Utility.read_file_line_by_line('{}/{}/{}.lab'.format(label_path, sett, filename)):
        spl = line.split(' ')
        xtic_list.append(float(spl[1])/50000)
        pos = (float(spl[1])/50000 + float(spl[0])/50000) /2

        text_pos = (float(spl[0])/50000 )#+ float(spl[0])/50000) /2

        intentsity = np.nan
        if not (('-sil+' in spl[2] ) | ('-pau+' in spl[2] )):
            count+=1
            key = 'tscsd_manual_{}_{}'.format(filename[12:12+3], count)
            intentsity = intense_object[key]
            print intentsity

        pattern = re.compile(r"""
            .+
            /J:.+-(?P<consonant>.+)\+.+
            /K:.+-(?P<vowel>.+)\+.+
            /L:.+-(?P<finalconsonant>.+)\+.+""",re.VERBOSE)
        match = re.match(pattern, spl[2])
        if match:
           
           syl = '{}-{}-{}'.format(match.group('consonant'), match.group('vowel'), match.group('finalconsonant'))
           print syl
           syl_ist.append((text_pos, syl))

        intensity_position.append([pos,intentsity])

    plt.plot(range(len(lf0)), lf0)
    for x in xtic_list:
        plt.plot([x, x], [plt.ylim()[0], plt.ylim()[1]], 'k--', lw=1)

    for t in syl_ist:
        plt.text(t[0], plt.ylim()[1], t[1],fontsize=8,rotation=45,
        color='green')

    ax2 = plt.twinx()

    xx, yy = np.array([]), np.array([])
    temp = 0
    for p in intensity_position:
        if len(yy)==0:
            temp = p[0]
        else:
            temp+=p[0]

        a = np.empty(p[0])
        a.fill(p[1])
        yy = np.append(yy,a)

    print len(yy)
    # print intensity_position

    intensity_position = np.array(intensity_position)

    xx = intensity_position[:,0]
    yy = intensity_position[:,1]


    ax2.plot(xx, yy, 'r-')
    ylim = ax2.get_ylim()
    ax2.set_ylim(ylim[0], 1.15)
    plt.gcf().set_size_inches(14, 3)
    plt.savefig('./test.eps')

    pass

if __name__ == '__main__':

    lf0_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_data/Manual_labeling_stress_unstress/raw/lf0/'
    label_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_data/Manual_labeling_stress_unstress/raw/label/'
    filename = 'tscsd_stust_a45'
    sett = 'a'
    intensity_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/Tonal_object/stress_intensity_dict-use_delta_and_delta-delta.npy'
    plot(lf0_path, label_path, filename, sett, intensity_path)
    pass





