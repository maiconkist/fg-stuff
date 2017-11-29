#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: OFDM Single
# Description: Single
# Generated: Wed Nov 29 16:51:23 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import ConfigParser
import SimpleXMLRPCServer
import hydra
import pmt
import sip
import sys
import threading
import time
from gnuradio import qtgui


class all_rx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "OFDM Single")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("OFDM Single")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "all_rx")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.vr2_pc = vr2_pc = ((-14, -7, 7, 14),)
        self.vr2_pattern2 = vr2_pattern2 = [1, -1, 1, -1]
        self.vr2_pattern1 = vr2_pattern1 = [0., 1.41421356, 0., -1.41421356]
        self.vr1_pc = vr1_pc = ((-27, -14, -7, 7, 14, 27),)
        self.vr1_pattern2 = vr1_pattern2 = [1, -1, 1, -1]
        self.vr1_pattern1 = vr1_pattern1 = [0., 1.41421356, 0., -1.41421356]
        self.fft_len = fft_len = 64
        self._xmlrpcport_config = ConfigParser.ConfigParser()
        self._xmlrpcport_config.read('./default')
        try: xmlrpcport = self._xmlrpcport_config.getint("vr1_tx", "xmlrpcport")
        except: xmlrpcport = 0
        self.xmlrpcport = xmlrpcport
        self.vr2_sw2 = vr2_sw2 = [0., 0., 0., 0., 0., 0.,] + vr2_pattern2 * ((fft_len-12)/len(vr2_pattern2))  + [0., 0., 0., 0., 0., 0.,]
        self.vr2_sw1 = vr2_sw1 = [0., 0., 0., 0., 0., 0.,] + vr2_pattern1 * ((fft_len-12)/len(vr2_pattern1))  +[0., 0., 0., 0., 0., 0.,]
        self.vr2_ps = vr2_ps = ((1, 1, -1, -1),)
        self.vr2_oc = vr2_oc = (sorted(tuple(set([x for x in range(-26,27)]) - set(vr2_pc[0]) - set([0,]))),)
        self.vr1_sw2 = vr1_sw2 = [0., 0., 0., 0., 0., 0.,] + vr1_pattern2 * ((fft_len-12)/len(vr1_pattern2))  +[0., 0., 0., 0., 0., 0.,]
        self.vr1_sw1 = vr1_sw1 = [0., 0., 0., 0., 0., 0.,] + vr1_pattern1 * ((fft_len-12)/len(vr1_pattern1))  +[0., 0., 0., 0., 0., 0.,]
        self.vr1_ps = vr1_ps = ((-1,1, 1, -1, -1, -1),)
        self.vr1_oc = vr1_oc = (sorted(tuple(set([x for x in range(-26,27)]) - set(vr1_pc[0]) - set([0,]))),)
        self._usrpip_config = ConfigParser.ConfigParser()
        self._usrpip_config.read('default')
        try: usrpip = self._usrpip_config.get("usrp", "ip")
        except: usrpip = "127.0.0.1"
        self.usrpip = usrpip
        self._usrp_s_config = ConfigParser.ConfigParser()
        self._usrp_s_config.read('./default')
        try: usrp_s = self._usrp_s_config.getfloat("usrp_hydra", "samprate")
        except: usrp_s = 4e6
        self.usrp_s = usrp_s
        self._usrp_f_config = ConfigParser.ConfigParser()
        self._usrp_f_config.read('./default')
        try: usrp_f = self._usrp_f_config.getfloat("usrp_hydra", "txfreq")
        except: usrp_f = 4e6
        self.usrp_f = usrp_f
        self._txoutport_config = ConfigParser.ConfigParser()
        self._txoutport_config.read('default')
        try: txoutport = self._txoutport_config.get("usrp", "txoutport")
        except: txoutport = "2666"
        self.txoutport = txoutport
        self._timeout_config = ConfigParser.ConfigParser()
        self._timeout_config.read('default')
        try: timeout = self._timeout_config.getint("global", "zmqtimeout")
        except: timeout = 100
        self.timeout = timeout
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
        self._maxnoutput_config = ConfigParser.ConfigParser()
        self._maxnoutput_config.read('default')
        try: maxnoutput = self._maxnoutput_config.getint("global", "maxnoutput")
        except: maxnoutput = 100
        self.maxnoutput = maxnoutput
        self._freq2_config = ConfigParser.ConfigParser()
        self._freq2_config.read('./default')
        try: freq2 = self._freq2_config.getfloat("usrp_hydra", "freq2")
        except: freq2 = 950e6
        self.freq2 = freq2
        self._freq1_config = ConfigParser.ConfigParser()
        self._freq1_config.read('./default')
        try: freq1 = self._freq1_config.getfloat("usrp_hydra", "freq1")
        except: freq1 = 950e6
        self.freq1 = freq1
        self.amp2 = amp2 = 0.01
        self.amp1 = amp1 = 0.01

        ##################################################
        # Blocks
        ##################################################
        self._amp1_range = Range(0, 1, 0.01, 0.01, 200)
        self._amp1_win = RangeWidget(self._amp1_range, self.set_amp1, 'amp1', "counter_slider", float)
        self.top_layout.addWidget(self._amp1_win)
        self.xmlrpc_server_0 = SimpleXMLRPCServer.SimpleXMLRPCServer(('192.168.10.30', xmlrpcport), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(usrp_s)
        self.uhd_usrp_source_0.set_center_freq(usrp_f, 0)
        self.uhd_usrp_source_0.set_normalized_gain(0, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_sink_0_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0_0.set_samp_rate(samprate2)
        self.uhd_usrp_sink_0_0.set_center_freq(freq2 + 4e6, 0)
        self.uhd_usrp_sink_0_0.set_normalized_gain(1.0, 0)
        self.uhd_usrp_sink_0_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samprate1)
        self.uhd_usrp_sink_0.set_center_freq(freq1 + 4e6, 0)
        self.uhd_usrp_sink_0.set_normalized_gain(1.0, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	512, #size
        	firdes.WIN_RECTANGULAR, #wintype
        	0, #fc
        	100, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.hydra_hydra_source_0 = hydra.hydra_source(2, 512, usrp_f, usrp_s,
        	 ((freq1, samprate1),
        	 (freq2, samprate2),
        	 ))

        self.digital_ofdm_tx_0_0 = digital.ofdm_tx(
        	  fft_len=64, cp_len=16,
        	  packet_length_tag_key="vr2tx",
        	  occupied_carriers=vr2_oc,
        	  pilot_carriers=vr2_pc,
        	  pilot_symbols=vr2_ps,
        	  sync_word1=vr2_sw1,
        	  sync_word2=vr2_sw2,
        	  bps_header=1,
        	  bps_payload=1,
        	  rolloff=0,
        	  debug_log=False,
        	  scramble_bits=False
        	 )
        self.digital_ofdm_tx_0 = digital.ofdm_tx(
        	  fft_len=64, cp_len=16,
        	  packet_length_tag_key="vr1tx",
        	  occupied_carriers=vr1_oc,
        	  pilot_carriers=vr1_pc,
        	  pilot_symbols=vr1_ps,
        	  sync_word1=vr1_sw1,
        	  sync_word2=vr1_sw2,
        	  bps_header=1,
        	  bps_payload=1,
        	  rolloff=0,
        	  debug_log=False,
        	  scramble_bits=False
        	 )
        self.digital_ofdm_rx_1 = digital.ofdm_rx(
        	  fft_len=64, cp_len=16,
        	  frame_length_tag_key='frame_'+"vr2",
        	  packet_length_tag_key="vr2",
        	  occupied_carriers=vr2_oc,
        	  pilot_carriers=vr2_pc,
        	  pilot_symbols=vr2_ps,
        	  sync_word1=vr2_sw1,
        	  sync_word2=vr2_sw2,
        	  bps_header=1,
        	  bps_payload=1,
        	  debug_log=False,
        	  scramble_bits=False
        	 )
        self.digital_ofdm_rx_0 = digital.ofdm_rx(
        	  fft_len=fft_len, cp_len=16,
        	  frame_length_tag_key='frame_'+"vr1rx",
        	  packet_length_tag_key="vr1rx",
        	  occupied_carriers=vr1_oc,
        	  pilot_carriers=vr1_pc,
        	  pilot_symbols=vr1_ps,
        	  sync_word1=vr1_sw1,
        	  sync_word2=vr1_sw2,
        	  bps_header=1,
        	  bps_payload=1,
        	  debug_log=False,
        	  scramble_bits=False
        	 )
        self.digital_burst_shaper_xx_0_0 = digital.burst_shaper_cc((([])), 2000, 2000, False, "vr1tx")
        self.digital_burst_shaper_xx_0 = digital.burst_shaper_cc((([])), 2000, 2000, False, "vr1tx")
        self.blocks_tagged_stream_to_pdu_0_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, "vr1rx")
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, "vr1rx")
        self.blocks_tag_debug_0_0 = blocks.tag_debug(gr.sizeof_char*1, '', ""); self.blocks_tag_debug_0_0.set_display(True)
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_char*1, '', ""); self.blocks_tag_debug_0.set_display(True)
        self.blocks_random_pdu_0_0 = blocks.random_pdu(50, 100, chr(0xFF), 2)
        self.blocks_random_pdu_0 = blocks.random_pdu(50, 100, chr(0xFF), 2)
        self.blocks_pdu_to_tagged_stream_0_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, "vr2tx")
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, "vr1tx")
        self.blocks_pdu_set_0_0 = blocks.pdu_set(pmt.intern("vr2rx"), pmt.intern("generate"))
        self.blocks_pdu_set_0 = blocks.pdu_set(pmt.intern("vr1rx"), pmt.intern("generate"))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vcc((amp1, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((amp1, ))
        self._amp2_range = Range(0, 1, 0.01, 0.01, 200)
        self._amp2_win = RangeWidget(self._amp2_range, self.set_amp2, 'amp2', "counter_slider", float)
        self.top_layout.addWidget(self._amp2_win)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_pdu_set_0, 'pdus'), (self.blocks_random_pdu_0, 'generate'))
        self.msg_connect((self.blocks_pdu_set_0_0, 'pdus'), (self.blocks_random_pdu_0_0, 'generate'))
        self.msg_connect((self.blocks_random_pdu_0, 'pdus'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))
        self.msg_connect((self.blocks_random_pdu_0_0, 'pdus'), (self.blocks_pdu_to_tagged_stream_0_0, 'pdus'))
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.blocks_pdu_set_0, 'pdus'))
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0_0, 'pdus'), (self.blocks_pdu_set_0_0, 'pdus'))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.digital_burst_shaper_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.digital_burst_shaper_xx_0_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.digital_ofdm_tx_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0_0, 0), (self.digital_ofdm_tx_0_0, 0))
        self.connect((self.digital_burst_shaper_xx_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.digital_burst_shaper_xx_0_0, 0), (self.uhd_usrp_sink_0_0, 0))
        self.connect((self.digital_ofdm_rx_0, 0), (self.blocks_tag_debug_0, 0))
        self.connect((self.digital_ofdm_rx_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))
        self.connect((self.digital_ofdm_rx_1, 0), (self.blocks_tag_debug_0_0, 0))
        self.connect((self.digital_ofdm_rx_1, 0), (self.blocks_tagged_stream_to_pdu_0_0, 0))
        self.connect((self.digital_ofdm_tx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_ofdm_tx_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.hydra_hydra_source_0, 0), (self.digital_ofdm_rx_0, 0))
        self.connect((self.hydra_hydra_source_0, 1), (self.digital_ofdm_rx_1, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.hydra_hydra_source_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "all_rx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_vr2_pc(self):
        return self.vr2_pc

    def set_vr2_pc(self, vr2_pc):
        self.vr2_pc = vr2_pc
        self.set_vr2_oc((sorted(tuple(set([x for x in range(-26,27)]) - set(self.vr2_pc[0]) - set([0,]))),))

    def get_vr2_pattern2(self):
        return self.vr2_pattern2

    def set_vr2_pattern2(self, vr2_pattern2):
        self.vr2_pattern2 = vr2_pattern2
        self.set_vr2_sw2([0., 0., 0., 0., 0., 0.,] + self.vr2_pattern2 * ((self.fft_len-12)/len(self.vr2_pattern2))  + [0., 0., 0., 0., 0., 0.,] )

    def get_vr2_pattern1(self):
        return self.vr2_pattern1

    def set_vr2_pattern1(self, vr2_pattern1):
        self.vr2_pattern1 = vr2_pattern1
        self.set_vr2_sw1([0., 0., 0., 0., 0., 0.,] + self.vr2_pattern1 * ((self.fft_len-12)/len(self.vr2_pattern1))  +[0., 0., 0., 0., 0., 0.,] )

    def get_vr1_pc(self):
        return self.vr1_pc

    def set_vr1_pc(self, vr1_pc):
        self.vr1_pc = vr1_pc
        self.set_vr1_oc((sorted(tuple(set([x for x in range(-26,27)]) - set(self.vr1_pc[0]) - set([0,]))),))

    def get_vr1_pattern2(self):
        return self.vr1_pattern2

    def set_vr1_pattern2(self, vr1_pattern2):
        self.vr1_pattern2 = vr1_pattern2
        self.set_vr1_sw2([0., 0., 0., 0., 0., 0.,] + self.vr1_pattern2 * ((self.fft_len-12)/len(self.vr1_pattern2))  +[0., 0., 0., 0., 0., 0.,] )

    def get_vr1_pattern1(self):
        return self.vr1_pattern1

    def set_vr1_pattern1(self, vr1_pattern1):
        self.vr1_pattern1 = vr1_pattern1
        self.set_vr1_sw1([0., 0., 0., 0., 0., 0.,] + self.vr1_pattern1 * ((self.fft_len-12)/len(self.vr1_pattern1))  +[0., 0., 0., 0., 0., 0.,] )

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.set_vr2_sw2([0., 0., 0., 0., 0., 0.,] + self.vr2_pattern2 * ((self.fft_len-12)/len(self.vr2_pattern2))  + [0., 0., 0., 0., 0., 0.,] )
        self.set_vr2_sw1([0., 0., 0., 0., 0., 0.,] + self.vr2_pattern1 * ((self.fft_len-12)/len(self.vr2_pattern1))  +[0., 0., 0., 0., 0., 0.,] )
        self.set_vr1_sw2([0., 0., 0., 0., 0., 0.,] + self.vr1_pattern2 * ((self.fft_len-12)/len(self.vr1_pattern2))  +[0., 0., 0., 0., 0., 0.,] )
        self.set_vr1_sw1([0., 0., 0., 0., 0., 0.,] + self.vr1_pattern1 * ((self.fft_len-12)/len(self.vr1_pattern1))  +[0., 0., 0., 0., 0., 0.,] )

    def get_xmlrpcport(self):
        return self.xmlrpcport

    def set_xmlrpcport(self, xmlrpcport):
        self.xmlrpcport = xmlrpcport

    def get_vr2_sw2(self):
        return self.vr2_sw2

    def set_vr2_sw2(self, vr2_sw2):
        self.vr2_sw2 = vr2_sw2

    def get_vr2_sw1(self):
        return self.vr2_sw1

    def set_vr2_sw1(self, vr2_sw1):
        self.vr2_sw1 = vr2_sw1

    def get_vr2_ps(self):
        return self.vr2_ps

    def set_vr2_ps(self, vr2_ps):
        self.vr2_ps = vr2_ps

    def get_vr2_oc(self):
        return self.vr2_oc

    def set_vr2_oc(self, vr2_oc):
        self.vr2_oc = vr2_oc

    def get_vr1_sw2(self):
        return self.vr1_sw2

    def set_vr1_sw2(self, vr1_sw2):
        self.vr1_sw2 = vr1_sw2

    def get_vr1_sw1(self):
        return self.vr1_sw1

    def set_vr1_sw1(self, vr1_sw1):
        self.vr1_sw1 = vr1_sw1

    def get_vr1_ps(self):
        return self.vr1_ps

    def set_vr1_ps(self, vr1_ps):
        self.vr1_ps = vr1_ps

    def get_vr1_oc(self):
        return self.vr1_oc

    def set_vr1_oc(self, vr1_oc):
        self.vr1_oc = vr1_oc

    def get_usrpip(self):
        return self.usrpip

    def set_usrpip(self, usrpip):
        self.usrpip = usrpip

    def get_usrp_s(self):
        return self.usrp_s

    def set_usrp_s(self, usrp_s):
        self.usrp_s = usrp_s
        self.uhd_usrp_source_0.set_samp_rate(self.usrp_s)

    def get_usrp_f(self):
        return self.usrp_f

    def set_usrp_f(self, usrp_f):
        self.usrp_f = usrp_f
        self.uhd_usrp_source_0.set_center_freq(self.usrp_f, 0)

    def get_txoutport(self):
        return self.txoutport

    def set_txoutport(self, txoutport):
        self.txoutport = txoutport

    def get_timeout(self):
        return self.timeout

    def set_timeout(self, timeout):
        self.timeout = timeout

    def get_samprate2(self):
        return self.samprate2

    def set_samprate2(self, samprate2):
        self.samprate2 = samprate2
        self.uhd_usrp_sink_0_0.set_samp_rate(self.samprate2)

    def get_samprate1(self):
        return self.samprate1

    def set_samprate1(self, samprate1):
        self.samprate1 = samprate1
        self.uhd_usrp_sink_0.set_samp_rate(self.samprate1)

    def get_maxnoutput(self):
        return self.maxnoutput

    def set_maxnoutput(self, maxnoutput):
        self.maxnoutput = maxnoutput

    def get_freq2(self):
        return self.freq2

    def set_freq2(self, freq2):
        self.freq2 = freq2
        self.uhd_usrp_sink_0_0.set_center_freq(self.freq2 + 4e6, 0)
        self.hydra_hydra_source_0.set_central_frequency(1, self.freq2)

    def get_freq1(self):
        return self.freq1

    def set_freq1(self, freq1):
        self.freq1 = freq1
        self.uhd_usrp_sink_0.set_center_freq(self.freq1 + 4e6, 0)
        self.hydra_hydra_source_0.set_central_frequency(0, self.freq1)

    def get_amp2(self):
        return self.amp2

    def set_amp2(self, amp2):
        self.amp2 = amp2

    def get_amp1(self):
        return self.amp1

    def set_amp1(self, amp1):
        self.amp1 = amp1
        self.blocks_multiply_const_vxx_0_0.set_k((self.amp1, ))
        self.blocks_multiply_const_vxx_0.set_k((self.amp1, ))


def main(top_block_cls=all_rx, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
