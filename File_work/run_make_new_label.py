'''
Created on Jan 26, 2016

@author: decha
'''

import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

if __name__ == '__main__':
#     /work/w2/decha/Data/GPR_data/GP_LVM_Data/Manual_labeling_stress_unstress/raw/label/a/

    label = '/work/w2/decha/Data/GPR_data/GP_LVM_Data/Manual_labeling_stress_unstress/raw/label/'

    label_index = '/work/w2/decha/Data/GPR_data/GP_LVM_Data/Manual_labeling_stress_unstress/raw/label_index/'

    for ch in Utility.char_range('a', 'h'):
        
        path = '{}/{}/'.format(label, ch)
        
        label_index_set = '{}/{}/'.format(label_index, ch)
        
        Utility.make_directory(label_index_set)
        
        for file in Utility.list_file(path):
            
            filepath = '{}/{}'.format(path, file)
            
            out_file = []
            
            outpath = '{}/{}'.format(label_index_set, file)
            
            count = 1
            
            for line in Utility.read_file_line_by_line(filepath):
#                 print line
                split = line.split(' ')
#                 print split[2]
                index = 'None'
                if ('-sil+' in split[2]) :
                    index = 'sil'
                elif ('-pau+' in split[2]) :
                    index = 'pau'
                else :
                    index = count
                    count+=1
                
                outline = '{} {} {}'.format(split[0],split[1],index)
                out_file.append(outline)
    
            if len(out_file) != len(Utility.read_file_line_by_line(filepath)):
                print file
            
            Utility.write_to_file_line_by_line(outpath, out_file)
    
        pass
    pass