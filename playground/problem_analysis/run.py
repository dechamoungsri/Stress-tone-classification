'''
Created on Jan 25, 2016

@author: decha
'''

import sys
# sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('../../')

from tool_box.GP_LVM.Data_Reader import DataReader

if __name__ == '__main__':
    
    # Find the mistake point in filelist
    
    # find_the_point_in_coordinate(file_path: string, area: rectangle)
    # return filelist with helpful information
    
#     main_path = '/work/w4/decha_4/ICASSP_2016/Data/16_scg_initial_method_manual_stress_label/PCA_init-optimize_by_scg/Tone_01234/duration_data_meansData-False_optimize-True_set-a-h/coeff_10/inputDim-3_ARD-True_lengthscale-1_bias-False/'
    main_path = '/Users/dechamoungsri/Desktop/Interspeech_2016_Data/Projection_data/PCA_init-optimize_by_scg/Tone_01234/duration_data_meansData-False_optimize-True_set-a-h/coeff_10/inputDim-3_ARD-True_lengthscale-1_bias-False/'
    input_sensitivity_file = '{}/input_sensitivity.pkl'.format(main_path)
    latent_data = '{}/latent_space_data.pkl'.format(main_path)
    labels = '{}/label_latent_space_data.pkl'.format(main_path)
    syllable_data_tag = '{}/syllable_data_tag.pkl'.format(main_path)
    
    area = dict()
    area['x_up'] = -100000000
    area['x_low'] = 100000000
    area['y_up'] = -100000000
    area['y_low'] = 100000000
    
    DataReader.find_data_point_from_coordinate(latent_data,input_sensitivity_file,labels,syllable_data_tag,area)
    
    # Get the file
    
    pass