from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel

def ring_topology():
    # Initialize the Mininet with a controller
    net = Mininet(controller=Controller, link=TCLink)

    # Add a controller
    controller = net.addController('c0')

    # Number of hosts in the ring
    num_hosts = 4

    # Add hosts and switches in a ring
    hosts = []
    switches = []

    for i in range(1, num_hosts + 1):
        host = net.addHost(f'h{i}')
        switch = net.addSwitch(f's{i}')
        hosts.append(host)
        switches.append(switch)
    
    # Add links to form the ring (each switch connects to two hosts and two adjacent switches)
    for i in range(num_hosts):
        # Connect host to its corresponding switch
        net.addLink(hosts[i], switches[i])

        # Connect each switch to the next switch in the ring
        net.addLink(switches[i], switches[(i + 1) % num_hosts])

    # Start the network
    net.start()

    # Test connectivity
    print("Testing connectivity between hosts:")
    net.pingAll()

    # Open Mininet CLI for further interaction
    CLI(net)

    # Stop the network after exiting CLI
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    ring_topology()
