'''
Created on Jan 25, 2016

@author: decha
'''

import sys
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../')

from tool_box.GP_LVM.Data_Reader import DataReader

if __name__ == '__main__':
    
    # Find the mistake point in filelist
    
    # find_the_point_in_coordinate(file_path: string, area: rectangle)
    # return filelist with helpful information
    
    tone = '2'
    
    main_path = '/work/w4/decha_4/ICASSP_2016/Data/16_scg_initial_method_manual_stress_label/PCA_init-optimize_by_scg/Tone_{}/duration_data_meansData-False_optimize-True_set-a-h/coeff_10/inputDim-3_ARD-True_lengthscale-1_bias-False/'.format(tone)
    input_sensitivity_file = '{}/input_sensitivity.pkl'.format(main_path)
    latent_data = '{}/latent_space_data.pkl'.format(main_path)
    labels = '{}/label_latent_space_data.pkl'.format(main_path)
    syllable_data_path = '/work/w2/decha/Data/GPR_data/GP_LVM_Data/Manual_labeling_stress_unstress/cut/tone_stressed_label/'
    
#     '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_data/Manual_labeling_stress_unstress/cut/tone_stressed_label/'
    
    area = dict()
    area['x_up'] = 2
    area['x_low'] = 1
    area['y_up'] = 3
    area['y_low'] = 2
    
    DataReader.find_data_point_from_coordinate(latent_data,input_sensitivity_file,labels,syllable_data_path,area,tone)
    
    # Get the file
    
    pass