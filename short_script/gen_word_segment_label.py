import sys
sys.path.append('../')
sys.path.append('../../')
# sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')

import re

from tool_box.util.utility import Utility

# syllable_files_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Training_data/03_GPR_syllable_level/full_time/tsc/sd/'
syllable_files_path = '/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/Inter_speech_2016/Training_data/03_GPR_syllable_level/full_time/tsc/sd/'

set_list = Utility.char_range('a', 'j')

pattern = re.compile(r"""(?P<time>.+\s.+)\s(?P<syllable>.+)/A:.+/S:.+/B:.+\-(?P<tone>.+)\+.+/C:.+\-(?P<syllable_index_in_word>.+)_.+\+.+/D:.+/F:.+\-.+_(?P<number_of_syllable_in_word>.+)\+.+/G:.+""",re.VERBOSE)

# out_p = '/work/w2/decha/Data/GPR_data/label/03_GPR_syllable_level/syllable_with_index/tsc/sd/'
out_p = '/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/word_segment_label/tsc/sd/'
Utility.make_directory(out_p)

for s in set_list:
    target_path = '{}/{}/'.format(syllable_files_path, s)
    print target_path
    for f in Utility.list_file(target_path):
        if f.startswith('.'): continue

        new_file = []

        Utility.make_directory('{}/{}/'.format(out_p, s))

        out_path = '{}/{}/{}'.format(out_p, s, f)
        print out_path

        for line in Utility.read_file_line_by_line('{}/{}'.format(target_path, f)):
            # print line
            match = re.match(pattern, line)
            if match:
               time = match.group('time')
               # print time
               syllable = match.group('syllable')
               # print syllable
               syllable_index = match.group('syllable_index_in_word')
               # print index
               tone = match.group('tone')
               # print tone
               number_of_syllable_in_word = match.group('number_of_syllable_in_word')

               o = '{}, {}, Tone : {}, Index : {}'.format(time, syllable, tone, syllable_index)
               new_file.append(o)

               # new_file.append(line)

               if syllable_index == number_of_syllable_in_word:
                new_file.append('------------------------------------------------------------------')


        Utility.write_to_file_line_by_line(out_path, new_file)

