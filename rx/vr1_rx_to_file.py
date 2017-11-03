#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: OFDM Single
# Description: Single
# Generated: Fri Sep 22 12:39:19 2017
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.digital.utils import tagged_streams
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import ConfigParser
import time


class vr1_rx_to_file(gr.top_block):

    def __init__(self, thefile='0'):
        gr.top_block.__init__(self, "OFDM Single")

        ##################################################
        # Parameters
        ##################################################
        self.thefile = thefile

        ##################################################
        # Variables
        ##################################################
        self.pilot_carriers = pilot_carriers = ((-42, -14, -7, 7, 14, 42),)
        self.pattern2 = pattern2 = [1, -1, 1, -1]
        self.pattern1 = pattern1 = [0., 1.41421356, 0., -1.41421356]
        self.fft_len = fft_len = 128
        self._usrpip_config = ConfigParser.ConfigParser()
        self._usrpip_config.read('default')
        try: usrpip = self._usrpip_config.get("usrp", "ip")
        except: usrpip = "127.0.0.1"
        self.usrpip = usrpip
        self._txoutport_config = ConfigParser.ConfigParser()
        self._txoutport_config.read('default')
        try: txoutport = self._txoutport_config.get("usrp", "txoutport")
        except: txoutport = "2666"
        self.txoutport = txoutport
        self._txgain_config = ConfigParser.ConfigParser()
        self._txgain_config.read('default')
        try: txgain = self._txgain_config.getfloat("rx", "txgain")
        except: txgain = 0.5
        self.txgain = txgain
        self._txfreq_config = ConfigParser.ConfigParser()
        self._txfreq_config.read('default')
        try: txfreq = self._txfreq_config.getfloat("usrp_hydra", "txfreq1")
        except: txfreq = 4.4e9
        self.txfreq = txfreq
        self._timeout_config = ConfigParser.ConfigParser()
        self._timeout_config.read('default')
        try: timeout = self._timeout_config.getint("global", "zmqtimeout")
        except: timeout = 100
        self.timeout = timeout
        self.sync_word2 = sync_word2 = [0., 0., 0., 0., 0., 0.,] + pattern2 * ((fft_len-12)/len(pattern2))  +[0., 0., 0., 0., 0., 0.,] 
        self.sync_word1 = sync_word1 = [0., 0., 0., 0., 0., 0.,] + pattern1 * ((fft_len-12)/len(pattern1))  +[0., 0., 0., 0., 0., 0.,] 
        self._samprate_config = ConfigParser.ConfigParser()
        self._samprate_config.read('default')
        try: samprate = self._samprate_config.getfloat("usrp_hydra", "samprate1")
        except: samprate = 4e6
        self.samprate = samprate
        self._rxgain_config = ConfigParser.ConfigParser()
        self._rxgain_config.read('default')
        try: rxgain = self._rxgain_config.getfloat("rx", "rxgain")
        except: rxgain = 0.5
        self.rxgain = rxgain
        self._rxfreq_config = ConfigParser.ConfigParser()
        self._rxfreq_config.read('default')
        try: rxfreq = self._rxfreq_config.getfloat("usrp_hydra", "rxfreq1")
        except: rxfreq = 4.4e9
        self.rxfreq = rxfreq
        self.pilot_symbols = pilot_symbols = ((-1,1, 1, -1, -1, -1),)
        self.packet_length_tag_key = packet_length_tag_key = "packet_len"
        self.occupied_carriers = occupied_carriers = (sorted(tuple(set([x for x in range(-56,57)]) - set(pilot_carriers[0]) - set([0,]))),)
        self._maxnoutput_config = ConfigParser.ConfigParser()
        self._maxnoutput_config.read('default')
        try: maxnoutput = self._maxnoutput_config.getint("global", "maxnoutput")
        except: maxnoutput = 100
        self.maxnoutput = maxnoutput
        self.length_tag_key = length_tag_key = "frame_len"
        self._amplitude_config = ConfigParser.ConfigParser()
        self._amplitude_config.read('default')
        try: amplitude = self._amplitude_config.getfloat("rx", "txamplitude")
        except: amplitude = 0.1
        self.amplitude = amplitude

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samprate)
        self.uhd_usrp_source_0.set_center_freq(txfreq, 0)
        self.uhd_usrp_source_0.set_normalized_gain(rxgain, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.blocks_skiphead_0 = blocks.skiphead(gr.sizeof_gr_complex*1, int(2 * samprate))
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, int(10 * samprate))
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, thefile, False)
        self.blocks_file_sink_0.set_unbuffered(False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_head_0, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.blocks_skiphead_0, 0), (self.blocks_head_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_skiphead_0, 0))    

    def get_thefile(self):
        return self.thefile

    def set_thefile(self, thefile):
        self.thefile = thefile
        self.blocks_file_sink_0.open(self.thefile)

    def get_pilot_carriers(self):
        return self.pilot_carriers

    def set_pilot_carriers(self, pilot_carriers):
        self.pilot_carriers = pilot_carriers
        self.set_occupied_carriers((sorted(tuple(set([x for x in range(-56,57)]) - set(self.pilot_carriers[0]) - set([0,]))),))

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

    def get_usrpip(self):
        return self.usrpip

    def set_usrpip(self, usrpip):
        self.usrpip = usrpip

    def get_txoutport(self):
        return self.txoutport

    def set_txoutport(self, txoutport):
        self.txoutport = txoutport

    def get_txgain(self):
        return self.txgain

    def set_txgain(self, txgain):
        self.txgain = txgain

    def get_txfreq(self):
        return self.txfreq

    def set_txfreq(self, txfreq):
        self.txfreq = txfreq
        self.uhd_usrp_source_0.set_center_freq(self.txfreq, 0)

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

    def get_samprate(self):
        return self.samprate

    def set_samprate(self, samprate):
        self.samprate = samprate
        self.uhd_usrp_source_0.set_samp_rate(self.samprate)
        self.blocks_head_0.set_length(int(10 * self.samprate))

    def get_rxgain(self):
        return self.rxgain

    def set_rxgain(self, rxgain):
        self.rxgain = rxgain
        self.uhd_usrp_source_0.set_normalized_gain(self.rxgain, 0)
        	

    def get_rxfreq(self):
        return self.rxfreq

    def set_rxfreq(self, rxfreq):
        self.rxfreq = rxfreq

    def get_pilot_symbols(self):
        return self.pilot_symbols

    def set_pilot_symbols(self, pilot_symbols):
        self.pilot_symbols = pilot_symbols

    def get_packet_length_tag_key(self):
        return self.packet_length_tag_key

    def set_packet_length_tag_key(self, packet_length_tag_key):
        self.packet_length_tag_key = packet_length_tag_key

    def get_occupied_carriers(self):
        return self.occupied_carriers

    def set_occupied_carriers(self, occupied_carriers):
        self.occupied_carriers = occupied_carriers

    def get_maxnoutput(self):
        return self.maxnoutput

    def set_maxnoutput(self, maxnoutput):
        self.maxnoutput = maxnoutput

    def get_length_tag_key(self):
        return self.length_tag_key

    def set_length_tag_key(self, length_tag_key):
        self.length_tag_key = length_tag_key

    def get_amplitude(self):
        return self.amplitude

    def set_amplitude(self, amplitude):
        self.amplitude = amplitude


def argument_parser():
    description = 'Single'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "", "--thefile", dest="thefile", type="string", default='0',
        help="Set 0 [default=%default]")
    return parser


def main(top_block_cls=vr1_rx_to_file, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(thefile=options.thefile)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
