#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Split 3
# Description: Split3
# Generated: Mon Sep 25 15:54:23 2017
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


class split3(gr.top_block):

    def __init__(self, maxoutbuffer=0):
        gr.top_block.__init__(self, "Split 3")

        ##################################################
        # Parameters
        ##################################################
        self.maxoutbuffer = maxoutbuffer

        ##################################################
        # Variables
        ##################################################
        self.pilot_carriers = pilot_carriers = ((-42, -14, -7, 7, 14, 42),)
        self.pattern2 = pattern2 = [1, -1, 1, -1]
        self.pattern1 = pattern1 = [0., 1.41421356, 0., -1.41421356]
        self.fft_len = fft_len = 128
        self._xmlrpcport_config = ConfigParser.ConfigParser()
        self._xmlrpcport_config.read('default')
        try: xmlrpcport = self._xmlrpcport_config.getint("split3", 'xmlrpcport')
        except: xmlrpcport = 8081
        self.xmlrpcport = xmlrpcport
        self._timeout_config = ConfigParser.ConfigParser()
        self._timeout_config.read('default')
        try: timeout = self._timeout_config.getint("global", "zmqtimeout")
        except: timeout = 100
        self.timeout = timeout
        self.sync_word2 = sync_word2 = [0., 0., 0., 0., 0., 0.,] + pattern2 * ((fft_len-12)/len(pattern2))  +[0., 0., 0., 0., 0., 0.,] 
        self.sync_word1 = sync_word1 = [0., 0., 0., 0., 0., 0.,] + pattern1 * ((fft_len-12)/len(pattern1))  +[0., 0., 0., 0., 0., 0.,] 
        self._split2port_config = ConfigParser.ConfigParser()
        self._split2port_config.read('default')
        try: split2port = self._split2port_config.get("split2", "port")
        except: split2port = "2200"
        self.split2port = split2port
        self._split2ip_config = ConfigParser.ConfigParser()
        self._split2ip_config.read('default')
        try: split2ip = self._split2ip_config.get("split2", "ip")
        except: split2ip = "127.0.0.1"
        self.split2ip = split2ip
        self.rolloff = rolloff = 0
        self.rate = rate = 0
        self._port_config = ConfigParser.ConfigParser()
        self._port_config.read('default')
        try: port = self._port_config.get("split3", "port")
        except: port = "2300"
        self.port = port
        self.pilot_symbols = pilot_symbols = ((-1,1, 1, -1, -1, -1),)
        self.occupied_carriers = occupied_carriers = (sorted(tuple(set([x for x in range(-26,27)]) - set(pilot_carriers[0]) - set([0,]))),)
        self._maxnoutput_config = ConfigParser.ConfigParser()
        self._maxnoutput_config.read('default')
        try: maxnoutput = self._maxnoutput_config.getint("global", "maxnoutput")
        except: maxnoutput = 100
        self.maxnoutput = maxnoutput
        self._ip_config = ConfigParser.ConfigParser()
        self._ip_config.read('default')
        try: ip = self._ip_config.get("split3", "ip")
        except: ip = "127.0.0.1"
        self.ip = ip

        ##################################################
        # Blocks
        ##################################################
        self.probe3 = blocks.probe_rate(gr.sizeof_gr_complex*1, 2000, 0.15)
        self.zeromq_push_sink_0 = zeromq.push_sink(gr.sizeof_gr_complex, 1, "tcp://" + ip + ":" + port, timeout, True, -1)
        self.zeromq_pull_source_0 = zeromq.pull_source(gr.sizeof_gr_complex, 1, "tcp://" + split2ip + ":" + split2port, timeout, True, -1)
        self.xmlrpc_server_0 = SimpleXMLRPCServer.SimpleXMLRPCServer((ip, xmlrpcport), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        
        def _rate_probe():
            while True:
                val = self.probe3.rate()
                try:
                    self.set_rate(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _rate_thread = threading.Thread(target=_rate_probe)
        _rate_thread.daemon = True
        _rate_thread.start()
            
        self.fft_vxx_0 = fft.fft_vcc(fft_len, False, (()), True, 1)
        self.digital_ofdm_cyclic_prefixer_0 = digital.ofdm_cyclic_prefixer(fft_len, fft_len+16, rolloff, "packet_len")
        self.digital_ofdm_carrier_allocator_cvc_0 = digital.ofdm_carrier_allocator_cvc(fft_len, occupied_carriers, pilot_carriers, pilot_symbols, (sync_word1, sync_word2), "packet_len")

        ##################################################
        # Connections
        ##################################################
        self.connect((self.digital_ofdm_carrier_allocator_cvc_0, 0), (self.fft_vxx_0, 0))    
        self.connect((self.digital_ofdm_cyclic_prefixer_0, 0), (self.probe3, 0))    
        self.connect((self.digital_ofdm_cyclic_prefixer_0, 0), (self.zeromq_push_sink_0, 0))    
        self.connect((self.fft_vxx_0, 0), (self.digital_ofdm_cyclic_prefixer_0, 0))    
        self.connect((self.zeromq_pull_source_0, 0), (self.digital_ofdm_carrier_allocator_cvc_0, 0))    

    def get_maxoutbuffer(self):
        return self.maxoutbuffer

    def set_maxoutbuffer(self, maxoutbuffer):
        self.maxoutbuffer = maxoutbuffer

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

    def get_timeout(self):
        return self.timeout

    def set_timeout(self, timeout):
        self.timeout = timeout

    def get_sync_word2(self):
        return self.sync_word2

    def set_sync_word2(self, sync_word2):
        self.sync_word2 = sync_word2

    def get_sync_word1(self):
        return self.sync_word1

    def set_sync_word1(self, sync_word1):
        self.sync_word1 = sync_word1

    def get_split2port(self):
        return self.split2port

    def set_split2port(self, split2port):
        self.split2port = split2port

    def get_split2ip(self):
        return self.split2ip

    def set_split2ip(self, split2ip):
        self.split2ip = split2ip

    def get_rolloff(self):
        return self.rolloff

    def set_rolloff(self, rolloff):
        self.rolloff = rolloff

    def get_rate(self):
        return self.rate

    def set_rate(self, rate):
        self.rate = rate

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_pilot_symbols(self):
        return self.pilot_symbols

    def set_pilot_symbols(self, pilot_symbols):
        self.pilot_symbols = pilot_symbols

    def get_occupied_carriers(self):
        return self.occupied_carriers

    def set_occupied_carriers(self, occupied_carriers):
        self.occupied_carriers = occupied_carriers

    def get_maxnoutput(self):
        return self.maxnoutput

    def set_maxnoutput(self, maxnoutput):
        self.maxnoutput = maxnoutput

    def get_ip(self):
        return self.ip

    def set_ip(self, ip):
        self.ip = ip


def argument_parser():
    description = 'Split3'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "", "--maxoutbuffer", dest="maxoutbuffer", type="intx", default=0,
        help="Set maxoutbuffer [default=%default]")
    return parser


def main(top_block_cls=split3, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(maxoutbuffer=options.maxoutbuffer)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
