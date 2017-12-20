
import sys
sys.path.append('../')
sys.path.append('../../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

import numpy as np

from DataModel.Syllables.Syllable import Syllable

from tool_box.util.utility import Utility

model_path = '/work/w13/decha/Inter_speech_2016_workplace/mix-projection-addtional/01_mix_a-5dims_BayesianGPLVMMiniBatch_data_no_delta_missing_data_subtract_typical_contour/BayesianGPLVMMiniBatch_Missing/Tone_01234/GP_model.npy'

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

name_index = np.array(Utility.load_obj('./name_index.pickle'))
phonemes = np.array(Utility.load_obj('./phonemes.pickle'))
prop_out = np.array(Utility.load_obj('./prop_out.pickle'))
stress = np.array(Utility.load_obj('./stress.pickle'))

# phone_index = np.where(phonemes=='r-a-z^-3')[0]
phone_index = np.arange(len(phonemes))

tups = []

for p in phone_index:
    # print p
    tups.append((name_index[p], phonemes[p], prop_out[p], stress[p], x[p], y[p]))

for t in tups:
    # print t[0]
    # if (t[4] > 1) & (t[5] < -1) &  (t[1] == 'k-aa-n^-0'):
    #     print t
    if ('a10' in t[0]) & (t[1] == 'k-aa-n^-0'):
        print t

# sorted_by_second = sorted(tups, key=lambda tup: tup[2])

# for t in sorted_by_second:
#     print t
