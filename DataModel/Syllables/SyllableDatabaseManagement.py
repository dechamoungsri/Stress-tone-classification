'''
Created on Jan 26, 2559 BE

@author: dechamoungsri
'''

import sys
# sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility
from Syllable import Syllable

import re
import numpy as np

class SyllableDatabaseManagement(object):
    '''
    classdocs
    '''
    un_voice_value = -1.00000000e+10

    def get_GP_LVM_training_data(self, feature_key, dur_position, num_sampling, exp=False, delta_bool=False, delta2_bool=False, missing_data=False, subtract_typical_contour=False, get_only_stress=False, non_unlabelled_stress=False, get_only_gpr_data=False, get_only_manual_data=False,
                    no_short_duration=False):

        Y_list = []
        name_index = []
        tone = []
        stress = []
        syllable_short_long_type = []
        syllalbe_position = []
        phonemes = []
        syllable_type = []

        # print self.syllables_list
        for syllable in self.syllables_list:
            # print syllable
            # print syllable.training_feature.keys()

            if no_short_duration:
                vt = syllable.get_vowel_length_type()
                if (vt == 'v') | (vt == 'vv') :
                    so_short_dur = 10
                else:
                    so_short_dur = 20

                if syllable.get_tonal_duration() < so_short_dur:
                    # print syllable.get_tonal_duration()
                    continue

            if get_only_gpr_data:
                if 'manual' in syllable.name_index:
                    continue

            if get_only_manual_data:
                if 'gpr' in syllable.name_index:
                    continue

            if non_unlabelled_stress:
                if syllable.stress_manual is None:
                    continue

            if get_only_stress:
                if syllable.stress_manual is not None:
                    if syllable.stress_manual != '1':
                        continue
                elif syllable.stress_manual is None:
                        continue

            if feature_key==Syllable.TRAINING_RAW_DATA:
                y = syllable.get_raw_with_missing_value(num_sampling, delta_bool, delta2_bool)
            elif feature_key==Syllable.TRAINING_RAW_DATA_VOWEL_FINAL:
                y = syllable.get_raw_with_missing_value(num_sampling, delta_bool, delta2_bool, duration=[1,2])
            elif missing_data:
                # y = self.get_missing_Y_features(syllable, num_sampling, subtract_typical_contour=subtract_typical_contour,
                #     feature_name=feature_key, 
                #     delta=delta_bool, 
                #     deltadelta=delta2_bool)
                y = syllable.get_Y_features(feature_key, num_sampling=num_sampling ,delta_bool=delta_bool, delta2_bool=delta2_bool, exp=exp, missing_data=missing_data)
            else :
                # y = self.get_Y_features(syllable, feature_key, delta_bool=delta_bool, delta2_bool=delta2_bool)
                y = syllable.get_Y_features(feature_key, num_sampling=num_sampling ,delta_bool=delta_bool, delta2_bool=delta2_bool, exp=exp)

            if feature_key == Syllable.Training_feature_phone_tonal_separated_with_noise_reduction:
                y = np.append(y, syllable.get_duration([1]))
                if syllable.final_consonant != 'z^':
                    y = np.append(y, syllable.get_duration([2]))
                # print y
                # print syllable.phone_duration
            else:
                duration = syllable.get_duration(dur_position)
                y = np.append(y, duration)
                pass
            
            Y_list.append(y)

            name_index.append(syllable.name_index)
            tone.append(syllable.tone)

            # print syllable.name_index, syllable.stress_manual

            if syllable.stress_manual is not None:
                if syllable.stress_manual == '1':
                    stress.append('Stress')
                else :
                    stress.append('Unstress')
            elif syllable.stress_manual is None:
                    stress.append('Unlabelled')

            syllable_short_long_type.append(syllable.get_syllable_short_long_type())
            syllalbe_position.append(syllable.get_is_final_position())

            phonemes.append(syllable.get_syllable_phoneme())

            syllable_type.append(syllable.get_syllable_type())

        return (Y_list,name_index,tone,stress,syllable_short_long_type,syllalbe_position, phonemes, syllable_type)

        pass

    def get_missing_Y_features(self, syllable, num_sampling, subtract_typical_contour,
            feature_name=None, 
            delta=False, 
            deltadelta=False):
        # return syllable.get_data_with_missing_values(50)
        return syllable.get_data_with_missing_values(
            num_sampling, subtract_typical_contour=subtract_typical_contour,
            feature_name=feature_name, 
            delta=delta, 
            deltadelta=deltadelta)
        pass

    def get_tone_n_syllable(self, target_tone):
        
        out_list = []

        for syllable in self.syllables_list:
            if syllable.tone == target_tone:
                # print syllable.tone
                out_list.append(syllable)

        return out_list

        pass 
        
    def get_number_of_syllable(self):
        return len(self.syllables_list)
        pass

    def get_syllable_at_index(self,index):
        return self.syllables_list[index]

    def config_tone_type(self):
        for syllable in self.syllables_list:
            syllable.tone = int(syllable.tone[1])

    def load_data_into_syllable_object(self, pattern, lf0_path=None, label_path_list=None):
        
        out_list = []
        
        print 'load_data_into_syllable_object'
        
        for file in label_path_list:
