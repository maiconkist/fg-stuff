import unittest

from mngmt import Manager
from mngmt.container import VirtualRadioSplit

class ContainerTest(unittest.TestCase):
    """A test case for basic container management"""

    def setUp(self):
        self.mng = Manager()
        self.mng.addHost(hostname = "local",
                   ip = "127.0.0.1:8443",
                   cert = ("./tests/lxd2.crt", "./tests/lxd2.key"))


    def tearDown(self):
        pass

    def testBuildVR(self):
        bs = VirtualRadioSplit(name = 'vr1',
            host_split1 = 'A',
            host_split2 = 'A',
            host_split3 = 'A')

        self.mng.createBundle(bs)

if __name__ == "__main__":
    unittest.main()
