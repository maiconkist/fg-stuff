#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: usrp
# Description: USRP
# Generated: Mon Sep 25 15:54:45 2017
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
from gnuradio import zeromq
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import ConfigParser
import SimpleXMLRPCServer
import sip
import sys
import threading
import time


class usrp(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "usrp")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("usrp")
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

        self.settings = Qt.QSettings("GNU Radio", "usrp")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self._xmlrpcport_config = ConfigParser.ConfigParser()
        self._xmlrpcport_config.read('default')
        try: xmlrpcport = self._xmlrpcport_config.getint("usrp", 'xmlrpcport')
        except: xmlrpcport = 8081
        self.xmlrpcport = xmlrpcport
        self.txrate = txrate = 0
        self._txoutport_config = ConfigParser.ConfigParser()
        self._txoutport_config.read('default')
        try: txoutport = self._txoutport_config.get("usrp", "txoutport")
        except: txoutport = "2666"
        self.txoutport = txoutport
        self.txgain = txgain = 1
        self._txfreq_config = ConfigParser.ConfigParser()
        self._txfreq_config.read('default')
        try: txfreq = self._txfreq_config.getfloat("usrp", "txfreq1")
        except: txfreq = 4.4e9
        self.txfreq = txfreq
        self._timeout_config = ConfigParser.ConfigParser()
        self._timeout_config.read('default')
        try: timeout = self._timeout_config.getint("global", "zmqtimeout")
        except: timeout = 100
        self.timeout = timeout
        self._samprate_config = ConfigParser.ConfigParser()
        self._samprate_config.read('default')
        try: samprate = self._samprate_config.getfloat("usrp", "samprate1")
        except: samprate = 1e6
        self.samprate = samprate
        self.rxrate = rxrate = 0
        self._rxport_config = ConfigParser.ConfigParser()
        self._rxport_config.read('default')
        try: rxport = self._rxport_config.get("rx", "port")
        except: rxport = "2300"
        self.rxport = rxport
        self._rxoutport_config = ConfigParser.ConfigParser()
        self._rxoutport_config.read('default')
        try: rxoutport = self._rxoutport_config.get("usrp", "rxoutport")
        except: rxoutport = "2666"
        self.rxoutport = rxoutport
        self._rxip_config = ConfigParser.ConfigParser()
        self._rxip_config.read('default')
        try: rxip = self._rxip_config.get("rx", "ip")
        except: rxip = "127.0.0.1"
        self.rxip = rxip
        self.rxgain = rxgain = 0
        self._rxfreq_config = ConfigParser.ConfigParser()
        self._rxfreq_config.read('default')
        try: rxfreq = self._rxfreq_config.getfloat("usrp", "rxfreq1")
        except: rxfreq = 4.4e9
        self.rxfreq = rxfreq
        self._maxnoutput_config = ConfigParser.ConfigParser()
        self._maxnoutput_config.read('default')
        try: maxnoutput = self._maxnoutput_config.getint("global", "maxnoutput")
        except: maxnoutput = 100
        self.maxnoutput = maxnoutput
        self._ip_config = ConfigParser.ConfigParser()
        self._ip_config.read('default')
        try: ip = self._ip_config.get("usrp", "ip")
        except: ip = "127.0.0.1"
        self.ip = ip
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
        self.amplitude = amplitude = 0.01

        ##################################################
        # Blocks
        ##################################################
        self._txgain_range = Range(0, 1, 0.01, 1, 200)
        self._txgain_win = RangeWidget(self._txgain_range, self.set_txgain, 'txgain', "counter_slider", float)
        self.top_layout.addWidget(self._txgain_win)
        self._rxgain_range = Range(0, 1, 0.01, 0, 200)
        self._rxgain_win = RangeWidget(self._rxgain_range, self.set_rxgain, 'rxgain', "counter_slider", float)
        self.top_layout.addWidget(self._rxgain_win)
        self._amplitude_range = Range(0, 1, 0.01, 0.01, 200)
        self._amplitude_win = RangeWidget(self._amplitude_range, self.set_amplitude, 'amplitude', "counter_slider", float)
        self.top_layout.addWidget(self._amplitude_win)
        self.ztxrate = blocks.probe_rate(gr.sizeof_gr_complex*1, 2000, 0.15)
        self.zrxrate = blocks.probe_rate(gr.sizeof_gr_complex*1, 2000, 0.15)
        self.zeromq_push_sink_0_0 = zeromq.push_sink(gr.sizeof_gr_complex, 1, "tcp://" + ip + ":" + rxoutport, 100, True, -1)
        self.zeromq_pull_source_0 = zeromq.pull_source(gr.sizeof_gr_complex, 1, "tcp://" + finalsplitip + ":" + finalsplitport, timeout, True, -1)
        self.xmlrpc_server_0_0 = SimpleXMLRPCServer.SimpleXMLRPCServer((ip, xmlrpcport), allow_none=True)
        self.xmlrpc_server_0_0.register_instance(self)
        self.xmlrpc_server_0_0_thread = threading.Thread(target=self.xmlrpc_server_0_0.serve_forever)
        self.xmlrpc_server_0_0_thread.daemon = True
        self.xmlrpc_server_0_0_thread.start()
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samprate)
        self.uhd_usrp_source_0.set_center_freq(rxfreq, 0)
        self.uhd_usrp_source_0.set_normalized_gain(rxgain, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0.set_bandwidth(samprate, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samprate)
        self.uhd_usrp_sink_0.set_center_freq(txfreq, 0)
        self.uhd_usrp_sink_0.set_normalized_gain(txgain, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_bandwidth(samprate, 0)
        
        def _txrate_probe():
            while True:
                val = self.ztxrate.rate()
                try:
                    self.set_txrate(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _txrate_thread = threading.Thread(target=_txrate_probe)
        _txrate_thread.daemon = True
        _txrate_thread.start()
            
        
        def _rxrate_probe():
            while True:
                val = self.zrxrate.rate()
                try:
                    self.set_rxrate(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _rxrate_thread = threading.Thread(target=_rxrate_probe)
        _rxrate_thread.daemon = True
        _rxrate_thread.start()
            
        self.qtgui_waterfall_sink_x_1 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samprate, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_1.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_1.enable_grid(False)
        self.qtgui_waterfall_sink_x_1.enable_axis_labels(True)
        
        if not True:
          self.qtgui_waterfall_sink_x_1.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_1.set_plot_pos_half(not True)
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_1.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_1.set_line_alpha(i, alphas[i])
        
        self.qtgui_waterfall_sink_x_1.set_intensity_range(-140, 10)
        
        self._qtgui_waterfall_sink_x_1_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_1_win)
        self.digital_burst_shaper_xx_0 = digital.burst_shaper_cc((([])), 2000, 100, False, "packet_len")
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_gr_complex*1, "Tx'd Packet", ""); self.blocks_tag_debug_0.set_display(True)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((amplitude, ))

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.digital_burst_shaper_xx_0, 0))    
        self.connect((self.digital_burst_shaper_xx_0, 0), (self.uhd_usrp_sink_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_waterfall_sink_x_1, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.zeromq_push_sink_0_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.zrxrate, 0))    
        self.connect((self.zeromq_pull_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.zeromq_pull_source_0, 0), (self.blocks_tag_debug_0, 0))    
        self.connect((self.zeromq_pull_source_0, 0), (self.ztxrate, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "usrp")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_xmlrpcport(self):
        return self.xmlrpcport

    def set_xmlrpcport(self, xmlrpcport):
        self.xmlrpcport = xmlrpcport

    def get_txrate(self):
        return self.txrate

    def set_txrate(self, txrate):
        self.txrate = txrate

    def get_txoutport(self):
        return self.txoutport

    def set_txoutport(self, txoutport):
        self.txoutport = txoutport

    def get_txgain(self):
        return self.txgain

    def set_txgain(self, txgain):
        self.txgain = txgain
        self.uhd_usrp_sink_0.set_normalized_gain(self.txgain, 0)
        	

    def get_txfreq(self):
        return self.txfreq

    def set_txfreq(self, txfreq):
        self.txfreq = txfreq
        self.uhd_usrp_sink_0.set_center_freq(self.txfreq, 0)

    def get_timeout(self):
        return self.timeout

    def set_timeout(self, timeout):
        self.timeout = timeout

    def get_samprate(self):
        return self.samprate

    def set_samprate(self, samprate):
        self.samprate = samprate
        self.uhd_usrp_source_0.set_samp_rate(self.samprate)
        self.uhd_usrp_source_0.set_bandwidth(self.samprate, 0)
        self.uhd_usrp_sink_0.set_samp_rate(self.samprate)
        self.uhd_usrp_sink_0.set_bandwidth(self.samprate, 0)
        self.qtgui_waterfall_sink_x_1.set_frequency_range(0, self.samprate)

    def get_rxrate(self):
        return self.rxrate

    def set_rxrate(self, rxrate):
        self.rxrate = rxrate

    def get_rxport(self):
        return self.rxport

    def set_rxport(self, rxport):
        self.rxport = rxport

    def get_rxoutport(self):
        return self.rxoutport

    def set_rxoutport(self, rxoutport):
        self.rxoutport = rxoutport

    def get_rxip(self):
        return self.rxip

    def set_rxip(self, rxip):
        self.rxip = rxip

    def get_rxgain(self):
        return self.rxgain

    def set_rxgain(self, rxgain):
        self.rxgain = rxgain
        self.uhd_usrp_source_0.set_normalized_gain(self.rxgain, 0)
        	

    def get_rxfreq(self):
        return self.rxfreq

    def set_rxfreq(self, rxfreq):
        self.rxfreq = rxfreq
        self.uhd_usrp_source_0.set_center_freq(self.rxfreq, 0)

    def get_maxnoutput(self):
        return self.maxnoutput

    def set_maxnoutput(self, maxnoutput):
        self.maxnoutput = maxnoutput

    def get_ip(self):
        return self.ip

    def set_ip(self, ip):
        self.ip = ip

    def get_finalsplitport(self):
        return self.finalsplitport

    def set_finalsplitport(self, finalsplitport):
        self.finalsplitport = finalsplitport

    def get_finalsplitip(self):
        return self.finalsplitip

    def set_finalsplitip(self, finalsplitip):
        self.finalsplitip = finalsplitip

    def get_amplitude(self):
        return self.amplitude

    def set_amplitude(self, amplitude):
        self.amplitude = amplitude
        self.blocks_multiply_const_vxx_0.set_k((self.amplitude, ))


def main(top_block_cls=usrp, options=None):

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
