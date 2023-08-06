import os
import logging
import logers
from types import SimpleNamespace
import json
import requests as req
import vanalytics_helper as v_helper
import mqtt_con as m_con
from enum import Enum
import numpy as np
import time

from util import ParserFftCalculation as fft_cal
import rpm as op_rpm

import gear.gear as algo_gearbox
import bearing.bearing as algo_bearing
import velocity_severity.machine_condition as algo_severity
import misalignment.misalignment as algo_misalignment
import looseness.looseness as algo_looseness
import machine_status.on_off as algo_onoff
import unbalance.unbalance as algo_unbalance

import vanalytics_helper as v_helper


log = logers.customLogger(logging.DEBUG)

DIR = os.path.dirname(__file__)
if not DIR:
    FILE_PATH = "main_config.json"
else:
    FILE_PATH = DIR + "/main_config.json"

with open(FILE_PATH, 'r') as readfile:
    main_config = json.load(readfile)

class VegamAlogrithm(Enum):
    VelocitySeverity = 1
    BearingFault = 2
    MisalignmentFault = 3
    UnbalanceFault = 4
    MechanicalLooseness = 5
    GearboxFault = 6
    MachineOnOff = 7

class CommonFeatures:
    #   will have site id list, used to get the equipment from the api for each site
    site_ids = []   
    #   if not able to get euipment, will store those site id here
    site_id_failed = [] 
    #   store the brokers and there respective client { key :- ipaddress_portnumber }
    brokers_dict = {}   

    #   will store id's for which metadata needs to be fetched { 'E': equipment_id & 'M': sensor_id}
    metadata_lookup = []    
    #   if not able to fetch metadata, id's will be stored here
    metadata_lookup_failed = [] 

    #   will store all the topics { 'topic_id': {'E': equipment_id, 'S': sensor_id, 'T': TagType}}
    topics_lookup = {}  
    #   will store the equipment data { equipment_id: {'E': equipment_data, 'M': equipment_metadata }}
    equipment_store = {}
    #   will store the sensor metadata {sensor_id: {'M': sensor_metadata}}    
    sensor_store = {}
    main_config = {}
    simulator_rpm = 0

    sensordata_lookup = {}

    updated_equipments = {
        VegamAlogrithm.VelocitySeverity: [],
        VegamAlogrithm.MisalignmentFault: [],
        VegamAlogrithm.UnbalanceFault: [],
        VegamAlogrithm.BearingFault: [],
        VegamAlogrithm.GearboxFault: [],
        VegamAlogrithm.MechanicalLooseness: [],
        VegamAlogrithm.MachineOnOff: []
    }

    @classmethod
    def get_site_to_moniter(cls):
        queryStr = "?ipAddress=" + main_config["initial_config"]["ip_address"]
        queryStr = queryStr + "&portNumber=" + str(main_config["initial_config"]["port_number"])
        
        url = main_config["vmaint_api"]["base_url"]
        url = url + "/GetSitesToProcess" + queryStr

        initial_data = None
        try:
            initial_data = req.post(url)
            if initial_data is not None:
                if initial_data.status_code == 200 and initial_data.text != 'null':
                    return json.loads(initial_data.text)
            return []
        except Exception as ex:
            log.error(f'Unable to get the initial list of sites from vmaint api with error: {ex}', exc_info=True)
    
    @classmethod
    def get_sites_equipments(cls):
        if len(CommonFeatures.site_ids) > 0:
            site_id = CommonFeatures.site_ids.pop()
            CommonFeatures.get_equipment_data(site_id)

    @classmethod
    def get_equipment_data(cls, site_id):
        '''
        @param site_id : site_id for which equipment data is required
        '''
        queryStr = "?ipAddress=" + main_config["initial_config"]["ip_address"]
        queryStr = queryStr + "&portNumber=" + str(main_config["initial_config"]["port_number"])
        queryStr = queryStr + "&siteID=" + str(site_id)

        url = main_config["vmaint_api"]["base_url"]
        url = url + "/GetAnalyticsEquipments" + queryStr

        equipment_data = None
        try:
            equipment_data = req.post(url)
            if equipment_data is not None:
                if equipment_data.status_code == 200 and equipment_data.text != 'null':
                    equipment_list = json.loads(equipment_data.text)
                    CommonFeatures.store_equipment_data(equipment_list)
                else:
                    CommonFeatures.site_id_failed.append(site_id)
            else:
                CommonFeatures.site_id_failed.append(site_id)
        except Exception as ex:
            log.error(f'Unable to get the equiment data from vmaint for the site id:- {site_id} with error {ex}', exc_info=True)
            CommonFeatures.site_id_failed.append(site_id)
        finally:
            CommonFeatures.get_sites_equipments()

    @classmethod
    def store_equipment_data(cls, equipment_list):
        '''
        @param equipment_list : list of equipments to be stored
        '''
        for equipment in equipment_list:
            equipment_obj = json.loads(json.dumps(equipment), object_hook=lambda d: SimpleNamespace(**d))                
            if len(equipment_obj.Brokers) == 0:
                continue
            CommonFeatures.equipment_store[equipment_obj.EquipmentID] = {'E' : equipment_obj, 'M' : None }
            CommonFeatures.metadata_lookup.append({ 'E' : equipment_obj.EquipmentID })
            temp = equipment_obj.Brokers[0]
            broker_key = temp.IpAddress + "_" + str(temp.PortNumber)
            if broker_key not in CommonFeatures.brokers_dict:
                broker = v_helper.BrokerInfo(temp.IpAddress, temp.PortNumber, temp.UserName, temp.Password)
                CommonFeatures.brokers_dict[broker_key] = broker
            if len(equipment_obj.AttachedSensors) > 0:
                for sensor in equipment_obj.AttachedSensors:
                    CommonFeatures.metadata_lookup.append({ 'S' : sensor.SensorMacID })
                    if (sensor.SensorMacID in CommonFeatures.sensor_store.keys()) == False:
                        CommonFeatures.sensor_store[sensor.SensorMacID] = None
                    if len(sensor.Tags) > 0:
                        for tag in sensor.Tags:
                            CommonFeatures.topics_lookup[tag.Topic] = { 'E' : equipment_obj.EquipmentID, 'S': sensor.SensorMacID, 'T': tag.TopicRepresents }
                            if tag.TopicType == "S":
                                CommonFeatures.brokers_dict[broker_key].SubTopics.append(tag.Topic)
                            
                        CommonFeatures.brokers_dict[broker_key].SubTopics = list(set(CommonFeatures.brokers_dict[broker_key].SubTopics))

    @classmethod
    def get_metadata(cls):
        if len(CommonFeatures.metadata_lookup) > 0:
            metadata_item = CommonFeatures.metadata_lookup.pop()
            CommonFeatures.call_metadata_api(metadata_item)

    @classmethod
    def call_metadata_api(cls, metadata_item):
        id = ""
        mtype = "E"
        if 'E' in metadata_item:
            id = metadata_item['E']
        else:
            id = metadata_item['S']
            mtype = "S"
        
        post_data = {
            "UniqueName" : id
            , "UniqueId" : ""
            , "Key": []
            , "Tag": []
        }

        url = main_config["metadata_api_info"]["base_url"]

        try:            
            metadata = req.post(url, json=post_data, headers={"Content-Type":"application/json"})
            if metadata is not None:
                if(metadata.status_code == 200 and metadata.text != 'null'):
                    metadata = json.loads(metadata.text)
                    CommonFeatures.store_metadata(metadata, metadata_item, mtype)
                else:
                    CommonFeatures.metadata_lookup_failed.append(metadata_item)
            else:
                CommonFeatures.metadata_lookup_failed.append(metadata_item)
        except Exception as ex:
            log.error(f'Unable to get the equiment/sensor data from metadata for the unique_name:- {id} with error: {ex}', exc_info=True)
            CommonFeatures.metadata_lookup_failed.append(metadata_item)
        finally:
            CommonFeatures.get_metadata()

    @classmethod
    def store_metadata(cls, metadata, metadata_item, mtype):
        try:
            metadata_obj = json.loads(json.dumps(metadata), object_hook=lambda d: SimpleNamespace(**d))
            if mtype == 'E':
                CommonFeatures.equipment_store[metadata_item['E']]['M'] = metadata_obj
            else:
                CommonFeatures.sensor_store[metadata_item['S']] = { 'M' : metadata_obj }
        except Exception as ex:
            log.error(f'Unable to store data {metadata} with error: {ex}', exc_info=True)

    @classmethod
    def connect_subscribe_mqtt(cls, broker_keys):
        '''
        @param broker_key : list of broker key [key: ipaddress + '_' + port] 
        '''
        if len(broker_keys) > 0:
            broker_key = broker_keys.pop()
            try:
                broker_info = CommonFeatures.brokers_dict[broker_key]
                if broker_info.MqttClient is not None and broker_info.MqttClient.isConnected == 1:
                    pass
                else:
                    broker_info.MqttClient = m_con.MqttClient(broker_info.ipAddress, broker_info.portNumber, broker_info.userName, broker_info.password, broker_info.brokerName)
                    broker_info.MqttClient.connect_broker()

                sub_topics = broker_info.SubTopics[:]
                sub_topics.append("se_poc/rpm")
                # broker_info.SubTopics = []
                broker_info.MqttClient.subscribe_topic(sub_topics)                
            except Exception as ex:
                log.error(f'Failed to connect/subscribe {broker_key} with error: {ex}', exc_info=True)
            finally:
                CommonFeatures.connect_subscribe_mqtt(broker_keys)

    @classmethod
    def updateEquipment(cls, equipments):
        CommonFeatures.store_equipment_data(equipments)

        if len(CommonFeatures.metadata_lookup) > 0:
            CommonFeatures.get_metadata()

        broker_keys = list(CommonFeatures.brokers_dict.keys())
        if len(broker_keys) > 0:
            CommonFeatures.connect_subscribe_mqtt(broker_keys)

    @classmethod
    def update_equipment_process(cls, equipments):
        for equipment in equipments:
            equipment_obj = json.loads(json.dumps(equipment), object_hook=lambda d: SimpleNamespace(**d))
            CommonFeatures.updated_equipments[VegamAlogrithm.VelocitySeverity].append(equipment_obj.EquipmentID)
            CommonFeatures.updated_equipments[VegamAlogrithm.MisalignmentFault].append(equipment_obj.EquipmentID)
            CommonFeatures.updated_equipments[VegamAlogrithm.UnbalanceFault].append(equipment_obj.EquipmentID)
            CommonFeatures.updated_equipments[VegamAlogrithm.BearingFault].append(equipment_obj.EquipmentID)
            CommonFeatures.updated_equipments[VegamAlogrithm.GearboxFault].append(equipment_obj.EquipmentID)
            CommonFeatures.updated_equipments[VegamAlogrithm.MechanicalLooseness].append(equipment_obj.EquipmentID)
            CommonFeatures.updated_equipments[VegamAlogrithm.MachineOnOff].append(equipment_obj.EquipmentID)

    @classmethod
    def getSensorMetadata(cls, sensor_id, args):
        '''
        @param sensor_id : sensor id for which metadata needs to be searched
        @args : list of metadata keys e.g.['power', 'modelnumber']
        @return : it will return list, [['256'], ['vsens_234']]
        '''
        output = []
        try:
            if sensor_id in CommonFeatures.sensor_store:
                if CommonFeatures.sensor_store[sensor_id] is not None:
                    if CommonFeatures.sensor_store[sensor_id]['M'] is not None:
                        metadata_prop = CommonFeatures.sensor_store[sensor_id]['M'].property
                        for t in args:
                            data = next(
                                (x for x in metadata_prop if x.key.lower() == t.lower()), None)
                            if data is not None:
                                output.append(data.value)
                            else:
                                output.append(None)
        except Exception as ex:
            log.error(
                f"failed to get sensor metadata for the list {args}", exc_info=True)
        finally:
            # TODO need to remove after all data is validated
            return output

    @classmethod
    def getEquipmentData(cls, equipment_id, sensor_id, args):
        '''
        @param equipment_id : equipment id for which data requied
        @param sensor_id : sensor id for which data needs to be searched
        @args : current version supports following keys ['axisx', 'axisy', 'axisz', 'connectionmode']
        @return : it will return list, ['x', 'y', 'z', 'B']
        '''
        output = []
        try:
            if equipment_id in CommonFeatures.equipment_store:
                equipment = CommonFeatures.equipment_store[equipment_id]['E']
                sensors = equipment.AttachedSensors
                req_sensor = next(
                    (x for x in sensors if x.SensorMacID == sensor_id), None)

                if req_sensor is not None:
                    for y in args:
                        y = y.lower()
                        if y == 'axisx':
                            output.append(req_sensor.AxisX)
                        elif y == "axisy":
                            output.append(req_sensor.AxisY)
                        elif y == "axisz":
                            output.append(req_sensor.AxisZ)
                        elif y == "connectionmode":
                            output.append(req_sensor.ConnectionMode)
                        else:
                            output.append(None)
        except Exception as ex:
            print(ex)
            #   write log here
        finally:
            # TODO need to remove after all data is validated
            return output

    @classmethod
    def getEquipmentMetaData(cls, equipment_id, args):
        '''
        @param equipment_id : equipment id for which metada requied
        @param sensor_id : sensor id for which metadata needs to be searched
        @args : list of metadata keys e.g.['power', 'modelnumber']
        @return : it will return list, [['256'], ['vsens_234']]
        '''
        output = []
        try:
            if equipment_id in CommonFeatures.equipment_store:
                data = CommonFeatures.equipment_store[equipment_id]['M']
                if data is not None:
                    metadata_prop = data.property
                    for t in args:
                        data = next(
                            (x for x in metadata_prop if x.key.lower() == t.lower()), None)
                        if data is not None:
                            output.append(data.value)
                        else:
                            output.append(None)
        except Exception as ex:
            log.error(
                f"failed to get equipment metadata for the list {args}", exc_info=True)
        finally:
            # TODO need to remove after all data is validated
            return output

    @classmethod
    def getAxisInfo(cls, equipment_id, sensor_id, args):
        output = []
        try:
            if equipment_id in CommonFeatures.equipment_store:
                equipment = CommonFeatures.equipment_store[equipment_id]['E']
                sensors = equipment.AttachedSensors
                req_sensor = next(
                    (x for x in sensors if x.SensorMacID == sensor_id), None)

                if req_sensor is not None:
                    for y in args:
                        y = y.lower()
                        if y == 'axisx':
                            output.append(req_sensor.AxisX.lower())
                        elif y == "axisy":
                            output.append(req_sensor.AxisY.lower())
                        elif y == "axisz":
                            output.append(req_sensor.AxisZ.lower())
                        else:
                            output.append(None)
        except Exception as ex:
            log.error(
                f"failed to get equipment axis details for the sensor_id: {sensor_id}", exc_info=True)
        finally:
            return output

    @classmethod
    def parse_rawdata(cls, data):
        try:
            # type_info = type(data)
            if isinstance(data, dict):
                d = str(data["v"]) + "$T$" + str(data["t"])
            else:
                d = json.loads(data)
                d = str(d["v"]) + "$T$" + str(d["t"])
            return d
        except Exception as ex:
            log.error(f"ERROR: failed to parse {data}")
            print(f"ERROR: failed to parse {data}")

    @classmethod
    def parse_fft_rawdata(cls, data):
        try:
            if isinstance(data, dict):
                d = str(data["v"])
            else:
                d = json.loads(data)
                d = d["v"]
            return d
        except Exception as ex:
            log.error(f"ERROR: failed to parse {data}")
            print(f"ERROR: failed to parse {data}")
       
    @classmethod    
    def process_fft_data(cls, data):
        if not isinstance(data, list) or len(data) < 1:
            return None
        
        try:
            item = json.loads(data[0])
            start_time = item['stime']

            item = json.loads(data[-1])
            end_time = item['etime']

            fft_list = []
            for x in data:
                val = json.loads(x)
                val = val['f']
                fft_list.append(val)
            
            return start_time, end_time, fft_list
        except Exception as ex:
            print(ex)


    @classmethod
    def clear_sensordata_lookup(cls, sensor_id):
        if sensor_id in CommonFeatures.sensordata_lookup:
            del CommonFeatures.sensordata_lookup[sensor_id]

