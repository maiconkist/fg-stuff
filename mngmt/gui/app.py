import os, sys, time, threading
sys.path.insert(0, os.getcwd())

from PyQt4 import QtGui, QtCore
import pyqtgraph as qtg

from gui import Ui_MainWindow
from mngmt import Manager
from mngmt.container import VirtualRadioSplit, VirtualRadioSingle, USRP, USRPHydra


manager = Manager()
manager.addHost(host_name="Regional",
                 ip="192.168.10.10:8443",
                 cert=("./tests/lxd.crt", "./tests/lxd.key"))
manager.addHost(host_name="Edge",
                ip="192.168.10.20:8443",
                cert=("./tests/lxd.crt", "./tests/lxd.key"))

bs1 = VirtualRadioSplit(name='vr1tx',
                        host_split1='Regional',
                        host_split2='Regional',
                        host_split3='Regional')

bs2 = VirtualRadioSingle(name='vr2tx',
                            host='Regional',
                            mode='vr2tx')

qtg.setConfigOption('background', (232, 232, 232))
qtg.setConfigOption('foreground', (0, 0, 0))

class Monitor(threading.Thread):
    def __init__(self, name, stopflag, ip, port, params):
        threading.Thread.__init__(self)
        self.name = name
        self.stopflag = stopflag
        self._params = params

        import xmlrpclib
        self.server = xmlrpclib.ServerProxy("http://%s:%d" % (ip, port))
        self.rates = {k: [] for k in self._params}

    def run(self):
        import signal
        print("Starting thread to monitor " + self.name)
        while not self.stopflag.wait(1):
            self.update()
        print ("Closing thread " + self.name)

    def update(self):
        for k in self.rates:
            try:
                s = [float(getattr(self.server, "get_" + param[0])()) * param[1] for param in self._params[k]]
                self.rates[k].append(sum(s))
            except Exception as e:
                self.rates[k].append(0.0)

        print self.rates

    def getData(self):
        """
        \return dict in the form {'name': val, 'name2', val}
        """
        return self.rates

class Plotter():
    MAX_ITEMS = 30

    def __init__(self, plot, title, monitor):
        self._plot = plot

        self._monitor = monitor

        plot.setTitle(title)
        plot.setLabel('bottom', 'Time (s)')
        plot.setLabel('left', 'Throughput (Mbps)')

        plot.addLegend()

        self._lines = {}
        for t, pcolor in zip(monitor.getData(), ['r', 'b', 'g']):
            self._lines[t] = plot.plot(pen=pcolor, name=t)

        monitor.start()

    def update(self):
        for l in self._lines:
            self._lines[l].setData(self._monitor.getData()[l], clear = True)


class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._plotters = []
        self._stop_event = ste = threading.Event()
        self._plotters.append(
            Plotter(plot=self.ui.vr1Split1Plot,
                    title='Split 1',
                    monitor=Monitor(name='vr1-split1',
                                    stopflag=ste,
                                    ip='192.168.10.101',
                                    port=8081,
                                    params={'Downlink': [('rate0', 8), ('rate1', 8)],
                                            'Uplink': [('rateRx', 8), ]})
            ))

        self._plotters.append(
            Plotter(plot=self.ui.vr1Split2Plot,
                    title='Split 2',
                    monitor=Monitor(name='vr1-split2',
                                    stopflag=ste,
                                    ip='192.168.10.102',
                                    port=8082,
                                    params={'Downlink': [('rate', 32), ]},)
            ))
        self._plotters.append(
            Plotter(plot=self.ui.vr1Split3Plot,
                    title='Split 3',
                    monitor=Monitor(name='vr1-split3',
                                    stopflag=ste,
                                    ip='192.168.10.103',
                                    port=8083,
                                    params={'Downlink': [('rate', 32), ]},)
            ))
        self._plotters.append(
            Plotter(plot=self.ui.vr2Split1Plot,
                    title='Split 1',
                    monitor=Monitor(name='vr2tx',
                                    stopflag=ste,
                                    ip='192.168.10.113',
                                    port=8081,
                                    params={'Downlink': [('tx_goodput', 8), ]},)
            ))
        self._plotters.append(
            Plotter(plot=self.ui.usrpVr1TxPlot,
                    title='VR1 IQ Downlink',
                    monitor=Monitor(name='usrpvr1',
                                    stopflag=ste,
                                    ip='192.168.10.104',
                                    port=8084,
                                    params={'Downlink': [('vr1_iq_txrate', 32), ]},)
            ))
        self._plotters.append(
            Plotter(plot=self.ui.usrpVr2TxPlot,
                    title='VR2 IQ Downlink',
                    monitor=Monitor(name='usrpvr2',
                                    stopflag=ste,
                                    ip='192.168.10.104',
                                    port=8084,
                                    params={'Downlink': [('vr2_iq_txrate', 32), ]},)
            ))
        self._plotters.append(
            Plotter(plot=self.ui.usrpTxPlot,
                    title='Container-USRP',
                    monitor=Monitor(name='usrp',
                                    stopflag=ste,
                                    ip='192.168.10.104',
                                    port=8084,
                                    params={'Downlink': [('usrp_iq_txrate', 32), ]},)
            ))


        self._plotters.append(
            Plotter(plot=self.ui.vr1DownlinkPlot,
                    title='Container-USRP',
                    monitor=Monitor(name='usrp',
                                    stopflag=ste,
                                    ip='192.168.10.104',
                                    port=8084,
                                    params={'Downlink': [('usrp_iq_txrate', 32), ]},)
            ))
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._updatePlot)
        self._timer.start(1000)


    def migrateVr1Split1(self, button):
        split_loc = str(button.text())
        bs1.migrate('vr1tx-split1', split_loc)

    def migrateVr1Split2(self, button):
        split_loc = str(button.text())
        bs1.migrate('vr1tx-split2', split_loc)

    def migrateVr1Split3(self, button):
        split_loc = str(button.text())
        bs1.migrate('vr1tx-split3', split_loc)

    def migrateVr2Split(self, button):
        split_loc = str(button.text())
        bs2.migrate(split_loc)

    def closeEvent(self, event):
        self._stop_event.set()
        manager.stopAll()

    def _updatePlot(self):
        print("Updating")
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
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())
