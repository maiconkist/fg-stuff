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
        self.params = params
        self.stopflag = stopflag

        import xmlrpclib
        self.server = xmlrpclib.ServerProxy("http://%s:%d" % (ip, port))

        self.rates = {k[0]:0 for k in self.params}


    def run(self):
        import signal
        print("Starting thread to monitor " + self.name)
        while not self.stopflag.wait(1):
            self.update()

        print ("Closing thread " + self.name)

    def update(self):
        for k in self.rates.iterkeys():
            try:
                self.rates[k] = float(getattr(self.server, "get_" + k)())
            except Exception as e:
                print(e)
                self.rates[k] = 0.0

    def getValue(self):
        x = sum([self.rates[k]*v for k, v in self.params])
        print(self.name + ': ' + str(x))
        return x

    def __str__(self):
        return "{}:\tn_elems: {:8.2f},\t{}: {:15.2f}".format(
                self.name,
                sum([k for k in self.rates.itervalues()]),
                self.params[0][0].rjust(15),
                sum([self.rates[k]*v for k, v in self.params]),
                )


class Plotter():
    MAX_ITEMS = 30

    def __init__(self, plot, title, monitor):
        self._plot = plot
        self._monitor = monitor

        plot.setTitle(title)
        plot.setLabel('bottom', 'Time (s)')
        plot.setLabel('left', 'Throughput (Mbps)')

        self._x = [0, ]
        self._y = [0, ]

        monitor.start()

    def _getData(self):
        import random
        import numpy as np

        self._x.append(self._x[-1] + 1)
        self._y.append(self._monitor.getValue())

        while len(self._x) > Plotter.MAX_ITEMS:
            del self._x[0]
            del self._y[0]

    def update(self):
        self._getData()
        self._plot.plot(self._x, self._y, clear = True)


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
                                    params=[('rate0', 8), ('rate1', 8)])
            ))

        self._plotters.append(
            Plotter(plot=self.ui.vr1Split2Plot,
                    title='Split 2',
                    monitor=Monitor(name='vr1-split2',
                                    stopflag=ste,
                                    ip='192.168.10.102',
                                    port=8082,
                                    params=[('rate', 32), ]),
            ))
        self._plotters.append(
            Plotter(plot=self.ui.vr1Split3Plot,
                    title='Split 3',
                    monitor=Monitor(name='vr1-split3',
                                    stopflag=ste,
                                    ip='192.168.10.103',
                                    port=8083,
                                    params=[('rate', 32), ]),
            ))
        self._plotters.append(
            Plotter(plot=self.ui.vr2Split1Plot,
                    title='Split 1',
                    monitor=Monitor(name='vr2tx',
                                    stopflag=ste,
                                    ip='192.168.10.113',
                                    port=8081,
                                    params=[('tx_goodput', 8), ]),
            ))
        self._plotters.append(
            Plotter(plot=self.ui.usrpTxPlot,
                    title='Container-USRP',
                    monitor=Monitor(name='usrp',
                                    stopflag=ste,
                                    ip='192.168.10.104',
                                    port=8084,
                                    params=[('usrp_iq_txrate', 32), ]),
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
