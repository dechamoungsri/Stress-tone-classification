
import sys

sys.path.append('../')
sys.path.append('../../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

stress_manual_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_data/Manual_labeling_stress_unstress/raw/label/'

start = 'a'
end = 'h'

# print Utility.load_obj('/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/Result_analysis/name_index.pickle')

out = []

for s in Utility.char_range(start, end):
    set_path = '{}/{}/'.format(stress_manual_path, s)
    for f in Utility.list_file(set_path):
        if f.startswith('.'): continue
        count = 0
        # print f
        filename = f[-7:-4] 
        # print filename
        lines = Utility.read_file_line_by_line('{}/{}'.format(set_path, f))
        for idx, line in enumerate(lines):
            # print line
            if ('-sil+' in line) | ('-pau+' in line): continue
            else :
                 count+=1
                 if ('-sil+' in lines[idx+1]) | ('-pau+' in lines[idx+1]): 
                    # tscsd_manual_d33_15
                    # print count
                    name = 'tscsd_manual_{}_{}'.format(filename, count)
                    print name
                    out.append(name)

Utility.save_obj(out, '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/list/followed_sil_manual_list.pickle')

