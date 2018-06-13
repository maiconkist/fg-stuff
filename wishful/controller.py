#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Maicon Kist"
__copyright__ = "Copyright (c) 2018 Connect Centre - Trinity College Dublin"
__version__ = "0.1.0"
__email__ = "kistm@tcd.ie"


# Genric imports
import gevent, threading
import xmlrpc.server as xmlserver


from ilock import ILock

# WiSHFUL imports
import wishful_controller
import wishful_upis as upis
import wishful_module_gnuradio

valid_nodes = ["vr1tx-split1", "vr1tx-split2", "vr1tx-split3", "vr2tx", "usrp"]
nodes = {}

amplitude1 = 0.1
amplitude2 = 0.1

values = {}
for n in valid_nodes:
    values[n] = {}


conf = {
    # list of files that will be send to agents
    'files' : {
		"vr1tx-split1" : "/home/connect/lxc/fg-stuff/tx_split/split1.py", 
		"vr1tx-split2" : "/home/connect/lxc/fg-stuff/tx_split/split2.py", 
		"vr1tx-split3" : "/home/connect/lxc/fg-stuff/tx_split/split3.py", 
		"vr2tx"        : "/home/connect/lxc/fg-stuff/tx_single/vr2_tx.py", 
		"usrp"        :  "/home/connect/lxc/fg-stuff/usrp/usrp_hydra.py", 
    },
    'port': {
		"vr1tx-split1" : 8081, 
		"vr1tx-split2" : 8082, 
		"vr1tx-split3" : 8083, 
		"vr2tx"        : 8081, 
		"usrp"         : 8084, 
    }
}

getters = {
		"vr1tx-split1" : ['rate0', 'rate1', 'iq_rxrate'], 
		"vr1tx-split2" : ['rate', ], 
		"vr1tx-split3" : ['rate', ], 
		"vr2tx"        : ['tx_iq_rate', 'iq_rxrate' ], 
		"usrp"        :  ['vr1_iq_txrate', 'vr2_iq_txrate', 'vr1_iq_rxrate', 'vr2_iq_rxrate'], 
}

#Create controller
# ::TRICKY:: update IP addresses to external interface
controller = wishful_controller.Controller(dl="tcp://192.168.10.10:8990", ul="tcp://192.168.10.10:8989")
controller.set_controller_info(name="TCD_RadioVirtualization", info="WishfulControllerInfo")
controller.add_module(moduleName="discovery",
	pyModuleName="wishful_module_discovery_pyre",
	className="PyreDiscoveryControllerModule",
	kwargs={"iface":"br0", "groupName":"tcd", "downlink":"tcp://192.168.10.10:8990", "uplink":"tcp://192.168.10.10:8989"})


@controller.new_node_callback()
def new_node(node):
    print("New node appeared: Name: %s" % (node.name, ))

    with ILock("controller"):
        if node.name in valid_nodes: 
            nodes[node.name] = node
            program_name = node.name
            program_code = open(conf['files'][program_name], "r").read()
            program_args = "" 
            program_port = conf['port'][program_name]

            controller.blocking(False).node(node).radio.activate_radio_program({'program_name': program_name, 'program_code': program_code, 'program_args': program_args,'program_type': 'py', 'program_port': program_port})
            print("Started program %s" % (program_name, ))


@controller.node_exit_callback()
def node_exit(node, reason):
    with ILock("controller"):
        if node in nodes.values():
            del nodes[node.name]
        print(("NodeExit : NodeName : {}   Reason : {}".format(node.name, reason)))

def main():

    # remove node during migration.
    def stop_monitoring(nodename):
        node_exit(nodes[nodename], 'Migrated')

    def set_vr1_amplitude(value):
        global amplitude1
        amplitude1 = value
    def set_vr2_amplitude(value):
        global amplitude2
        amplitude2 = value
    # Downlink monitors
    def get_vr1tx_split1_downlink():
        return values['vr1tx-split1']['rate0']*8 + values['vr1tx-split1']['rate1']*8
    def get_vr1tx_split2_downlink():
        return values['vr1tx-split2']['rate']*32
    def get_vr1tx_split3_downlink():
        return values['vr1tx-split3']['rate']*32
    def get_vr2tx_downlink():
        return values['vr2tx']['tx_iq_rate']*32
    def get_usrp_vr1_downlink():
        return values['usrp']['vr1_iq_txrate']*32
    def get_usrp_vr2_downlink():
        return values['usrp']['vr2_iq_txrate']*32

    # Uplink monitors
    def get_vr1tx_split1_uplink():
        return values['vr1tx-split1']['iq_rxrate']*32
    def get_vr2tx_uplink():
        return values['vr2tx']['iq_rxrate']*32
    def get_usrp_vr1_uplink():
        return values['usrp']['vr1_iq_rxrate']*32
    def get_usrp_vr2_uplink():
        return values['usrp']['vr2_iq_rxrate']*32

    server = xmlserver.SimpleXMLRPCServer(("127.0.0.1", 44444), allow_none=True, logRequests=False)

    server.register_function(stop_monitoring)
    server.register_function(set_vr1_amplitude)
    server.register_function(set_vr2_amplitude)

    server.register_function(get_vr1tx_split1_downlink)
    server.register_function(get_vr1tx_split2_downlink)
    server.register_function(get_vr1tx_split3_downlink)
    server.register_function(get_vr2tx_downlink)
    server.register_function(get_usrp_vr1_downlink)
    server.register_function(get_usrp_vr2_downlink)
    server.register_function(get_vr1tx_split1_uplink)
    server.register_function(get_vr2tx_uplink)
    server.register_function(get_usrp_vr1_uplink)
    server.register_function(get_usrp_vr2_uplink)
    server_thread = threading.Thread(target = server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    # We expect two agents (tx and rx).
    # Observation: we dont check if the agents connectict are in fact the ones that we want.
    while len(nodes) < len(valid_nodes):
        print('-- Nodes connected: {}/{}'.format(len(nodes), len(valid_nodes)))
        gevent.sleep(2)

    while True:
            with ILock("controller"):
                for node in nodes.values():
                    print("Getting info from: " + node.name)
                    values[node.name] = controller.node(node).radio.get_parameters(getters[node.name])

                    if node.name == 'usrp':
                        controller.node(nodes['usrp']).radio.set_parameters({'amplitude1': amplitude1, 'amplitude2': amplitude2})


            gevent.sleep(1)

if __name__ == '__main__':
    controller.start()
    try: 
        main()
    except Exception as e:
        print("Caught Exception into main controller loop: " + str(e))
        for node in nodes:
            controller.node(node).radio.deactivate_radio_program(node.name)
