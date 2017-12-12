from mngmt import Manager

class Container(object):

    RUNNING = 'Running'
    STOPPED = 'Stopped'

    def __init__(self, name, origin=None, host=None,
                 start_cmd=None, stop_cmd=None):
        self.name = name
        self._origin = origin
        self._host = host
        self._start_cmd = start_cmd
        self._stop_cmd = stop_cmd

    @property
    def _pylxd_container(self):
        return Manager().getHostClient(self._host).containers.get(self.name)

    @property
    def is_running(self):
        return self._pylxd_container.status == Container.RUNNING

    def create(self):
        mng = Manager()
        client = mng.getHostClient(self._host)

        # If container already instantiated, just start it
        cont_exists = mng.containerExists(self._host, self.name)
        if cont_exists:
            print("\tContainer " + self.name + "already in " + self._host)
        # If container not instantiated, create it
        else:
            img_exists = mng.imageExists(self._host, self.name)
            if img_exists:
                print("\tBase Image " + self._origin +
                      " not in " + self._host)
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
        if self.is_running:
            print(self.name + " executing command `" + cmd + "`")
            cmd_l = [c for c in cmd.split(' ')]
            cmd_ret = self._pylxd_container.execute(cmd_l)
        else:
            print(self.name + " is not running. Cannot execute command `" + cmd + "`")

        return cmd_ret

    def start(self):
        if self.is_running:
            print("Container " + self.name + " already running")
            return
        try:
            self._pylxd_container.start()
            if self._start_cmd is not None:
                return self.execute(self._start_cmd)
        except Exception as e:
            print(e)

    def stop(self):
        if not self.is_running:
            print("Container " + self.name + " is already stopped")
            return

        try:
            print("Stopping container " + self.name)
            if self._stop_cmd is not None:
                self.execute(self._stop_cmd)

            self._pylxd_container.stop()
        except Exception as e:
            print("Error stopping container: " + str(e))

    def destroy(self):
        self.stop()
        self._pylxd_container.destroy()

    def migrate(self, host, new_name=None):
        other_client = Manager().getHostClient(host)
        self._pylxd_container.migrate(other_client)



class ContainerBundle(object):
    def __init__(self, bundlename):
        self._name = bundlename
        self._bundle = {}

    def addContainer(self, name, origin, host, start_cmd='', stop_cmd=''):
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

    def create(self):
        try:
            for container in self:
                container.create()
        except:
            print("Error")

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
            print("Error stopping container: " + str(e))

    def migrate(self, container_name, host_dst, new_name=None):
        container = self._bundle[container_name]
        container.migrate(host_dst, new_name)


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
                          start_cmd='bash /root/fg-stuff/start_container.sh split3',
                          stop_cmd='killall python')
