
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../')
sys.path.append('../')

from tool_box.util.utility import Utility

from DataModel.Syllables.Syllable import Syllable

def add_phone_dur(dur_path, object_list_path):

    for obj_path in object_list_path:

        syl_object = Utility.load_obj(obj_path)
        syl_list = syl_object.syllables_list

        for syl in syl_list:
            syl.set_phone_duration(dur_path)

        Utility.save_obj(syl_object, obj_path)

    pass

def check_result(object_list_path):
    for obj_path in object_list_path:

        syl_object = Utility.load_obj(obj_path)
        syl_list = syl_object.syllables_list

        for syl in syl_list:
            print syl.get_phone_duration()
        
    pass

if __name__ == '__main__':

    dur_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_data/gpr_stress_unstress/dur/'

    object_list_path = [
        # '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/gpr_syllable_obj/syllable_0.pickle',
        # '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/gpr_syllable_obj/syllable_1.pickle',
        # '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/gpr_syllable_obj/syllable_2.pickle',
        # '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/gpr_syllable_obj/syllable_3.pickle',
        # '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/gpr_syllable_obj/Syllable_4.pickle',
        '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/gpr_syllable_obj/Syllable_object.pickle'
    ]

    add_phone_dur(dur_path, object_list_path)

    check_result(object_list_path)

    pass



