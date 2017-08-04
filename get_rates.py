import xmlrpclib
import time


class Split(object):

    def __init__(self, name, ip, port, params):
        self.name = name
        self.params = params
        self.server = xmlrpclib.ServerProxy("http://%s:%d" % (ip, port))

        self.rates = {k[0]:0 for k in self.params}


    def update(self):
        for k in self.rates.iterkeys():
            self.rates[k] = getattr(self.server, "get_" + k)()


    def __str__(self):
        return "{name}: n_elems: {n_elems}, rate: {rate}".format(
                name = self.name,
                n_elems = sum([k for k in self.rates.itervalues()]),
                rate = sum([self.rates[k]*v for k, v in self.rates.iteritems()]),
                )



def main():
   splits = [ Split('split1', '192.168.10.101', 8081, [('split1_0', 8), ('split1_1', 8)]),
              Split('split2', '192.168.10.102', 8082, [('split2', 32), ]),
              Split('split3', '192.168.10.103', 8083, [('split3', 32), ]),
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
