from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel

def tree_topology():
    # Initialize the Mininet with a controller
    net = Mininet(controller=Controller, link=TCLink)

    # Add a controller
    controller = net.addController('c0')

    # Add primary switches
    primary_switch_1 = net.addSwitch('s1')
    primary_switch_2 = net.addSwitch('s2')

    # Add child switches for each primary switch
    child_switches = []
    for i in range(1, 3):
        child_switch_1 = net.addSwitch(f's1{i}')
        child_switch_2 = net.addSwitch(f's2{i}')
        child_switches.extend([child_switch_1, child_switch_2])

        # Connect each child switch to its respective primary switch
        net.addLink(primary_switch_1, child_switch_1)
        net.addLink(primary_switch_2, child_switch_2)

    # Add hosts and connect them to child switches
    host_id = 1
    for child_switch in child_switches:
        for _ in range(2):  # Each child switch gets two hosts
            host = net.addHost(f'h{host_id}')
            net.addLink(host, child_switch)
            host_id += 1

    # Start the network
    net.start()

    # Test connectivity
    net.pingAll()

    # Open Mininet CLI for further interaction
    CLI(net)

    # Stop the network after exiting CLI
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    tree_topology()
