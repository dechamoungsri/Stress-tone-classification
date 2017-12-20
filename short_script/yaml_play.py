
import sys

sys.path.append('../')
sys.path.append('../../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

def get_syllable_list_from_syl_based_utterance_object(utt, syl_list=[]):

    for u in utt: 
        # print u
        if u['unit'] == 'syllable':
            syl = '{}-{}-{}-{}'.format(u['consonant'],u['vowel'],u['final_consonant'],u['tone_type'])
            syl_list.append(syl)
        else:
            get_syllable_list_from_syl_based_utterance_object(u['inners'], syl_list=syl_list)

    pass

if __name__ == '__main__':

    utt_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Training_data/03_GPR_syllable_level/utt/tsc/sd/a/tscsda01.utt.yaml'

    utt = Utility.yaml_load(utt_path)

    syl_list = []
    get_syllable_list_from_syl_based_utterance_object(utt, syl_list=syl_list)

    print syl_list

    # Utility.print_yaml_formatted(utt)

    pass