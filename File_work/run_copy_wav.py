'''
Created on Jan 26, 2016

@author: decha
'''

import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

if __name__ == '__main__':
    
    outpath = '/work/w2/decha/Data/GPR_data/GP_LVM_Data/Manual_labeling_stress_unstress/raw/wav/'
    
    source = '/home/h1/decha/data/TrainingData/wav/16k/test/'
    
    for ch in Utility.char_range('a', 'h'):
        Utility.make_directory('{}/{}'.format(outpath,ch))
    
    list = '/work/w2/decha/Data/GPR_data/GP_LVM_Data/Manual_labeling_stress_unstress/raw/stress_unstressed_label_file_index.test.txt'
    
    for line in Utility.read_file_line_by_line(list):
        label = line.split(' ')
        
        
        ori = label[0].split('.')[0]
        dest = label[1].split('.')[0]
    
        set = dest.split('_')[2][0]
    
        print ori, dest, set
        
        src = '{}/{}.wav'.format(source,ori)
        dst = '{}/{}/{}.wav'.format(outpath,set,dest)
        
        Utility.copyFile(src, dst)
    
    pass