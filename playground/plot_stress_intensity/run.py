
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../')
sys.path.append('../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/')
import matplotlib.mlab as mlab
from tool_box.util.utility import Utility
import scipy.stats as stats
from DataModel.Syllables.Syllable import Syllable
from DataModel.Syllables.SyllableDatabaseManagement import SyllableDatabaseManagement
from sklearn import preprocessing

import numpy as np
import matplotlib.pyplot as plt
import GPy

out = dict()
outpath = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/Tonal_object/stress_intensity_dict-use_delta_and_delta-delta.npy'

def gen_stress_intensity(tone_path):

    model_object = Utility.load_obj('{}/GP_model.npy'.format(tone_path))
    name_index = Utility.load_obj('{}/name_index.npy'.format(tone_path))
    labels = Utility.load_obj('{}/clustered_label.npy'.format(tone_path))

    data = model_object.X.mean
    data = np.array(data)
    # print data

    inverselengthscale = model_object.input_sensitivity()
    lengthscale=1/np.array(inverselengthscale, dtype=float)
    kernel = GPy.kern.RBF(len(data[0]), lengthscale=lengthscale, ARD=True)

    stress = 'x'
    num_stress = '1000000'

    # print labels
    for s in set(labels):
        if s == -1 : continue

        if len(labels[labels==s]) < num_stress:
            num_stress = len(labels[labels==s])
            stress = s

        print s, len(labels[labels==s])

    print stress, num_stress
    labels = np.array(labels)
    stress_index = np.where(labels==stress) 
    print 'Stress index'
    # print stress_index

    stress_data = data[stress_index]
    # print stress_data
    means = []
    for idx, i in enumerate(range(len(stress_data[0]))):
        means.append(np.mean(stress_data[:,idx]))

    means = np.array(means)

    # for idx, latent in enumerate(data):
    #     print latent
    #     print means
    # x = -1*np.log(kernel.K(np.array(data), np.array([means])))
    # print x
    
    # x = 1-(x/max(x))
    # x = preprocessing.normalize( x[:,0] )

    # x = 1/x[0]

    mask_unstress = np.ones(len(data), dtype=bool)
    mask_unstress.fill(True)
    mask_unstress[stress_index] = False

    # print mask_unstress

    x = np.arange(len(data), dtype=float)
    x[stress_index] = 1.1

    # unstress = np.array(x[mask_unstress])
    # print unstress
    x[mask_unstress] = kernel.K(data[mask_unstress], np.array([means]))

    # print x[mask_unstress]

    x[mask_unstress] = preprocessing.normalize( x[mask_unstress] )[0] 
    # x = x - np.mean(x)
    x[mask_unstress] = preprocessing.MinMaxScaler().fit_transform(x[mask_unstress])
    # x = x[:,0]
    print x

    for idx, n in enumerate(name_index):
        out[n] = x[idx]

    # Utility.plot_graph(range(x), x, outfile)
    plt.clf()
    h = sorted(x)
    fit = stats.norm.pdf(h, np.mean(h), np.std(h)) 
    plt.plot(h,fit, )
    plt.hist(x, bins=100, alpha=0.25, normed=True)
    plt.legend()
    plt.savefig('{}/stress_intensity_distribution.pdf'.format(tone_path))
    
    pass

if __name__ == '__main__':

    base_data_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/Tonal_object/remove_all_silence_file/'

    base_path_list = [
       '/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/06_Tonal_part_projection_noise_reduction-250-iters-opt/'
        ]

    vowel_type = ['v', 'vv','vn']
    #['v', 'vv','vn', 'vvn', 'vsg', 'vvsg']

    input_dims = [10]

    for syst in base_path_list:
        for v in Utility.list_file(syst):
            if '.' in v : continue
            for dims in input_dims:

                delta_path = '{}/{}/input_dims_{}'.format(syst, v, dims)
                for d in Utility.list_file(delta_path):
                    if 'alias' in d : continue
                    if d.startswith('.'): continue
                    if d != 'delta-True_delta-delta-True': continue
                    for tone in Utility.list_file('{}/{}/'.format(delta_path, d)):
                        if tone.startswith('.'): continue
                        tone_path = '{}/{}/{}/'.format(delta_path, d, tone)
                        
                        if '01234' in tone_path : continue

                        # print tone_path
                        print tone, d, v
                        gen_stress_intensity(tone_path)
                        # sys.exit()

    print 'Dict length : {}'.format(len(out))
    Utility.save_obj(out, outpath)

    pass





