#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GNURadio Agent: Example tutorial of WiSHFUL (agent side)

Usage:
   wishful_simple_agent [options] [-q | -v]

Options:
   --logfile name      Name of the logfile
   --config configFile Config file path

Example:
   ./wishful_example_tutorial_agent -v --config ./tx.yaml
   ./wishful_example_tutorial_agent -v --config ./rx.yaml

Other options:
   -h, --help          show this help message and exit
   -q, --quiet         print less text
   -v, --verbose       print more text
   --version           show version and exit
"""

import logging
import signal
import sys, os
import yaml
import wishful_agent

__author__ = "Maicon Kist"
__copyright__ = "Copyright (c) 2017 Connect Centre - Trinity College Dublin" 
__version__ = "0.1.0"
__email__ = "kistm@tcd.ie"


def get_ip_address(ifname):
    import socket
    import fcntl
    import struct
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], 'utf-8'))
    )[20:24])


ip_to_name = {
	"192.168.10.101": "vr1tx-split1",
	"192.168.10.102": "vr1tx-split2",
	"192.168.10.103": "vr1tx-split3",
	"192.168.10.104": "usrp"       ,
	"192.168.10.113": "vr2tx"       ,
}

"""
Setting of agent node
"""
agent_PC_interface = "eth0"
"""
END setting of agent node
"""


""" START WiSHFUL agent setting """
"""
The WiSHFUL controller module is the core module of the WiSHFUL framework and allow all the basics functions
such as the node discovery, the UPI functions execution on local and remote node, perform the messages exchange between
global control program and local control program, and all the other management functions of the framework. The different
works of the controller are  performed by different module can be added on demand in the controller
"""
#Create agent
agent = wishful_agent.Agent()
name = ip_to_name[get_ip_address(agent_PC_interface)]

#Configure agent, we specify in the parameters the controller name and a string information related to the
#controller
agent.set_agent_info(name=name, info="Example tutorial Agent", iface=agent_PC_interface)


#the following rows add all the needed modules to the controller

#add the discovery module, responsable for the nodes discovery procedure
#we specify interface and the name of the nodes group

agent.add_module(moduleName="discovery", pyModule="wishful_module_discovery_pyre",
                 className="PyreDiscoveryAgentModule", kwargs={"iface":agent_PC_interface, "groupName":"wishful_1234"})

#add the net_linux module,
agent.add_module(moduleName="gnuradio", pyModule="wishful_module_gnuradio",
                 className="GnuRadioModule")


""" END WiSHFUL agent setting """


""" START Define logging controller """
""" we use the python logging system module (https://docs.python.org/2/library/logging.html) """

#set the logging name
log = logging.getLogger('wishful_agent')

""" END Define logging controller """


if __name__ == "__main__":
    try:
        from docopt import docopt
    except:
        print("""
        Please install docopt using:
            pip install docopt==0.6.1
        For more refer to:
        https://github.com/docopt/docopt
        """)
        raise

    #get program arguments
    args = docopt(__doc__, version=__version__)

    #set the logging level by argument parameters
    log_level = logging.INFO  # default
    if args['--verbose']:
        log_level = logging.DEBUG
    elif args['--quiet']:
        log_level = logging.ERROR

    #set the logging format
    logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s.%(funcName)s() - %(levelname)s - %(message)s')

    try:
        #Start agent
        agent.run()
    except KeyboardInterrupt:
        log.debug("Agent exits")
    finally:
        log.debug("Exit")
        agent.stop()
