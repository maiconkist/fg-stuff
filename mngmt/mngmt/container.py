from mngmt import Manager

class Container(object):

    RUNNING = 'Running'
    STOPPED = 'Stopped'

    def __init__(self, name,
                 origin=None,
                 host=None,
                 start_cmd=None,
                 stop_cmd=None,
                 manageable=True):
        self.name = name
        self._origin = origin
        self._host_name = host
        self._start_cmd = start_cmd
        self._stop_cmd = stop_cmd
        self._manageable = manageable

        Manager().registerContainer(self)

    @property
    def _pylxd_container(self):
        return Manager().getLXDHostClient(self._host_name).containers.get(self.name)

    @property
    def is_running(self):
        return self._pylxd_container.status == Container.RUNNING

    @property
    def has_ipaddr(self, iface = 'eth0'):

        ip = None
        try:
            ip = self._pylxd_container.state().network[iface]['addresses'][0]['address']
        except Exceptiona as e:
            print("Error getting ip address: " + str(e))

        try:
            parts = ip.split('.')
            if len(parts) == 4 and all(0 <= int(part) < 256 for part in parts):
                return True
        except (ValueError, AttributeError, TypeError):
            # ValueError: one of the 'parts' not convertible to integer
            # AttributeError or TypeError :`ip` isn't even a string
            return False

        return False

    def create(self):
        mng = Manager()
        client = mng.getLXDHostClient(self._host_name)

        # If container already instantiated, just start it
        cont_exists = mng.containerExists(self._host_name, self.name)
        if cont_exists:
            print("\tContainer " + self.name + " already in " + self._host_name)
        # If container not instantiated, create it
        else:
            img_exists = mng.imageExists(self._host_name, self.name)
            if img_exists:
                print("\tBase Image " + self._origin +
                      " not in " + self._host_name)
                return

            print("Creating " + self.name)
            client.containers.create({
                'name': self.name,
                'source': {'type': 'image',
                           'alias': 'gnuradio'}
            }, wait=True)

        print("\tDONE")

    def execute(self, cmd):
        cmd_ret = None
        print("Executing command `" + str(cmd) + "` in " + str(self.name) + "@" + str(self._host_name))
        if self.is_running:
            cmd_l = [c for c in cmd.split(' ')]
            print(cmd_l)
            cmd_ret = self._pylxd_container.execute(cmd_l)
        else:
            print(self.name + " is not running. Cannot execute command `" + cmd + "`")

        return cmd_ret

    def start(self):
        if self._manageable is False:
            return

        if self.is_running:
            print("Container " + self.name + " already running")
        else:
            try:
                self._pylxd_container.start(wait=True)
            except Exception as e:
                print(e)

        print("Waiting container" + self.name + " to start")
        while not self.is_running:
            print("Waiting container" + self.name + " to start")
        print("Container " + self.name + " is running.")

        if self._start_cmd is not None:
            return self.execute(self._start_cmd)

    def stop(self):
        if self._manageable is False:
            return

        if not self.is_running:
            print("Container " + self.name + " is already stopped")
            return

        if self._stop_cmd is not None:
            self.execute(self._stop_cmd)

        print("Stopping container " + self.name)
        while self.is_running:
            try:
                self._pylxd_container.stop(wait=True)
            except Exception as e:
                print("Error stopping container 1: " + str(e))

    def destroy(self):
        self.stop()
        self._pylxd_container.destroy()

    def migrate(self, host_name, new_name=None):
        print("Migrating container " + self.name)
        other_client = Manager().getLXDHostClient(host_name)

        running = self.is_running
        self.stop()

        try:
            self._pylxd_container.migrate(other_client, wait=True)
        except Exception as e:
            print("Error migrating container " + self.name + ": " + str(e))

        # update host 
        print("Updating host")
        self._host_name = host_name

        # start in new host
        if running:
            self.start()


class ContainerBundle(object):
    def __init__(self, bundlename):
        self._name = bundlename
        self._bundle = {}

    def addContainer(self, name, origin, host, start_cmd=None, stop_cmd=None):
        """
        @param name Container name
        @param origin  Base container name
        @param host Host name
        @param start_cmd
        @param stop_cmd
        """
        c = Container(name=name,
                      origin=origin,
                      host=host,
                      start_cmd=start_cmd,
                      stop_cmd=stop_cmd)
        self._bundle[name] = c

    def __iter__(self):
        self._it = 0
        return self

    def __next__(self):
        if self._it == len(self._bundle):
            raise StopIteration
        self._it += 1
        return self._bundle[self._it - 1]

    @property
    def has_ipaddr(self):
        # if at least one container have not gotten an IP address yet, return False
        for name, container in self._bundle.items():
            # if at least one container have not gotten an IP address yet, return False
            if container.has_ipaddr is False:
                return False

        return True

    def create(self):
        try:
            for name, container in self._bundle.items():
                container.create()
        except Exception as e:
            print("Error creating container: " + str(e))

    def start(self):
        try:
            for name, container in self._bundle.items():
                container.start()
        except Exception as e:
            print("Error starting container:" + str(e))

    def stop(self):
        try:
            for name, container in self._bundle.items():
                container.stop()
        except Exception as e:
            print("Error stopping container 2: " + str(e))

    def migrate(self, container_name, host_dst, new_name=None):
        container = self._bundle[container_name]
        container.migrate(host_dst, new_name)

class VirtualRadioSplit(ContainerBundle):
    def __init__(self, name, host_split1, host_split2, host_split3):
        ContainerBundle.__init__(self, name)

        self.addContainer(name=name + '-split1', origin='gnuradio',
                          host=host_split1,
                          #start_cmd='bash /root/fg-stuff/start_container.sh ' + name + '-split1',
                          stop_cmd='killall python3')

        self.addContainer(name=name + '-split2', origin='gnuradio',
                          host=host_split2,
                          #start_cmd='bash /root/fg-stuff/start_container.sh ' + name + '-split2',
                          stop_cmd='killall python3')

        self.addContainer(name=name + '-split3', origin='gnuradio',
                          host=host_split3,
                          #start_cmd='bash /root/fg-stuff/start_container.sh ' + name + '-split3',
                          stop_cmd='killall python3')

class VirtualRadioSingle(Container):
    def __init__(self, name, host, mode):
        if mode not in ['vr1tx', 'vr2tx']:
            raise ValueError("VirtualRadio mode needs to be either 'vr1tx' or 'vr2tx'")

        Container.__init__(self,
                           name,
                           origin='gnuradio',
                           host=host,
                           #start_cmd='bash /root/fg-stuff/start_container.sh ' + mode,
                           stop_cmd='killall python3')

class USRP(Container):
    def __init__(self, name, host):
        Container.__init__(self,
                           name=name,
                           origin='gnuradio',
                           host=host,
                           #start_cmd='bash /root/fg-stuff/start_container.sh usrp',
                           stop_cmd='killall python3')

class USRPHydra(Container):
    def __init__(self, name, host):
        Container.__init__(self,
                           name=name,
                           origin='gnuradio',
                           host=host,
                           #start_cmd='bash /root/fg-stuff/start_container.sh usrphydra',
                           stop_cmd='killall python3')
