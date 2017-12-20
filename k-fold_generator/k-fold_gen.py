
import sys
import os
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

def gen_fold_with_balance_stress_unstress(syl_object, fold):

    base_path = Utility.get_base_path(syl_object)
    print base_path

    base_name = Utility.get_basefilename(syl_object)
    print base_name

    outpath = '{}/{}_fold'.format(base_path, base_name)
    Utility.make_directory(outpath)

    syl_manage_object = Utility.load_obj(syl_object)

    stress_list = []
    unstress_list = []

    print len(syl_manage_object.syllables_list)

    for syl in syl_manage_object.syllables_list:
        # print syl.stress_manual
        if syl.stress_manual == '1':
            stress_list.append(syl)
        elif  syl.stress_manual == '0':
            unstress_list.append(syl)

    print len(stress_list), len(unstress_list)

    out_list = []
    for i in range(fold):
        out_list.append([])

    print out_list
    i = 0
    for syl in stress_list:
        out_list[i].append(syl)
        i+=1
        if i == fold:
            i=0

    print 'Stress length: '
    for o in out_list:
        print len(o)

    i = 0
    for syl in unstress_list:
        out_list[i].append(syl)
        i+=1
        if i == fold:
            i=0

    print 'Unstress length: '
    for o in out_list:
        print len(o)

    for i in range(fold):
        syl_o = SyllableDatabaseManagement(syllable_list=out_list[i])
        Utility.save_obj(syl_o, '{}/{}_{}-fold_{}.pickle'.format(outpath, base_name, fold ,i))

    pass

if __name__ == '__main__':

    basepath = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/mix_object/current_version/'

    fold = 3

    for v in Utility.list_file(basepath):
        if v.startswith('.'): continue
        vowel_path = '{}/{}/'.format(basepath, v)
        for tone_obj in Utility.list_file(vowel_path):
            if tone_obj.startswith('.'): continue
            tone_obj_path = '{}/{}'.format(vowel_path, tone_obj)
            print tone_obj_path
            if os.path.isfile(tone_obj_path):
                gen_fold_with_balance_stress_unstress(tone_obj_path, fold)
        # sys.exit()

    pass
