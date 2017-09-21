#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: usrp_hydra
# Description: USRP with hydra
# Generated: Thu Sep 21 16:26:50 2017
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
import hydra
import sip
import sys
import threading
import time


class usrp_hydra(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "usrp_hydra")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("usrp_hydra")
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

        self.settings = Qt.QSettings("GNU Radio", "usrp_hydra")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self._xmlrpcport_config = ConfigParser.ConfigParser()
        self._xmlrpcport_config.read('default')
        try: xmlrpcport = self._xmlrpcport_config.getint("usrp", 'xmlrpcport')
        except: xmlrpcport = 8081
        self.xmlrpcport = xmlrpcport
        self.txrate2 = txrate2 = 0
        self.txrate1 = txrate1 = 0
        self._txgain_config = ConfigParser.ConfigParser()
        self._txgain_config.read('default')
        try: txgain = self._txgain_config.getfloat("usrp", "txgain")
        except: txgain = 0.9
        self.txgain = txgain
        self._timeout_config = ConfigParser.ConfigParser()
        self._timeout_config.read('default')
        try: timeout = self._timeout_config.getint("global", "zmqtimeout")
        except: timeout = 100
        self.timeout = timeout
        self._samprate2_config = ConfigParser.ConfigParser()
        self._samprate2_config.read('default')
        try: samprate2 = self._samprate2_config.getfloat("usrp_hydra", "samprate2")
        except: samprate2 = 1e6
        self.samprate2 = samprate2
        self._samprate1_config = ConfigParser.ConfigParser()
        self._samprate1_config.read('default')
        try: samprate1 = self._samprate1_config.getfloat("usrp_hydra", "samprate1")
        except: samprate1 = 1e6
        self.samprate1 = samprate1
        self._samprate_config = ConfigParser.ConfigParser()
        self._samprate_config.read('default')
        try: samprate = self._samprate_config.getfloat("usrp_hydra", "samprate")
        except: samprate = 1e6
        self.samprate = samprate
        self._rxgain_config = ConfigParser.ConfigParser()
        self._rxgain_config.read('default')
        try: rxgain = self._rxgain_config.getfloat("usrp", "rxgain")
        except: rxgain = 0.9
        self.rxgain = rxgain
        self._maxnoutput_config = ConfigParser.ConfigParser()
        self._maxnoutput_config.read('default')
        try: maxnoutput = self._maxnoutput_config.getint("global", "maxnoutput")
        except: maxnoutput = 100
        self.maxnoutput = maxnoutput
        self._ip_config = ConfigParser.ConfigParser()
        self._ip_config.read('default')
        try: ip = self._ip_config.get("usrp_hydra", "ip")
        except: ip = '1e6'
        self.ip = ip
        self.freq2 = freq2 = 951.2e6
        self.freq1 = freq1 = 950e6
        self._freq_config = ConfigParser.ConfigParser()
        self._freq_config.read('default')
        try: freq = self._freq_config.getfloat("usrp_hydra", "freq")
        except: freq = 950e6
        self.freq = freq
        self._finalsplitport2_config = ConfigParser.ConfigParser()
        self._finalsplitport2_config.read('default')
        try: finalsplitport2 = self._finalsplitport2_config.get("usrp_hydra", "finalsplitport2")
        except: finalsplitport2 = "2300"
        self.finalsplitport2 = finalsplitport2
        self._finalsplitport1_config = ConfigParser.ConfigParser()
        self._finalsplitport1_config.read('default')
        try: finalsplitport1 = self._finalsplitport1_config.get("usrp_hydra", "finalsplitport1")
        except: finalsplitport1 = "2300"
        self.finalsplitport1 = finalsplitport1
        self._finalsplitip2_config = ConfigParser.ConfigParser()
        self._finalsplitip2_config.read('default')
        try: finalsplitip2 = self._finalsplitip2_config.get("usrp_hydra", "finalsplitip2")
        except: finalsplitip2 = "127.0.0.1"
        self.finalsplitip2 = finalsplitip2
        self._finalsplitip1_config = ConfigParser.ConfigParser()
        self._finalsplitip1_config.read('default')
        try: finalsplitip1 = self._finalsplitip1_config.get("usrp_hydra", "finalsplitip1")
        except: finalsplitip1 = "127.0.0.1"
        self.finalsplitip1 = finalsplitip1
        self.amplitude2 = amplitude2 = 0.05
        self.amplitude1 = amplitude1 = 0.05

        ##################################################
        # Blocks
        ##################################################
        self.ztxrate = blocks.probe_rate(gr.sizeof_gr_complex*1, 2000, 0.15)
        self._freq2_range = Range(948e6, 952e6, 50e3, 951.2e6, 200)
        self._freq2_win = RangeWidget(self._freq2_range, self.set_freq2, 'VR2 freq', "counter_slider", float)
        self.top_layout.addWidget(self._freq2_win)
        self._freq1_range = Range(948e6, 952e6, 50e3, 950e6, 200)
        self._freq1_win = RangeWidget(self._freq1_range, self.set_freq1, 'VR1 freq', "counter_slider", float)
        self.top_layout.addWidget(self._freq1_win)
        self._amplitude2_range = Range(0, 1, 0.01, 0.05, 200)
        self._amplitude2_win = RangeWidget(self._amplitude2_range, self.set_amplitude2, 'VR2 amplitude', "counter_slider", float)
        self.top_layout.addWidget(self._amplitude2_win)
        self._amplitude1_range = Range(0, 1, 0.01, 0.05, 200)
        self._amplitude1_win = RangeWidget(self._amplitude1_range, self.set_amplitude1, 'VR1 amplitude', "counter_slider", float)
        self.top_layout.addWidget(self._amplitude1_win)
        self.ztxrate_1 = blocks.probe_rate(gr.sizeof_gr_complex*1, 2000, 0.15)
        self.zeromq_pull_source_0_1 = zeromq.pull_source(gr.sizeof_gr_complex, 1, "tcp://" + finalsplitip2 + ":" + finalsplitport2, timeout, True, -1)
        self.zeromq_pull_source_0 = zeromq.pull_source(gr.sizeof_gr_complex, 1, "tcp://" + finalsplitip1 + ":" + finalsplitport1, timeout, True, -1)
        self.xmlrpc_server_0_0 = SimpleXMLRPCServer.SimpleXMLRPCServer((ip, xmlrpcport), allow_none=True)
        self.xmlrpc_server_0_0.register_instance(self)
        self.xmlrpc_server_0_0_thread = threading.Thread(target=self.xmlrpc_server_0_0.serve_forever)
        self.xmlrpc_server_0_0_thread.daemon = True
        self.xmlrpc_server_0_0_thread.start()
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
        
        def _txrate2_probe():
            while True:
                val = self.ztxrate.rate()
                try:
                    self.set_txrate2(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _txrate2_thread = threading.Thread(target=_txrate2_probe)
        _txrate2_thread.daemon = True
        _txrate2_thread.start()
            
        
        def _txrate1_probe():
            while True:
                val = self.ztxrate.rate()
                try:
                    self.set_txrate1(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _txrate1_thread = threading.Thread(target=_txrate1_probe)
        _txrate1_thread.daemon = True
        _txrate1_thread.start()
            
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samprate, #bw
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
        self.hydra_hydra_sink_0 = hydra.hydra_sink(2, 1024, freq, samprate,
        	 ((freq1, samprate1), 
        	 (freq2, samprate2),
        	 ))
          
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vcc((amplitude2, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((amplitude1, ))

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.hydra_hydra_sink_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.hydra_hydra_sink_0, 1))    
        self.connect((self.hydra_hydra_sink_0, 0), (self.qtgui_waterfall_sink_x_0, 0))    
        self.connect((self.hydra_hydra_sink_0, 0), (self.uhd_usrp_sink_1, 0))    
        self.connect((self.zeromq_pull_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.zeromq_pull_source_0, 0), (self.ztxrate, 0))    
        self.connect((self.zeromq_pull_source_0_1, 0), (self.blocks_multiply_const_vxx_0_0, 0))    
        self.connect((self.zeromq_pull_source_0_1, 0), (self.ztxrate_1, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "usrp_hydra")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_xmlrpcport(self):
        return self.xmlrpcport

    def set_xmlrpcport(self, xmlrpcport):
        self.xmlrpcport = xmlrpcport

    def get_txrate2(self):
        return self.txrate2

    def set_txrate2(self, txrate2):
        self.txrate2 = txrate2

    def get_txrate1(self):
        return self.txrate1

    def set_txrate1(self, txrate1):
        self.txrate1 = txrate1

    def get_txgain(self):
        return self.txgain

    def set_txgain(self, txgain):
        self.txgain = txgain

    def get_timeout(self):
        return self.timeout

    def set_timeout(self, timeout):
        self.timeout = timeout

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
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samprate)

    def get_rxgain(self):
        return self.rxgain

    def set_rxgain(self, rxgain):
        self.rxgain = rxgain

    def get_maxnoutput(self):
        return self.maxnoutput

    def set_maxnoutput(self, maxnoutput):
        self.maxnoutput = maxnoutput

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

    def get_finalsplitport2(self):
        return self.finalsplitport2

    def set_finalsplitport2(self, finalsplitport2):
        self.finalsplitport2 = finalsplitport2

    def get_finalsplitport1(self):
        return self.finalsplitport1

    def set_finalsplitport1(self, finalsplitport1):
        self.finalsplitport1 = finalsplitport1

    def get_finalsplitip2(self):
        return self.finalsplitip2

    def set_finalsplitip2(self, finalsplitip2):
        self.finalsplitip2 = finalsplitip2

    def get_finalsplitip1(self):
        return self.finalsplitip1

    def set_finalsplitip1(self, finalsplitip1):
        self.finalsplitip1 = finalsplitip1

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


def main(top_block_cls=usrp_hydra, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start(100)
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
