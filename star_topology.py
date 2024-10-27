from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel

def star_topology():
    # Initialize the Mininet with a controller
    net = Mininet(controller=Controller)

    # Add a controller
    controller = net.addController('c0')

    # Add a switch
    s1 = net.addSwitch('s1')

    # Add hosts
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')

    # Add links (connecting each host to the switch)
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)

    # Start the network
    net.start()

    # Run connectivity test between hosts
    print("Testing connectivity between hosts:")
    net.pingAll()

    # Drop into CLI for further testing
    CLI(net)

    # Stop the network
    net.stop()

if __name__ == '__main__':
    # Set log level to info for better visibility
    setLogLevel('info')
    star_topology()
