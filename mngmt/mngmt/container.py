
class Container(object):
    def __init__(self, name, origin = None, host = None):
        self._name = name
        self._origin = origin
        self._host = host

    def create(self):
        print("Creating " + self._name)

class ContainerBundle(object):
    def __init__(self, bundlename):
        self._name = bundlename
        self._bundle = []

    def addContainer(self, name, origin, host):
        """
        @param base  Base container name
        @param container Container created from base
        """
        c = Container(name=name, origin=origin, host=host)
        self._bundle.append(c)


    def __iter__(self):
        self._it = 0
        print '----------------------------------'
        return self

    def next(self):
        if self._it == len(self._bundle):
            raise StopIteration
        self._it += 1
        return self._bundle[self._it - 1]

class VirtualRadioSplit(ContainerBundle):
    def __init__(self, name, host_split1, host_split2, host_split3):
        ContainerBundle.__init__(self, name)

        self.addContainer(name = name + '-split1', origin = 'gnuradio',
                    host = name + '' + host_split1)
        self.addContainer(name = name + '-split2', origin = 'gnuradio',
                    host = host_split2)
        self.addContainer(name = name + '-split3', origin = 'gnuradio',
                    host = host_split3)
