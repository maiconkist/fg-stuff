#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Maicon Kist"
__copyright__ = "Copyright (c) 2018 Connect Centre - Trinity College Dublin"
__version__ = "0.1.0"
__email__ = "kistm@tcd.ie"


# Genric imports
import gevent, threading
import xmlrpc.server as xmlserver

# WiSHFUL imports
import wishful_controller
import wishful_upis as upis
import wishful_module_gnuradio



valid_nodes = ["vr1tx-split1", "vr1tx-split2", "vr1tx-split3", "vr2tx", "usrp"]

nodes = {}

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

    if node.name in valid_nodes: 
        nodes[node.name] = node
        program_name = node.name
        program_code = open(conf['files'][program_name], "r").read()
        program_args = "" 
        program_port = conf['port'][program_name]

        controller.blocking(False).node(node).radio.activate_radio_program({'program_name': program_name, 'program_code': program_code, 'program_args': program_args,'program_type': 'py', 'program_port': program_port})


@controller.node_exit_callback()
def node_exit(node, reason):
    if node in nodes.values():
        del nodes[node.name]
    print(("NodeExit : NodeID : {} Reason : {}".format(node.id, reason)))


@controller.add_callback(upis.radio.get_parameters)
def get_vars_response(group, node, data):
    """ This function implements a callback called when ANY get_* function is called in ANY of the nodes

    :param group: Experiment group name
    :param node: Node used to execute the UPI
    :param data: ::TODO::
    """
    print("{} get_channel_reponse : Group:{}, NodeId:{}, msg:{}".format(datetime.datetime.now(), group, node.id, data))

def main():

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

    server = xmlserver.SimpleXMLRPCServer(("127.0.0.1", 44444), allow_none=True)

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


    while True:
        for node in nodes.values():
            values[node.name] = controller.node(node).radio.get_parameters(getters[node.name])

        gevent.sleep(2)

if __name__ == '__main__':
    controller.start()
    main()
