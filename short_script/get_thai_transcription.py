
import sys
sys.path.append('../')
sys.path.append('../../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')

import re

from tool_box.util.utility import Utility

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

# training_list_file = '/home/h1/decha/Dropbox/train_set.list'
training_list_file = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_data/Manual_labeling_stress_unstress/raw/stress_unstressed_label_file_index.txt'
# training_list_file = '/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/train_set.list'

# gpr_file = sys.argv[1]

list_file = Utility.read_file_line_by_line(training_list_file)

xml_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Training_data/XML_txt/'
# xml_path = '/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/Inter_speech_2016/Training_data/XML_txt/'

for ind in range(1, 50+1):
    gpr_file = 'tscsd_stust_a45'#'tscsde{}'.format(Utility.fill_zero(ind,2))
    for line in list_file:
        if gpr_file in line:
            # print line

            splt = line.split('_')
            # print splt

            file_num = splt[3]
            PRG = splt[4]
            SEN = splt[5].split('.')[0]

            # print file_num, PRG, SEN

            xml_file = '{}/NewCorpus_all{}.txt'.format(xml_path, file_num)
            xml = Utility.read_file_line_by_line(xml_file)

            into_file = []
            print '------------------------------------------------------'
            print gpr_file
            # print '------------------------------------------------------'
            for l in xml:
                p = l.split('\t')
                if (p[0] == PRG) & (p[1] == SEN):
                    print p[2]
                    into_file.append(l)
                    break

            print '------------------------------------------------------'
    sys.exit()
        
