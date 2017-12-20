
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

import numpy as np
import matplotlib.pyplot as plt

import GPy

import itertools

def get_data_from_a_giving_name_index(name_list, name_index_object, data_object):

    data_list_index = []

    for n in name_list:

        if len(np.where(name_index_object==n)[0]) == 0 : 
            print n
            print 'Error here'
            sys.exit()

        idx = np.where(name_index_object==n)[0][0]
        data_list_index.append(idx)

    if len(data_object[data_list_index]) != len(name_list):
        print len(data_object[data_list_index]), len(name_list)
        print 'Error'
        sys.exit()

    return data_object[data_list_index]

    pass

def get_means(sort_list, target_index, name_index, model, path):
    # len(sort_list)-1
    data_group = sort_list[target_index][0]
    data = get_data_from_a_giving_name_index( 
        Utility.load_obj(  '{}/group_list/{}.npy'.format(path, data_group) ) ,
        name_index, model
        )
    
    outmean = []
    for l in range(len(data[0])):
        outmean.append( np.mean(data[:,l]) )

    print outmean
    return np.array(outmean)

    pass
def get_group_of_unclassified_data(mean_stress, mean_unstress):
    pass

def get_data(path):

    clustered_label = Utility.load_obj('{}/clustered_label.npy'.format(path))
    # print len(clustered_label)
    best_measure_params = Utility.load_obj('{}/best_measure_params.npy'.format(path))
    # print best_measure_params
    name_index = np.array( Utility.load_obj('{}/name_index.npy'.format(path)) )
    # print len(name_index)
    m = Utility.load_obj('{}/GP_model.npy'.format(path))
    model = m.X.mean
    model = np.array(model)
    # print model

    input_sensitivity = m.input_sensitivity()
    print 'Input sent : ', input_sensitivity

    group_list = ['-1', '0', '1', '2']

    sort_list = []

    for group in group_list:
        g = '{}/group_list/{}.npy'.format(path, group)
        if Utility.is_file_exist(g):
            names = Utility.load_obj(g)
            sort_list.append((group, len(names)))

    Utility.sort_by_index(sort_list, 1)
    print sort_list

    unstressed_mean = get_means(sort_list, len(sort_list)-1, name_index, model, path)
    unstressed_list = Utility.load_obj( '{}/group_list/{}.npy'.format(path, sort_list[len(sort_list)-1][0]) )

    stressed_mean = get_means(sort_list, len(sort_list)-2, name_index, model, path)
    stressed_list = Utility.load_obj( '{}/group_list/{}.npy'.format(path, sort_list[len(sort_list)-2][0]) )

    Utility.save_obj( 
        {'unstress_mean': unstressed_mean, 'stress_mean': stressed_mean}, 
        '{}/mean_of_unstress_stress.npy'.format(path) )

    lengthscale=1/np.array(input_sensitivity, dtype=float)
    kernel = GPy.kern.RBF(10, lengthscale=lengthscale, ARD=True)

    print len(unstressed_list), len(stressed_list)

    for idx, g in enumerate(sort_list):
        if idx == (len(sort_list)-2): break
        names = Utility.load_obj('{}/group_list/{}.npy'.format(path, g[0]))

        print len(names)

        latent_data = get_data_from_a_giving_name_index(names, name_index, model)

        stu = np.array([unstressed_mean, stressed_mean])
        distance = -1*np.log(kernel.K( latent_data, stu ))

        for n, dis in zip(names, distance):
            if dis[0] > dis[1]:
                unstressed_list = np.append(unstressed_list, n)
            else : 
                stressed_list = np.append(stressed_list, n)

    print len(unstressed_list), len(stressed_list)
    # print unstressed_list, stressed_list
    return (unstressed_list, stressed_list)

if __name__ == '__main__':

    outpath = './stress_dict/'

    latent_path = '/work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/06_Tonal_part_projection_noise_reduction-250-iters-opt/'

    # //work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/06_Tonal_part_projection_noise_reduction-250-iters-opt//vvv/input_dims_10/delta-True_delta-delta-True/BGP_LVM_Tone_0//clustered_label.npy
    # /work/w13/decha/Inter_speech_2016_workplace/Tonal_projection/06_Tonal_part_projection_noise_reduction-250-iters-opt/vvv/input_dims_10/delta-True_delta-delta-True/BGP_LVM_Tone_0/clustered_label.npy

    vowel_type = ['vvv', 'vvvn', 'vvvsg']

    tone_type = ['0', '1', '2', '3', '4']

    input_dims = ['10']

    feature = ['delta-True_delta-delta-True']

    a = [vowel_type, input_dims, feature, tone_type]

    iters = list(itertools.product(*a))

    # print iters, len(iters)

    unstressed_list, stressed_list = np.array([]), np.array([])

    for it in iters:
        object_path = '{}/{}/input_dims_{}/{}/BGP_LVM_Tone_{}/'.format(latent_path, it[0], it[1], it[2], it[3])
        print object_path
        un, st = get_data(object_path)
        unstressed_list = np.append(unstressed_list, un)
        stressed_list = np.append(stressed_list, st)

        print 'Unstress, Stress' 
        print len(unstressed_list), len(stressed_list)

        # sys.exit()

    Utility.save_obj(unstressed_list, '{}/unstress_name_list.npy'.format(outpath))
    Utility.save_obj(stressed_list, '{}/stress_name_list.npy'.format(outpath))

    pass
