
import sys
sys.path.append('../')
sys.path.append('../../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

import re

from tool_box.util.utility import Utility

def gen_tonal_part_duration(phone_level_label, pattern, start_set, end_set, outpath):

    for sett in Utility.char_range(start_set, end_set):
        set_path = '{}/{}/'.format(phone_level_label, sett)
        for f in Utility.list_file(set_path):
            if f.startswith('.'): continue
            file_path = '{}/{}'.format(set_path, f)

            phone_frame_list = []
            syllable_count = 0

            for line in Utility.read_file_line_by_line(file_path):
                match = re.match(pattern, line)
                if match:
                    start_time = match.group('start_time')
                    end_time = match.group('end_time')

                    if match.group('phone_position_in_syllable') == 'x': continue

                    phone_position_in_syllable = int(match.group('phone_position_in_syllable'))
                    phone_number_in_syllable = int(match.group('phone_number_in_syllable'))

                    frame = (float(end_time) - float(start_time))/50000

                    if phone_position_in_syllable == 1:
                        phone_frame_list = []
                        phone_frame_list.append(frame)
                    elif phone_position_in_syllable == phone_number_in_syllable:
                        phone_frame_list.append(frame)
                        if phone_number_in_syllable == 2:
                            phone_frame_list.append(0)

                        syllable_count+=1
                        print phone_frame_list
                        outfile = '{}/{}/{}/{}_dur.npy'.format(outpath, sett, f.split('.')[0], syllable_count)
                        print outfile
                        Utility.make_directory('{}/{}/{}/'.format(outpath, sett, f.split('.')[0]))
                        Utility.save_obj(phone_frame_list, outfile)
                    elif phone_position_in_syllable == 2:
                        phone_frame_list.append(frame)

                else:
                    print 'Not match', f

                pass

if __name__ == '__main__':
    # print 'panda'

    # 0 317500 X-sil+s/A:x_x-x_x+1_1/B:x-x+4/C:x_x-x_x+1_1/D:x-x+3/E:x-x+1/F:x_x-x_x+3_1/G:x_20_11/H:x_x-56_1+3_1/I:0
    # phone_level_label = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_data/Manual_labeling_stress_unstress/raw/label_phone/tsc/sd/'

    phone_level_label = '/work/w2/decha/Data/GPR_data/label/01_part_of_speech/full_time/tsc/sd/'

    # outpath = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_data/Manual_labeling_stress_unstress/raw/dur/'

    outpath = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_data/gpr_stress_unstress/dur/'

    # pattern = re.compile(r"""
    #     (?P<start_time>.+)\s(?P<end_time>.+)\s
    #     .+
    #     /A:.+\-(?P<phone_position_in_syllable>.+)_.+\+.+
    #     /B:.+
    #     /D:.+\-(?P<phone_number_in_syllable>.+)\+.+
    #     /E:.+
    #     /G:.+""",re.VERBOSE)

    # 29802500 30227500 sil-l+xx/A:x_x-1_1+2_2/B:x-3+0/C:x_x-1_1+1_2/D:x-3+3/E:x-1+2/F:x_x-3_1+6_2/G:x_18_12/H:x-47+47
    pattern = re.compile(r"""
        (?P<start_time>.+)\s(?P<end_time>.+)\s
        .+
        /A:.+\-(?P<phone_position_in_syllable>.+)_.+\+.+
        /B:.+
        /D:.+\-(?P<phone_number_in_syllable>.+)\+.+
        /E:.+
        /G:.+""",re.VERBOSE)

    gen_tonal_part_duration(phone_level_label, pattern, 'a', 'j', outpath)
