import os, sys, time
sys.path.insert(0, os.getcwd())

from gui import Ui_MainWindow
from PyQt4 import QtGui, QtCore

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


class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

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
        manager.stopAll()

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
