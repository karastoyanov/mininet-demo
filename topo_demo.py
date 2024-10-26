from mininet.net import Mininet
from mininet.node import Controller
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

def complex_topology():
    # Initialize the Mininet with a controller and TCLink for bandwidth control
    net = Mininet(controller=Controller, link=TCLink)

    # Add controller
    controller = net.addController('c0')

    # Add switches
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')

    # Add hosts
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')

    # Create links with optional bandwidth limits
    net.addLink(h1, s1, bw=10)   # 10 Mbps link between h1 and s1
    net.addLink(h2, s1, bw=20)   # 20 Mbps link between h2 and s1
    net.addLink(h3, s2, bw=15)   # 15 Mbps link between h3 and s2
    net.addLink(s1, s2, bw=25)   # 25 Mbps link between s1 and s2

    # Start the network
    net.start()

    # Automated connectivity tests
    print("Running ping test between h1 and h2:")
    h1, h2, h3 = net.get('h1', 'h2', 'h3')
    print(h1.cmd('ping -c 3 %s' % h2.IP()))

    print("Running ping test between h1 and h3:")
    print(h1.cmd('ping -c 3 %s' % h3.IP()))

    # Automated bandwidth test
    print("Running iperf test between h1 and h2:")
    print(h1.cmd('iperf -s -u -i 1 &'))
    print(h2.cmd('iperf -c %s -u -t 5' % h1.IP()))

    print("Running iperf test between h1 and h3:")
    print(h1.cmd('iperf -s -u -i 1 &'))
    print(h3.cmd('iperf -c %s -u -t 5' % h1.IP()))

    # Manipulate link state
    print("Bringing down link between s1 and s2:")
    s1, s2 = net.get('s1', 's2')
    net.configLinkStatus(s1, s2, 'down')
    
    print("Testing connectivity after link down:")
    print(h1.cmd('ping -c 3 %s' % h3.IP()))  # This should fail

    print("Bringing link back up between s1 and s2:")
    net.configLinkStatus(s1, s2, 'up')

    print("Testing connectivity after link is back up:")
    print(h1.cmd('ping -c 3 %s' % h3.IP()))  # This should succeed

    # Start HTTP server and access it from another host
    print("Starting HTTP server on h1:")
    h1.cmd('python3 -m http.server 80 &')
    print("Accessing HTTP server from h2:")
    print(h2.cmd('curl %s' % h1.IP()))

    # Start CLI for manual testing if needed
    CLI(net)

    # Stop the network
    net.stop()

if __name__ == '__main__':
    # Set log level to info for better visibility
    setLogLevel('info')
    complex_topology()
