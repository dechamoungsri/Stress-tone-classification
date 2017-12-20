
import sys
sys.path.append('../')
sys.path.append('../../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import GPy

import numpy as np

if __name__ == '__main__':

    path = ['01_manual_labeling_object', '02_delta_delta-delta', '03_delta', '04_no_delta', '06_02_with_3-dimentionality']

    projection_path = [0,1,2,3,4,5]

    for i in range(0,6):

        # print i

        if i == 4:
            projection_path[i] = '/work/w13/decha/Inter_speech_2016_workplace/Data/05_missing_data_no_delta/BGP_LVM/'
        elif i == 5:
            projection_path[i] = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/{}/BGP_LVM/'.format(path[4])
        else :
            projection_path[i] = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/{}/BGP_LVM/'.format(path[i])

    # print projection_path

    

    for p in projection_path:
        for tone in ['0','1','2','3','4','01234']:
            data_path = '{}/Tone_{}/'.format(p, tone)
            # print data_path

            gp_model_path = '{}/GP_model.npy'.format(data_path)
            model = Utility.load_obj(gp_model_path)

            input_sensitivity = model.input_sensitivity()

            data = model.X.mean
            data_object = np.array(data)

            input_sensitive_path = '{}/input_sentivity.npy'.format(data_path)
            data_object_path = '{}/data_object.npy'.format(data_path)
            
            Utility.save_obj(input_sensitivity, input_sensitive_path)
            Utility.save_obj(data_object, data_object_path)

        #     break
        # break

    pass