#             print file
            
            set = SyllableDatabaseManagement.get_file_set(file)
            # print set
            
            filename = Utility.get_basefilename(file)
            # print filename
            
            file_index = filename[-2:]
#             print file_index
            
            count = 0
            for line in Utility.read_file_line_by_line(file):
                # print line
                match = re.match(pattern, line)
                if match:
                    
                    tone = match.group('tone')
                    if 'x' in tone:
                        continue
                    
                    count+=1
                    syllable_position_in_word = match.group('syllable_position')
                    number_of_syllable_in_word = match.group('number_of_syllable')
                    # stress = match.group('stress')

                    if 'stress' in match.groupdict():
                        stress = match.group('stress')
                    else :
                        stress = None

                    consonant = match.group('consonant')
                    vowel = match.group('vowel')
                    finalconsonant = match.group('finalconsonant')
                    part_of_speech = match.group('part_of_speech')
                    
                    time_duration = int(match.group('end')) - int(match.group('start'))
                    
                    raw_data_path = '{}/{}/{}/{}.lf0'.format(lf0_path,set,filename,count)
                    raw_data = np.loadtxt(raw_data_path)

                    duration = len(raw_data)
                    
                    name_index = 'tscsd_gpr_{}{}_{}'.format(set, file_index , count)
                    
                    syllable = Syllable(
                        raw_data=raw_data, 
                        name_index=name_index, 
                        number_of_syllable_in_word=number_of_syllable_in_word, 
                        syllable_position_in_word=syllable_position_in_word, 
                        syllable_index_in_file=count, 
                        tone=int(tone), 
                        stress_manual=stress, 
                        filename=filename, 
                        consonant=consonant, 
                        vowel=vowel, 
                        final_consonant=finalconsonant, 
                        duration=duration, 
                        part_of_speech=part_of_speech, 
                        time_duration=time_duration)

                    out_list.append(syllable)
#                     print syllable
#                     print len(syllable.raw_data)
                else :
                    print line
#             print count        
#             return
        
        print 'Load finish : {} Syllables'.format(len(out_list))
        self.syllables_list = out_list
        pass

    def get_un_voice_file(self):
        for syl in self.syllables_list:
            un_voice_index = np.where(syl.raw_data==SyllableDatabaseManagement.un_voice_value)
            deleted_raw = np.delete(syl.raw_data, un_voice_index)
            if len(deleted_raw) == 0:
                print syl.name_index

    def get_syllable_by_name_index(self, name_index):
        for syl in self.syllables_list:
            if syl.name_index == name_index:
                return syl
        print 'Cannot find : {}'.format(name_index)

    @staticmethod
    def get_file_set(filepath):
        return filepath[-7]
        pass

    def dump(self,path):
        Utility.save_obj(self, path)

    def __init__(self, load_data_object=None, syllable_list=None):
        '''
        Constructor
        '''
        self.syllables_list = syllable_list
        if load_data_object is not None:
            self.syllables_list = Utility.load_obj(load_data_object)
    
        
    