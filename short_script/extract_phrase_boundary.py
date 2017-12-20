
import sys

sys.path.append('../')
sys.path.append('../../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

phrase_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Intonation_phrase_work_place/word_segment_label_23Feb_temp/tsc/sd/'

start = 'a'
end = 'd'

# 'tscsd_gpr_{}{}_{}'.format(set, file_index , count)

single_list = []
poly_list = []
followed_by_sil_list = []

for sett in Utility.char_range(start, end):
    files_in_set = '{}/{}/'.format(phrase_path, sett)
    for f in Utility.list_file(files_in_set):
        if f.startswith('.'): continue
        phrase_file = '{}/{}'.format(files_in_set, f)
        count = 0
        file_index = f.split('.')[0]
        file_index = file_index[-2] + file_index[-1]
        # print file_index
        lines = Utility.read_file_line_by_line(phrase_file)
        for idx, line in enumerate(lines):
            
            if ('sil-sil+sil' in line) | ('pau-pau+pau' in line) | ('------------------------------------------------------------------' in line): pass
            else :
                count = count + 1
                if ('sil-sil+sil' in lines[idx+2]) | ('pau-pau+pau' in lines[idx+2]): 
                    followed_by_sil_list.append('tscsd_gpr_{}{}_{}'.format(sett, file_index , count))
                elif ('------------------------------------------------------------------' in lines[idx-1] ) & ('------------------------------------------------------------------' in lines[idx+1] ) :
                    # print line
                    single_list.append('tscsd_gpr_{}{}_{}'.format(sett, file_index , count))
                    # print 'tscsd_gpr_{}{}_{}'.format(sett, file_index , count)

                    # print 'tscsd_gpr_{}{}_{}'.format(sett, file_index , count)
                elif ('------------------------------------------------------------------' in lines[idx+1] ) :
                    poly_list.append('tscsd_gpr_{}{}_{}'.format(sett, file_index , count))
                    # print 'tscsd_gpr_{}{}_{}'.format(sett, file_index , count)

        # if '03' in f:
        #     sys.exit(0)

outpath = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/list/name_index_a_to_d'
Utility.save_obj(single_list, '{}_single.pickle'.format(outpath))
Utility.save_obj(followed_by_sil_list, '{}_followed_by_sil.pickle'.format(outpath))
Utility.save_obj(poly_list, '{}_poly.pickle'.format(outpath))


