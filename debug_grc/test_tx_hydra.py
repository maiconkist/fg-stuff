#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: OFDM Tx
# Description: Example of an OFDM Transmitter
# Generated: Tue Oct 17 10:07:03 2017
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import ConfigParser
import SimpleXMLRPCServer
import hydra
import numpy
import threading
import time


class test_tx_hydra(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "OFDM Tx")

        ##################################################
        # Variables
        ##################################################
        self.pilot_carriers = pilot_carriers = ((-42, -14, -7, 7, 14, 42),)
        self.pattern2 = pattern2 = [1, -1, 1, -1]
        self.pattern1 = pattern1 = [0., 1.41421356, 0., -1.41421356]
        self.fft_len = fft_len = 128
        self._xmlrpcport_config = ConfigParser.ConfigParser()
        self._xmlrpcport_config.read('./default')
        try: xmlrpcport = self._xmlrpcport_config.getint("usrp_hydra", "xmlrpcport")
        except: xmlrpcport = 8084
        self.xmlrpcport = xmlrpcport
        self.sync_word2 = sync_word2 = [0., 0., 0., 0., 0., 0.,] + pattern2 * ((fft_len-12)/len(pattern2))  +[0., 0., 0., 0., 0., 0.,] 
        self.sync_word1 = sync_word1 = [0., 0., 0., 0., 0., 0.,] + pattern1 * ((fft_len-12)/len(pattern1))  +[0., 0., 0., 0., 0., 0.,] 
        self._samprate2_config = ConfigParser.ConfigParser()
        self._samprate2_config.read('./default')
        try: samprate2 = self._samprate2_config.getfloat("usrp_hydra", "samprate2")
        except: samprate2 = 1e6
        self.samprate2 = samprate2
        self._samprate1_config = ConfigParser.ConfigParser()
        self._samprate1_config.read('./default')
        try: samprate1 = self._samprate1_config.getfloat("usrp_hydra", "samprate1")
        except: samprate1 = 1e6
        self.samprate1 = samprate1
        self._samprate_config = ConfigParser.ConfigParser()
        self._samprate_config.read('./default')
        try: samprate = self._samprate_config.getfloat("usrp_hydra", "samprate")
        except: samprate = 4e6
        self.samprate = samprate
        self.rolloff = rolloff = 0
        self.pilot_symbols = pilot_symbols = ((-1,1, 1, -1, -1, -1),)
        self.packet_len = packet_len = 100
        self.occupied_carriers = occupied_carriers = (sorted(tuple(set([x for x in range(-26,27)]) - set(pilot_carriers[0]) - set([0,]))),)
        self.length_tag_key = length_tag_key = "packet_len"
        self._ip_config = ConfigParser.ConfigParser()
        self._ip_config.read('./default')
        try: ip = self._ip_config.get("usrp_hydra", "ip")
        except: ip = 'localhost'
        self.ip = ip
        self._freq2_config = ConfigParser.ConfigParser()
        self._freq2_config.read('./default')
        try: freq2 = self._freq2_config.getfloat("usrp_hydra", "txfreq2")
        except: freq2 = 950.4e6
        self.freq2 = freq2
        self._freq1_config = ConfigParser.ConfigParser()
        self._freq1_config.read('./default')
        try: freq1 = self._freq1_config.getfloat("usrp_hydra", "txfreq1")
        except: freq1 = 948.6e6
        self.freq1 = freq1
        self._freq_config = ConfigParser.ConfigParser()
        self._freq_config.read('./default')
        try: freq = self._freq_config.getfloat("usrp_hydra", "freq")
        except: freq = 950e6
        self.freq = freq
        self._amplitude2_config = ConfigParser.ConfigParser()
        self._amplitude2_config.read('./default')
        try: amplitude2 = self._amplitude2_config.getfloat("usrp_hydra", "amplitude2")
        except: amplitude2 = 0.1
        self.amplitude2 = amplitude2
        self._amplitude1_config = ConfigParser.ConfigParser()
        self._amplitude1_config.read('./default')
        try: amplitude1 = self._amplitude1_config.getfloat("usrp_hydra", "amplitude1")
        except: amplitude1 = 0.1
        self.amplitude1 = amplitude1

        ##################################################
        # Blocks
        ##################################################
        self.xmlrpc_server_0 = SimpleXMLRPCServer.SimpleXMLRPCServer((ip, 8084), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        self.uhd_usrp_sink_1 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_1.set_samp_rate(samprate)
        self.uhd_usrp_sink_1.set_center_freq(freq, 0)
        self.uhd_usrp_sink_1.set_normalized_gain(1, 0)
        self.uhd_usrp_sink_1.set_antenna('TX/RX', 0)
        self.hydra_hydra_sink_0 = hydra.hydra_sink(2, 1024, freq, samprate,
        	 ((freq1, samprate1), 
        	 (freq2, samprate2),
        	 ))
          
        self.digital_ofdm_tx_0_1 = digital.ofdm_tx(
        	  fft_len=64, cp_len=16,
        	  packet_length_tag_key=length_tag_key,
        	  occupied_carriers=(sorted(tuple(set([x for x in range(-26,26)]) - set(pilot_carriers[0]) - set([0,]))),),
        	  pilot_carriers=pilot_carriers,
        	  pilot_symbols=pilot_symbols,
        	  sync_word1=[0., 0., 0., 0., 0., 0.,] + pattern1 * ((64-12)/len(pattern1))  +[0., 0., 0., 0., 0., 0.,] ,
        	  sync_word2=[0., 0., 0., 0., 0., 0.,] + pattern2 * ((64-12)/len(pattern2))  +[0., 0., 0., 0., 0., 0.,] ,
        	  bps_header=1,
        	  bps_payload=1,
        	  rolloff=0,
        	  debug_log=False,
        	  scramble_bits=False
        	 )
        self.digital_ofdm_tx_0 = digital.ofdm_tx(
        	  fft_len=128, cp_len=16,
        	  packet_length_tag_key=length_tag_key,
        	  occupied_carriers=(sorted(tuple(set([x for x in range(-60,60)]) - set(pilot_carriers[0]) - set([0,]))),),
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
        self.blocks_stream_to_tagged_stream_0_1 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, packet_len/2, length_tag_key)
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, packet_len, length_tag_key)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vcc((amplitude2, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((amplitude1, ))
        self.analog_random_source_x_0_1 = blocks.vector_source_b(map(int, numpy.random.randint(5, 10, 1000)), True)
        self.analog_random_source_x_0 = blocks.vector_source_b(map(int, numpy.random.randint(0, 5, 1000)), True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))    
        self.connect((self.analog_random_source_x_0_1, 0), (self.blocks_stream_to_tagged_stream_0_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.hydra_hydra_sink_0, 1))    
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.hydra_hydra_sink_0, 0))    
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_ofdm_tx_0, 0))    
        self.connect((self.blocks_stream_to_tagged_stream_0_1, 0), (self.digital_ofdm_tx_0_1, 0))    
        self.connect((self.digital_ofdm_tx_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.digital_ofdm_tx_0_1, 0), (self.blocks_multiply_const_vxx_0_0, 0))    
        self.connect((self.hydra_hydra_sink_0, 0), (self.uhd_usrp_sink_1, 0))    

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

    def get_xmlrpcport(self):
        return self.xmlrpcport

    def set_xmlrpcport(self, xmlrpcport):
        self.xmlrpcport = xmlrpcport

    def get_sync_word2(self):
        return self.sync_word2

    def set_sync_word2(self, sync_word2):
        self.sync_word2 = sync_word2

    def get_sync_word1(self):
        return self.sync_word1

    def set_sync_word1(self, sync_word1):
        self.sync_word1 = sync_word1

    def get_samprate2(self):
        return self.samprate2

    def set_samprate2(self, samprate2):
        self.samprate2 = samprate2

    def get_samprate1(self):
        return self.samprate1

    def set_samprate1(self, samprate1):
        self.samprate1 = samprate1

    def get_samprate(self):
        return self.samprate

    def set_samprate(self, samprate):
        self.samprate = samprate
        self.uhd_usrp_sink_1.set_samp_rate(self.samprate)

    def get_rolloff(self):
        return self.rolloff

    def set_rolloff(self, rolloff):
        self.rolloff = rolloff

    def get_pilot_symbols(self):
        return self.pilot_symbols

    def set_pilot_symbols(self, pilot_symbols):
        self.pilot_symbols = pilot_symbols

    def get_packet_len(self):
        return self.packet_len

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len
        self.blocks_stream_to_tagged_stream_0_1.set_packet_len(self.packet_len/2)
        self.blocks_stream_to_tagged_stream_0_1.set_packet_len_pmt(self.packet_len/2)
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.packet_len)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.packet_len)

    def get_occupied_carriers(self):
        return self.occupied_carriers

    def set_occupied_carriers(self, occupied_carriers):
        self.occupied_carriers = occupied_carriers

    def get_length_tag_key(self):
        return self.length_tag_key

    def set_length_tag_key(self, length_tag_key):
        self.length_tag_key = length_tag_key

    def get_ip(self):
        return self.ip

    def set_ip(self, ip):
        self.ip = ip

    def get_freq2(self):
        return self.freq2

    def set_freq2(self, freq2):
        self.freq2 = freq2
        self.hydra_hydra_sink_0.set_central_frequency(1, self.freq2)

    def get_freq1(self):
        return self.freq1

    def set_freq1(self, freq1):
        self.freq1 = freq1
        self.hydra_hydra_sink_0.set_central_frequency(0, self.freq1)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_sink_1.set_center_freq(self.freq, 0)

    def get_amplitude2(self):
        return self.amplitude2

    def set_amplitude2(self, amplitude2):
        self.amplitude2 = amplitude2
        self.blocks_multiply_const_vxx_0_0.set_k((self.amplitude2, ))

    def get_amplitude1(self):
        return self.amplitude1

    def set_amplitude1(self, amplitude1):
        self.amplitude1 = amplitude1
        self.blocks_multiply_const_vxx_0.set_k((self.amplitude1, ))


def main(top_block_cls=test_tx_hydra, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
