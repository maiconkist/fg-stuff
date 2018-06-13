import pylxd

def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class Manager():
    def __init__(self):
        self._hosts = {}
        self._container = []

    def addHost(self, host_name, ip, cert):
        self._hosts[host_name] = pylxd.Client(endpoint='https://' + ip,
                                              cert=cert,
                                              verify=False)

    def registerContainer(self, container):
        self._container.append(container)

    def getContainer(self, container_name):

        for c in self._container:
            if c.name == container_name:
                return c
        return None

    def getContainerList(self):
        return self._container

    def getLXDContainerList(self, host_name=None):
        if host_name is not None:
            return self._hosts[host_name].containers.all()
        else:
            r = []
            for hosts, client in self._hosts.items():
                r.extend(client.containers.all())
            return r

    def getLXDContainerByName(self, host_name, container_name):
        if host_name is not None:
            return self._hosts[host_name].containers.get(container_name)

        return None

    def getLXDHostClient(self, host_name):
        return self._hosts[host_name]

    def containerExists(self, host_name, container_name):
        if host_name is not None:
            return self._hosts[host_name].containers.exists(container_name)

        return None

    def imageExists(self, host_name, container_name, alias=True):
        if host_name is not None:
            return self._hosts[host_name].images.exists(container_name, alias)

        return None

    def create(self, bundle):
        bundle.create()

    def stopAll(self):
        for l in self._container:
            l.stop()
