
import sys
sys.path.append('../')
sys.path.append('../../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

import re

from tool_box.util.utility import Utility

print 'panda'

# list_file = '/work/w2/decha/Data/GPR_data/script_copy_to_GPR/train_set.list'
list_file = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_data/Manual_labeling_stress_unstress/raw/stress_unstressed_label_file_index.test.txt'

# src_path = '/home/h1/decha/data/TrainingData/label/Stress-labeling/fullsyn+time_addstress/'
src_path = '/home/h1/decha/data/TrainingData/label/original/mono/'
# dest_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_data/Manual_labeling_stress_unstress/raw/label_phone/'
dest_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_data/Manual_labeling_stress_unstress/raw/mono/'

files = Utility.read_file_line_by_line(list_file)

# pattern = re.compile(r"""(?P<tsc>...)(?P<sd>..)(?P<sett>.)(?P<index>..)\.lab\s(?P<filename>.+)\.lab""",re.VERBOSE)
pattern = re.compile(r"""(?P<filename>.+)\.lab\s(?P<tsc>...)(?P<sd>..)_stust_(?P<sett>.)(?P<index>..)\.lab""",re.VERBOSE)

for line in files:
    # print line
    match = re.match(pattern, line)
    if match:
       tsc = match.group('tsc')
       sd = match.group('sd')
       sett = match.group('sett')
       index = match.group('index')
       filename = match.group('filename')

       print(tsc, sd, sett, index, filename)

       file_format = 'lab'

       src = '{}/{}.{}'.format(src_path, filename,file_format)
       print src

       dest = '{}/{}/{}/{}/{}{}_stust_{}{}.{}'.format(dest_path, tsc, sd, sett, tsc,sd,sett,index,file_format)
       print dest

       Utility.make_directory('{}/{}/{}/{}/'.format(dest_path, tsc, sd, sett))

       Utility.copyFile(src, dest)
       # Utility.copyFile
       # sys.exit()


