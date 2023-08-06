

import numpy as np
import pandas as pd
# import enum
import vanalytics_helper as v_helper
import logers as log
import logging
import util2 as fft_cal

import vmaint_constants as constants
import json
import time


class Looseness_Analysis(object):

    log = log.customLogger(logging.DEBUG)

    '''
    This is a class to analyse looseness
    '''

    def __init__(self, samplingFrequency, noOfSample, windowsize, operating_rpm,
                 sensor_id, equipment_id, avgfft_data, freqn):
        '''
        samplingFrequency, windowsize : from sensor details (metadata)
        noOfSample : Number of sampales
        fftlist : FFT data from mqtt
        FREQUENCY_LIMIT = float(0.20)
        RMS_2X_THRESHOLD = float(0.40)
        RMS_3X_THRESHOLD = float(0.30)
        '''
        self.sampling_frequency = samplingFrequency
        self.number_sample = noOfSample
        self.window_size = windowsize
        self.operating_rpm = operating_rpm
        self.Equipment_id = equipment_id
        self.Sensor_id = sensor_id
        self.avgfft_data = avgfft_data
        self.Limits_of_harmonics = []
        self.sub_limits = []
        self.limit_low = []
        self.limit_high = []
        self.limit_max_values = []
        self.limit2 = []
        self.freqn = freqn
        self.amp_data = []

    def Start_End_Array(self):
        # Shaft Rotational Speed
        try:
            if self.operating_rpm is not None:
                range1_limit=self.operating_rpm*constants.THIRTY_PERCENT
                for j in range(1, 7):
                    Rpm = (self.operating_rpm)*j
                    range_of_harmonics=Rpm-range1_limit,Rpm+range1_limit
                    self.Limits_of_harmonics.append(range_of_harmonics)
                values = pd.DataFrame(self.Limits_of_harmonics, columns=['start_limit', 'end_limit'])
                return values  
        except Exception as e:
            print(e)

    def Maximum_value_at_harmonics(self):
        try:
            if self.Start_End_Array() is not None:
                # range values at corresponding harmonics
                limit_range = self.Start_End_Array()

                harmonics = limit_range.iloc[[0, 1, 2, 3, 4, 5]]
                #print(harmonics)

                for i in range(6):

                    amp_low = int(harmonics.iloc[i, 0])
                    #amp_low.tolist()
                    amp_high = int(harmonics.iloc[i, 1])
                    self.limit_low.append(amp_low)

                    self.limit_high.append(amp_high)
                    #self.limit_low=[round(num, 2) for num in self.limit_low]
                    #self.limit_high = [round(num, 2) for num in self.limit_high]
                df1 = pd.DataFrame(self.limit_low)
                df2 = pd.DataFrame(self.limit_high)

                return df1, df2

        except Exception as e:
            print(e)

    def max_val(self):
        try:
            if self.avgfft_data is not None:
                # fft_data = self.RpmFromVib()[1]
                FFT_DF = self.avgfft_data
                data1, data2 = self.Maximum_value_at_harmonics()
                for j in range(6):
                    amp_low2 = int(data1.iloc[j, 0])
                    amp_high2 = int(data2.iloc[j, 0])
                    #prxint(FFT_DF)
                    #print(type(self.freqn))
                    #freqndata=np.array(self.freqn)

                    data = [idx for idx, element in enumerate(
                        self.freqn) if amp_low2 <= element <= amp_high2]

                    amplitude_data = [FFT_DF[i] for i in data]
                    
                    max_value_1 = max(amplitude_data)
                    #print(max_value_1)
                    self.limit2.append(max_value_1)

                return self.limit2
            else:
                return
        except Exception as e:
            print(e)
    def Looseness_Check(self):

        try:
            max_amplitude_at_harmonics = self.max_val()
            max_amp1x = max_amplitude_at_harmonics[0]
            amp_2x_6x = max_amplitude_at_harmonics[1:]
            #print(newlist_amp)
            max_amp_1x_120 = constants.ONE_TWENTY_PERCENT*max_amp1x
            faultCounter = 0
            if amp_2x_6x is not None:
                for i in amp_2x_6x:
                    if i > max_amp_1x_120:
                        faultCounter = faultCounter+1
                    if faultCounter >= constants.TWO:
                        result = str('Looseness')
                        break
                    else:
                        result = str('No Looseness')

                return result

            else:
                return

        except Exception as e:
            print(e)

    def Looseness_Total_Check(self):
        looseness_output_res = []
        try:
            Looseness_Check = self.Looseness_Check()
            if Looseness_Check is not None:
                if Looseness_Check == 'Looseness':
                    Looseness_Check = '14'
                    los_result = 'Looseness'
                    looseness_output_res.append(los_result)

                else:
                    Looseness_Check = '13'
                    los_result = 'no Looseness'
                    looseness_output_res.append(los_result)

                data = [self.Equipment_id, self.Sensor_id, "F", json.dumps(
                    looseness_output_res) + "$T$" + str(time.time())]
                v_helper.helper.data_to_publish.append(data)

                return looseness_output_res
            else:
                return
        except Exception as e:

            print(e)
