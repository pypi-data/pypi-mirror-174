import numpy as np
import pandas as pd
import math
from numpy.linalg import norm
from numpy import (dot, arccos, clip)
import logers as log
import logging
import vanalytics_helper as v_helper
import util as fft_cal
import rpm as Shaftspeed
import vmaint_constants as constants
import json
import time


class unbalance(object):

    log = log.customLogger(logging.DEBUG)

    def __init__(self, sampling_freq, noOfSample, windowsize, operating_rpm, sensor_id,
                 equipment_id, horizontAccelData, verticalAccelData, avg_fft, rms):
        '''
        sampling_freq : Sampling Frequency of the sensor
        noOfSample : Number of samples in FFT, Accelerometer X and Accelerometer Y
        windowsize : window size of the fft data
        shaftSpeed : Maximum speed of the Motor
        horizontAccelData : Accelerometer X-axes data
        verticalAccelData : Accelerometer Y-axes data
        fftlist : FFT X-axes Data
        END_THRESHOLD = Amplitude range 1.2 times  (float(1.2))
        SECONDS = 60 seconds
        ANGLE_IN_DEGREE = Complete Angle (360 deg)
        IDEAL_DEGREE = Ideal phase difference
        DEGREE_RANGE = Limit for the Phase difference(+-30 deg)
        START_FREQ_LIMIT = start of frequency range for 1st Harmonic
        END_FREQ_LIMIT = End of frequency range for 1st Harmonic
        LoosenessRange = Harmonics for the other faults
        HARMONIC_ALLOWANCE = At each harmonics frequency limit is 0.2
        MAX_AMP_LIMIT_1X = Amplitude 40 percent at 1st Harmonic
        HARMONIC_END = Harmonics (2X to 10X)
        HARMONICS_RANGE = Harmonics range (0.5X, 1X, 1.5X, 2X,....10.5X)
        START_RANGE = 0
        TWO = 2
        START = 0.0
        END = 1.0
        INI_WINDOWSIZE = 0
        '''
        self.Sampling_Frequency = sampling_freq
        self.Number_sample = noOfSample
        self.Window_Size = windowsize
        self.operating_rpm = operating_rpm
        self.Sensor_id = sensor_id
        self.Equipment_id = equipment_id
        self.dataframe_X = horizontAccelData
        self.dataframe_Y = verticalAccelData
        self.avgfft_data = avg_fft
        self.window_val = self.Window_Size
        self.HarmonicsStart = []
        self.HarmonicsEnd = []
        self.Harmonic_Frequency = []
        self.rms = rms
        self.rms_threshold = constants.THREE

    def unbalance_axes(self):
        try:

            if self.operating_rpm is not None:
                time = 1 / self.Sampling_Frequency
                # FFT Frequencies
                fft_x = np.linspace(int(constants.START), int(constants.END) /
                                    (constants.TWO * time), self.Window_Size)
                fft_x_list = list(fft_x)
                # FFT Averaged Data
                #fft_y_list = self.RpmFromVib()[1]
                # RMS of FFT Data
                #fft_rms_Amp = self.RpmFromVib()[2]
                # Taking only those data which is above 1.2 times fft rms
                # taking amplitude above 1.5*rms
                fft_rms_index = [index for index, value in enumerate(self.avgfft_data)
                                 if value > constants.END_THRESHOLD * self.rms]

                fft_rms_values = [value for index, value in enumerate(self.avgfft_data)
                                  if value > constants.END_THRESHOLD * self.rms]
                frequency_above_rms = [fft_x_list[fft_rms_index[i]]
                                       for i in range(len(fft_rms_index))]
                # # Taking rpm 1x range to detect unbalance fault
                rpm1xranage = [frequency_above_rms[i] for i in range(len(frequency_above_rms))
                               if constants.START_FREQ_LIMIT * self.operating_rpm <= frequency_above_rms[i] <= constants.END_FREQ_LIMIT * self.operating_rpm]
                #            # Index of the freq above rms value
                #            indexFreqAboveRMS = [frequency_above_rms[rpm1xranage[i]]
                #                                        for i in range(len(rpm1xranage))]
                indexFreqAboveRMS = frequency_above_rms.index(rpm1xranage[0])

                # Amplitude of the freq
                max1xrpmAmplitude = fft_rms_values[indexFreqAboveRMS]

                # amplitudes and corresponding freq above the threshold and max amplitude in the list
                #            return RPM#fft_rms_values, frequency_above_rms, max1xrpmAmplitude
                return fft_rms_values, frequency_above_rms, max1xrpmAmplitude
            else:
                return
        except:
            self.log.error(
                "Exception occurred while checking Frequency above Threshold", exc_info=True)

    def unbalance_harmonics_check(self):

        values = self.unbalance_axes()
        if values is not None:
            fft_rms_values = values[0]
            frequency_above_rms = values[1]
            max1xrpmAmplitude = values[2]
        else:
            return
        # harmonicsfrequ = self.unbalance_harmonics_check()
        #rpm = int(self.RpmFromVib()[0])
        try:
            if self.operating_rpm is not None:

                harmonics = np.arange(int(constants.START), int(
                    constants.HARMONIC_END), float(constants.HARMONICS_RANGE))

                for j in harmonics:
                    # print(j)
                    Start_val = (
                        (self.operating_rpm * j) - (self.operating_rpm * float(constants.HARMONIC_ALLOWANCE)))
                    End_val = (
                        (self.operating_rpm * j) + (self.operating_rpm * float(constants.HARMONIC_ALLOWANCE)))
                    self.HarmonicsStart.append(Start_val)
                    self.HarmonicsEnd.append(End_val)

                k = list(zip(self.HarmonicsStart, self.HarmonicsEnd))
                # Checking for multiple harmonics with 20%, from 2x to 10.5x
                # and checking harmonics corresponding to 1x harmonic
                for harmonic_freq_values in frequency_above_rms:
                    for i, j in k:
                        if i <= harmonic_freq_values <= j:
                            self.Harmonic_Frequency.append(
                                harmonic_freq_values)
                        else:
                            pass
                harmonicAmpli = [fft_rms_values[frequency_above_rms.index(
                    i)] for i in self.Harmonic_Frequency]
                # Considering harmonics above 40% of 1x harmonics to detect other faults
                HrmAmpAbv40_per1x = [i for i in harmonicAmpli if i >
                                     float(constants.MAX_AMP_LIMIT_1X) * max1xrpmAmplitude]
                return HrmAmpAbv40_per1x
            else:
                return
        # return HrmAmpAbv40_per1x
        except:
            self.log.error("Exception occurred while checking amplitudes at multiple Harmonics",
                           exc_info=True)

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
            self.log.error(
                "Exception occurred while checking Unbalance acc data", exc_info=True)
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

    def unbalance_total_check(self):
        unbalance_output_res = []
        try:
            # For phase angle range
            start_angle = int(constants.IDEAL_DEGREE - constants.DEGREE_RANGE)
            end_angle = int(constants.IDEAL_DEGREE + constants.DEGREE_RANGE)
            Angle = self.phasefind()
            AmplitueAbove40Percent1XHarmonic = self.unbalance_harmonics_check()
            # Returning faults with respect to their condition
            # Check for other faults
            if AmplitueAbove40Percent1XHarmonic != []:
                Unbalance_result = "9"
                unbalance_output_res.append(Unbalance_result)

            # Unbalance phase angle should be 90 degree with allowance(+- 30 deg)
            elif start_angle <= Angle <= end_angle:
                Unbalance_result = "10"
                unbalance_output_res.append(Unbalance_result)

            # There's no Unbalance Fault
            else:
                Unbalance_result = "9"
                unbalance_output_res.append(Unbalance_result)

            # data = [self.Equipment_id, self.Sensor_id, "F", json.dumps(
            #     unbalance_output_res) + "$T$" + str(time.time())]
            # v_helper.helper.data_to_publish.append(data)

            return unbalance_output_res
        except:
            self.log.error(
                "Exception occurred while checking Unbalance result", exc_info=True)
