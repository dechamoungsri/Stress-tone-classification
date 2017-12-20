'''
Created on Jan 26, 2559 BE

@author: dechamoungsri
'''

import sys
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('../../')

import numpy as np
import matplotlib.pyplot as plt
import copy

from Data_Processing.Inteporation_method.Interpolation import Interpolation
from tool_box.util.utility import Utility

from scipy.fftpack import dct
from scipy.fftpack import idct

class Syllable(object):
    '''
    This is just a syllable object 
    Contain a syllable information
    '''
    
    TRAINING_RAW_DATA = 'TRAINING_RAW_DATA'
    TRAINING_RAW_DATA_VOWEL_FINAL = 'TRAINING_RAW_DATA_VOWEL_FINAL'

    MISSING_VALUES = 'MISSING_VALUES'

    TRAINING_FEATURE_ORIGINAL = 'TRAINING_FEATURE_ORIGINAL'

    TRAINING_FEATURE_POLYNOMIAL_2_DEGREE = 'TRAINING_FEATURE_POLYNOMIAL_2_DEGREE'
    COEFFICIENT_POLYNOMIAL_2_DEGREE = 'TRAINING_FEATURE_POLYNOMIAL_2_DEGREE_COEFFICIENT'
    TRAINING_FEATURE_POLYNOMIAL_2_DEGREE_VOICE = 'TRAINING_FEATURE_POLYNOMIAL_2_DEGREE_VOICE'

    Training_feature_tonal_part_raw_remove_head_tail_having_missing = 'Training_feature_tonal_part_raw_remove_head_tail_having_missing'
    Training_feature_tonal_part_raw_remove_head_tail_interpolated = 'Training_feature_tonal_part_raw_remove_head_tail_interpolated'

    Training_feature_tonal_part_dct_coeff = 'coeff_from_Training_feature_tonal_part_raw_remove_head_tail_interpolated'

    Training_feature_consonant_raw_remove_head_tail_having_missing = 'Training_feature_consonant_raw_remove_head_tail_having_missing'
    Training_feature_consonant_raw_remove_head_tail_interpolated = 'Training_feature_consonant_raw_remove_head_tail_interpolated'
    Training_feature_vowel_raw_remove_head_tail_having_missing = 'Training_feature_vowel_raw_remove_head_tail_having_missing'
    Training_feature_vowel_raw_remove_head_tail_interpolated = 'Training_feature_vowel_raw_remove_head_tail_interpolated'
    Training_feature_final_consonant_raw_remove_head_tail_having_missing = 'Training_feature_final_consonant_raw_remove_head_tail_having_missing'
    Training_feature_final_consonant_raw_remove_head_tail_interpolated = 'Training_feature_final_consonant_raw_remove_head_tail_interpolated'

    Training_feature_phone_tonal_separated_with_noise_reduction = 'Training_feature_phone_tonal_separated_with_noise_reduction'

    un_voice_value = -1.00000000e+10
    
    short_vowel = ['va', 'ia', 'q', '@', 'a', 'e', 'i', 'o', 'u', 'v', 'x', 'ua']
    consonant_cluster = ['khr', 'khw', 'khl', 'kl', 'pr', 'kr', 'tr', 'kw', 'pl', 'fr', 'phl', 'bl', 'br', 'phr', 'fl', 'dr', 'thr']
    diphthong_list = ['va', 'ia', 'ua', 'vva', 'iia', 'uua']

    nasal_list = ['n^', 'm^', 'ng^']

    VOWEL_LENGTH_TYPE = ['v', 'vv', 'vn', 'vvn', 'vsg', 'vvsg']

    def get_raw_with_missing_value(self, num_sampling, delta_bool, delta2_bool, duration=[0,1,2]):
        y = np.copy(self.raw_data)
        y[y<0] = np.nan
        if len(duration)==2:
            x = np.linspace(self.phone_duration[0] , len(y), num=num_sampling)
        else:
            x = np.linspace(0, len(y), num=num_sampling)

        # print self.phone_duration
        # print len(y)
        # print x
        # if self.phone_duration[0] > len(y):
        #     print self.name_index
        #     print self.phone_duration
        #     print len(y)
        #     print x
        #     sys.exit()

        y = np.interp(x, np.arange(len(y)), y)
        y = self.gen_delta_and_deltadelta(y, delta_bool, delta2_bool)
        return y

    def get_duration(self, dur_position):
        out = 0
        for i in dur_position:
            out += self.phone_duration[i]
        return out

    def get_Y_features(self, feature_key, num_sampling, delta_bool, delta2_bool, exp=False, subtract_means=False, output=None, missing_data=False):

        if feature_key.startswith('coeff_'):
            return self.training_feature[feature_key][0:num_sampling]

        if feature_key == Syllable.Training_feature_phone_tonal_separated_with_noise_reduction:

            if self.final_consonant != 'z^':
                final_consonant_y = self.training_feature[Syllable.Training_feature_final_consonant_raw_remove_head_tail_interpolated]
                final_consonant_y = self.get_intepolate_feature(final_consonant_y, delta_bool, delta2_bool, num_sampling, noise_reduction=True)

            vowel_y = self.training_feature[Syllable.Training_feature_vowel_raw_remove_head_tail_interpolated]
            vowel_y = self.get_intepolate_feature(vowel_y, delta_bool, delta2_bool, num_sampling, noise_reduction=True)

            if self.final_consonant != 'z^':
                return np.append(vowel_y, final_consonant_y)
            else :
                return vowel_y

        y = np.copy(self.training_feature[feature_key])
        # print self.is_un_voice_tonal_file, self.name_index

        if missing_data:
            y[y<0] = np.nan

        if exp:
            y = np.exp(y)

        if subtract_means:
            y = y - np.average(y)

        # x = np.linspace(0, len(y), num=num_sampling)
        # y = np.interp(x, np.arange(len(y)), y)
        y = self.get_intepolate_feature(y, delta_bool, delta2_bool, num_sampling, noise_reduction=True)

        return y

    def gen_delta_and_deltadelta(self, y, delta_bool, delta2_bool):
        if delta_bool:
            delta = np.gradient(y)
            if delta2_bool:
                delta2 = np.gradient(delta)

                y = np.append(y, delta)
                y = np.append(y, delta2)
            else :
                y = np.append(y, delta)

        return y

    def get_intepolate_feature(self, y, delta_bool, delta2_bool, num_sampling, noise_reduction=True):
        x = np.linspace(0, len(y), num=num_sampling)
        y = np.interp(x, np.arange(len(y)), y)
        y = self.dct_noise_reduction(y)
        y = self.gen_delta_and_deltadelta(y, delta_bool, delta2_bool)
        return y

    def plot_by_phoneme(self, outpath):

        x = np.arange(len(self.raw_data))

        plt.clf()
        plt.plot(x, self.raw_data,'--', c='black')

        y1 = self.training_feature[Syllable.Training_feature_consonant_raw_remove_head_tail_having_missing]
        plt.plot(np.arange(0, len(y1)) , y1,'b-', alpha=0.5)

        y2 = self.training_feature[Syllable.Training_feature_vowel_raw_remove_head_tail_having_missing]
        plt.plot(
            np.arange(int(self.phone_duration[0]), int(self.phone_duration[0])+len(y2)) , 
            y2,
            'r-', 
            alpha=0.5)

        if self.final_consonant != 'z^' : 
            y3 = self.training_feature[Syllable.Training_feature_final_consonant_raw_remove_head_tail_having_missing]
            plt.plot(
                np.arange(
                    int(self.phone_duration[0]+self.phone_duration[1]), 
                    int(self.phone_duration[0]+self.phone_duration[1])+len(y3)) , 
                y3,
                'g-', alpha=0.5)

        plt.savefig(outpath)

        pass

    def dct_noise_reduction(self, y, coeff_number = 5):

        dct_coeff = dct(y, type=2, norm='ortho')

        window = np.zeros(len(dct_coeff))
        window[:coeff_number] = 1

        inverse_dct = dct(dct_coeff*window, 3, norm='ortho')
        indx = np.arange(len(inverse_dct))
        inverse_dct = np.interp(np.linspace(0, len(inverse_dct), num=len(y) ) , indx, inverse_dct)

        return inverse_dct

    def gen_separated_vowel_final_consonant(self):
        # print self.final_consonant

        consonant_data = np.copy(self.raw_data)[
                0 : 
                self.phone_duration[0]
                ]
        vowel_data = np.copy(self.raw_data)[
                self.phone_duration[0] : 
                self.phone_duration[0]+self.phone_duration[1]
                ]
        final_consonant_data = np.copy(self.raw_data)[
                self.phone_duration[0]+self.phone_duration[1] :
                len(self.raw_data)]

        # print self.phone_duration
        # print self.raw_data
        # print consonant_data
        # print vowel_data
        # print final_consonant_data

        self.is_unvoice = [False, False, False]

        self.gen_training_feature(
            consonant_data, 
            Syllable.Training_feature_consonant_raw_remove_head_tail_having_missing, 
            Syllable.Training_feature_consonant_raw_remove_head_tail_interpolated,
            0)

        self.gen_training_feature(
            vowel_data, 
            Syllable.Training_feature_vowel_raw_remove_head_tail_having_missing, 
            Syllable.Training_feature_vowel_raw_remove_head_tail_interpolated,
            1)

        if self.final_consonant != 'z^' : 
            self.gen_training_feature(
                final_consonant_data, 
                Syllable.Training_feature_final_consonant_raw_remove_head_tail_having_missing, 
                Syllable.Training_feature_final_consonant_raw_remove_head_tail_interpolated,
                2)

        # print self.is_consonant_unvoice, self.is_vowel_unvoice, self.is_final_consonant_unvoice

        return

    def gen_training_feature(self, feature, key_missing, key_interpolated, unvoice_position):

        start,end = self.get_start_end_voice_region(feature)
        data = np.take(feature, np.arange(start, end+1, dtype=np.int16))
        self.training_feature[key_missing] = np.copy(data)

        unvoice_index = np.where( data == Syllable.un_voice_value)

        # print data

        self.is_unvoice[unvoice_position] = False
        if len( unvoice_index[0]) != 0:

                if len( unvoice_index[0]) == len(data):
                    self.is_unvoice[unvoice_position] = True
                else :
                    x = np.arange(len(data))
                    y = np.copy(data)

                    x = np.delete(x, unvoice_index)
                    y = np.delete(y, unvoice_index)

                    poly_cor = np.polyfit(x, y, 2)
                    poly_val = np.polyval(poly_cor, unvoice_index)

                    data[unvoice_index] = poly_val[0]
                    self.is_unvoice[unvoice_position] = False

        self.training_feature[key_interpolated] = np.copy(data)

        pass

    def get_tonal_part_data(self):
        initial_consonant_duration = self.phone_duration[0]
        indices = np.arange(initial_consonant_duration+1, len(self.raw_data), dtype=np.int16)

        if initial_consonant_duration > len(self.raw_data):
            print self.name_index
            print self.raw_data
            print self.phone_duration, len(self.raw_data)
            print self.consonant, self.vowel, self.final_consonant

        tonal_part_data = np.take(self.raw_data, indices)

        return tonal_part_data

    def gen_tonal_part_training_feature(self, missing_key, intepolate_key):

        initial_consonant_duration = self.phone_duration[0]
        indices = np.arange(initial_consonant_duration+1, len(self.raw_data), dtype=np.int16)

        # print self.raw_data
        # print initial_consonant_duration, len(self.raw_data)

        # if self.name_index == 'tscsd_manual_b03_23':
        if initial_consonant_duration > len(self.raw_data):
            print self.name_index
            print self.raw_data
            print self.phone_duration, len(self.raw_data)
            print self.consonant, self.vowel, self.final_consonant

        tonal_part_data = np.take(self.raw_data, indices)

        start,end = self.get_start_end_voice_region(tonal_part_data)

        tonal_part_data = np.take(tonal_part_data, np.arange(start, end+1, dtype=np.int16))

        self.training_feature[missing_key] = np.copy(tonal_part_data)

        unvoice_index = np.where( tonal_part_data == Syllable.un_voice_value)

        # if self.name_index == 'tscsd_manual_b03_23':
        #     print tonal_part_data

        self.is_un_voice_tonal_file = False

        if len( unvoice_index[0]) != 0:

            if len( unvoice_index[0]) == len(tonal_part_data):
                self.is_un_voice_tonal_file = True
            else:
                # print self.name_index, self.consonant, self.vowel, self.final_consonant
                # print tonal_part_data

                x = np.arange(len(tonal_part_data))
                y = np.copy(tonal_part_data)

                x = np.delete(x, unvoice_index)
                y = np.delete(y, unvoice_index)

                poly_cor = np.polyfit(x, y, 2)
                poly_val = np.polyval(poly_cor, unvoice_index)

                tonal_part_data[unvoice_index] = poly_val[0]

                self.is_un_voice_tonal_file = False

        self.training_feature[intepolate_key] = np.copy(tonal_part_data)

        pass

    def get_vowel_length_type(self):

        vowel_type = 'vv'

        if self.is_short_vowel():
            vowel_type = 'v'

        final_consonant_type = 'sg'

        if self.final_consonant in Syllable.nasal_list:
            final_consonant_type = 'n'
        elif self.final_consonant == 'z^':
            final_consonant_type = ''

        return vowel_type + final_consonant_type

    def get_syllable_type(self):

        short_or_long = self.get_syllable_short_long_type()
        cluster = 'Cluster-consonant'
        if self.consonant in Syllable.consonant_cluster:
            cluster = 'Non-cluster-consonant'

        diphthong = 'Monophthong'
        if self.vowel in Syllable.diphthong_list:
            diphthong = 'Diphthong'

        type_vowel = 'long'
        if self.vowel in Syllable.short_vowel:
            type_vowel = 'short'

        return '{}_{}_{}_vowel-{}'.format(short_or_long, cluster, diphthong, type_vowel)

        pass

    def get_syllable_short_long_type(self):

        # print self.consonant, self.vowel, self.final_consonant

        if self.final_consonant in ['k^','p^','t^']:
            return 'short'
        elif self.final_consonant in ['z^']:
            if self.vowel in Syllable.short_vowel:
                return 'short'
        
        return 'long'

        pass

    def get_is_final_position(self):

        if int(self.number_of_syllable_in_word) == 1:
            return 'Mono-syllabic'
        elif int(self.syllable_position_in_word) == int(self.number_of_syllable_in_word):
            return 'Final-syllable'
        else :
            return 'Non-Final syllable'

        pass

    def get_data_with_missing_values(self, 
        num_sampling, subtract_typical_contour, feature_name=None, 
        delta=False, deltadelta=False):

        x = np.linspace(0, len(self.raw_data), num=num_sampling)
        Y = np.interp(x, np.arange(len(self.raw_data)), self.raw_data)

        data = Y

        if feature_name is not None:
            training_data = np.interp(x, np.arange(len(self.training_feature[feature_name])), self.training_feature[feature_name])
            # print training_data, len(training_data)
            data = training_data

        data[ Y<0 ] = np.nan

        if subtract_typical_contour: 
            typical_tone_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/Typical_contour/50dims/tone_{}.pickle'.format(self.tone)
            typical_tone_obj = Utility.load_obj(typical_tone_path)
            data = data - typical_tone_obj

        # print data, len(data)

        if delta:
            y_delta = np.gradient(data)
            # print y_delta
            if deltadelta:
                y_delta_delta = np.gradient(y_delta)
                # print y_delta_delta
                y_delta = np.append(y_delta, y_delta_delta)
            data = np.append(data, y_delta)

        # print np.array(data), len(data)

        return np.array(data)

    def plot(self, output, compare_feature=None, voice=False):
        
        if self.training_feature[compare_feature] is None:
            print 'No {} feature'.format(compare_feature)
        
        y2 = self.training_feature[compare_feature]
        
        if voice:
            x = self.get_voice_region(len(y2))
            y = np.interp(x, np.arange(len(self.raw_data)), self.raw_data)
        else :
            x = np.arange(len(self.raw_data))
            y = copy.copy(self.raw_data)
        
        y[y == Syllable.un_voice_value] = 'nan'

        print len(y), len(x), len(y2)
        # y = np.exp(y)
        plt.clf()
        plt.plot(x, y, 'b', x, y2, 'r')
        # plt.plot(x, y, 'b', x, y2, 'r')
        plt.savefig(output)
        plt.clf()
        pass
    
    def plot_delta(self, output,x,y,y1=None,y2=None):

        # y = y - np.average(y)

        if y2 is not None:
            plt.plot(x, y, 'b', label='Original')
            plt.plot(x, y1, 'r', label='Delta')
            plt.plot(x, y2, 'g', label='Delta-Delta')
            plt.legend()
            plt.savefig(output)
            plt.clf()
        elif y1 is not None:
            plt.plot(x, y, 'b', x, y1, 'r')
            plt.savefig(output)
            plt.clf()
        else :
            plt.plot(x, y, 'b')
            plt.savefig(output)
            plt.clf()

    def get_voice_region(self, num_sampling):
        
        start = None
        end = None
        
        for idx, lf0 in enumerate(self.raw_data):
            if lf0 != Syllable.un_voice_value:
