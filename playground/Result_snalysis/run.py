import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility
from tool_box.plotting.horizontal_histogram.Horizontal_Histogram import HorizontalHistogram
from tool_box.plotting.scatter.scatter_plotting import GP_LVM_Scatter

from tool_box.Latex_tool.latext_tool import Latext_Tool

def latex_gen(system_names):

    figure_array = []

    caption_array = []

    for name in system_names:
        figs = []
        caps = []

        cap_name = name.replace("_", "\_")

        for tone in ['0','1','2']:
            filename = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/{}/BGP_LVM/Tone_{}/stress_unstress_plot.eps'.format(name, tone)
            figs.append(filename)
            caps.append('Method : {}, Tone : {}'.format(cap_name, tone))
        figure_array.append(figs)
        caption_array.append(caps)

        figs = []
        caps = []
        for tone in ['3','4','01234']:
            filename = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/{}/BGP_LVM/Tone_{}/stress_unstress_plot.eps'.format(name, tone)
            figs.append(filename)
            caps.append('Method : {}, Tone : {}'.format(cap_name, tone))
        figure_array.append(figs)
        caption_array.append(caps)

    for f in figure_array:
        print f

    # figure_array = [[0,1,2,3,4]]
    # caption_array = None
    outpath = '/work/w13/decha/Inter_speech_2016_workplace/2015_02_05_Projection_result/projection.tex'

    Latext_Tool.plot_all_data(figure_array, caption_array, outpath)

    pass

def run_plot_and_latex():

    # output_name = '02_delta_delta-delta'
    # output_name = '03_delta'
    # output_name = '04_no_delta'
    system_names = ['02_delta_delta-delta','03_delta','04_no_delta','05_missing_data_no_delta','06_02_with_3-dimentionality']

    for output_name in system_names:

        base_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/{}/BGP_LVM/'.format(output_name)
        object_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/01_manual_labeling_object/'
        
        for tone in ['0','1','2','3','4', '01234']:

            model_path = '{}/Tone_{}/GP_model.npy'.format(base_path, tone)
            data_object = '{}/syllable_{}.pickle'.format(object_path,tone)

            if tone == '01234':
                data_object = '{}/syllable_all.pickle'.format(object_path)

            outpath = '{}/Tone_{}/stress_unstress_plot.eps'.format(base_path, tone)

            GP_LVM_Scatter.plot_scatter(Utility.load_obj(model_path), Utility.load_obj(data_object), outpath)

    pass

if __name__ == '__main__':

    run_plot_and_latex()
    system_names = ['02_delta_delta-delta','03_delta','04_no_delta','05_missing_data_no_delta','06_02_with_3-dimentionality']
    latex_gen(system_names)

    pass