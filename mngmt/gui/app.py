import os, sys, time, threading, psutil, subprocess
sys.path.insert(0, os.getcwd())

from PyQt4 import QtGui, QtCore
import pyqtgraph as qtg
import xmlrpc.client
from collections import OrderedDict

from gui import Ui_MainWindow
from mngmt import Manager, Container
from mngmt.container import VirtualRadioSplit, VirtualRadioSingle, USRP, USRPHydra

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

wishful_controller_ip = ("127.0.0.1", 44444)
server = xmlrpc.client.ServerProxy("http://%s:%d" % wishful_controller_ip )

manager = Manager()
manager.addHost(host_name="Regional",
        ip="192.168.10.10:8443",
        cert=("./tests/lxd.crt", "./tests/lxd.key"))
manager.addHost(host_name="Edge",
        ip="192.168.10.20:8443",
        cert=("./tests/lxd.crt", "./tests/lxd.key"))

Container(name='usrp', origin='gnuradio', host='Edge', manageable=False)

bs1 = VirtualRadioSplit(name='vr1tx',
                        host_split1='Regional',
                        host_split2='Regional',
                        host_split3='Regional')
bs2 = VirtualRadioSingle(name='vr2tx',
                            host='Edge',
                            mode='vr2tx')

qtg.setConfigOption('background', (232, 232, 232))
qtg.setConfigOption('foreground', (0, 0, 0))


MAX_ITEMS = 50

class WiSHFULMonitor(threading.Thread):

    def __init__(self, name, stopflag, server, func):
        threading.Thread.__init__(self)
        self.name = name
        self.stopflag = stopflag
        self._func = func
        self.rates = []
        self.server = server
        self._lvalid = None

    def run(self):
        print("Starting thread to monitor " + self.name)
        while not self.stopflag.wait(1):
            self.update()
        print ("Closing thread " + self.name)

    def update(self):
        try:
            s = float(getattr(self.server, "get_" + self._func)())
            if len(self.rates) > 3 and ((s == self.rates[-1]) and s == self.rates[-2] and s == self.rates[-3]):
                self._lvalid = s
                s = 0.0
            elif self.rates[-1] == 0.0 and self._lvalid == s:
                s = 0.0
            self.rates.append(s)
            while len(self.rates) > MAX_ITEMS:
                self.rates.pop(0)
        except Exception as e:
            print(e)
            self.rates.append(0.0)

    def getData(self):
        avgs = []
        for i in range(0, len(self.rates)):
            try:
                avgs.append(sum(self.rates[max(i-5, 0):i]) / len(self.rates[max(0, i-5):i]))
            except:
                avgs.append(self.rates[i])

        return {self.name : avgs}


class ContainerMonitor(object):
    def __init__(self, name, stopflag, labelsEdge, labelsRegional):
        self.name = name
        self.stopflag = stopflag
        self.labelsEdge = labelsEdge
        self.labelsRegional = labelsRegional

    def update(self):
        clist = manager.getLXDContainerList("Edge")
        for i in self.labelsEdge:
            i.setText(", ".join([r.name for r in clist if r.status == 'Running' ]))

        clist = manager.getLXDContainerList("Regional")
        for i in self.labelsRegional:
            i.setText(", ".join([r.name for r in clist if r.status == 'Running' ]))

class RAMMonitor(threading.Thread):

    def __init__(self, name, addr, stopflag):
        threading.Thread.__init__(self)
        self.name = name
        self.stopflag = stopflag

        self.cmd = 'ssh connect@' + addr + ' "python -c \'import psutil; print(psutil.virtual_memory().percent)\'"'

        def getxxx():
            def xxx():
                return subprocess.check_output(self.cmd, stdin=None, stderr=subprocess.STDOUT, shell=True)
            return xxx

        self.getter = getxxx()
        self.rates = [float(self.getter()), ]

    def run(self):
        import signal
        print("Starting thread to monitor " + self.name)
        while not self.stopflag.wait(1):
            self.update()
        print ("Closing thread " + self.name)

    def update(self):
        self.rates.append(float(self.getter()))

        while len(self.rates) > MAX_ITEMS:
            self.rates.pop(0)

    def getData(self):
        avgs = []
        for i in range(0, len(self.rates)):
            try:
                avgs.append(sum(self.rates[max(i-5, 0):i]) / len(self.rates[max(0, i-5):i]))
            except:
                avgs.append(self.rates[i])


        return {self.name : avgs}


