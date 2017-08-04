#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: OFDM Tx
# Description: Example of an OFDM Transmitter
# Generated: Wed Aug  2 16:36:10 2017
##################################################

from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio import zeromq
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import ConfigParser
import SimpleXMLRPCServer
import threading
import time


class tx_ofdm(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "OFDM Tx")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 100000
        self._finalsplitport_config = ConfigParser.ConfigParser()
        self._finalsplitport_config.read('default')
        try: finalsplitport = self._finalsplitport_config.get("usrp", "finalsplitport")
        except: finalsplitport = "2300"
        self.finalsplitport = finalsplitport
        self._finalsplitip_config = ConfigParser.ConfigParser()
        self._finalsplitip_config.read('default')
        try: finalsplitip = self._finalsplitip_config.get("usrp", "finalsplitip")
        except: finalsplitip = "127.0.0.1"
        self.finalsplitip = finalsplitip

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_pull_source_0 = zeromq.pull_source(gr.sizeof_gr_complex, 1, "tcp://" + finalsplitip + ":" + finalsplitport, 100, False, -1)
        self.xmlrpc_server_0 = SimpleXMLRPCServer.SimpleXMLRPCServer(('localhost', 8080), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(0, 0)
        self.uhd_usrp_sink_0.set_gain(0, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.zeromq_pull_source_0, 0), (self.uhd_usrp_sink_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_finalsplitport(self):
        return self.finalsplitport

    def set_finalsplitport(self, finalsplitport):
        self.finalsplitport = finalsplitport

    def get_finalsplitip(self):
        return self.finalsplitip

    def set_finalsplitip(self, finalsplitip):
        self.finalsplitip = finalsplitip


def main(top_block_cls=tx_ofdm, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
