
import sys
sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

x = Utility.load_obj('/work/w13/decha/Inter_speech_2016_workplace/mix-projection-addtional/01_mix_a-5dims_BayesianGPLVMMiniBatch_data_no_delta_missing_data_subtract_typical_contour/BayesianGPLVMMiniBatch_Missing/Tone_01234/followed_list_used_x.pickle')

y = Utility.load_obj('/work/w13/decha/Inter_speech_2016_workplace/mix-projection-addtional/01_mix_a-5dims_BayesianGPLVMMiniBatch_data_no_delta_missing_data_subtract_typical_contour/BayesianGPLVMMiniBatch_Missing/Tone_01234/followed_list_used_y.pickle')

stress = Utility.load_obj('/work/w13/decha/Inter_speech_2016_workplace/mix-projection-addtional/01_mix_a-5dims_BayesianGPLVMMiniBatch_data_no_delta_missing_data_subtract_typical_contour/BayesianGPLVMMiniBatch_Missing/Tone_01234/followed_list_used_stress_followed.pickle')

tone = Utility.load_obj('/work/w13/decha/Inter_speech_2016_workplace/mix-projection-addtional/01_mix_a-5dims_BayesianGPLVMMiniBatch_data_no_delta_missing_data_subtract_typical_contour/BayesianGPLVMMiniBatch_Missing/Tone_01234/followed_list_used_tone.pickle')

name_index = Utility.load_obj('/work/w13/decha/Inter_speech_2016_workplace/mix-projection-addtional/01_mix_a-5dims_BayesianGPLVMMiniBatch_data_no_delta_missing_data_subtract_typical_contour/BayesianGPLVMMiniBatch_Missing/Tone_01234/name_index.npy')

print len(name_index)
print len(x)

for idx, xi in enumerate(x):
    if (xi < -1) & (stress[idx] == 'Stress') :
        print name_index[idx], tone[idx]
