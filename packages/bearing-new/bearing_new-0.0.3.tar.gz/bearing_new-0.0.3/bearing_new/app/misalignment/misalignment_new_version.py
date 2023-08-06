
import numpy as np
import pandas as pd
# import enum
import vanalytics_helper as v_helper
import logers as log
import logging
import util2 as fft_cal
import json
import time
import vmaint_constants as constants


class Misalignment_Analysis(object):

    log = log.customLogger(logging.DEBUG)

    '''
    This is a class to analyse looseness
    '''

    def __init__(self, samplingFrequency, noOfSample, windowsize, operating_rpm, operating_rpm1,
                 sensor_id, equipment_id, avgfft_data_radial, avgfft_data_axial, freqn_axial, freqn_radial):
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
        self.operating_rpm1 = operating_rpm1
        self.Equipment_id = equipment_id
        self.Sensor_id = sensor_id
        self.avgfft_data_radial = avgfft_data_radial
        self.avgfft_data_axial = avgfft_data_axial
        self.sub_limits = []
        self.freqn_axial = freqn_axial
        self.freqn_radial = freqn_radial
        self.limit = []
    def Start_End_Array(self):
        # Shaft Rotational Speed
        try:
            if self.operating_rpm and self.operating_rpm1 is not None:
                rpm_ = [self.operating_rpm, self.operating_rpm1]
                for k in range(len(rpm_)):
                    for i in range(1, 7):
                        Rpm = (int(rpm_[k]))*i
                        limits = Rpm-(0.2*Rpm), Rpm+(0.2*Rpm)
                        self.sub_limits.append(limits)
                axial = self.sub_limits[:6]
                axial_value = pd.DataFrame(
                    axial, columns=['start_limit', 'end_limit'])
                #axial_harmonics = axial_value.iloc[[0,1,2,3,4,5]]
                axial_low_limit = axial_value["start_limit"]
                axial_low_limit_toframe = axial_low_limit.to_frame(
                    name="start_limit")
                axial_high_limit = axial_value["end_limit"]
                axial_high_limit_toframe = axial_high_limit.to_frame(
                    name="end_limit")

                radial = self.sub_limits[6:]
                radial_value = pd.DataFrame(
                    radial, columns=['start_limit', 'end_limit'])
                radial_low_limit = radial_value["start_limit"]
                radial_low_limit_toframe = radial_low_limit.to_frame(
                    name="start_limit")
                radial__high_limit = radial_value["end_limit"]
                radial__high_limit_toframe = radial__high_limit.to_frame(
                    name="end_limit")
                return axial_low_limit_toframe, axial_high_limit_toframe, radial_low_limit_toframe, radial__high_limit_toframe
            else:
                return
        except Exception as e:
            print(e)

    def max_val_blueprint(self, data1, data2, fft_data, freqn):
        try:
            for j in range(6):
                amp_low = int(data1.iloc[j, 0])
                amp_high = int(data2.iloc[j, 0])
                data = [idx for idx, element in enumerate(
                    freqn) if amp_low <= element <= amp_high]
                amplitude_data = [fft_data[i] for i in data]
                max_value_1 = max(amplitude_data)
                self.limit.append(max_value_1)
            return self.limit
        except Exception as e:
            print(e)

    def max_val(self):
        try:
            axial_data_low, axial_data_high, radial_data_low, radial_data_high = self.Start_End_Array()
            limit_2_axial = self.max_val_blueprint(
                axial_data_low, axial_data_high, self.avgfft_data_axial, self.freqn_axial)
            limit_2_radial = self.max_val_blueprint(
                radial_data_low, radial_data_high, self.avgfft_data_radial, self.freqn_radial)
            return limit_2_axial, limit_2_radial
        except Exception as e:
            print(e)

    def Misalignment_Check(self, max_amplitude):

        try:
            max_amp1x = max_amplitude[0]
            max_amp_2x = max_amplitude[1]
            max_amp_range1 = constants.ONE_RANGE*max_amp1x
            max_amp_range3 = constants.THREE_RANGE*max_amp1x
            max_amp2 = constants.TWO_RANGE*max_amp1x

            if max_amp_range1 >= max_amp_2x <= max_amp2:
                result = str('acceptable misalignment')

            elif max_amp2 > max_amp_2x <= max_amp_range3:
                result = str('misalignment')
                if max_amp_2x > max_amp_range3:
                   result = str('severe misalignment')

            else:
                result = str('No misalignment')

            return result
        except Exception as e:
            print(e)

    def mis_total_check(self, mis_check):
        misalignment_output_res = []
        try:

            if mis_check is not None:
                if mis_check == 'misalignment':
                    Misalignment_Check = "14"
                    misalignment_output_res.append(Misalignment_Check)

                if mis_check == 'severe misalignment':
                    Misalignment_Check = "14"
                    misalignment_output_res.append(Misalignment_Check)
                if mis_check == 'No misalignment':
                    Misalignment_Check = "13"
                    misalignment_output_res.append(Misalignment_Check)

                return misalignment_output_res
            else:
                return
        except Exception as e:
            print(e)

    def mis_total_axis_check(self):
        try:
            max_axial_amp, max_radial_amp = self.max_val()
            axial_misalignment_check = self.Misalignment_Check(max_axial_amp)
            radial_misalignment_check = self.Misalignment_Check(max_radial_amp)
            mis_axial_total_check = self.mis_total_check(
                axial_misalignment_check)
            mis_radial_total_check = self.mis_total_check(
                radial_misalignment_check)

            if mis_axial_total_check == "14" or mis_radial_total_check == "14":
                misalignment_res = "14"
            else:
                misalignment_res = "13"
            data = [self.Equipment_id, self.Sensor_id, "F", json.dumps(
                misalignment_res) + "$T$" + str(time.time())]
            v_helper.helper.data_to_publish.append(data)
            return misalignment_res
        except Exception as e:
            print(e)
