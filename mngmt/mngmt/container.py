from mngmt import Manager


class Container(object):

    RUNNING = 'Running'
    STOPPED = 'Stopped'

    def __init__(self, name, origin=None, host=None, start_cmd=None):
        self._name = name
        self._origin = origin
        self._host = host
        self._start_cmd = start_cmd

        self._pylxd_container = None

    @property
    def is_running(self):
        return self._pylxd_container.status == Container.RUNNING

    def create(self):
        mng = Manager()
        client = mng.getHostClient(self._host)

        # If container already instantiated, just start it
        cont_exists = mng.containerExists(self._host, self._name)
        if cont_exists:
            print("\tContainer " + self._name + "already in " + self._host)
        # If container not instantiated, create it
        else:
            img_exists = mng.imageExists(self._host, self._name)
            if img_exists:
                print("\tBase Image " + self._origin +
                      " not in " + self._host)
                return

            print("Creating " + self._name)
            client.containers.create({
                'name': self._name,
                'source': {'type': 'image',
                           'alias': 'gnuradio'}
            }, wait=True)

        self._pylxd_container = client.containers.get(self._name)
        print("\tDONE")

    def start(self):
        if self.is_running:
            print("Container " + self._name + " already running")
        else:
            self._pylxd_container.start()

        cmd_ret = None
        if self._start_cmd is not None:
            cmd_l = [cmd for cmd in self._start_cmd.split(' ')]
            cmd_ret = self._pylxd_container.execute(cmd_l)

        return cmd_ret


class ContainerBundle(object):
    def __init__(self, bundlename):
        self._name = bundlename
        self._bundle = []

    def addContainer(self, name, origin, host, start_cmd=''):
        """
        @param base  Base container name
        @param container Container created from base
        """
        c = Container(name=name,
                      origin=origin,
                      host=host,
                      start_cmd=start_cmd)
        self._bundle.append(c)

    def __iter__(self):
        self._it = 0
        return self

    def __next__(self):
        if self._it == len(self._bundle):
            raise StopIteration
        self._it += 1
        return self._bundle[self._it - 1]

    def create(self):
        try:
            for container in self:
                container.create()
        except:
            print("Error")

    def start(self):
        try:
            for container in self._bundle:
                container.start()
        except:
            print("Error")


class VirtualRadioSplit(ContainerBundle):
    def __init__(self, name, host_split1, host_split2, host_split3):
        ContainerBundle.__init__(self, name)

        self.addContainer(name=name + '-split1', origin='gnuradio',
                          host=host_split1,
                          start_cmd='bash /root/fg-stuff/start_container.sh split1')

        self.addContainer(name=name + '-split2', origin='gnuradio',
                          host=host_split2,
                          start_cmd='bash /root/fg-stuff/start_container.sh split2')

        self.addContainer(name=name + '-split3', origin='gnuradio',
                          host=host_split3,
                          start_cmd='bash /root/fg-stuff/start_container.sh split3')

    def startCmdHandler(self, container, cmd_output):
        print(cmd_output)