class CPUMonitor(threading.Thread):
    def __init__(self, name, addr, stopflag, label):
        threading.Thread.__init__(self)
        self.name = name
        self.stopflag = stopflag
        self.label = label

        self.cmd = 'ssh connect@' + addr + ' "python -c \'import psutil; print(psutil.cpu_percent())\'"'

        def getxxx():
            def xxx():
                return subprocess.check_output(self.cmd, stdin=None, stderr=subprocess.STDOUT, shell=True)
            return xxx

        self.getter = getxxx()
        self.rates = [float(self.getter()), ]

    def run(self):
        print("Starting thread to monitor " + self.name)
        while not self.stopflag.wait(1):
            self.update()
        print ("Closing thread " + self.name)

    def update(self):
        self.rates.append(float(self.getter()))

        while len(self.rates) > MAX_ITEMS:
            self.rates.pop(0)

    def getData(self):
        avgs = []
        for i in range(0, len(self.rates)):
            try:
                avgs.append(sum(self.rates[max(i-5, 0):i]) / len(self.rates[max(0, i-5):i]))
            except:
                avgs.append(self.rates[i])

        clist = manager.getLXDContainerList(self.name)
        self.label.setText(", ".join([r.name for r in clist if r.status == 'Running' ]))

        return {self.name : avgs}


class MonitorList(object):
    def __init__(self, monitors):
        self._monitors = monitors

    def is_alive(self):
        return True if True in [x.is_alive() for x in self._monitors] else False

    def getData(self):
        d = {}
        for e in self._monitors:
            d.update(e.getData())

        return OrderedDict(sorted(d.items()))

    def start(self):
        for e in self._monitors:
            e.start()


class ERMonitor(threading.Thread):
    def __init__(self, name, stopflag, manager, regional_name, edge_name,  monitors, links, label):
        threading.Thread.__init__(self)
        self.name      = name
        self.stopflag = stopflag
        self._manager  = manager
        self._rname = regional_name
        self._ename = edge_name
        self._monitors = monitors
        self._rates     = []
        self._label = label
        self.links = links



    def getData(self):
        return {self.name: self._rates}


    def update(self):
        val = 0
        txt = ""

        for p1, p2 in self.links:
            if p1 not in self._monitors.keys() or p2 not in self._monitors.keys():
                continue
            c1 = self._manager.getContainer(p1)
            c2 = self._manager.getContainer(p2)
            if c1.is_running and c2.is_running:
                if c1._host_name != c2._host_name:
                    tmp = OrderedDict(self._monitors[p1].getData())
                    if len(tmp.keys()) > 1:
                        raise Exception("More than 1 key in hashtable")
                    if len(tmp[list(tmp.keys())[0]]) > 0:
                        val += tmp[list(tmp.keys())[0]][-1]
                        txt += p1 + ", "
            else:
                print(c1.name + ' is not running') if c1.is_running == False else None
                print(c2.name + ' is not running') if c2.is_running == False else None

        self._rates.append(val)
        self._label.setText(txt)

        while len(self._rates) > MAX_ITEMS:
            self._rates.pop(0)

    def run(self):
        for m in self._monitors.values():
            if not m. is_alive():
                m.start()

        print("Starting thread to monitor " + self.name)
        while not self.stopflag.wait(1):
            self.update()
        print ("Closing thread " + self.name)


class Plotter():

    def __init__(self, plot, title, monitor, xrange=None, yrange=None):
        self._plot = plot

        self._monitor = monitor

        plot.setTitle(title)
        plot.setLabel('bottom', 'Time (s)')
        plot.setLabel('left', 'Throughput (Mbps)')

        if xrange is not None:
            plot.setXRange(xrange[0], xrange[1])
        if yrange is not None:
            plot.setYRange(yrange[0], yrange[1])

        plot.addLegend()

        self._lines = {}
        for t, pcolor in zip(monitor.getData(), ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'w']):
            self._lines[t] = plot.plot(pen=pcolor, name=t)

        if not monitor.is_alive():
            monitor.start()

    def update(self):
        if not self._plot.isVisible():
            return

        for l in self._lines:
            self._lines[l].setData(self._monitor.getData()[l], clear = True)

