
import sys
sys.path.append('../')
sys.path.append('../../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

import numpy as np

from DataModel.Syllables.Syllable import Syllable

from tool_box.util.utility import Utility

from scipy.stats import multivariate_normal

data_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/mix_syllable_obj/mix_syllable_all.pickle'

model_path = '/work/w13/decha/Inter_speech_2016_workplace/mix-projection-addtional/01_mix_a-5dims_BayesianGPLVMMiniBatch_data_no_delta_missing_data_subtract_typical_contour/BayesianGPLVMMiniBatch_Missing/Tone_01234/GP_model.npy'

syllable_management = Utility.load_obj(data_path)
y, name_index, tone, stress, syllable_short_long_type, syllable_positions, phonemes = syllable_management.get_GP_LVM_training_data(Syllable.TRAINING_FEATURE_POLYNOMIAL_2_DEGREE_VOICE, subtract_typical_contour=False)

model = Utility.load_obj(model_path)
data = model.X.mean

x = []
y = []

input_sensitivity = model.input_sensitivity()
print input_sensitivity

index = Utility.get_input_sensitivity(input_sensitivity, 2)
print index

for i in range(len(data)):
    x.append(data[i,index[0]])
    y.append(data[i,index[1]])

x = np.asarray(x)
y = np.asarray(y)

stress = np.array(stress)
stress_index = np.where(stress=='Stress')

x_stress = x[stress_index]
y_stress = y[stress_index]

mux = np.mean(x_stress)
muy = np.mean(y_stress)

sigmaxy = np.cov(x_stress,y_stress)

model2d = multivariate_normal(mean=[mux,muy], cov=sigmaxy)

# print model2d.pdf([mux,muy])

prop_out = []

for idx, val in enumerate(x):
    k = model2d.pdf([x[idx], y[idx]])
    prop_out.append(k)
    print k

outpath_file = '/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/Result_analysis/'
Utility.save_obj(prop_out, '{}prop_out.pickle'.format(outpath_file))
Utility.save_obj(phonemes, '{}phonemes.pickle'.format(outpath_file))
Utility.save_obj(name_index, '{}name_index.pickle'.format(outpath_file))
Utility.save_obj(stress, '{}stress.pickle'.format(outpath_file))
