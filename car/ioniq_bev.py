""" Module for the Hyundai Ioniq Electric 28kWh """
from .car import Car
from .isotp_decoder import IsoTpDecoder

b2101 = bytes.fromhex('2101')
b2102 = bytes.fromhex('2102')
b2103 = bytes.fromhex('2103')
b2104 = bytes.fromhex('2104')
b2105 = bytes.fromhex('2105')
b2180 = bytes.fromhex('2180')
b22b002 = bytes.fromhex('22b002')

Fields = (
    {'cmd': b2101, 'canrx': 0x7ec, 'cantx': 0x7e4,
     'fields': (
         {'padding': 6},                                                            # _,_,a,b,c,d
         {'name': 'SOC_BMS', 'width': 1, 'scale': .5},                              # e
         {'name': 'availableChargePower', 'width': 2, 'scale': .01},                # f,g
         {'name': 'availableDischargePower', 'width': 2, 'scale': .01},             # h,i
         {'name': 'bmsBits1', 'width': 1},                                          # j
         {'name': 'dcBatteryCurrent', 'width': 2, 'signed': True, 'scale': .1},     # k,l
         {'name': 'dcBatteryVoltage', 'width': 2, 'scale': .1},                     # m,n
         {'name': 'batteryMaxTemperature', 'width': 1, 'signed': True},             # o
         {'name': 'batteryMinTemperature', 'width': 1, 'signed': True},             # p
         {'name': 'cellTemp%02d', 'idx': 1, 'cnt': 5, 'width': 1, 'signed': True},  # q,r,s,t,u
         {'padding': 1},                                                            # v
         {'name': 'batteryInletTemperature', 'width': 1, 'signed': True},           # w
         {'name': 'maxCellVoltage', 'width': 1, 'scale': 0.02},                     # x
         {'name': 'maxCellVoltageNumber', 'width': 1},                              # y
         {'name': 'minCellVoltage', 'width': 1, 'scale': 0.02},                     # z
         {'name': 'minCellVoltageNumber', 'width': 1},                              # aa
         {'name': 'fanStatus', 'width': 1},                                         # ab
         {'name': 'fanFeedback', 'width': 1, 'scale': 100},                         # ac
         {'name': 'auxBatteryVoltage', 'width': 1, 'scale': .1},                    # ad
         {'name': 'cumulativeChargeCurrent', 'width': 4, 'scale': .1},              # ae,af,ag,ah
         {'name': 'cumulativeDischargeCurrent', 'width': 4, 'scale': .1},           # ai,aj,ak,al
         {'name': 'cumulativeEnergyCharged', 'width': 4, 'scale': .1},              # am,an,ao,ap
         {'name': 'cumulativeEnergyDischarged', 'width': 4, 'scale': .1},           # aq,ar,as,at
         {'name': 'operatingSeconds', 'width': 4},                                  # au,av,aw,ax
         {'name': 'bmsBits2', 'width': 1},                                          # ay
         {'name': 'inverterCapacitorVoltage', 'width': 2},                          # az,ba
         {'name': 'driveMotorSpeed1', 'width': 2, 'signed': True},                  # bb,bc
         {'name': 'driveMotorSpeed2', 'width': 2, 'signed': True},                  # bd,be
         {'name': 'isolationResistance', 'width': 2},                               # bf,bg
         # Len: 61
     )
     },
    {'cmd': b2102, 'canrx': 0x7ec, 'cantx': 0x7e4,
     'fields': (
         {'padding': 6},
         {'name': 'cellVoltage%02d', 'idx': 1, 'cnt': 32, 'width': 1, 'scale': .02},
         # Len: 38
     )
     },
    {'cmd': b2103, 'canrx': 0x7ec, 'cantx': 0x7e4,
     'fields': (
         {'padding': 6},
         {'name': 'cellVoltage%02d', 'idx': 33, 'cnt': 32, 'width': 1, 'scale': .02},
         # Len: 38
     )
     },
    {'cmd': b2104, 'canrx': 0x7ec, 'cantx': 0x7e4,
     'fields': (
         {'padding': 6},
         {'name': 'cellVoltage%02d', 'idx': 65, 'cnt': 32, 'width': 1, 'scale': .02},
         # Len: 38
     )
     },
    {'cmd': b2105, 'canrx': 0x7ec, 'cantx': 0x7e4,
     'fields': (
         {'padding': 11},                                               # _,_,a,b,c,d,e,f,g,h,i
         {'name': 'cellTemp%02d', 'idx': 6, 'cnt': 7, 'width': 1, 'signed': True},  # j,k,l,m,n,o,p
         {'padding': 4},                                                        # q,r,s,t
         {'name': 'cellVoltageDeviation', 'width': 1, 'scale': 0.02},           # u
         {'padding': 1},                                                        # v
         {'name': 'airbagWireDuty', 'width': 1},                                # w
         {'name': 'batteryHeater1Temperature', 'width': 1, 'signed': True},     # x
         {'name': 'batteryHeater2Temperature', 'width': 1, 'signed': True},     # y
         {'name': 'soh', 'width': 2, 'scale': .1},                              # z,aa
         {'name': 'maxCellDeteriorationNo', 'width': 1},                        # ab
         {'name': 'minCellDeterioration', 'width': 2, 'scale': 0.1},            # ac,ad
         {'name': 'minCellDeteriorationNo', 'width': 1},                        # ae
         {'name': 'SOC_DISPLAY', 'width': 1, 'scale': .5},                      # af
         {'padding': 11},                                       # ag,ah,ai,aj,ak,al,am,an,ao,ap,aq
         # Len: 45
     )
     },
    {'cmd': b2180, 'canrx': 0x7ee, 'cantx': 0x7e6,
     'fields': (
         {'padding': 14},
         {'name': 'externalTemperature', 'width': 1, 'scale': .5, 'offset': -40},   # m
         {'padding': 10},
         # Len: 25
     )
     },
    {'cmd': b22b002, 'canrx': 0x7ce, 'cantx': 0x7c6, 'optional': True,
     'fields': (
         {'padding': 9},                # _,_,a,b,c,d,e,f
         {'name': 'odo', 'width': 3},   # g,h,i
         {'padding': 3},                # j,k,l
         # Len: 15
     )
     },
    {'computed': True,
     'fields': (
         {'name': 'dcBatteryPower',
          'lambda': lambda d: d['dcBatteryCurrent'] * d['dcBatteryVoltage'] / 1000.0},
         {'name': 'charging',
          'lambda': lambda d: int(d['bmsBits1'] & 0x80 != 0)},
         {'name': 'normalChargePort',
          'lambda': lambda d: int(d['bmsBits1'] & 0x20 != 0)},
         {'name': 'rapidChargePort',
          'lambda': lambda d: int(d['bmsBits1'] & 0x40 != 0)},
     )
     },
)


class IoniqBev(Car):
    """ Class for Ioniq Electric """

    def __init__(self, config, dongle, watchdog, gps):
        Car.__init__(self, config, dongle, watchdog, gps)
        self._dongle.set_protocol('CAN_11_500')
        self._isotp = IsoTpDecoder(self._dongle, Fields)

    def read_dongle(self, data):
        """ Fetch data from CAN-bus and decode it.
            "data" needs to be a dictionary that will
            be modified with decoded data """

        data.update(self.get_base_data())
        data.update(self._isotp.get_data())

    def get_base_data(self):
        return {
            "CAPACITY": 28,
            "SLOW_SPEED": 2.3,
            "NORMAL_SPEED": 4.6,
            "FAST_SPEED": 50.0
        }

    def get_abrp_model(self):
        return 'hyundai:ioniq:17:28:other'

    def get_evn_model(self):
        return 'IONIQ_BEV'
