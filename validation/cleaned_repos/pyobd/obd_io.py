import decimal
import re
import string
import time
from math import ceil
from pdb import set_trace as bp

import obd
import obd_sensors
import serial
import wx  # due to debugEvent messaging
from obd_sensors import hex_to_int


def truncate(num, n):
    integer = int(num * (10**n)) / (10**n)
    return float(integer)


GET_DTC_COMMAND = "03"
CLEAR_DTC_COMMAND = "04"
GET_FREEZE_DTC_COMMAND = "07"
import logging
import traceback

from debugEvent import *

logger = logging.getLogger(__name__)


class OBDConnection:
    def __init__(self, portnum, _notify_window, baud, SERTIMEOUT, RECONNATTEMPTS, FAST):
        self._notify_window = _notify_window
        if baud == "AUTO":
            baud = None
        if portnum == "AUTO":
            portnum = None
        if FAST == "FAST":
            FAST = True
        else:
            FAST = False

        counter = 0
        while counter < RECONNATTEMPTS:
            counter = counter + 1
            wx.PostEvent(
                self._notify_window,
                DebugEvent([2, "Connection attempt:" + str(counter)]),
            )
            try:
                self.connection.close()
            except:
                pass
            self.connection = obd.OBD(
                portstr=portnum,
                baudrate=baud,
                fast=FAST,
                timeout=truncate(float(SERTIMEOUT), 1),
            )
            if self.connection.status() == "Car Connected":
                wx.PostEvent(
                    self._notify_window,
                    DebugEvent(
                        [2, "Connected to: " + str(self.connection.port_name())]
                    ),
                )
                break
            else:
                self.connection.close()
            time.sleep(1)

    def close(self):
        """Resets device and closes all associated filehandles"""
        self.connection.close()
        self.ELMver = "Unknown"

    def sensor(self, sensor_index):
        """Returns 3-tuple of given sensors. 3-tuple consists of
        (Sensor Name (string), Sensor Value (string), Sensor Unit (string) )"""
        ###for command in self.connection.supported_commands[1].name
        pass
        # sensor = obd_sensors.SENSORS[sensor_index]
        # r = self.get_sensor_value(sensor)
        # return (sensor.name,r, sensor.unit)

    def clear_dtc(self):
        """Clears all DTCs and freeze frame data"""
        # self.send_command(CLEAR_DTC_COMMAND)
        # r = self.get_result()
        r = self.connection.query(obd.commands["CLEAR_DTC"])
        return r

    def log(self, sensor_index, filename):
        file = open(filename, "w")
        start_time = time.time()
        if file:
            data = self.sensor(sensor_index)
            file.write("%s     \t%s(%s)\n" % ("Time", string.strip(data[0]), data[2]))
            while 1:
                now = time.time()
                data = self.sensor(sensor_index)
                line = "%.6f,\t%s\n" % (now - start_time, data[1])
                file.write(line)
                file.flush()
