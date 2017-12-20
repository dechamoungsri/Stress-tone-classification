
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../')
sys.path.append('../')

from tool_box.util.utility import Utility

from DataModel.Syllables.Syllable import Syllable

if __name__ == '__main__':
    output_file = '/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/playground/latex_analysis/max_iters_analysisi/'
    outpath = '{}_{}.tex'.format(output_file, 'maxiter')
    Latext_Tool.plot_all_data(figure_array, caption_array, outpath)
    pass
