
import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../Inter_speech_2016/')
sys.path.append('../../')

import numpy as np

from tool_box.util.utility import Utility
from DataModel.Syllables.SyllableDatabaseManagement import SyllableDatabaseManagement
from DataModel.Syllables.Syllable import Syllable

object_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/01_manual_labeling_object/'
tone_name = 'all'

data_object = '{}/syllable_{}.pickle'.format(object_path,tone_name)
data_object = Utility.load_obj(data_object)

y, name_index, tone, stress, syllable_short_long_type, syllable_positions, phonemes, syllable_type = data_object.get_GP_LVM_training_data(Syllable.TRAINING_FEATURE_POLYNOMIAL_2_DEGREE_VOICE, subtract_typical_contour=False)

y = np.array(y)

# print tone 
# print np.where( np.array(tone) == 4 )
followed_list_file = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/list/followed_sil_manual_list.pickle'
followed_list = Utility.load_obj(followed_list_file)
fow_index = []
name_index = np.array(name_index)
for f in followed_list:
    k = np.where(name_index == f)[0]
    for kk in k:
        fow_index.append(kk.astype(int))

stress = np.array(stress)
stress_index = np.where(stress == 'Stress')
unstress_index = np.where(stress == 'Unstress')

stress[stress_index] = 'Unstress'
stress[fow_index] = 'Stress'

# print fow_index, stress

for target_tone in [0,1,2,3,4]:

    tone_stress = np.intersect1d(np.where( np.array(tone) == target_tone)[0] , np.where( np.array(stress) == 'Stress')[0] ).astype(int)

    y_tone = y[tone_stress][:, :-1]
    # y_tone_means = np.mean(y_tone, axis=1)
    # print y_tone.shape
    # print y_tone_means

    # y_temp = []
    # for idx, yt in enumerate(y_tone):
    #     # print yt, y_tone_means[idx], yt-y_tone_means[idx]
    #     y_temp.append(yt-y_tone_means[idx])

    # y_tone = np.array(y_temp)

    out_object = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/Typical_contour/50dims/tone_{}.pickle'.format(target_tone)
    # y_means = Utility.load_obj(out_object) #
    y_means = np.mean(y_tone, axis=0)
    x = np.arange(len(y_means))
    # print y_means, len(y_means), x

    outname = '/home/h1/decha/Dropbox/Inter_speech_2016/temporary_output/tone_{}_typical.eps'.format(target_tone)

    Utility.plot_graph(x, y_means, outname)

    # out_object = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/Typical_contour/50dims/tone_{}.pickle'.format(target_tone)
    Utility.save_obj(y_means, out_object)