#                 print lf0
                start = idx
                break
        
        for idx, lf0 in reversed(list(enumerate(self.raw_data))):
            if lf0 != Syllable.un_voice_value:
                end = idx
                break
    
#         print start, end
        if (start is None) | (end is None):
            return np.linspace(0, len(self.raw_data), num=num_sampling)
        else:
            return np.linspace(start, end, num=num_sampling)
    
    def get_start_end_voice_region(self, tonal_part_data):
        
        start = None
        end = None
        
        for idx, lf0 in enumerate(tonal_part_data):
            if lf0 != Syllable.un_voice_value:
#                 print lf0
                start = idx
                break
        
        for idx, lf0 in reversed(list(enumerate(tonal_part_data))):
            if lf0 != Syllable.un_voice_value:
                end = idx
                break
    
#         print start, end
        if (start is None) | (end is None):
            return (0, len(tonal_part_data)-1)
        else:
            return (start, end)

    def get_syllable_phoneme(self):
        return '{}-{}-{}-{}'.format(self.consonant, self.vowel, self.final_consonant, self.tone)

    def set_poly_val(self, degree, key_storage, key_sampling, key_coeff_storage, num_sampling):
        
        # print self.name_index
        # print self.raw_data
        poly_coeff = Interpolation.poly_nomial_interpolate(self.raw_data, degree)
        # print poly_coeff
        self.training_feature[key_coeff_storage] = poly_coeff

        self.training_feature[key_storage] = np.polyval(poly_coeff, np.arange(len(self.raw_data)))
    
        voice_frame = self.get_voice_region(num_sampling)
        
        self.training_feature[key_sampling] = np.polyval(poly_coeff, voice_frame)

    def set_phone_duration(self, dur_path):

        # print self.name_index

        name = self.name_index.split('_')
        #tscsd_manual_a01_5
        sett = name[2][0]
        #tscsd_stust_a08
        # filename = '{}_{}_{}'.format(name[0], 'stust', name[2])
        filename = '{}{}{}'.format(name[0], '', name[2])
        path = '{}/{}/{}/{}_dur.npy'.format(dur_path, sett, filename, name[3])

        self.phone_duration = Utility.load_obj(path)
        # print self.phone_duration

    def get_phone_duration(self):
        return self.phone_duration

    def get_tonal_duration(self):
        return self.phone_duration[1] + self.phone_duration[2]

    def is_short_vowel(self):
        return self.vowel in Syllable.short_vowel

    def set_preceeding_succeeding_name_index(self, preceeding, succeeding):
        self.preceeding_name = preceeding
        self.succeeding_name = succeeding

    def set_latent_for_single_space(self, latent_variable):
        self.single_space_latent = latent_variable

    def __str__(self):
        return 'Syllable name index {}'.format(self.name_index)
    
    def __init__(self, 
                 raw_data=None, name_index=None, number_of_syllable_in_word=None, 
                 syllable_position_in_word=None, syllable_index_in_file=None, 
                 tone=None, stress_manual=None, filename=None, consonant=None, vowel=None, 
                 final_consonant=None, duration=None, part_of_speech=None, time_duration=None ):
        '''
        Constructor
        '''
        
        self.raw_data = raw_data
        self.name_index = name_index
        self.number_of_syllable_in_word = number_of_syllable_in_word
        self.syllable_position_in_word = syllable_position_in_word
        self.syllable_index_in_file = syllable_index_in_file
        self.tone = tone
        self.stress_manual = stress_manual
        self.filename = filename
        self.consonant = consonant
        self.vowel = vowel
        self.final_consonant = final_consonant
        self.duration = duration
        self.part_of_speech = part_of_speech
        self.time_duration = time_duration
        self.training_feature = dict()
        