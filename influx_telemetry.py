#!/usr/bin/env python3

import threading
import influxdb
import pyrfc3339
from datetime import datetime, timezone
from time import time
from threading import Timer, Lock
import logging
from math import isnan

class InfluxTelemetry:
    def __init__(self, config, car, gps, evnotify):
        self.log = logging.getLogger("EVNotiPi/InfluxDB")
        self.log.info("Initializing InfluxDB")

        self.evn_akey = evnotify.config['akey']
        self.car = car
        self.cartype = car.getEVNModel()
        self.gps = gps
        self.poll_interval = config['interval']
        self.running = False
        self.timer = None
        self.watchdog = time()
        self.watchdog_timeout = self.poll_interval * 10

        try:
            Influx = influxdb.InfluxDBClient(config['host'], config['port'],
                    config['user'], config['pass'], config['dbname'],
                    retries=1, timeout=1)

        except influxdb.exceptions.InfluxDBClientError as e:
            self.log.error(e)
            Influx = None
        except influxdb.exceptions.InfluxDBServerError as e:
            self.log.error(e)
            Influx = None

        self.influx = Influx
        self.data_queue = []

    def start(self):
        if self.influx:
            self.running = True
            self.timer = Timer(0, self.submitData)
            self.timer.start()

    def stop(self):
        if self.running:
            self.timer.cancel()
        self.running = False

    def submitData(self):
        if not self.running: return

        now = time()
        self.watchdog = now

        data = self.car.getData()
        if data and 'timestamp' in data:
            tags = {
                    "cartype": self.cartype,
                    "akey": self.evn_akey,
                    }

            fields = {}
            if 'SOC_DISPLAY' in data:
                fields.update({
                    'SOC_DISPLAY': data['SOC_DISPLAY'],
                    })
            if 'SOC_BMS' in data:
                fields.update({
                    'SOC_BMS': data['SOC_BMS'],
                    })

            if 'EXTENDED' in data:
                fields.update(data['EXTENDED'])
            if 'ADDITIONAL' in data:
                fields.update(data['ADDITIONAL'])

            fix = self.gps.fix()
            if fix and fix.mode > 1:
                fields.update({
                        'latitude':  float(fix.latitude),
                        'longitude': float(fix.longitude),
                        'gdop':      float(fix.gdop),
                        'pdop':      float(fix.pdop),
                        'hdop':      float(fix.hdop),
                        'vdop':      float(fix.vdop),
                        'distance':  float(fix.distance),
                        })
                if not isnan(fix.speed):
                    fields.update({
                        'speed':     float(fix.speed),
                        })
                if fix.mode > 2:
                    fields.update({
                        'altitude':  float(fix.altitude),
                        })
                if fix.device:
                    tags.update({
                        'gps_device': fix.device
                        })

            self.submit(measurement="telemetry", time=data['timestamp'],
                    fields=fields, tags=tags)

        # Prime next loop iteration
        if self.running:
            runtime = time() - now
            interval = self.poll_interval - (runtime if runtime > self.poll_interval else 0)
            self.timer = Timer(interval, self.submitData)
            self.timer.start()


    def submit(self, measurement, time, tags, fields):
        self.data_queue.append({
            "measurement": measurement,
            "time": pyrfc3339.generate(datetime.fromtimestamp(time, timezone.utc)),
            "tags": tags,
            "fields": {**fields, 'data_queue_len': len(self.data_queue)}
            })

        try:
            self.influx.write_points(self.data_queue)
            self.data_queue = []
        except influxdb.exceptions.InfluxDBClientError as e:
            self.log.error("InfluxDBClientError qlen({}): code({}) content({}) last_data({})".format(len(self.data_queue), str(e.code), str(e.content), self.data_queue[-1]))
            if e.code == 400:
                self.data_queue = []
        except Exception as e:
            self.log.error("InfluxTelemetry len({}): {}".format(len(self.data_queue), str(e)))


    def checkWatchdog(self):
        return (time() - self.watchdog) <= self.watchdog_timeout