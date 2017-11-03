#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Split 1
# Description: Split1
# Generated: Thu Nov  2 15:09:00 2017
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import zeromq
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import ConfigParser
import SimpleXMLRPCServer
import numpy
import threading
import time


class split1(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Split 1")

        ##################################################
        # Variables
        ##################################################
        self.pilot_carriers = pilot_carriers = ((-42, -14, -7, 7, 14, 42),)
        self.pattern2 = pattern2 = [1, -1, 1, -1]
        self.pattern1 = pattern1 = [0., 1.41421356, 0., -1.41421356]
        self.occupied_carriers = occupied_carriers = (sorted(tuple(set([x for x in range(-26, 27)]) - set(pilot_carriers[0]) - set([0,]))),)
        self.fft_len = fft_len = 128
        self._xmlrpcport_config = ConfigParser.ConfigParser()
        self._xmlrpcport_config.read('default')
        try: xmlrpcport = self._xmlrpcport_config.getint("split1", "xmlrpcport")
        except: xmlrpcport = 8080
        self.xmlrpcport = xmlrpcport
        self._usrpport_config = ConfigParser.ConfigParser()
        self._usrpport_config.read('default')
        try: usrpport = self._usrpport_config.get("usrp", "rxoutport")
        except: usrpport = "2101"
        self.usrpport = usrpport
        self._usrpip_config = ConfigParser.ConfigParser()
        self._usrpip_config.read('default')
        try: usrpip = self._usrpip_config.get("usrp", "ip")
        except: usrpip = "127.0.0.1"
        self.usrpip = usrpip
        self._timeout_config = ConfigParser.ConfigParser()
        self._timeout_config.read('default')
        try: timeout = self._timeout_config.getint("global", "zmqtimeout")
        except: timeout = 100
        self.timeout = timeout
        self._throttle_config = ConfigParser.ConfigParser()
        self._throttle_config.read('default')
        try: throttle = self._throttle_config.getint("split1", "throttle")
        except: throttle = int(100e3)
        self.throttle = throttle
        self.sync_word2 = sync_word2 = [0., 0., 0., 0., 0., 0.,] + pattern2 * ((fft_len-12)/len(pattern2))  +[0., 0., 0., 0., 0., 0.,] 
        self.sync_word1 = sync_word1 = [0., 0., 0., 0., 0., 0.,] + pattern1 * ((fft_len-12)/len(pattern1))  +[0., 0., 0., 0., 0., 0.,] 
        self.rate1 = rate1 = 0
        self.rate0 = rate0 = 0
        self.pilot_symbols = pilot_symbols = ((-1,1, 1, -1, -1, -1),)
        self._payloadport_config = ConfigParser.ConfigParser()
        self._payloadport_config.read('default')
        try: payloadport = self._payloadport_config.get("split1", "payloadport")
        except: payloadport = "2101"
        self.payloadport = payloadport
        self.payload_mod = payload_mod = digital.constellation_bpsk()
        self._maxnoutput_config = ConfigParser.ConfigParser()
        self._maxnoutput_config.read('default')
        try: maxnoutput = self._maxnoutput_config.getint("global", "maxnoutput")
        except: maxnoutput = 100
        self.maxnoutput = maxnoutput
        self._ip_config = ConfigParser.ConfigParser()
        self._ip_config.read('default')
        try: ip = self._ip_config.get("split1", "ip")
        except: ip = "127.0.0.1"
        self.ip = ip
        self._headerport_config = ConfigParser.ConfigParser()
        self._headerport_config.read('default')
        try: headerport = self._headerport_config.get("split1", "headerport")
        except: headerport = "2100"
        self.headerport = headerport
        self.header_mod = header_mod = digital.constellation_bpsk()
        self.hdr_format = hdr_format = digital.header_format_ofdm(occupied_carriers, 1, "packet_len",)

        ##################################################
        # Blocks
        ##################################################
        self.probe1_1 = blocks.probe_rate(gr.sizeof_char*1, 500.0, 0.15)
        self.probe1_0 = blocks.probe_rate(gr.sizeof_char*1, 500.0, 0.15)
        self.zeromq_push_sink_1 = zeromq.push_sink(gr.sizeof_char, 1, "tcp://" + ip + ":" + payloadport, timeout, True, -1)
        self.zeromq_push_sink_0 = zeromq.push_sink(gr.sizeof_char, 1, "tcp://" + ip + ":" + headerport, timeout, True, -1)
        self.xmlrpc_server_0 = SimpleXMLRPCServer.SimpleXMLRPCServer((ip, xmlrpcport), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        
        def _rate1_probe():
            while True:
                val = self.probe1_1.rate()
                try:
                    self.set_rate1(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _rate1_thread = threading.Thread(target=_rate1_probe)
        _rate1_thread.daemon = True
        _rate1_thread.start()
            
        
        def _rate0_probe():
            while True:
                val = self.probe1_0.rate()
                try:
                    self.set_rate0(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _rate0_thread = threading.Thread(target=_rate0_probe)
        _rate0_thread.daemon = True
        _rate0_thread.start()
            
        self.digital_protocol_formatter_bb_0 = digital.protocol_formatter_bb(hdr_format, "packet_len")
        self.digital_crc32_bb_0 = digital.crc32_bb(False, "packet_len", True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, 10e3,True)
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 100, "packet_len")
        self.blocks_repack_bits_bb_0_0 = blocks.repack_bits_bb(8, 1, "packet_len", False, gr.GR_LSB_FIRST)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(8, payload_mod.bits_per_symbol(), "packet_len", False, gr.GR_LSB_FIRST)
        self.analog_random_source_x_0 = blocks.vector_source_b(map(int, numpy.random.randint(0, 2, 1000)), True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.probe1_1, 0))    
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.zeromq_push_sink_1, 0))    
        self.connect((self.blocks_repack_bits_bb_0_0, 0), (self.probe1_0, 0))    
        self.connect((self.blocks_repack_bits_bb_0_0, 0), (self.zeromq_push_sink_0, 0))    
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_crc32_bb_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))    
        self.connect((self.digital_crc32_bb_0, 0), (self.blocks_repack_bits_bb_0, 0))    
        self.connect((self.digital_crc32_bb_0, 0), (self.digital_protocol_formatter_bb_0, 0))    
        self.connect((self.digital_protocol_formatter_bb_0, 0), (self.blocks_repack_bits_bb_0_0, 0))    

    def get_pilot_carriers(self):
        return self.pilot_carriers

    def set_pilot_carriers(self, pilot_carriers):
        self.pilot_carriers = pilot_carriers
        self.set_occupied_carriers((sorted(tuple(set([x for x in range(-26, 27)]) - set(self.pilot_carriers[0]) - set([0,]))),))

    def get_pattern2(self):
        return self.pattern2

    def set_pattern2(self, pattern2):
        self.pattern2 = pattern2
        self.set_sync_word2([0., 0., 0., 0., 0., 0.,] + self.pattern2 * ((self.fft_len-12)/len(self.pattern2))  +[0., 0., 0., 0., 0., 0.,] )

    def get_pattern1(self):
        return self.pattern1

    def set_pattern1(self, pattern1):
        self.pattern1 = pattern1
        self.set_sync_word1([0., 0., 0., 0., 0., 0.,] + self.pattern1 * ((self.fft_len-12)/len(self.pattern1))  +[0., 0., 0., 0., 0., 0.,] )

    def get_occupied_carriers(self):
        return self.occupied_carriers

    def set_occupied_carriers(self, occupied_carriers):
        self.occupied_carriers = occupied_carriers
        self.set_hdr_format(digital.header_format_ofdm(self.occupied_carriers, 1, "packet_len",))

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.set_sync_word2([0., 0., 0., 0., 0., 0.,] + self.pattern2 * ((self.fft_len-12)/len(self.pattern2))  +[0., 0., 0., 0., 0., 0.,] )
        self.set_sync_word1([0., 0., 0., 0., 0., 0.,] + self.pattern1 * ((self.fft_len-12)/len(self.pattern1))  +[0., 0., 0., 0., 0., 0.,] )

    def get_xmlrpcport(self):
        return self.xmlrpcport

    def set_xmlrpcport(self, xmlrpcport):
        self.xmlrpcport = xmlrpcport

    def get_usrpport(self):
        return self.usrpport

    def set_usrpport(self, usrpport):
        self.usrpport = usrpport

    def get_usrpip(self):
        return self.usrpip

    def set_usrpip(self, usrpip):
        self.usrpip = usrpip

    def get_timeout(self):
        return self.timeout

    def set_timeout(self, timeout):
        self.timeout = timeout

    def get_throttle(self):
        return self.throttle

    def set_throttle(self, throttle):
        self.throttle = throttle

    def get_sync_word2(self):
        return self.sync_word2

    def set_sync_word2(self, sync_word2):
        self.sync_word2 = sync_word2

    def get_sync_word1(self):
        return self.sync_word1

    def set_sync_word1(self, sync_word1):
        self.sync_word1 = sync_word1

    def get_rate1(self):
        return self.rate1

    def set_rate1(self, rate1):
        self.rate1 = rate1

    def get_rate0(self):
        return self.rate0

    def set_rate0(self, rate0):
        self.rate0 = rate0

    def get_pilot_symbols(self):
        return self.pilot_symbols

    def set_pilot_symbols(self, pilot_symbols):
        self.pilot_symbols = pilot_symbols

    def get_payloadport(self):
        return self.payloadport

    def set_payloadport(self, payloadport):
        self.payloadport = payloadport

    def get_payload_mod(self):
        return self.payload_mod

    def set_payload_mod(self, payload_mod):
        self.payload_mod = payload_mod

    def get_maxnoutput(self):
        return self.maxnoutput

    def set_maxnoutput(self, maxnoutput):
        self.maxnoutput = maxnoutput

    def get_ip(self):
        return self.ip

    def set_ip(self, ip):
        self.ip = ip

    def get_headerport(self):
        return self.headerport

    def set_headerport(self, headerport):
        self.headerport = headerport

    def get_header_mod(self):
        return self.header_mod

    def set_header_mod(self, header_mod):
        self.header_mod = header_mod

    def get_hdr_format(self):
        return self.hdr_format

    def set_hdr_format(self, hdr_format):
        self.hdr_format = hdr_format


def main(top_block_cls=split1, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
