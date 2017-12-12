import unittest

from mngmt import Manager
from mngmt.container import VirtualRadioSplit


class ContainerTest(unittest.TestCase):
    """A test case for basic container management"""

    def setUp(self):
        self.mng = Manager()
        self.mng.addHost(host_name="local",
                         ip="localhost:8443",
                         cert=("./tests/lxd.crt", "./tests/lxd.key"))

    def tearDown(self):
        pass

    def testBuildVR(self):
        bs = VirtualRadioSplit(name='vr1', host_split1='local',
                               host_split2='local',
                               host_split3='local')

        self.mng.create(bs)

        #bs.start()
        #bs.stop()

        bs.migrate('vr1-split1', 'B')

if __name__ == "__main__":
    unittest.main()
