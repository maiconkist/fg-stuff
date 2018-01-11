import os, sys, time, threading
sys.path.insert(0, os.getcwd())

from PyQt4 import QtGui, QtCore
import pyqtgraph as qtg

from gui import Ui_MainWindow
from mngmt import Manager, Container
from mngmt.container import VirtualRadioSplit, VirtualRadioSingle, USRP, USRPHydra

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
                            host='Regional',
                            mode='vr2tx')

qtg.setConfigOption('background', (232, 232, 232))
qtg.setConfigOption('foreground', (0, 0, 0))

class Monitor(threading.Thread):
    MAX_ITEMS = 50

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

                while len(self.rates[k]) > Monitor.MAX_ITEMS:
                    self.rates[k].pop(0)

            except Exception as e:
                self.rates[k].append(0.0)

    def getData(self):
        """
        \return dict in the form {'name': val, 'name2', val}
        """
        return self.rates


class MonitorList(object):
    def __init__(self, monitors):
        self._monitors = monitors

    def getData(self):
        d = {}
        for e in self._monitors:
            d.update(e.getData())
        return d

    def start(self):
        for e in self._monitors:
            e.start()


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
        for t, pcolor in zip(monitor.getData(), ['r', 'b', 'g', 'c', 'm', 'y', 'k', 'w']):
            self._lines[t] = plot.plot(pen=pcolor, name=t)

        monitor.start()

    def update(self):
        for l in self._lines:
            self._lines[l].setData(self._monitor.getData()[l], clear = True)


