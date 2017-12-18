import unittest

from mngmt import Manager
from mngmt.container import VirtualRadioSplit, VirtualRadioSingle, USRP, USRPHydra


class ContainerTest(unittest.TestCase):
    """A test case for basic container management"""

    def setUp(self):
        self.mng = Manager()
        self.mng.addHost(host_name="regional",
                         ip="192.168.10.10:8443",
                         cert=("./tests/lxd.crt", "./tests/lxd.key"))

        self.mng.addHost(host_name="edge",
                         ip="192.168.10.20:8443",
                         cert=("./tests/lxd.crt", "./tests/lxd.key"))

    def tearDown(self):
        pass

    def testBuildVR(self):
        bs1 = VirtualRadioSingle(name='vr1tx',
                                host='regional',
                                mode='vr1tx')

        self.mng.create(bs1)
        bs1.start()

        import time
        while bs1.ipaddr is None:
            print('waiting ip')
            time.sleep(1)


        usrp = USRP(name='usrp', host='edge')
        self.mng.create(usrp)
        usrp.start()


        time.sleep(30)

        bs1.migrate('edge')
        usrp.stop()
        usrp.start()

        time.sleep(30)
        self.mng.stopAll()

if __name__ == "__main__":
    unittest.main()
