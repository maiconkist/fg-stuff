#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gevent

# WiSHFUL imports
import wishful_controller
import wishful_upis as upis
import wishful_module_gnuradio

nodes = {}


valid_nodes = ["vr1tx-split1", "vr1tx-split2", "vr1tx-split3", "vr2tx", "usrp"]
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
        program_args = '' 
        program_port = conf['port'][program_name]

        controller.blocking(False).node(node).radio.activate_radio_program({'program_name': program_name, 'program_code': program_code, 'program_args': program_args,'program_type': 'py', 'program_port': program_port})


@controller.node_exit_callback()
def node_exit(node, reason):
    if node in nodes.values():
        del nodes[node.name]
    print(("NodeExit : NodeID : {} Reason : {}".format(node.id, reason)))


def main():

    while True:
        gevent.sleep(2)


if __name__ == '__main__':
    controller.start()
    main()
