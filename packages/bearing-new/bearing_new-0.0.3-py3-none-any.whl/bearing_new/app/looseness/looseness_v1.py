import numpy as np
import pandas as pd
# import enum
import vanalytics_helper as v_helper
import logers as log
import logging
import util as fft_cal
import rpm as Shaftspeed
import vmaint_constants as constants
import json
import time


class Looseness_Analysis(object):

    log = log.customLogger(logging.DEBUG)

    '''
    This is a class to analyse looseness
    '''

    def __init__(self, samplingFrequency, noOfSample, windowsize,operating_rpm,
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
        self.rms = rms
        self.rms_threshold = constants.THREE

    
    def Start_End_Array(self):
        # Shaft Rotational Speed
        try:
            if self.operating_rpm is not None:
                for i in range(int(constants.END), constants.HARM_END_RNG):
                    Rpm = self.operating_rpm * i
                    limits = Rpm - (constants.FREQUENCY_LIMIT *
                                    Rpm), Rpm + (constants.FREQUENCY_LIMIT * Rpm)
                    self.sub_limits.append(limits)
                    
                return self.sub_limits
            else:
                return
        except:
            self.log.error(
                "Exception occurred while checking limits for the harmonics", exc_info=True)


class limits_of_harmonics(Looseness_Analysis):

    def Rms_Ranges(self):

        try:
            # fft values are averaged  
            if self.rms is not None:
            # self.rms_2 = self.rms*0.40
                self.rms_3 = self.rms * constants.RMS_3X_THRESHOLD
                return self.rms_3
            else:
                return
        except:
            self.log.error("Exception occurred while checking RMS values at 1X, 2X and 3X harmonics",
                           exc_info=True)

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
                harmonics = limit_range.iloc[[4, 6]]
                amp_one = int(harmonics.iloc[0, 0])
                amp_two = int(harmonics.iloc[0, 1])
                amp_three = int(harmonics.iloc[1, 0])
                amp_four = int(harmonics.iloc[1, 1])
            else:
                return
            
            if self.avgfft_data is not None:
            # Frequency range at harmonics 1X, 2X and 3X
            # fft_data = self.RpmFromVib()[1]
                FFT_DF = pd.DataFrame(self.avgfft_data)
                harmonics_at_1 = FFT_DF.iloc[amp_one: amp_two]
                harmonics_at_2 = FFT_DF.iloc[amp_three: amp_four]
    
                # Fetching Maximum amplitudes at harmonics 1X, 2X and 3X
                max_value_1X = max(harmonics_at_1[0])
                max_value_2X = max(harmonics_at_2[0])
                return max_value_1X, max_value_2X
            else:
                return
        except:
            self.log.error(
                "Exception occurred while checking Maximum value at harmonics", exc_info=True)

    def Looseness_Check(self):

        try:
            max_amplitude_at_harmonics = self.Maximum_value_at_harmonics()
            if max_amplitude_at_harmonics is not None:
                amplitude_5 = float(max_amplitude_at_harmonics[0])
                amplitude_7 = float(max_amplitude_at_harmonics[1])
            else:
                return
                
            if self.Rms_Ranges() is not None:
                rms = self.Rms_Ranges()
            else:
                return
            # If the max amplitude(amplitude_1) at harmonics 1X greater than RMS(rms_1),
            # then there might be a misalignmnet
            if amplitude_5 > float(rms):
                result = str("Looseness")
                if amplitude_7 > float(rms):
                    result = str("Severe Looseness")
            else:
                result = str('No Looseness')
            return result
        except Exception as e:
            self.log.error(
                "Exception occurred while checking Looseness Result", exc_info=True)
            print(e)
        # return rms

    def Looseness_Total_Check(self):
        looseness_output_res = []
        try:
            Looseness_Check = self.Looseness_Check()
            if Looseness_Check is not None:
                if Looseness_Check == 'Looseness':
                    Looseness_Check = "14"
                    looseness_output_res.append(Looseness_Check)
                elif Looseness_Check == 'Severe Looseness':
                    Looseness_Check = "15"
                    looseness_output_res.append(Looseness_Check)
                else:
                    Looseness_Check = "13"
                    looseness_output_res.append(Looseness_Check)

                # data = [self.Equipment_id, self.Sensor_id, "F", json.dumps(
                #     looseness_output_res) + "$T$" + str(time.time())]                
                # v_helper.helper.data_to_publish.append(data)                
                return looseness_output_res
            else:
                return
        except Exception as e:
            self.log.error(
                "Exception occurred while checking Looseness Analysis Status", exc_info=True)
            print(e)
