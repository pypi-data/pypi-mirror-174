
import numpy as np
import pandas as pd
# import enum
import vanalytics_helper as v_helper
import logers as log
import logging
import util2 as fft_cal
from statistics import mean
import math
from numpy.linalg import norm
from numpy import (dot, arccos, clip)
import vmaint_constants as constants
import json
import time


class Unbalance_Analysis(object):

    log = log.customLogger(logging.DEBUG)

    def __init__(self, samplingFrequency, noOfSample, windowsize, operating_rpm_X,
                 sensor_id, equipment_id, avgfft_data_X, avgfft_data_Y, avgfft_data_Z, freqn_X, freqn_Y, freqn_Z, accx, accy):
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
        self.operating_rpm_X = operating_rpm_X
        
        #self.operating_rpm1 = operating_rpm1
        self.Equipment_id = equipment_id
        self.Sensor_id = sensor_id
        self.avgfft_data_X = avgfft_data_X
        self.avgfft_data_Y = avgfft_data_Y
        self.avgfft_data_Z = avgfft_data_Z
        self.sub_limits = []

        self.freqn_X = freqn_X
        self.freqn_Y = freqn_Y
        self.freqn_Z = freqn_Z
        self.Limits_of_harmonics = []
        self.sub_limits = []
        self.limit_low = []
        self.limit_high = []
        self.limit_max_values = []
        self.limit2 = []
        self.limit3 = []
        #self.freqn = freqn
        self.dataframe_X = accx
        self.dataframe_Y = accy

        self.hrm = []

    def Start_End_Array(self, fftdata, freqn, operating_rpm,limit):
        # Shaft Rotational Speed
        try:
            if operating_rpm is not None:
                FFT_DF = fftdata
                #limit = operating_rpm *0.35
                for j in range(1, 11):
                    Rpm = (operating_rpm)*j
                    lower_limit, upper_limit = Rpm - limit, Rpm + limit
                    harmonic_value = [idx for idx, element in enumerate(
                        freqn) if lower_limit <= element <= upper_limit]
                    #self.hrm.append(harmonic_value)
                    amplitude_data = [FFT_DF[i] for i in harmonic_value]
                    max_value_1 = max(amplitude_data)
                    self.limit2.append(max_value_1)

                return self.limit2, amplitude_data
                # return self.amp_data

            else:
                return
        except Exception as e:
            print(e)

    def accelerometer_data(self):

        try:
            if (self.dataframe_X is not None) and (self.dataframe_Y is not None):
                # Accelerometer X-axes Data
                amplitudeX = pd.DataFrame(self.dataframe_X)
                # converting string to numeric
                amplitudeX = amplitudeX.apply(pd.to_numeric, errors='coerce')
                x = amplitudeX[0]
                # Accelerometer Y-axes Data
                amplitudeY = pd.DataFrame(self.dataframe_Y)
                # converting string to numeric
                amplitudeY = amplitudeY.apply(pd.to_numeric, errors='coerce')
                y = amplitudeY[0]
                return x, y
            else:
                return
        except Exception as e:
            print(e)

    def phasefind(self):
        try:
            horizontalaxesamplitude, verticalamplitude = self.accelerometer_data()
            if (horizontalaxesamplitude is not None) and (verticalamplitude is not None):
                if len(horizontalaxesamplitude) != len(verticalamplitude):
                    # Absolute value of difference
                    difference = abs(
                        len(horizontalaxesamplitude) - len(verticalamplitude))
                    diff = -(int(difference))
                    # If the lenth of Acc_X-axes is greater than Acc_Y-axes
                    if len(horizontalaxesamplitude) > len(verticalamplitude):
                        # Eliminate the noOfdifference in Acceleromer X-axes
                        df_horizontal = horizontalaxesamplitude[: diff]
                        df_vertical = verticalamplitude
                    # If the lenth of Acc_Y-axes is greater than Acc_X-axes
                    elif len(verticalamplitude) > len(horizontalaxesamplitude):
                        # Eliminate the noOfdifference in Acceleromer Y-axes
                        df_vertical = verticalamplitude[: diff]
                        df_horizontal = horizontalaxesamplitude
                    # Data for calculating Phase Difference
                    amplitudeX = df_horizontal
                    amplitudeY = df_vertical
                    c = dot(amplitudeX, amplitudeY) / \
                        norm(amplitudeX)/norm(amplitudeY)
                    # Phase Difference in Radians
                    angleinradians = arccos(clip(c, -1, 1))
                    # Phase Difference in degrees
                    angleindegree = (
                        (angleinradians * int(constants.ANGLE_IN_DEGREE)) / int(constants.TWO * math.pi))
                else:
                    amplitudeX = horizontalaxesamplitude
                    amplitudeY = verticalamplitude
                    c = dot(amplitudeX, amplitudeY) / \
                        norm(amplitudeX)/norm(amplitudeY)
                    # Phase Difference in Radians
                    angleinradians = arccos(clip(c, -1, 1))
                    # Phase Difference in degrees
                    angleindegree = (
                        (angleinradians * int(constants.ANGLE_IN_DEGREE)) / (int(constants.TWO) * math.pi))
                return angleindegree
            else:
                return
        except Exception as e:
            print(e)
    def amp_call(self,operatingRpm):
        try:
            limit1=operatingRpm*constants.THIRTY_PERCENT
            limit2=operatingRpm*constants.THIRTY_FIVE_PERCENT
            if self.number_sample and self.window_size==8192:
                max_ampx,ampx = self.Start_End_Array(
                    self.avgfft_data_X, self.freqn_X, self.operating_rpm_X,limit1)
                max_ampy,ampy = self.Start_End_Array(
                    self.avgfft_data_Y, self.freqn_Y, self.operating_rpm_X,limit1)
                max_ampz,ampz = self.Start_End_Array(
                    self.avgfft_data_Z, self.freqn_Z, self.operating_rpm_X,limit1)
            else:
                max_ampx,ampx = self.Start_End_Array(
                    self.avgfft_data_X, self.freqn_X, self.operating_rpm_X,limit2)
                max_ampy,ampy = self.Start_End_Array(
                    self.avgfft_data_Y, self.freqn_Y, self.operating_rpm_X,limit2)
                max_ampz,ampz = self.Start_End_Array(
                    self.avgfft_data_Z, self.freqn_Z, self.operating_rpm_X,limit2)
            return max_ampx,ampx
        except Exception as e:
            print(e)
    def Unbalance_Check(self):
        unbalance_output_res = []
        try:
            max_amp_x, amp_x = self.amp_call(self.operating_rpm_X)
            angle_phase = int(self.phasefind())
            amplitude_list = max_amp_x[1:]
            avg = mean(amplitude_list)
            max_amp1x = amplitude_list[0]
            maxamp1x = constants.limit*max_amp1x
            if avg <= maxamp1x:
                #print("imbalance is present")
                if angle_phase in range(0, 120):
                        Unbalance_result = "10"
                        unbalance_output_res.append(Unbalance_result)
                else:
                        Unbalance_result = "9"

                        unbalance_output_res.append(Unbalance_result)
            else:
                Unbalance_result = "9"
                unbalance_output_res.append(Unbalance_result)
            data = [self.Equipment_id, self.Sensor_id, "F", json.dumps(unbalance_output_res) + "$T$" + str(time.time())]
            v_helper.helper.data_to_publish.append(data)
            return unbalance_output_res

        except Exception as e:
            print(e)
