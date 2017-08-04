#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Split 3
# Description: Split3
# Generated: Fri Aug  4 16:53:00 2017
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio import zeromq
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import ConfigParser
import SimpleXMLRPCServer
import threading
import time


class Split3(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Split 3")

        ##################################################
        # Variables
        ##################################################
        self.occupied_carriers = occupied_carriers = (range(-26, -21) + range(-20, -7) + range(-6, 0) + range(1, 7) + range(8, 21) + range(22, 27),)
        self.length_tag_key = length_tag_key = "packet_len"
        self._timedomainport_config = ConfigParser.ConfigParser()
        self._timedomainport_config.read('default')
        try: timedomainport = self._timedomainport_config.get("split3", "timedomainport")
        except: timedomainport = "2300"
        self.timedomainport = timedomainport
        self.tag_rate = tag_rate = 0
        self.sync_word2 = sync_word2 = [0, 0, 0, 0, 0, 0, -1, -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 0, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 0, 0, 0, 0, 0] 
        self.sync_word1 = sync_word1 = [0., 0., 0., 0., 0., 0., 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 0., 0., 0., 0., 0.]
        self.symbol_rate = symbol_rate = 0
        self._split3ip_config = ConfigParser.ConfigParser()
        self._split3ip_config.read('default')
        try: split3ip = self._split3ip_config.get("split3", "ip")
        except: split3ip = "127.0.0.1"
        self.split3ip = split3ip
        self.split3 = split3 = 0
        self._split2ip_config = ConfigParser.ConfigParser()
        self._split2ip_config.read('default')
        try: split2ip = self._split2ip_config.get("split2", "ip")
        except: split2ip = "127.0.0.1"
        self.split2ip = split2ip
        self.samp_rate = samp_rate = 100000
        self.rolloff = rolloff = 0
        self._preofdmport_config = ConfigParser.ConfigParser()
        self._preofdmport_config.read('default')
        try: preofdmport = self._preofdmport_config.get("split2", "preofdmport")
        except: preofdmport = "2200"
        self.preofdmport = preofdmport
        self.pilot_symbols = pilot_symbols = ((1, 1, 1, -1,),)
        self.pilot_carriers = pilot_carriers = ((-21, -7, 7, 21,),)
        self.payload_mod = payload_mod = digital.constellation_qpsk()
        self.packet_len = packet_len = 96
        self.header_mod = header_mod = digital.constellation_bpsk()
        self.hdr_format = hdr_format = digital.header_format_ofdm(occupied_carriers, 1, length_tag_key,)
        self.fft_len = fft_len = 64

        ##################################################
        # Blocks
        ##################################################
        self.probe3 = blocks.probe_rate(gr.sizeof_gr_complex*1, 500.0, 0.15)
        self.zeromq_push_sink_0 = zeromq.push_sink(gr.sizeof_gr_complex, 1, "tcp://" + split3ip + ":" + timedomainport, 100, True, -1)
        self.zeromq_pull_source_0 = zeromq.pull_source(gr.sizeof_gr_complex, 1, "tcp://" + split2ip + ":" + preofdmport, 100, True, -1)
        self.xmlrpc_server_0 = SimpleXMLRPCServer.SimpleXMLRPCServer(('localhost', 8080), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        
        def _tag_rate_probe():
            while True:
                val = self.tagger.rate()
                try:
                    self.set_tag_rate(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _tag_rate_thread = threading.Thread(target=_tag_rate_probe)
        _tag_rate_thread.daemon = True
        _tag_rate_thread.start()
            
        
        def _symbol_rate_probe():
            while True:
                val = self.symbolr.rate()
                try:
                    self.set_symbol_rate(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _symbol_rate_thread = threading.Thread(target=_symbol_rate_probe)
        _symbol_rate_thread.daemon = True
        _symbol_rate_thread.start()
            
        
        def _split3_probe():
            while True:
                val = self.probe3.rate()
                try:
                    self.set_split3(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _split3_thread = threading.Thread(target=_split3_probe)
        _split3_thread.daemon = True
        _split3_thread.start()
            
        self.fft_vxx_0 = fft.fft_vcc(fft_len, False, (()), True, 1)
        self.digital_ofdm_cyclic_prefixer_0 = digital.ofdm_cyclic_prefixer(fft_len, fft_len+fft_len/4, rolloff, length_tag_key)
        self.digital_ofdm_carrier_allocator_cvc_0 = digital.ofdm_carrier_allocator_cvc(fft_len, occupied_carriers, pilot_carriers, pilot_symbols, (sync_word1, sync_word2), length_tag_key)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.digital_ofdm_carrier_allocator_cvc_0, 0), (self.fft_vxx_0, 0))    
        self.connect((self.digital_ofdm_cyclic_prefixer_0, 0), (self.probe3, 0))    
        self.connect((self.digital_ofdm_cyclic_prefixer_0, 0), (self.zeromq_push_sink_0, 0))    
        self.connect((self.fft_vxx_0, 0), (self.digital_ofdm_cyclic_prefixer_0, 0))    
        self.connect((self.zeromq_pull_source_0, 0), (self.digital_ofdm_carrier_allocator_cvc_0, 0))    

    def get_occupied_carriers(self):
        return self.occupied_carriers

    def set_occupied_carriers(self, occupied_carriers):
        self.occupied_carriers = occupied_carriers
        self.set_hdr_format(digital.header_format_ofdm(self.occupied_carriers, 1, self.length_tag_key,))

    def get_length_tag_key(self):
        return self.length_tag_key

    def set_length_tag_key(self, length_tag_key):
        self.length_tag_key = length_tag_key
        self.set_hdr_format(digital.header_format_ofdm(self.occupied_carriers, 1, self.length_tag_key,))

    def get_timedomainport(self):
        return self.timedomainport

    def set_timedomainport(self, timedomainport):
        self.timedomainport = timedomainport

    def get_tag_rate(self):
        return self.tag_rate

    def set_tag_rate(self, tag_rate):
        self.tag_rate = tag_rate

    def get_sync_word2(self):
        return self.sync_word2

    def set_sync_word2(self, sync_word2):
        self.sync_word2 = sync_word2

    def get_sync_word1(self):
        return self.sync_word1

    def set_sync_word1(self, sync_word1):
        self.sync_word1 = sync_word1

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate

    def get_split3ip(self):
        return self.split3ip

    def set_split3ip(self, split3ip):
        self.split3ip = split3ip

    def get_split3(self):
        return self.split3

    def set_split3(self, split3):
        self.split3 = split3

    def get_split2ip(self):
        return self.split2ip

    def set_split2ip(self, split2ip):
        self.split2ip = split2ip

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_rolloff(self):
        return self.rolloff

    def set_rolloff(self, rolloff):
        self.rolloff = rolloff

    def get_preofdmport(self):
        return self.preofdmport

    def set_preofdmport(self, preofdmport):
        self.preofdmport = preofdmport

    def get_pilot_symbols(self):
        return self.pilot_symbols

    def set_pilot_symbols(self, pilot_symbols):
        self.pilot_symbols = pilot_symbols

    def get_pilot_carriers(self):
        return self.pilot_carriers

    def set_pilot_carriers(self, pilot_carriers):
        self.pilot_carriers = pilot_carriers

    def get_payload_mod(self):
        return self.payload_mod

    def set_payload_mod(self, payload_mod):
        self.payload_mod = payload_mod

    def get_packet_len(self):
        return self.packet_len

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len

    def get_header_mod(self):
        return self.header_mod

    def set_header_mod(self, header_mod):
        self.header_mod = header_mod

    def get_hdr_format(self):
        return self.hdr_format

    def set_hdr_format(self, hdr_format):
        self.hdr_format = hdr_format

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len


def main(top_block_cls=Split3, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
