import xmlrpclib
import time


class Split(object):

    def __init__(self, name, ip, port, params):
        self.name = name
        self.params = params
        self.server = xmlrpclib.ServerProxy("http://%s:%d" % (ip, port))

        self.rates = {k[0]:0 for k in self.params}


    def update(self):
        #print("Requesting data to " + str(self.server))
        for k in self.rates.iterkeys():
            self.rates[k] = float(getattr(self.server, "get_" + k)())


    def __str__(self):
        return "{}:\tn_elems: {:8.2f},\t{}: {:15.2f}".format(
                self.name,
                sum([k for k in self.rates.itervalues()]),
                self.params[0][0].rjust(15),
                sum([self.rates[k]*v for k, v in self.params]),
                )


def main():
   splits = [
              Split('split1', '192.168.10.101', 8081, [('rate0', 8), ('rate1', 8)]),
              Split('split2', '192.168.10.102', 8082, [('rate', 32), ]),
              Split('split3', '192.168.10.103', 8083, [('rate', 32), ]),
              Split('usrp',   '192.168.10.104', 8084, [('vr1_iq_txrate', 32), ]),
              Split('usrp',   '192.168.10.104', 8084, [('vr2_iq_txrate', 32), ]),
              Split('usrp',   '192.168.10.104', 8084, [('usrp_iq_txrate', 32), ]),
              Split('vr_tx2', '192.168.10.29',  8081, [('rx_goodput', 8), ]),
              Split('vr_tx2', '192.168.10.29',  8081, [('tx_goodput', 8), ]),
              Split('vr_rx',  '192.168.10.30',  8085, [('rx_goodput', 8), ]),
              Split('vr_rx',  '192.168.10.30',  8085, [('tx_goodput', 8), ]),
            ]

   while True:
      for s in splits:
          s.update()
          print s

      print("-------------------------------")
      time.sleep(2)


if __name__ == "__main__":

   try:
      main()
   except KeyboardInterrupt:
      pass
