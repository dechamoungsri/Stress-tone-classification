'''
Created on Jan 26, 2559 BE

@author: dechamoungsri
'''
import re
import sys
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')

sys.path.append('../../')

from DataModel.Syllables.SyllableDatabaseManagement import SyllableDatabaseManagement
from tool_box.util.utility import Utility

if __name__ == '__main__':
    
    labo_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_data/'
    
    # label_path = '{}/Manual_labeling_stress_unstress/raw/label/'.format(labo_path)
    # lf0_path = '{}/Manual_labeling_stress_unstress/cut/lf0/'.format(labo_path)

    label_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Training_data/03_GPR_syllable_level/full_time/tsc/sd/'
    lf0_path = '{}//cut_lf0/'.format(labo_path)
    
    label_path_list = []
    
    outpath = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/gpr_syllable_obj/Syllable_object.pickle'

    start_set = 'a'
    end_set = 'j'

    # outpath = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/01_manual_labeling_object/Syllable_object.pickle'
    
    for set in Utility.char_range(start_set, end_set):
        set_path = '{}/{}'.format(label_path, set)
        for file in Utility.list_file(set_path):
            if file.startswith('.'): continue
            filepath = '{}/{}'.format(set_path, file)
            label_path_list.append(filepath)
    
    # print label_path_list
    
    # pattern = re.compile(r"""(?P<start>.+)\s(?P<end>.+)\s
    #     .+\-(?P<tone>.+)\+.+
    #     /C:.+\-(?P<syllable_position>.+)\_.+\+.+
    #     /D.+
    #     /F:.+\-.+\_(?P<number_of_syllable>.+)\+.+
    #     /G:.+
    #     /H:.+\-(?P<part_of_speech>.+)\+.+
    #     /I:(?P<stress>.+)
    #     /J:.+\-(?P<consonant>.+)\+.+
    #     /K:.+\-(?P<vowel>.+)\+.+
    #     /L:.+\-(?P<finalconsonant>.+)\+.+
    #     """,re.VERBOSE)

    # 29802500 31043750 l-xx+w^/A:sil-sil+sil/S:th-a+m^/B:x-3+0/C:x_x-1_1+1_2/D:x-3+3/E:x-1+2/F:x_x-3_1+6_2/G:x_18_12/H:x-47+47

    # GPR-Data 
    pattern = re.compile(r"""(?P<start>.+)\s(?P<end>.+)\s
        (?P<consonant>.+)\-(?P<vowel>.+)\+(?P<finalconsonant>.+)
        /A:.+
        /B:.+\-(?P<tone>.+)\+.+
        /C:.+\-(?P<syllable_position>.+)\_.+\+.+
        /D.+
        /F:.+\-.+\_(?P<number_of_syllable>.+)\+.+
        /G:.+
        /H:.+\-(?P<part_of_speech>.+)\+.+
        """,re.VERBOSE)

    syllable_management = SyllableDatabaseManagement()
    syllable_management.load_data_into_syllable_object(pattern, lf0_path=lf0_path,label_path_list=label_path_list)
    
    Utility.save_obj(syllable_management, outpath)
    
    count = 0
    for set in Utility.char_range(start_set, end_set):
        set_path = '{}/{}'.format(lf0_path, set)
        for file in Utility.list_file(set_path):
            if file.startswith('.'): continue
            filepath = '{}/{}/'.format(set_path, file)
            for f in Utility.list_file(filepath):
                if f.startswith('.'): continue
                count+=1
    print count
    
    syllable_management = Utility.load_obj(outpath)
    print syllable_management.get_number_of_syllable()
    
    pass