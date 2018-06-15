#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: VR1 TX all-in-one
# Description: Single
# Generated: Fri Jun  8 10:41:31 2018
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
import psutil
import threading
import time


class vr1_tx(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "VR1 TX all-in-one")

        ##################################################
        # Variables
        ##################################################
        self.pilot_carriers = pilot_carriers = ((-27, -14, -7, 7, 14, 27),)
        self.pattern2 = pattern2 = [1, -1, 1, -1]
        self.pattern1 = pattern1 = [0., 1.41421356, 0., -1.41421356]
        self.fft_len = fft_len = 64
        self.zcpu = zcpu = psutil
        self._xmlrpcport_config = ConfigParser.ConfigParser()
        self._xmlrpcport_config.read('./default')
        try: xmlrpcport = self._xmlrpcport_config.getint("vr1_tx", "xmlrpcport")
        except: xmlrpcport = 8081
        self.xmlrpcport = xmlrpcport
        self._usrpip_config = ConfigParser.ConfigParser()
        self._usrpip_config.read('./default')
        try: usrpip = self._usrpip_config.get("usrp_hydra", "ip")
        except: usrpip = "127.0.0.1"
        self.usrpip = usrpip
        self._txport_config = ConfigParser.ConfigParser()
        self._txport_config.read('./default')
        try: txport = self._txport_config.get("vr1_tx", "port")
        except: txport = "2666"
        self.txport = txport
        self.tx_goodput = tx_goodput = 0
        self.sync_word2 = sync_word2 = [0., 0., 0., 0., 0., 0.,] + pattern2 * ((fft_len-12)/len(pattern2))  +[0., 0., 0., 0., 0., 0.,] 
        self.sync_word1 = sync_word1 = [0., 0., 0., 0., 0., 0.,] + pattern1 * ((fft_len-12)/len(pattern1))  +[0., 0., 0., 0., 0., 0.,] 
        self._samprate_config = ConfigParser.ConfigParser()
        self._samprate_config.read('./default')
        try: samprate = self._samprate_config.getfloat("usrp_hydra", "samprate1")
        except: samprate = 0
        self.samprate = samprate
        self._rxport_config = ConfigParser.ConfigParser()
        self._rxport_config.read('./default')
        try: rxport = self._rxport_config.get("usrp_hydra", "rxport1")
        except: rxport = "2666"
        self.rxport = rxport
        self.pilot_symbols = pilot_symbols = ((-1,1, 1, -1, -1, -1),)
        self.packet_len = packet_len = 100
        self.occupied_carriers = occupied_carriers = (sorted(tuple(set([x for x in range(-26,27)]) - set(pilot_carriers[0]) - set([0,]))),)
        self._ip_config = ConfigParser.ConfigParser()
        self._ip_config.read('./default')
        try: ip = self._ip_config.get("vr1_tx", "ip")
        except: ip = "127.0.0.1"
        self.ip = ip
        self.cpu_percent = cpu_percent = 0

        ##################################################
        # Blocks
        ##################################################
        self.ztxrate = blocks.probe_rate(gr.sizeof_char*1, 2000, 0.15)
        self.zeromq_push_sink_0 = zeromq.push_sink(gr.sizeof_gr_complex, 1, "tcp://" + ip + ":" + txport, 100, True, -1)
        self.xmlrpc_server_0_0 = SimpleXMLRPCServer.SimpleXMLRPCServer(('127.0.0.1', xmlrpcport), allow_none=True)
        self.xmlrpc_server_0_0.register_instance(self)
        self.xmlrpc_server_0_0_thread = threading.Thread(target=self.xmlrpc_server_0_0.serve_forever)
        self.xmlrpc_server_0_0_thread.daemon = True
        self.xmlrpc_server_0_0_thread.start()
        
        def _tx_goodput_probe():
            while True:
                val = self.ztxrate.rate()
                try:
                    self.set_tx_goodput(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _tx_goodput_thread = threading.Thread(target=_tx_goodput_probe)
        _tx_goodput_thread.daemon = True
        _tx_goodput_thread.start()
            
        self.digital_ofdm_tx_0 = digital.ofdm_tx(
        	  fft_len=fft_len, cp_len=16,
        	  packet_length_tag_key="packet_len",
        	  occupied_carriers=occupied_carriers,
        	  pilot_carriers=pilot_carriers,
        	  pilot_symbols=pilot_symbols,
        	  sync_word1=sync_word1,
        	  sync_word2=sync_word2,
        	  bps_header=1,
        	  bps_payload=1,
        	  rolloff=0,
        	  debug_log=False,
        	  scramble_bits=False
        	 )
        
        def _cpu_percent_probe():
            while True:
                val = self.zcpu.cpu_percent()
                try:
                    self.set_cpu_percent(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1))
        _cpu_percent_thread = threading.Thread(target=_cpu_percent_probe)
        _cpu_percent_thread.daemon = True
        _cpu_percent_thread.start()
            
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samprate,True)
        self.blocks_tag_debug_0_0 = blocks.tag_debug(gr.sizeof_char*1, "Tx'd Packet", ""); self.blocks_tag_debug_0_0.set_display(True)
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, packet_len, "packet_len")
        self.analog_random_source_x_0 = blocks.vector_source_b(map(int, numpy.random.randint(0, 255, 1000)), True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))    
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_tag_debug_0_0, 0))    
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_ofdm_tx_0, 0))    
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.ztxrate, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.zeromq_push_sink_0, 0))    
        self.connect((self.digital_ofdm_tx_0, 0), (self.blocks_throttle_0, 0))    

    def get_pilot_carriers(self):
        return self.pilot_carriers

    def set_pilot_carriers(self, pilot_carriers):
        self.pilot_carriers = pilot_carriers
        self.set_occupied_carriers((sorted(tuple(set([x for x in range(-26,27)]) - set(self.pilot_carriers[0]) - set([0,]))),))

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

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.set_sync_word2([0., 0., 0., 0., 0., 0.,] + self.pattern2 * ((self.fft_len-12)/len(self.pattern2))  +[0., 0., 0., 0., 0., 0.,] )
        self.set_sync_word1([0., 0., 0., 0., 0., 0.,] + self.pattern1 * ((self.fft_len-12)/len(self.pattern1))  +[0., 0., 0., 0., 0., 0.,] )

    def get_zcpu(self):
        return self.zcpu

    def set_zcpu(self, zcpu):
        self.zcpu = zcpu

    def get_xmlrpcport(self):
        return self.xmlrpcport

    def set_xmlrpcport(self, xmlrpcport):
        self.xmlrpcport = xmlrpcport

    def get_usrpip(self):
        return self.usrpip

    def set_usrpip(self, usrpip):
        self.usrpip = usrpip

    def get_txport(self):
        return self.txport

    def set_txport(self, txport):
        self.txport = txport

    def get_tx_goodput(self):
        return self.tx_goodput

    def set_tx_goodput(self, tx_goodput):
        self.tx_goodput = tx_goodput

    def get_sync_word2(self):
        return self.sync_word2

    def set_sync_word2(self, sync_word2):
        self.sync_word2 = sync_word2

    def get_sync_word1(self):
        return self.sync_word1

    def set_sync_word1(self, sync_word1):
        self.sync_word1 = sync_word1

    def get_samprate(self):
        return self.samprate

    def set_samprate(self, samprate):
        self.samprate = samprate
        self.blocks_throttle_0.set_sample_rate(self.samprate)

    def get_rxport(self):
        return self.rxport

    def set_rxport(self, rxport):
        self.rxport = rxport

    def get_pilot_symbols(self):
        return self.pilot_symbols

    def set_pilot_symbols(self, pilot_symbols):
        self.pilot_symbols = pilot_symbols

    def get_packet_len(self):
        return self.packet_len

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.packet_len)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.packet_len)

    def get_occupied_carriers(self):
        return self.occupied_carriers

    def set_occupied_carriers(self, occupied_carriers):
        self.occupied_carriers = occupied_carriers

    def get_ip(self):
        return self.ip

    def set_ip(self, ip):
        self.ip = ip

    def get_cpu_percent(self):
        return self.cpu_percent

    def set_cpu_percent(self, cpu_percent):
        self.cpu_percent = cpu_percent


def main(top_block_cls=vr1_tx, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
