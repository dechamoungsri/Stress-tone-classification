
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
from scipy.fftpack import dct
from scipy.fftpack import idct

import numpy as np
import matplotlib.pyplot as plt

followed_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/list/followed_sil_manual_list.pickle'
followed_list = Utility.load_obj(followed_path)

def interp(y, num_index):
    x = np.linspace(0, len(y), num=num_index)
    return np.interp(np.arange(0,num_index), x, y)

def plot(raw, duration, outpath, syl ,stress, name_index, idct_value, interp_value):
    plt.clf()
    plt.plot(np.arange(len(raw)), raw, 'b-')
    plt.plot(np.arange(len(raw)), idct_value, 'r-')
    # plt.plot(np.arange(len(raw)), interp_value, 'g-')
    print outpath
    dur_x = 0
    for d in duration:
        dur_x += d
        plt.plot((dur_x, dur_x), (plt.ylim()[0], plt.ylim()[1]), 'k--')
    
    if stress == '1':
        plt.text(plt.xlim()[1], plt.ylim()[1], 'Stress',
        verticalalignment='top', horizontalalignment='right',
        color='red', fontsize=25)
        # print outpath

    if name_index in followed_list:
        plt.text(plt.xlim()[0], plt.ylim()[1], 'Followed by silence',
        verticalalignment='top', horizontalalignment='left',
        color='green', fontsize=25)
        # print 'sil', outpath

    plt.title('{}, Stress : {}'.format(syl, stress))
    # print outpath
    plt.savefig(outpath)

def plot_syllable(syllable_list, outpath):

    num = 50

    for syl in syllable_list:

        raw = np.copy(syl.raw_data)
        duration = syl.phone_duration

        start_end = syl.get_start_end_voice_region(syl.get_tonal_part_data())

        raw[raw<0] = np.nan
        raw = np.exp(raw)

        # print start_end
        start = start_end[0] + duration[0]
        end = start_end[1] + duration[0]
        # print start, end

        # print len(syl.training_feature[Syllable.Training_feature_tonal_part_dct_coeff])
        # print syl.training_feature[Syllable.Training_feature_tonal_part_dct_coeff][0]

        coeff_number = 5
        window = np.zeros(len(syl.training_feature[Syllable.Training_feature_tonal_part_dct_coeff]))
        window[:coeff_number] = 1

        idctx = dct(syl.training_feature[Syllable.Training_feature_tonal_part_dct_coeff]*window, 3, norm='ortho')
        indx = np.arange(len(idctx))
        idctx = np.interp(np.linspace(0, len(idctx), num=end-start+1 ) , indx, idctx)

        # print idctx

        idct_value = np.arange(len(raw)).astype(float)
        idct_value.fill(np.nan)
        idct_value[np.arange(start,end).astype(int)] = idctx

        # print idct_value

        interp = np.exp(syl.training_feature[Syllable.Training_feature_tonal_part_raw_remove_head_tail_interpolated])
        interp = np.interp(np.linspace(0, len(interp), num=end-start+1 ) , np.arange(len(interp)), interp)
        interp_value = np.arange(len(raw)).astype(float)
        interp_value.fill(np.nan)
        interp_value[np.arange(start,end).astype(int)] = interp

        # if syl.name_index == 'tscsd_manual_a24_42':
        #     print np.exp(syl.training_feature[Syllable.Training_feature_tonal_part_raw_remove_head_tail_interpolated])
        #     print interp
        #     print interp_value
            
        #     print interp_value
        #     sys.exit()

        out = '{}/{}_tone_{}_dur_{}_syl_{}_stress_{}.eps'.format(
            outpath, syl.name_index, 
            syl.tone, syl.get_tonal_duration(), 
            '{}-{}-{}'.format(syl.consonant, syl.vowel, syl.final_consonant), 
            syl.stress_manual)

        plot(raw, duration, out, '{}-{}-{}, Tone: {}, Tonal duration: {}'.format(syl.consonant, syl.vowel, syl.final_consonant, syl.tone, syl.get_tonal_duration()), syl.stress_manual, syl.name_index, idct_value, interp_value)

    pass

def run(syllable_object, main_out_path):
    vowel_type = ['v', 'vv', 'vn', 'vvn', 'vsg', 'vvsg']
    tones = ['0','1','2','3','4']

    syllable_lists = dict()
    for v in vowel_type:
        for t in tones:
            syllable_lists['{}_{}'.format(v, t)] = []

    for syl in syllable_object.syllables_list:
        syllable_lists['{}_{}'.format(syl.get_vowel_length_type(), syl.tone)].append(syl)

    for s in syllable_lists:
        spl = s.split('_')
        outpath = '{}/{}/{}/'.format(main_out_path, spl[0], spl[1])
        Utility.make_directory(outpath)
        plot_syllable(syllable_lists[s], outpath)

if __name__ == '__main__':

    syllable_object = Utility.load_obj('/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/Tonal_object/remove_all_silence_file/all_vowel_type/syllable_object_01234.pickle')

    main_out_path = '/work/w13/decha/Inter_speech_2016_workplace/Fix_stress_label/'

    # run(syllable_object, main_out_path)
    
    print 'finish'

    pass
