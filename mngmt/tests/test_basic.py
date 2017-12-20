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
        #self.mng.stopAll()

    def testBuildVRSingle(self):
        return
        bs1 = VirtualRadioSingle(name='vr1tx',
                                host='regional',
                                mode='vr1tx')

        self.mng.create(bs1)
        bs1.start()

        import time
        while bs1.has_ipaddr is False:
            print('waiting ip')
            time.sleep(1)

        usrp = USRP(name='usrp', host='edge')
        self.mng.create(usrp)
        usrp.start()

        while usrp.has_ipaddr is False:
            print('waiting ip')
            time.sleep(1)

        time.sleep(10)

        bs1.migrate('edge')
        usrp.stop()
        usrp.start()

        time.sleep(10)
        self.mng.stopAll()

    def testUSRPHyDRA(self):
        #usrp = USRPHydra(name='usrp', host='edge')
        #bs1 = VirtualRadioSingle(name='vr1tx',
        #                        host='regional',
        #                        mode='vr1tx')
        bs1 = VirtualRadioSplit(name='vr1tx',
                                 host_split1='regional',
                                 host_split2='regional',
                                 host_split3='regional')

        bs2 = VirtualRadioSingle(name='vr2tx',
                                host='regional',
                                mode='vr2tx')

        import time

        #self.mng.create(usrp)
        #usrp.start()
        #while usrp.has_ipaddr is False:
            #print('waiting ip')
            #time.sleep(1)

        self.mng.create(bs1)
        bs1.start()
        while bs1.has_ipaddr is False:
            print('waiting ip')
            time.sleep(1)

        self.mng.create(bs2)
        bs2.start()
        while bs2.has_ipaddr is False:
            print('waiting ip')
            time.sleep(1)


if __name__ == "__main__":

    try:
        unittest.main()
    except KeyboardInterrupt as e:
        print(e)