class ERMonitor(object):
    def __init__(self, name, stopflag, manager, regional_name, edge_name,  monitors):
        self.name      = name
        self._manager  = manager
        self._rname = regional_name
        self._ename = edge_name
        self._monitors = monitors
        self._rates     = []


        self.links = [
            ('vr1tx-split1', 'vr1tx-split2'),
            ('vr1tx-split2', 'vr1tx-split3'),
            ('vr1tx-split3', 'usrp'),
            ('vr2tx',  'usrp')
        ]

    def getData(self):
        val = 0
        for p1, p2 in self.links:
            c1 = self._manager.getContainer(p1)
            c2 = self._manager.getContainer(p2)
            if c1.is_running and c2.is_running:
                if c1._host_name != c2._host_name:
                    print('Adding: ' + c1.name)
                    tmp = self._monitors[p1].getData()
                    if len(tmp['Downlink']) > 0:
                        val += tmp['Downlink'][-1]
            else:
                print(c1.name + ' is not running') if c1.is_running == False else None
                print(c2.name + ' is not running') if c2.is_running == False else None

        self._rates.append(val)

        while len(self._rates) > Monitor.MAX_ITEMS:
            self._rates.pop(0)

        return {'Downlink': self._rates}

    def start(self):
        for m in self._monitors.itervalues():
            m.start()


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._plotters = []
        self._stop_event = ste = threading.Event()
        #self._plotters.append(
        #    Plotter(plot=self.ui.vr1Split1Plot,
        #            title='Split 1',
        #            monitor=Monitor(name='vr1-split1',
        #                            stopflag=ste,
        #                            ip='192.168.10.101',
        #                            port=8081,
        #                            params={'Downlink': [('rate0', 8), ('rate1', 8)],
        #                                    'Uplink': [('rateRx', 8), ]})
        #    )
        #)
        #self._plotters.append(
        #    Plotter(plot=self.ui.vr1Split2Plot,
        #            title='Split 2',
        #            monitor=Monitor(name='vr1-split2',
        #                            stopflag=ste,
        #                            ip='192.168.10.102',
        #                            port=8082,
        #                            params={'Downlink': [('rate', 32), ]},)
        #    )
        #)
        #self._plotters.append(
        #    Plotter(plot=self.ui.vr1Split3Plot,
        #            title='Split 3',
        #            monitor=Monitor(name='vr1-split3',
        #                            stopflag=ste,
        #                            ip='192.168.10.103',
        #                            port=8083,
        #                            params={'Downlink': [('rate', 32), ]},)
        #    )
        #)
        #self._plotters.append(
        #    Plotter(plot=self.ui.vr2Split1Plot,
        #            title='VR 2',
        #            monitor=Monitor(name='vr2tx',
        #                            stopflag=ste,
        #                            ip='192.168.10.113',
        #                            port=8081,
        #                            params={'Downlink': [('tx_goodput', 8), ]},)
        #    )
        #)
        #self._plotters.append(
        #    Plotter(plot=self.ui.usrpVr1TxPlot,
        #            title='VR1 IQ Downlink',
        #            monitor=Monitor(name='usrpvr1',
        #                            stopflag=ste,
        #                            ip='192.168.10.104',
        #                            port=8084,
        #                            params={'Downlink': [('vr1_iq_txrate', 32), ]},)
        #    )
        #)
        #self._plotters.append(
        #    Plotter(plot=self.ui.usrpVr2TxPlot,
        #            title='VR2 IQ Downlink',
        #            monitor=Monitor(name='usrpvr2',
        #                            stopflag=ste,
        #                            ip='192.168.10.104',
        #                            port=8084,
        #                            params={'Downlink': [('vr2_iq_txrate', 32), ]},)
        #    )
        #)
        #self._plotters.append(
        #    Plotter(plot=self.ui.usrpTxPlot,
        #            title='Container-USRP',
        #            monitor=Monitor(name='usrp',
        #                            stopflag=ste,
        #                            ip='192.168.10.104',
        #                            port=8084,
        #                            params={'Downlink': [('usrp_iq_txrate', 32), ]},)
        #    )
        #)

        self._plotters.append(
            Plotter(plot=self.ui.vr1DownlinkPlot,
                    title='Downlink VR 1',
                    monitor= MonitorList([
                        #Monitor(name='usrp',
                                #stopflag=ste,
                                #ip='192.168.10.104',
                                #port=8084,
                                #params={'Container-USRP': [('usrp_iq_txrate', 32), ]},),
                        Monitor(name='split1',
                                stopflag=ste,
                                ip='192.168.10.101',
                                port=8081,
                                params={'VR1 Split 1': [('rate0', 8), ('rate1', 8)]},),
                        Monitor(name='split2',
                                stopflag=ste,
                                ip='192.168.10.102',
                                port=8082,
                                params={'VR1 Split 2': [('rate', 32), ]},),
                        Monitor(name='split3',
                                stopflag=ste,
                                ip='192.168.10.103',
                                port=8083,
                                params={'VR1 Split 3': [('rate', 32), ]},),
                    ])
            )
        )
        self._plotters.append(
            Plotter(plot=self.ui.vr1UplinkPlot,
                    title='Uplink VR 1',
                    monitor= MonitorList([
                        Monitor(name='split1',
                                stopflag=ste,
                                ip='192.168.10.101',
                                port=8081,
                                params={'Split 1': [('rateRx', 8)]},),
                    ])
            )
        )

        self._plotters.append(
            Plotter(plot=self.ui.vr2DownlinkPlot,
                    title='Downlink VR 2',
                    monitor= Monitor(name='vr2',
                                     stopflag=ste,
                                     ip='192.168.10.113',
                                     port=8081,
                                     params={'VR2': [('tx_iq_rate', 32), ]},),
            )
        )
        self._plotters.append(
            Plotter(plot=self.ui.vr2UplinkPlot,
                    title='Uplink VR2',
                    monitor= Monitor(name='vr2',
                                     stopflag=ste,
                                     ip='192.168.10.104',
                                     port=8084,
                                     params={'VR2': [('rx_goodput', 8), ]},),
            )
        )

        self._plotters.append(
            Plotter(plot=self.ui.usrpDownlinkPlot,
                    title='Downlink',
                    monitor= Monitor(name='usrp',
                                     stopflag=ste,
                                     ip='192.168.10.104',
                                     port=8084,
                                     params={'VR1 IQ': [('vr1_iq_txrate', 32), ],
                                             'VR2 IQ': [('vr2_iq_txrate', 32), ]},
                    ),
            )
        )
        self._plotters.append(
            Plotter(plot=self.ui.usrpUplinkPlot,
                    title='Uplink',
                    monitor= Monitor(name='usrp',
                                     stopflag=ste,
                                     ip='192.168.10.104',
                                     port=8084,
                                     params={'VR1 IQ': [('vr1_iq_rxrate', 32), ],
                                             'VR2 IQ': [('vr2_iq_rxrate', 32), ]},
                    ),
            )
        )


        vr1Split1Monitor = Monitor(name='vr1split1',
                                stopflag=ste,
                                ip='192.168.10.101',
                                port=8081,
                                params={'Downlink': [('rate0', 8), ('rate1', 8)]},)
        vr1Split2Monitor = Monitor(name='vr1split2',
                                stopflag=ste,
                                ip='192.168.10.102',
                                port=8082,
                                params={'Downlink': [('rate', 32), ]},)
        vr1Split3Monitor = Monitor(name='vr1split3',
                                stopflag=ste,
                                ip='192.168.10.103',
                                port=8083,
                                params={'Downlink': [('rate', 32)]},)
        vr2TxMonitor = Monitor(name='vr2',
                                stopflag=ste,
                                ip='192.168.10.113',
                                port=8081,
                                params={'Downlink': [('tx_iq_rate', 32)]},)

        self._plotters.append(
            Plotter(plot=self.ui.ERDownlinkPlot,
                    title='Downlink',
                    monitor= ERMonitor(name='erDownlink',
                                       stopflag=ste,
                                       manager=manager,
                                       regional_name='Regional',
                                       edge_name='Edge',
                                       monitors = {'vr1tx-split1': vr1Split1Monitor, 'vr1tx-split2': vr1Split2Monitor, 'vr1tx-split3': vr1Split3Monitor, 'vr2tx': vr2TxMonitor}
                    ),
            )
        )

        self._plotters.append(
            Plotter(plot=self.ui.edgeCPUPlot,
                    title='',
                    monitor= Monitor(name='usrp',
                                     stopflag=ste,
                                     ip='192.168.10.104',
                                     port=8084,
                                     params={'CPU': [('cpu_percent', 1.0), ]},
                    ),
            )
        )

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
        #manager.stopAll()

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
    #init()

    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
