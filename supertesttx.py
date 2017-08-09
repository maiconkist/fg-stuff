#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Supertesttx
# Generated: Wed Aug  9 16:30:14 2017
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import zeromq
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import ConfigParser


class supertesttx(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Supertesttx")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self._repforwardip_config = ConfigParser.ConfigParser()
        self._repforwardip_config.read('default')
        try: repforwardip = self._repforwardip_config.get("ping", "repforwardip")
        except: repforwardip = "127.0.0.1"
        self.repforwardip = repforwardip
        self._payloadport_config = ConfigParser.ConfigParser()
        self._payloadport_config.read('default')
        try: payloadport = self._payloadport_config.get("split1", "payloadport")
        except: payloadport = "2101"
        self.payloadport = payloadport
        self._ip_config = ConfigParser.ConfigParser()
        self._ip_config.read('default')
        try: ip = self._ip_config.get("split1", "ip")
        except: ip = "127.0.0.1"
        self.ip = ip

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_push_sink_0 = zeromq.push_sink(gr.sizeof_char, 1, "tcp://" + ip + ":" + payloadport, 100, True, -1)
        self.zeromq_pull_source_0 = zeromq.pull_source(gr.sizeof_char, 1, "tcp://" + repforwardip + ":" + payloadport, 100, True, -1)
        self.blocks_tuntap_pdu_0 = blocks.tuntap_pdu('tap0', 10000, False)
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, 'packet_len')
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.blocks_tuntap_pdu_0, 'pdus'))    
        self.msg_connect((self.blocks_tuntap_pdu_0, 'pdus'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))    
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.zeromq_push_sink_0, 0))    
        self.connect((self.zeromq_pull_source_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_repforwardip(self):
        return self.repforwardip

    def set_repforwardip(self, repforwardip):
        self.repforwardip = repforwardip

    def get_payloadport(self):
        return self.payloadport

    def set_payloadport(self, payloadport):
        self.payloadport = payloadport

    def get_ip(self):
        return self.ip

    def set_ip(self, ip):
        self.ip = ip


def main(top_block_cls=supertesttx, options=None):

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
