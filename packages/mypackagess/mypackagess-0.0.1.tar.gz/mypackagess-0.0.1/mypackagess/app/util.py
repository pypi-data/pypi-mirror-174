import logging
import sys
import math
#   external library
import numpy as np
import pandas as pd
import vanalytics_helper as v_helper
import logers as log_file
import itertools
import vmaint_constants as constants

# ParserFftCalculation  class calculates and returns the AVERAGE, rms, frequencies whose amplitude are >3*rms


class ParserFftCalculation(object):
    #log = log_file.customLogger(logging.DEBUG)

    @classmethod
    def parse_fft_rawdata(cls, sampling_frequency, fft_data, rms_threshold_range = constants.THREE):
        try:
            fft_average = [sum(e)/len(e) for e in zip(*fft_data)]
            # frequencies are selected
            xf = np.linspace(constants.START_RANGE, constants.END / (constants.TWO *
                                                                     (constants.END / sampling_frequency)), len(fft_average))
            # rms is calculated using average of FFT
            rms = np.sqrt(np.mean(np.square(fft_average)))

            # list of all indices [looseness, misalignment, unbalanace]
            index = [list(fft_average).index(i) for i in fft_average]
            amplitude = [i for i in fft_average]
            #frequency = [list(xf)[i] for i in index]
            frequency=list(xf)
            # checks for amplitudes index greater than 3 times of RMS [bearing, gearbox]
            rms_index = [list(fft_average).index(
                i) for i in fft_average if i > rms_threshold_range * rms]
            rms_amplitude = [list(fft_average).index(
                i) for i in fft_average if i > rms_threshold_range * rms]
            rms_frequency = [list(xf)[i] for i in rms_index]
            

            
            
            # # checks for amplitudes index greater thn 3*rms
            # amplitude_rms_index = [list(fft_average).index(
            #     i) for i in fft_average if i > rms_threshold_range * rms_of_fft_average]
            # # checks for the amplitudes for the index values
            # horizontamplitudabove_rms_values = [
            #     i for i in fft_average if i > rms_threshold_range * rms_of_fft_average]
            # # corresponding freqns of amplitudes greater than 3*rms
            # frequency_above_rms_values = [list(xf)[i]
            #                               for i in amplitude_rms_index]

            output = [fft_average, rms, amplitude, frequency, rms_amplitude, rms_frequency]
            return output

        except Exception as e:
            print(e)