
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

import numpy as np
import matplotlib.pyplot as plt

import re

if __name__ == '__main__':

    path = sys.argv[1]

    for line in Utility.read_file_line_by_line(path):
        if 'color' not in line: continue
        files = line.split('&')
        # {\color{red} tscsd\_manual\_b11\_2 } & {\color{red} tscsd\_manual\_g36\_10 } & {\color{red} tscsd\_manual\_b35\_5 } & {\color{red} tscsd\_manual\_g37\_5 }\\
        # print files
        for f in files:
            pattern = re.compile(r""".*{.+color.+\s(?P<filename>.+)\s}.*""",re.VERBOSE)
            match = re.match(pattern, f)
            if match:
                filename = match.group('filename')
                print filename.replace('\_', '_')

    pass
