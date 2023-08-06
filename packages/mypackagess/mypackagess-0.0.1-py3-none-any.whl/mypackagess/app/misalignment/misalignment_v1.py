import numpy as np
import pandas as pd
import vanalytics_helper as v_helper
import logers as log
import logging
import util as fft_cal
import rpm as Shaftspeed
import json
import vmaint_constants as constants
import time


class Misalignment_Analysis(object):

    log = log.customLogger(logging.DEBUG)

    
    """This is a class to analyse misalignment"""

    def __init__(self, samplingFrequency, noOfSample, windowsize, operating_rpm,
                 sensor_id, equipment_id, avgfft_data,rms):
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
        self.rms_threshold = constants.THREE
        self.rms=float(rms)
    
    def Start_End_Array(self):
        try:
            if self.operating_rpm is not None:
                for i in range(int(constants.END), constants.HARM_END_RNG):
                    Rpm = self.operating_rpm * i
                    limits = Rpm - (constants.FREQUENCY_LIMIT *
                                    Rpm), Rpm + (constants.FREQUENCY_LIMIT * Rpm)
                    self.sub_limits.append(limits)
                    
                return self.sub_limits
        except:
            self.log.error(
                "Exception occurred while checking limits for the harmonics", exc_info=True)


class limits_of_harmonics(Misalignment_Analysis):

    def Rms_Ranges(self):

        try:
            # RMS calculated from FFT data
            # RMS at 1X Harmonic
            
            if self.rms is not None:
                # RMS at 2X Harmonic
                self.rms_2 = self.rms * constants.RMS_2X_THRESHOLD
                # RMS at 3X Harmonic
                self.rms_3 = self.rms * constants.RMS_3X_THRESHOLD
                rms = [self.rms, self.rms_2, self.rms_3]
                
                return rms
            else:
                return
        except:
            self.log.error("Exception occurred while checking RMS values at 1X, 2X and 3X harmonics",
                           exc_info=True)
#        return rms

    def Limits_of_Harmonics(self):
        try:
            if self.Start_End_Array() is not None:
                for j in self.Start_End_Array():
                    self.Limits_of_harmonics.append(j)

                values = pd.DataFrame(self.Limits_of_harmonics, columns=[
                                      'start_limit', 'end_limit'])
                return values
            else:
                return
        except:
            self.log.error(
                "Exception occurred while checking Limit ranges", exc_info=True)

    def Maximum_value_at_harmonics(self):
        try:
            if self.Limits_of_Harmonics() is not None:
                # range values at corresponding harmonics
                limit_range = self.Limits_of_Harmonics()
                harmonics = limit_range.iloc[[0, 1, 2]]
                amp_one = int(harmonics.iloc[0, 0])
                amp_two = int(harmonics.iloc[0, 1])
                amp_three = int(harmonics.iloc[1, 0])
                amp_four = int(harmonics.iloc[1, 1])
                amp_five = int(harmonics.iloc[2, 0])
                amp_six = int(harmonics.iloc[2, 1])
            else:
                return
            # Frequency range at harmonics 1X, 2X and 3X
            if  self.avgfft_data is not None:
                FFT_DF = pd.DataFrame(self.avgfft_data)
                harmonics_at_1 = FFT_DF.iloc[amp_one: amp_two]
                harmonics_at_2 = FFT_DF.iloc[amp_three: amp_four]
                harmonics_at_3 = FFT_DF.iloc[amp_five: amp_six]
                # Fetching Maximum amplitudes at harmonics 1X, 2X and 3X
                max_value_1X = max(harmonics_at_1[0])
                max_value_2X = max(harmonics_at_2[0])
                max_value_3X = max(harmonics_at_3[0])

                return max_value_1X, max_value_2X, max_value_3X
            else:
                return
        except:
            self.log.error(
                "Exception occurred while checking Maximum value at harmonics", exc_info=True)

    def Misalignment_Check(self):

        try:
            # Maximum Amplitudes at harmonics 1X, 2X, 3X
            max_amplitude_at_harmonics = self.Maximum_value_at_harmonics()
            if max_amplitude_at_harmonics is not None:
                amplitude_1 = float(max_amplitude_at_harmonics[0])
                amplitude_2 = float(max_amplitude_at_harmonics[1])
                amplitude_3 = float(max_amplitude_at_harmonics[2])
            else:
                return
            # RMS calculated from FFT data
            rms = self.Rms_Ranges()
            if rms is not None:
                rms_1 = float(rms[0])
                rms_2 = float(rms[1])
                rms_3 = float(rms[2])
            else:
                return
            # If the max amplitude(amplitude_1) at harmonics 1X greater than RMS(rms_1),
            # then there might be a misalignmnet
            if amplitude_1 >= rms_1:
                result = str("Harmonic at 1x RPM")
                # If the max amplitude at harmonics(amplitude_2) 2X greater than RMS_2(rms_2), then Axial Misalignment
                if amplitude_2 >= rms_2:
                    result = str('Axial Misalignment')

                # If the max amplitude at harmonics 2X greater than max amplitude at harmonics 1X,
                # then Parallel Misalignment
                elif amplitude_2 >= amplitude_1:
                    result = str('ParalleMisalignment')

                    # If the max amplitude(amplitude_3) at harmonics 3X greater than RMS_3(rms_3), then Severe Misalignment
                    if amplitude_3 >= rms_3:
                        result = str('Severe Misalignment')

            else:
                result = str('No Misalignment')
            return result
        except:
            self.log.error(
                "Exception occurred while checking Misalignment Result", exc_info=True)

    def Misalignment_Total_Check(self):

        misalignment_output_res = []
        try:
           # Checking the result
            Misalignment_Check = self.Misalignment_Check()
            if Misalignment_Check is not None:
                if Misalignment_Check == 'Axial_Misalignment':
                    Misalignment_Check = "5"
                    misalignment_output_res.append(Misalignment_Check)
                elif Misalignment_Check == 'Parallel_Misalignment':
                    Misalignment_Check = "6"
                    misalignment_output_res.append(Misalignment_Check)
                elif Misalignment_Check == 'Severe Misalignment':
                    Misalignment_Check = "7"
                    misalignment_output_res.append(Misalignment_Check)
                else:
                    Misalignment_Check = "8"
                    misalignment_output_res.append(Misalignment_Check)

                # F -> "Fault"
                # data = [self.Equipment_id, self.Sensor_id, "F", json.dumps(
                #     misalignment_output_res) + "$T$" + str(time.time())]
                # v_helper.helper.data_to_publish.append(data)
                
                return misalignment_output_res
            else:
                return None
        except:
            self.log.error(
                "Exception occurred while checking Misalignment Analysis Status", exc_info=True)
