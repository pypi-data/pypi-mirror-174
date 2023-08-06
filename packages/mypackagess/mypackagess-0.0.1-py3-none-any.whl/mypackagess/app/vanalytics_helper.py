__name__ = "vanalytics_helper"

#import queue
import json

from multiprocessing import Queue

class helper:
    data_to_publish = []
    # data_queue = queue.Queue(maxsize=0)
    data_queue = Queue(maxsize=0)


class BrokerInfo:

    def __init__(self, ipAddress, portNumber, userName, password, brokerName=None, qos=2):
        self.ipAddress = ipAddress
        self.portNumber = portNumber
        self.userName = userName
        self.password = password
        self.brokerName = brokerName
        self.isConnected = 0
        self.qos = qos
        self.MqttClient = None
        self.SubTopics = []

class EquipmentInfo:
    
    def __init__(self, equipmentNumber, equipmentName, equipmentClass, attachedSensors):
        self.equipmentNumber = equipmentNumber
        self.equipmentName = equipmentName
        self.equipmentClass = equipmentClass
        self.SensorInfo = attachedSensors

class SensorInfo:
    
    def __init__(self, sensorIdentifier, connectionMode, axisX, axisY, axisZ, sensorIdentifierOld, tags):
        self.sensorIdentifier = sensorIdentifier
        self.connectionMode = connectionMode
        self.axisX = axisX
        self.axisY = axisY
        self.axisZ = axisZ
        self.sensorIdentifierOld = sensorIdentifierOld
        self.Tags = tags

class Tags:
    
    def __init__(self, topicRepresents, topic, topicType, broker):
        self.topicRepresents = topicRepresents
        self.topic = topic
        self.topicType = topicType
        self.unique_id = None
        self.BrokerInfo = broker

class Entity:

    def __init__(self, unique_id, unique_name, group, description, properties):
        self.unique_id = unique_id
        self.unique_name = unique_name
        self.group = group
        self.description = description
        self.property = properties

class Property:

    def __init__(self, key, value, data_type, tag, range, unit, description):
        self.key = key
        self.value = value
        self.data_type = data_type
        self.tag = tag
        self.range = range
        self.unit = unit
        self.description = description
