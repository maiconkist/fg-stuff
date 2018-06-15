#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Split 2
# Description: Split 2
# Generated: Wed Jun 13 11:23:51 2018
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
import psutil
import threading
import time


class split2(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Split 2")

        ##################################################
        # Variables
        ##################################################
        self.zcpu = zcpu = psutil
        self._xmlrpcport_config = ConfigParser.ConfigParser()
        self._xmlrpcport_config.read('default')
        try: xmlrpcport = self._xmlrpcport_config.getint("split2", "xmlrpcport")
        except: xmlrpcport = 8080
        self.xmlrpcport = xmlrpcport
        self._timeout_config = ConfigParser.ConfigParser()
        self._timeout_config.read('./default')
        try: timeout = self._timeout_config.getint("global", "zmqtimeout")
        except: timeout = 100
        self.timeout = timeout
        self._split1ip_config = ConfigParser.ConfigParser()
        self._split1ip_config.read('./default')
        try: split1ip = self._split1ip_config.get("split1", "ip")
        except: split1ip = "127.0.0.1"
        self.split1ip = split1ip
        self.rate = rate = 0
        self._port_config = ConfigParser.ConfigParser()
        self._port_config.read('./default')
        try: port = self._port_config.get("split2", "port")
        except: port = '2200'
        self.port = port
        self._payloadport_config = ConfigParser.ConfigParser()
        self._payloadport_config.read('./default')
        try: payloadport = self._payloadport_config.get("split1", "payloadport")
        except: payloadport = "2101"
        self.payloadport = payloadport
        self.payload_mod = payload_mod = digital.constellation_bpsk()
        self._maxnoutput_config = ConfigParser.ConfigParser()
        self._maxnoutput_config.read('./default')
        try: maxnoutput = self._maxnoutput_config.getint("global", "maxnoutput")
        except: maxnoutput = 100
        self.maxnoutput = maxnoutput
        self._ip_config = ConfigParser.ConfigParser()
        self._ip_config.read('./default')
        try: ip = self._ip_config.get("split2", "ip")
        except: ip = "127.0.0.1"
        self.ip = ip
        self._headerport_config = ConfigParser.ConfigParser()
        self._headerport_config.read('./default')
        try: headerport = self._headerport_config.get("split1", "headerport")
        except: headerport = "2100"
        self.headerport = headerport
        self.header_mod = header_mod = digital.constellation_bpsk()
        self.cpu_percent = cpu_percent = 0

        ##################################################
        # Blocks
        ##################################################
        self.probe2 = blocks.probe_rate(gr.sizeof_gr_complex*1, 2000, 0.15)
        self.zeromq_push_sink_0 = zeromq.push_sink(gr.sizeof_gr_complex, 1, "tcp://" + ip + ":" + port, timeout, True, -1)
        self.zeromq_pull_source_1 = zeromq.pull_source(gr.sizeof_char, 1, "tcp://" + split1ip + ":" + payloadport, timeout, True, -1)
        self.zeromq_pull_source_0 = zeromq.pull_source(gr.sizeof_char, 1, "tcp://" + split1ip + ":" + headerport, timeout, True, -1)
        self.xmlrpc_server_0 = SimpleXMLRPCServer.SimpleXMLRPCServer(('127.0.0.1', xmlrpcport), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        
        def _rate_probe():
            while True:
                val = self.probe2.rate()
                try:
                    self.set_rate(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _rate_thread = threading.Thread(target=_rate_probe)
        _rate_thread.daemon = True
        _rate_thread.start()
            
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc((payload_mod.points()), 1)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc((header_mod.points()), 1)
        
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
            
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, 1e6,True)
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, "packet_len", 0)
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_gr_complex*1, '', ""); self.blocks_tag_debug_0.set_display(True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.blocks_tag_debug_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.probe2, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.zeromq_push_sink_0, 0))    
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_tagged_stream_mux_0, 0))    
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.blocks_tagged_stream_mux_0, 1))    
        self.connect((self.zeromq_pull_source_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))    
        self.connect((self.zeromq_pull_source_1, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))    

    def get_zcpu(self):
        return self.zcpu

    def set_zcpu(self, zcpu):
        self.zcpu = zcpu

    def get_xmlrpcport(self):
        return self.xmlrpcport

    def set_xmlrpcport(self, xmlrpcport):
        self.xmlrpcport = xmlrpcport

    def get_timeout(self):
        return self.timeout

    def set_timeout(self, timeout):
        self.timeout = timeout

    def get_split1ip(self):
        return self.split1ip

    def set_split1ip(self, split1ip):
        self.split1ip = split1ip

    def get_rate(self):
        return self.rate

    def set_rate(self, rate):
        self.rate = rate

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

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

    def get_cpu_percent(self):
        return self.cpu_percent

    def set_cpu_percent(self, cpu_percent):
        self.cpu_percent = cpu_percent


def main(top_block_cls=split2, options=None):

    tb = top_block_cls()


    def xxx():
        xarr = []
        while True:
           xarr.append(tb.get_rate())


           if len(xarr) >= 3 and  xarr[0] == xarr[1] and xarr[1] == xarr[2]:
              import sys
              tb.stop()
              exit()

           while len(xarr) > 3:
               xarr.pop(0)

           time.sleep(2)
    #th = threading.Thread(target = xxx)
    #th.daemon = True
    #th.start()

    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