class Axis:
    def __init__(self):
        self.x = []
        self.y = []
        self.z = []

class VibrationParam:
    def __init__(self):
        self.Fft = Axis()
        self.Rms = Axis()
        self.Velocity = Axis()
        self.Displacement = Axis()
        self.Acc = Axis()

class VsensStreamProcessor:
    def __init__(self, sensorID, equipmentID):
        self.SensorID = sensorID
        self.EquipmentID = equipmentID
        self.StreamData = VibrationParam()
        self.WindowSize = None
        self.NoOfSamples = None
        self.SamplingFrequency = None
        self.Window = 0

        self.TempStore = {}
        self.BeingProcessed = False

    def update_dataset(self):
        try:
            output = CommonFeatures.getSensorMetadata(
            self.SensorID, ['numberofsamples', 'windowsize', 'samplingfrequency'])

            if output is not None and len(output) == 3:
                self.NoOfSamples = output[0]
                self.WindowSize = output[1]
                self.SamplingFrequency = output[2]

            if self.NoOfSamples is not None:
                self.NoOfSamples = int(self.NoOfSamples[0])
            else:
                self.NoOfSamples = int(
                    CommonFeatures.main_config["default_meta_values"]["numberofsamples"])

            if self.WindowSize is not None:
                self.WindowSize = int(self.WindowSize[0])
            else:
                self.WindowSize = int(
                    CommonFeatures.main_config["default_meta_values"]["windowsize"])
            
            if self.SamplingFrequency is not None:
                self.SamplingFrequency = int(self.SamplingFrequency[0])
            else:
                self.SamplingFrequency = int(
                    CommonFeatures.main_config["default_meta_values"]["samplingfrequency"])

            # test data
            #self.NoOfSamples = 8192
            #self.WindowSize = 1024
            #self.SamplingFrequency = 6400

            self.Window = int(self.NoOfSamples/self.WindowSize)
            return 0
        except Exception as ex:
            log.error(
                f"Error while updating dataset information for Sensor: {self.SensorID}", exc_info=True)

    def axis_selection(self):
        pass

    def store_data(self, tag_type, raw_data):
        if tag_type.startswith("VELOCITY"):
            raw_data = CommonFeatures.parse_rawdata(raw_data)
            if raw_data is None:
                return

            if tag_type == "VELOCITYX":
                self.StreamData.Velocity.x.append(raw_data)
            elif tag_type == "VELOCITYY":
                self.StreamData.Velocity.y.append(raw_data)
            elif tag_type == "VELOCITYZ":
                self.StreamData.Velocity.z.append(raw_data)

        elif tag_type.startswith("FFT"):
            raw_data = CommonFeatures.parse_fft_rawdata(raw_data)
            if raw_data is None:
                return

            if tag_type == "FFTX":
                self.StreamData.Fft.x.append(raw_data)
            elif tag_type == "FFTY":
                self.StreamData.Fft.y.append(raw_data)
            elif tag_type == "FFTZ":
                self.StreamData.Fft.z.append(raw_data)
        
        elif tag_type.startswith("ACC"):
            raw_data = CommonFeatures.parse_rawdata(raw_data)
            if raw_data is None:
                return

            if tag_type == "ACCX":
                self.StreamData.Acc.x.append(raw_data)
            elif tag_type == "ACCY":
                self.StreamData.Acc.y.append(raw_data)
            elif tag_type == "ACCZ":
                self.StreamData.Acc.z.append(raw_data)

        elif tag_type.startswith("RMS"):
            raw_data = CommonFeatures.parse_rawdata(raw_data)
            if raw_data is None:
                return

            if tag_type == "RMSX":
                self.StreamData.Rms.x.append(raw_data)
            elif tag_type == "RMSY":
                self.StreamData.Rms.y.append(raw_data)
            elif tag_type == "RMSZ":
                self.StreamData.Rms.z.append(raw_data)

        else:
            return

    def check_conditions_for_algo_process(self, is_time_based=False):
        if is_time_based:
            packet = self.StreamData.Acc.x[0]
            packet = int(packet.split("$T$")[1])
            packet = int(str(packet)[:10]) #int(packet % 10000000000)
            now = int(str(time.time())[:10])
            diff = (now - packet)/60
            if diff >= 20:
                return True
            else:
                return False
        else:
            if (len(self.StreamData.Fft.x) >= self.Window and len(self.StreamData.Fft.y) >= self.Window
                    and len(self.StreamData.Fft.z) >= self.Window and len(self.StreamData.Velocity.x) >= self.Window
                    and len(self.StreamData.Velocity.y) >= self.Window and len(self.StreamData.Velocity.z) >= self.Window
                    and len(self.StreamData.Rms.x) >= self.Window
                    and len(self.StreamData.Rms.y) >= self.Window and len(self.StreamData.Rms.z) >= self.Window
                    and len(self.StreamData.Acc.x) >= self.NoOfSamples and len(self.StreamData.Acc.y) >= self.NoOfSamples
                    and len(self.StreamData.Acc.z) >= self.NoOfSamples):
                return True
            else:
                return False

    def update_temp_data(self, items):
        if items is None:
            items = ["powerOfMotor", "innerDiameterDriveEnd", "noOfTeethOnPinion", "outerDiameterDriveEnd", "maximumRPM","bearingPartDriveEnd","numberOfBallOrRollerDriveEnd","contactAngleDriveEnd"]
        
        output = CommonFeatures.getEquipmentMetaData(self.EquipmentID, items)
        
        self.TempStore["power"] = None
        self.TempStore["shaftPosition"] = None
        self.TempStore["pinionTeeth"] = None
        self.TempStore["bearingPartNo"] = None
        self.TempStore["maxRpm"] = None
        self.TempStore["numberOfBalls"] = None
        self.TempStore["innerDiameter"] = None
        self.TempStore["outerDiameter"] = None
        self.TempStore["angle"] = None
        #print(output[0][0] + " " + output[2][0] + " "+ output[4][0])

        #test purpose
        #self.TempStore["power"] = 800
        #self.TempStore["shaftPosition"] = "horizontal"
        #self.TempStore["pinionTeeth"] = 32
        #self.TempStore["bearingPartNo"] = "22410 CC/W23"
        #self.TempStore["maxRpm"] = 997

        try:
            if len(items) == len(output):            
                if output[0][0] is not None:
                    t = output[0][0].strip()
                    if len(t) > 0:
                        self.TempStore["power"] = float(t)
                
                if output[1][0] is not None:
                    t = output[1][0].strip()
                    if len(t) > 0:
                        self.TempStore["innerDiameter"] = t            
                
                if output[2][0] is not None:
                    t = output[2][0].strip()
                    if len(t) > 0:
                        self.TempStore["pinionTeeth"] = int(t)
                if output[3][0] is not None:
                    t = output[1][0].strip()
                    if len(t) > 0:
                        self.TempStore["outerDiameter"] = t   
                            
                if output[5][0] is not None:
                    t = output[5][0].strip()
                    if len(t) > 0:
                        self.TempStore["bearingPartNo"] = t
                
                if output[6][0] is not None:
                    t = output[6][0].strip()
                    if len(t) > 0:
                        self.TempStore["numberOfBalls"] = int(t)
                if output[7][0] is not None:
                    t = output[7][0].strip()
                    if len(t) > 0:
                        self.TempStore["angle"] = float(t)
                if output[4][0] is not None:
                    t = output[4][0].strip()
                    if len(t) > 0:
                        self.TempStore["maxRpm"] = int(t)
        except Exception as ex:
            print(ex)
        
    def process_burst(self):
        if self.BeingProcessed == True:
            return
        
        self.BeingProcessed = True
        try:
            self.update_temp_data(None)

            
            #   parsing velocity
            parsed_velocityX = []
            parsed_velocityY  = []        
            parsed_velocityZ = []        
            for x in self.StreamData.Velocity.x:
                val = x.split("$T$")[0]
                parsed_velocityX.append(float(val))
            avg_velocityX = np.mean(parsed_velocityX)

            for x in self.StreamData.Velocity.y:
                val = x.split("$T$")[0]
                parsed_velocityY.append(float(val))
            avg_velocityY = np.mean(parsed_velocityY)

            for x in self.StreamData.Velocity.z:
                val = x.split("$T$")[0]
                parsed_velocityZ.append(float(val))
            avg_velocityZ = np.mean(parsed_velocityZ)

            #   parsing rms
            parsed_RmsX = []
            parsed_RmsY = []
            parsed_RmsZ = []
            for x in self.StreamData.Rms.x:
                val = x.split("$T$")[0]
                parsed_RmsX.append(float(val))
            avg_RmsX = np.mean(parsed_RmsX)

            for x in self.StreamData.Rms.y:
                val = x.split("$T$")[0]
                parsed_RmsY.append(float(val))
            avg_RmsY = np.mean(parsed_RmsY)

            for x in self.StreamData.Rms.z:
                val = x.split("$T$")[0]
                parsed_RmsZ.append(float(val))
            avg_RmsZ = np.mean(parsed_RmsZ)

            # parsing accelerometer data
            parsed_accX = []
            parsed_accY = []
            parsed_accZ = []
            for x in self.StreamData.Acc.x:
                val = x.split("$T$")[0]
                if len(val) > 0:
                    parsed_accX.append(val)
            for x in self.StreamData.Acc.y:
                val = x.split("$T$")[0]
                if len(val) > 0:
                    parsed_accY.append(val)
            for x in self.StreamData.Acc.z:
                val = x.split("$T$")[0]
                if len(val) > 0:
                    parsed_accZ.append(val)

            #   parsing fft
            parsed_fftX = CommonFeatures.process_fft_data(self.StreamData.Fft.x)
            parsed_fftY = CommonFeatures.process_fft_data(self.StreamData.Fft.y)
            parsed_fftZ = CommonFeatures.process_fft_data(self.StreamData.Fft.z)

            # output [fft_average 0, rms 1, amplitude 2, frequency 3, rms_amplitude 4, rms_frequency 5]
            avg_fftX = fft_cal.parse_fft_rawdata(self.SamplingFrequency, parsed_fftX[2])
            avg_fftY = fft_cal.parse_fft_rawdata(self.SamplingFrequency, parsed_fftY[2])
            avg_fftZ = fft_cal.parse_fft_rawdata(self.SamplingFrequency, parsed_fftZ[2])

            fft_bearingX = avg_fftX[5]
            fft_bearingY = avg_fftY[5]
            fft_bearingZ = avg_fftZ[5]

            frequency_X = avg_fftX[3]
            frequency_Y = avg_fftY[3]
            frequency_Z = avg_fftZ[3]

            rms_X = avg_fftX[1]
            rms_Y = avg_fftY[1]
            rms_Z = avg_fftZ[1]

            horizontal_amp_X = avg_fftX[2]
            horizontal_amp_Y = avg_fftY[2]
            horizontal_amp_Z = avg_fftZ[2]

            fft_X = avg_fftX[0]
            fft_Y = avg_fftY[0]
            fft_Z = avg_fftZ[0]
            
            #   get the RPM
            rpm_from_vib_X = op_rpm.RpmFromVibration(self.SamplingFrequency, self.WindowSize, self.TempStore["maxRpm"],
                                                   self.SensorID, self.EquipmentID, fft_X)
            operating_rpm_X = rpm_from_vib_X.Speed_Detection()
            del rpm_from_vib_X
                        
            # machine on off
            # onOff = algo_onoff.MachineStatus(fft_X, self.SamplingFrequency, self.EquipmentID, self.SensorID)
            onOff = algo_onoff.MachineStatus(rms_X, self.SamplingFrequency, self.EquipmentID, self.SensorID)
            onOff_output = onOff.check_machine_status()
            del onOff

            if onOff_output == 0:
                print(f"{self.EquipmentID} is currently not running.")
                # self.dispose()
                # return

            # velocity severity
            severity = algo_severity.velocity_severity(
                self.TempStore["power"], avg_velocityX, self.EquipmentID, self.SensorID)
            severity_output = severity.velocity_total_check()

            if severity_output == 0:
                print(f"{self.EquipmentID}/{self.SensorID} is in Good state, skipping algorithm testing.")
                # self.dispose()
                # return
            
            # if rpm value is none, return from here
            
            # bearing
            bearing_output = []
            try:
                bearing_obj = algo_bearing.Bearing(
                    self.TempStore["numberOfBalls"], self.TempStore["innerDiameter"], self.TempStore["outerDiameter"], 
                    self.TempStore["angle"], self.TempStore["bearingPartNo"], operating_rpm_X, self.SamplingFrequency, 
                    self.NoOfSamples, self.WindowSize, self.EquipmentID, self.SensorID, fft_X, fft_Y, fft_Z,frequency_X,avg_fftX[5], avg_fftY[5], avg_fftZ[5], rms_X)
                bearing_output = bearing_obj.bearing_total_check()
                if bearing_output is None:
                    bearing_output = []
            except Exception as ex:
                print(ex)
            # finally:
                # del bearing_obj

            # gearbox
            gear_output = []
            try:
                gear_obj = algo_gearbox.Gear(operating_rpm_X,self.TempStore["pinionTeeth"], self.SamplingFrequency,
                                             self.NoOfSamples, self.WindowSize, self.EquipmentID, self.SensorID, fft_X, fft_Y, fft_Z, frequency_X,avg_fftX[5], avg_fftY[5], avg_fftZ[5], rms_X)
                gear_output = gear_obj.gmff_total_check()
                if gear_output is None:
                    gear_output = []
            except Exception as ex:
                print(ex)
            # finally:
                # del gear_obj

            # misalignment
            misalignment_output = []
            try:
                misalignment_obj = algo_misalignment.Misalignment_Analysis(
                    self.SamplingFrequency, self.NoOfSamples, self.WindowSize, operating_rpm_X, self.SensorID,
                    self.EquipmentID, fft_X, fft_Y, fft_Z, frequency_X, frequency_Y, frequency_Z)
                misalignment_output = misalignment_obj.mis_total_axis_check()
                if misalignment_output is None:
                    misalignment_output = []
            except Exception as ex:
                print(ex)
            # finally:
                # del misalignment_obj

            # looseness
            looseness_output = []
            try:
                looseness_obj = algo_looseness. Looseness_Analysis(
                    self.SamplingFrequency, self.NoOfSamples, self.WindowSize, operating_rpm_X, self.SensorID,
                    self.EquipmentID, fft_X, fft_Y, fft_Z, frequency_X, frequency_Y, frequency_Z)
                looseness_output = looseness_obj.Looseness_Total_Check()
                if looseness_output is None:
                    looseness_output = []
            except Exception as ex:
                print(ex)
            # finally:
                # del looseness_obj

            # unbalance
            unbalance_output = []
            try:
                unbalance_obj = algo_unbalance.unbalance(
                    self.SamplingFrequency, self.NoOfSamples, self.WindowSize, operating_rpm_X, self.SensorID,
                    self.EquipmentID,fft_X, fft_Y, fft_Z,rms_X)
                unbalance_output = unbalance_obj.unbalance_total_check()
                if unbalance_output is None:
                    unbalance_output = []
            except Exception as ex:
                print(ex)
            
            # finally:
            # del unbalance_obj

            temp_list = bearing_output + gear_output + misalignment_output + looseness_output + unbalance_output
            final_output = [str(x) if isinstance(x, int) else x for x in temp_list]
            # formatted_output = {}
            # formatted_output['d'] = final_output
            data = [self.EquipmentID, self.SensorID, "FO",
                    json.dumps(final_output) + "$T$" + str(time.time())]
            v_helper.helper.data_to_publish.append(data)
        except Exception as ex:
            print(ex)
        finally:
            self.dispose()

    def dispose(self):
        CommonFeatures.clear_sensordata_lookup(self.SensorID)

    def __del__(self):
        print('Object Destroyed...')
