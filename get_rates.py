import xmlrpclib
import time


def main():
   rates = [(("split1_0", "split1_1"), 8), ("split2", 32), ("split3", 32)]

   server = xmlrpclib.ServerProxy("http://localhost:8080/")


   while True:
      for name, size in rates:

	 if isinstance(name, str):
         	val = getattr(server, "get_" + name)()
         	print("%s: \tnum: %10.2f \t rate: %10.2f" % (name, val, val * size))
	 else:
		val = sum([getattr(server, "get_" + _n)() for _n in name])
         	print("%s: \tnum: %10.2f \t rate: %10.2f" % (name[0].split("_")[0], val, val * size))

      print("-------------------------------")
      time.sleep(2)


if __name__ == "__main__":

   try:
      main()
   except KeyboardInterrupt:
      pass
