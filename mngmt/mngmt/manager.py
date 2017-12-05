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

    def addHost(self, hostname, ip, cert):
        self._hosts[hostname] = pylxd.Client(endpoint = 'https://' + ip,
                cert = cert,
                verify = False)

    def getContainerList(self, hostname):
        return self._hosts[hostname].containers.all()

    def getContainerByName(self, hostname, containername):
        return self._hosts[hostname].containers.get(containername)

    def createBundle(self, bundle):
        for container in bundle:
            container.create()