class LCDNumber():
    def __init__(self, plot, monitor, div, avg=False):
        self._plot = plot
        self._monitor = monitor
        self._div = div
        self._avg = avg

    def update(self):
        if not self._plot.isVisible():
            return

        if self._avg == False:
            d = list(self._monitor.getData().values())[0][-1]
            d /= self._div
            self._plot.display(d)
        else:
            vals = list(self._monitor.getData().values())[0]
            d = sum(vals)/len(vals)
            d /= self._div
            self._plot.display(d)


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        def make_it_red(pallete):
            palette.setColor(palette.WindowText, QtGui.QColor(255, 255, 255))
            palette.setColor(palette.Background, QtGui.QColor(255, 0, 0))
            palette.setColor(palette.Light, QtGui.QColor(232, 232, 232))
            palette.setColor(palette.Dark, QtGui.QColor(232, 232, 232))

        def make_it_blue(pallete):
            palette.setColor(palette.WindowText, QtGui.QColor(255, 255, 255))
            palette.setColor(palette.Background, QtGui.QColor(0, 0, 255))
            palette.setColor(palette.Light, QtGui.QColor(232, 232, 232))
            palette.setColor(palette.Dark, QtGui.QColor(232, 232, 232))

        def make_it_green(palette):
            palette.setColor(palette.WindowText, QtGui.QColor(0, 0, 0))
            palette.setColor(palette.Background, QtGui.QColor(0, 255, 0))
            palette.setColor(palette.Light, QtGui.QColor(232, 232, 232))
            palette.setColor(palette.Dark, QtGui.QColor(232, 232, 232))

        self._plotters = []
        self._stop_event = ste = threading.Event()

        # Downlink monitors
        self._vr1Split1DownlinkMon = WiSHFULMonitor(name='Split1 to Split2 Rate',
                                             stopflag=ste,
                                             server = server,
                                             func="vr1tx_split1_downlink")
        self._vr1Split2DownlinkMon = WiSHFULMonitor(name='Split2 to Split3 Rate',
                                             stopflag=ste,
                                             server = server,
                                             func="vr1tx_split2_downlink")
        self._vr1Split3DownlinkMon = WiSHFULMonitor(name='Split3 to USRP rate',
                                             stopflag=ste,
                                             server = server,
                                             func="vr1tx_split3_downlink")
        self._vr2Split1DownlinkMon= WiSHFULMonitor(name='NB-IoT to USRP',
                                      stopflag=ste,
                                      server = server,
                                      func="vr2tx_downlink")
        self._usrpVr1DownlinkMon = WiSHFULMonitor(name='LTE IQ',
                                           stopflag=ste,
                                           server = server,
                                           func="usrp_vr1_downlink")
        self._usrpVr2DownlinkMon = WiSHFULMonitor(name='NB-IoT IQ',
                                           stopflag=ste,
                                           server = server,
                                           func="usrp_vr2_downlink")

        self._erDownlinkMon = ERMonitor(name='Downlink',
                                        stopflag=ste,
                                        manager=manager,
                                        regional_name='Regional',
                                        edge_name='Edge',
                                        label = self.ui.ERDownlinkLabel,
                                        monitors = {
                                            'vr1tx-split1': self._vr1Split1DownlinkMon,
                                            'vr1tx-split2': self._vr1Split2DownlinkMon,
                                            'vr1tx-split3': self._vr1Split3DownlinkMon,
                                            'vr2tx': self._vr2Split1DownlinkMon,
                                            'usrp': self._usrpVr1DownlinkMon,},
                                        links = [('vr1tx-split1', 'vr1tx-split2'),
                                                 ('vr1tx-split2', 'vr1tx-split3'),
                                                 ('vr1tx-split3', 'usrp'),
                                                 ('vr2tx',  'usrp')],
        )

        # Uplink monitors
        self._vr1Split1UplinkMon = WiSHFULMonitor(name='USRP-LTE Uplink',
                                           stopflag=ste,
                                           server = server,
                                           func="vr1tx_split1_uplink")
        self._vr2Split1UplinkMon = WiSHFULMonitor(name='vr2tx',
                                           stopflag=ste,
                                           server = server,
                                           func="vr2tx_uplink")
        self._usrpVr1UplinkMon = WiSHFULMonitor(name='LTE IQ',
                                         stopflag=ste,
                                         server = server,
                                         func="usrp_vr1_uplink")
        self._usrpVr2UplinkMon = WiSHFULMonitor(name='NB-IoT IQ',
                                         stopflag=ste,
                                         server = server,
                                         func="usrp_vr2_uplink")

        self._erUplinkMon = ERMonitor(name='Uplink',
                                      stopflag=ste,
                                      manager=manager,
                                      regional_name='Regional',
                                      edge_name='Edge',
                                      label = self.ui.ERUplinkLabel,
                                      monitors = {
                                          'vr1tx-split1': self._usrpVr1UplinkMon,
                                          'vr2tx': self._usrpVr2UplinkMon,
                                          'usrp': self._usrpVr1UplinkMon},
                                      links = [
                                          ('vr2tx', 'usrp'),
                                          ('vr1tx-split1', 'usrp'),
                                      ],
        )

        # CPU Monitors
        self._regionalCPUMon = CPUMonitor(name='Regional', addr='localhost', stopflag=ste, label = self.ui.regionalCPULabel)
        self._edgeCPUMon     = CPUMonitor(name='Edge', addr='192.168.10.20', stopflag=ste, label =self.ui.edgeCPULabel)

        # RAM Monitors
        self._regionalRAMMon = RAMMonitor(name='Regional', addr = 'localhost', stopflag=ste)
        self._edgeRAMMon     = RAMMonitor(name='Edge', addr = '192.168.10.20', stopflag=ste)

        # plots downlink
        self._plotters.append(
            Plotter(plot=self.ui.vr1DownlinkPlot,
                    title='Downlink VR 1',
                    monitor= MonitorList([
                        self._vr1Split1DownlinkMon,
                        self._vr1Split2DownlinkMon,
                        self._vr1Split3DownlinkMon,]),
                    yrange=(0,31*10**6)
            )
        )
        self._plotters.append(
            Plotter(plot=self.ui.vr2DownlinkPlot,
                    title='Downlink VR 2',
                    monitor= self._vr2Split1DownlinkMon,
                    yrange=(0,31*10**6)
            )
        )

        self._plotters.append(
            Plotter(plot=self.ui.usrpDownlinkPlot,
                    title='Downlink',
                    monitor= MonitorList([self._usrpVr1DownlinkMon, self._usrpVr2DownlinkMon]),
                    yrange=(0,31*10**6)
            )
        )

        # LCD downlinks
        palette = self.ui.vr1Split1DownlinkLCD.palette()
        make_it_red(palette)
        self.ui.vr1Split1DownlinkLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.vr1Split1DownlinkLCD,
                      monitor=self._vr1Split1DownlinkMon,
                      div = 10**6
            )
        )
        palette = self.ui.vr1Split1DownlinkAvgLCD.palette()
        make_it_red(palette)
        self.ui.vr1Split1DownlinkAvgLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.vr1Split1DownlinkAvgLCD,
                      monitor=self._vr1Split1DownlinkMon,
                      div = 10**6,
                      avg=True
            )
        )

        palette = self.ui.vr1Split2DownlinkLCD.palette()
        make_it_green(palette)
        self.ui.vr1Split2DownlinkLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.vr1Split2DownlinkLCD,
                      monitor=self._vr1Split2DownlinkMon,
                      div=10**6
            )
        )
        palette = self.ui.vr1Split2DownlinkAvgLCD.palette()
        make_it_green(palette)
        self.ui.vr1Split2DownlinkAvgLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.vr1Split2DownlinkAvgLCD,
                      monitor=self._vr1Split2DownlinkMon,
                      div = 10**6,
                      avg=True
            )
        )

        palette = self.ui.vr1Split3DownlinkLCD.palette()
        make_it_blue(palette)
        self.ui.vr1Split3DownlinkLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.vr1Split3DownlinkLCD,
                      monitor=self._vr1Split3DownlinkMon,
                      div=10**6
            )
        )
        palette = self.ui.vr1Split3DownlinkAvgLCD.palette()
        make_it_blue(palette)
        self.ui.vr1Split3DownlinkAvgLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.vr1Split3DownlinkAvgLCD,
                      monitor=self._vr1Split3DownlinkMon,
                      div = 10**6,
                      avg=True
            )
        )

        palette = self.ui.vr2Split1DownlinkLCD.palette()
        make_it_red(palette)
        self.ui.vr2Split1DownlinkLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.vr2Split1DownlinkLCD,
                      monitor=self._vr2Split1DownlinkMon,
                      div=10**6
            )
        )
        palette = self.ui.vr2Split1DownlinkAvgLCD.palette()
        make_it_red(palette)
        self.ui.vr2Split1DownlinkAvgLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.vr2Split1DownlinkAvgLCD,
                      monitor=self._vr2Split1DownlinkMon,
                      div=10**6,
                      avg=True
            )
        )

        palette = self.ui.usrpVr1DownlinkLCD.palette()
        make_it_red(palette)
        self.ui.usrpVr1DownlinkLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.usrpVr1DownlinkLCD,
                      monitor=self._usrpVr1DownlinkMon,
                      div=10**6
            )
        )
        palette = self.ui.usrpVr1DownlinkAvgLCD.palette()
        make_it_red(palette)
        self.ui.usrpVr1DownlinkAvgLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.usrpVr1DownlinkAvgLCD,
                      monitor=self._usrpVr1DownlinkMon,
                      div=10**6,
                      avg=True
            )
        )
        palette = self.ui.usrpVr2DownlinkLCD.palette()
        make_it_green(palette)
        self.ui.usrpVr2DownlinkLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.usrpVr2DownlinkLCD,
                      monitor=self._usrpVr2DownlinkMon,
                      div=10**6
            )
        )
        palette = self.ui.usrpVr2DownlinkAvgLCD.palette()
        make_it_green(palette)
        self.ui.usrpVr2DownlinkAvgLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.usrpVr2DownlinkAvgLCD,
                      monitor=self._usrpVr2DownlinkMon,
                      div=10**6,
                      avg=True
            )
        )


        # plots uplink
        self._plotters.append(
            Plotter(plot=self.ui.vr1UplinkPlot,
                    title='Uplink VR 1',
                    monitor=self._vr1Split1UplinkMon,
                    yrange=(0,31*10**6)
            )
        )
        self._plotters.append(
            Plotter(plot=self.ui.vr2UplinkPlot,
                    title='Uplink VR2',
                    monitor= self._vr2Split1UplinkMon,
                    yrange=(0,31*10**6)
            )
        )
        self._plotters.append(
            Plotter(plot=self.ui.usrpUplinkPlot,
                    title='Uplink',
                    monitor= MonitorList([self._usrpVr1UplinkMon, self._usrpVr2UplinkMon]),
                    yrange=(0,31*10**6)
            )
        )


        # LCD uplink
        palette = self.ui.vr1Split1UplinkLCD.palette()
        make_it_red(palette)
        self.ui.vr1Split1UplinkLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.vr1Split1UplinkLCD,
                      monitor=self._vr1Split1UplinkMon,
                      div=10**6
            )
        )
        palette = self.ui.vr1Split1UplinkAvgLCD.palette()
        make_it_red(palette)
        self.ui.vr1Split1UplinkAvgLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.vr1Split1UplinkAvgLCD,
                      monitor=self._vr1Split1UplinkMon,
                      div=10**6,
                      avg=True
            )
        )

        palette = self.ui.vr2Split1UplinkLCD.palette()
        make_it_red(palette)
        self.ui.vr2Split1UplinkLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.vr2Split1UplinkLCD,
                      monitor=self._vr2Split1UplinkMon,
                      div=10**6
            )
        )
        palette = self.ui.vr2Split1UplinkAvgLCD.palette()
        make_it_red(palette)
        self.ui.vr2Split1UplinkAvgLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.vr2Split1UplinkAvgLCD,
                      monitor=self._vr2Split1UplinkMon,
                      div=10**6,
                      avg=True
            )
        )

        palette = self.ui.usrpVr1UplinkLCD.palette()
        make_it_red(palette)
        self.ui.usrpVr1UplinkLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.usrpVr1UplinkLCD,
                      monitor=self._usrpVr1UplinkMon,
                      div=10**6
            )
        )
        palette = self.ui.usrpVr1UplinkAvgLCD.palette()
        make_it_red(palette)
        self.ui.usrpVr1UplinkAvgLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.usrpVr1UplinkAvgLCD,
                      monitor=self._usrpVr1UplinkMon,
                      div=10**6,
                      avg=True,
            )
        )

        palette = self.ui.usrpVr2UplinkLCD.palette()
        make_it_green(palette)
        self.ui.usrpVr2UplinkLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.usrpVr2UplinkLCD,
                      monitor=self._usrpVr2UplinkMon,
                      div=10**6
            )
        )
        palette = self.ui.usrpVr2UplinkAvgLCD.palette()
        make_it_green(palette)
        self.ui.usrpVr2UplinkAvgLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.usrpVr2UplinkAvgLCD,
                      monitor=self._usrpVr2UplinkMon,
                      div=10**6,
                      avg=True,
            )
        )

        # ER Downlink
        self._plotters.append(
            Plotter(plot=self.ui.ERDownlinkPlot,
                    title='Downlink',
                    monitor= self._erDownlinkMon,
                    yrange=(0,31*10**6)
            )
        )
        palette = self.ui.ERDownlinkLCD.palette()
        make_it_red(palette)
        self.ui.ERDownlinkLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.ERDownlinkLCD,
                      monitor=self._erDownlinkMon,
                      div=10**6
            )
        )
        palette = self.ui.ERDownlinkAvgLCD.palette()
        make_it_red(palette)
        self.ui.ERDownlinkAvgLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.ERDownlinkAvgLCD,
                      monitor=self._erDownlinkMon,
                      div=10**6,
                      avg=True
            )
        )
        # ER Uplink
        self._plotters.append(
            Plotter(plot=self.ui.ERUplinkPlot,
                    title='Uplink',
                    monitor= self._erUplinkMon,
                    yrange=(0,31*10**6)
            )
        )

        palette = self.ui.ERUplinkLCD.palette()
        make_it_red(palette)
        self.ui.ERUplinkLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.ERUplinkLCD,
                      monitor=self._erUplinkMon,
                      div=10**6
            )
        )
        palette = self.ui.ERUplinkAvgLCD.palette()
        make_it_red(palette)
        self.ui.ERUplinkAvgLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.ERUplinkAvgLCD,
                      monitor=self._erUplinkMon,
                      div=10**6,
                      avg=True
            )
        )


        # CPU Plots
        self._plotters.append(
            Plotter(plot=self.ui.edgeCPUPlot,
                    title='Edge CPU usage [%]',
                    monitor= self._edgeCPUMon,
                    yrange=(0,100),
            )
        )
        self._plotters.append(
            Plotter(plot=self.ui.regionalCPUPlot,
                    title='Regional CPU usage [%]',
                    monitor=  self._regionalCPUMon,
                    yrange=(0,100),
            )
        )

        # CPU LCD
        palette = self.ui.edgeCPULCD.palette()
        make_it_red(palette)
        self.ui.edgeCPULCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.edgeCPULCD,
                      monitor=self._edgeCPUMon,
                      div = 1.0
            )
        )
        palette = self.ui.edgeCPUAvgLCD.palette()
        make_it_red(palette)
        self.ui.edgeCPUAvgLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.edgeCPUAvgLCD,
                      monitor=self._edgeCPUMon,
                      div = 1.0,
                      avg = True
            )
        )


        palette = self.ui.regionalCPULCD.palette()
        make_it_red(palette)
        self.ui.regionalCPULCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.regionalCPULCD,
                      monitor=self._regionalCPUMon,
                      div = 1.0
            )
        )
        palette = self.ui.regionalCPUAvgLCD.palette()
        make_it_red(palette)
        self.ui.regionalCPUAvgLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.regionalCPUAvgLCD,
                      monitor=self._regionalCPUMon,
                      div = 1.0,
                      avg = True
            )
        )

        # RAM PLOTS
        self._plotters.append(
            Plotter(plot=self.ui.regionalRAMPlot,
                    title='Regional RAM usage [%]',
                    monitor=  self._regionalRAMMon,
                    yrange=(0,100),
            )
        )

        self._plotters.append(
            Plotter(plot=self.ui.edgeRAMPlot,
                    title='Edge RAM usage [%]',
                    monitor=  self._edgeRAMMon,
                    yrange=(0,100),
            )
        )

        # RAM LCDs
        palette = self.ui.regionalRAMLCD.palette()
        make_it_red(palette)
        self.ui.regionalRAMLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.regionalRAMLCD,
                      monitor=self._regionalRAMMon,
                      div = 1.0
            )
        )
        palette = self.ui.regionalRAMAvgLCD.palette()
        make_it_red(palette)
        self.ui.regionalRAMAvgLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.regionalRAMAvgLCD,
                      monitor=self._regionalRAMMon,
                      div = 1.0,
                      avg = True
            )
        )

        palette = self.ui.edgeRAMLCD.palette()
        make_it_red(palette)
        self.ui.edgeRAMLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.edgeRAMLCD,
                      monitor=self._edgeRAMMon,
                      div = 1.0
            )
        )
        palette = self.ui.edgeRAMAvgLCD.palette()
        make_it_red(palette)
        self.ui.edgeRAMAvgLCD.setPalette(palette)
        self._plotters.append(
            LCDNumber(plot=self.ui.edgeRAMAvgLCD,
                      monitor=self._edgeRAMMon,
                      div = 1.0,
                      avg = True
            )
        )

        self._plotters.append(
                ContainerMonitor(name = "containerMonitor",
                    stopflag = ste,
                    labelsEdge = (self.ui.edgeCPULabel, self.ui.edgeRAMLabel),
                    labelsRegional = (self.ui.regionalCPULabel, self.ui.regionalRAMLabel),
                    )
        )

        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._updatePlot)
        self._timer.start(1000)

    def migrateVr1Split1(self, button):
        server.stop_monitoring("vr1tx-split1")
        split_loc = str(button.text())
        bs1.migrate('vr1tx-split1', split_loc)

        if split_loc == "Regional":
            self.ui.vr1SplitView.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/images/vr1_split_d.jpg")))
        elif split_loc == "Edge":
            self.ui.vr1SplitView.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/images/vr1_split_c.jpg")))
        else:
            print("Unknown remote location at Vr1Split2: " + str(split_loc))

    def migrateVr1Split2(self, button):
        server.stop_monitoring("vr1tx-split1")
        server.stop_monitoring("vr1tx-split2")
        server.stop_monitoring("vr1tx-split3")
        split_loc = str(button.text())

        bs1.stop()
        bs1._bundle['vr1tx-split2'] = Container(name='vr1tx-split2', origin='gnuradio', host=split_loc)
        bs1.start()

        if split_loc == "Regional":
            self.ui.vr1SplitView.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/images/vr1_split_b.jpg")))
        elif split_loc == "Edge":
            self.ui.vr1SplitView.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/images/vr1_split_c.jpg")))
        else:
            print("Unknown remote location at Vr1Split2: " + str(split_loc))

    def migrateVr1Split3(self, button):
        server.stop_monitoring("vr1tx-split3")
        split_loc = str(button.text())
        bs1.migrate('vr1tx-split3', split_loc)

        if split_loc == "Regional":
            self.ui.vr2SplitView.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/images/vr1_split_a.jpg")))
        elif split_loc == "Edge":
            self.ui.vr2SplitView.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/images/vr1_split_b.jpg")))
        else:
            print("Unknown remote location at Vr1Split3: " + str(split_loc))

        updateCPUPplot()
        updateRAMplot()


    def vr1Toogled(self, toogled):
        if self.ui.vr1ToogleAll.text() == "Stop All":
            server.stop_monitoring("vr1tx-split1")
            server.stop_monitoring("vr1tx-split2")
            server.stop_monitoring("vr1tx-split3")
            bs1.stop()
            self.ui.vr1ToogleAll.setText("Start All")

        elif self.ui.vr1ToogleAll.text() == "Start All":
            bs1.start()
            self.ui.vr1ToogleAll.setText("Stop All")


    def vr1MigrateAllEdge(self, toogled):
        print("--------------------------------------------------------------")
        server.stop_monitoring("vr1tx-split1")
        server.stop_monitoring("vr1tx-split2")
        server.stop_monitoring("vr1tx-split3")
 
        print("11111111111111111111111111111111111111111111111111111111111111")
        bs1.stop()
        print("22222222222222222222222222222222222222222222222222222222222222")
        bs1._bundle['vr1tx-split1'] = Container(name='vr1tx-split1', origin='gnuradio', host='Edge')
        bs1._bundle['vr1tx-split2'] = Container(name='vr1tx-split2', origin='gnuradio', host='Edge')
        bs1._bundle['vr1tx-split3'] = Container(name='vr1tx-split3', origin='gnuradio', host='Edge')
        bs1.start()

        print("33333333333333333333333333333333333333333333333333333333333333")

        self.ui.vr1Split1RadioEdge.setChecked(True)
        self.ui.vr1Split2RadioEdge.setChecked(True)
        self.ui.vr1Split3RadioEdge.setChecked(True)

    def vr1MigrateAllRegional(self, toogled):
        server.stop_monitoring("vr1tx-split1")
        server.stop_monitoring("vr1tx-split2")
        server.stop_monitoring("vr1tx-split3")

        bs1.stop()
        bs1._bundle['vr1tx-split1'] = Container(name='vr1tx-split1', origin='gnuradio', host='Regional')
        bs1._bundle['vr1tx-split2'] = Container(name='vr1tx-split2', origin='gnuradio', host='Regional')
        bs1._bundle['vr1tx-split3'] = Container(name='vr1tx-split3', origin='gnuradio', host='Regional')
        bs1.start()

        self.ui.vr1Split1RadioRegional.setChecked(True)
        self.ui.vr1Split2RadioRegional.setChecked(True)
        self.ui.vr1Split3RadioRegional.setChecked(True)

    def migrateVr2Split(self, button):
        server.stop_monitoring("vr2tx")
        split_loc = str(button.text())
        bs2.migrate(split_loc)

        if split_loc == "Regional":
            self.ui.vr2SplitView.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/images/vr2_split_a.jpg")))
        elif split_loc == "Edge":
            self.ui.vr2SplitView.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/images/vr2_split_b.jpg")))
        else:
            print("Unknown remote location at Vr2Split: " + str(split_loc))

    def vr2Toogled(self, toogled):
        if self.ui.vr2ToogleAll.text() == "Stop All":
            server.stop_monitoring("vr2tx")
            bs2.stop()
            self.ui.vr2ToogleAll.setText("Start All")
        elif self.ui.vr2ToogleAll.text() == "Start All":
            bs2.start()
            self.ui.vr2ToogleAll.setText("Stop All")

    def vr1Amplitude(self, value):
        server.set_vr1_amplitude(value/1000.0)

    def vr2Amplitude(self, value):
        server.set_vr2_amplitude(value/1000.0)

    def closeEvent(self, event):
        self._stop_event.set()
        manager.stopAll()

    def _updatePlot(self):
        for p in self._plotters:
            p.update()


def init():
    manager.create(bs1)
    bs1.start()
    while bs1.has_ipaddr is False:
        print('waiting ip bs1')
        time.sleep(1)

    manager.create(bs2)
    bs2.start()
    while bs2.has_ipaddr is False:
        print('waiting ip bs2')
        time.sleep(1)

if __name__ == '__main__':
    init()
    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
