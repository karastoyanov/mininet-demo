from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel
import heapq

def mesh_topology():
    # Initialize the Mininet with a controller
    net = Mininet(controller=Controller, link=TCLink)

    # Add a controller
    controller = net.addController('c0')

    # Number of hosts in the mesh
    num_hosts = 4

    # Add hosts and switches in a mesh topology
    hosts = []
    switches = []

    for i in range(1, num_hosts + 1):
        host = net.addHost(f'h{i}')
        switch = net.addSwitch(f's{i}')
        hosts.append(host)
        switches.append(switch)
    
    # Connect each host to its corresponding switch
    for i in range(num_hosts):
        net.addLink(hosts[i], switches[i])

    # Connect each switch to every other switch to form a full mesh
    for i in range(num_hosts):
        for j in range(i + 1, num_hosts):
            net.addLink(switches[i], switches[j])

    # Start the network
    net.start()

    # Represent the network as a graph (adjacency list)
    # Here, we assume each link has a weight of 1 for simplicity
    graph = {f's{i+1}': {} for i in range(num_hosts)}
    for i in range(num_hosts):
        for j in range(i + 1, num_hosts):
            # Bidirectional links between switches
            graph[f's{i+1}'][f's{j+1}'] = 1
            graph[f's{j+1}'][f's{i+1}'] = 1

    # Function to find the shortest path using Dijkstra's algorithm
    def dijkstra(graph, start, end):
        # Priority queue and distance dictionary
        queue = [(0, start)]
        distances = {node: float('inf') for node in graph}
        distances[start] = 0
        previous_nodes = {node: None for node in graph}

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            if current_node == end:
                break

            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(queue, (distance, neighbor))

        # Reconstruct the shortest path
        path, node = [], end
        while previous_nodes[node] is not None:
            path.insert(0, node)
            node = previous_nodes[node]
        if path:
            path.insert(0, node)

        return path, distances[end]

    # Test Dijkstra's algorithm to find the shortest path between two switches
    start_node = 's1'
    end_node = 's3'
    path, distance = dijkstra(graph, start_node, end_node)
    print(f"Shortest path from {start_node} to {end_node}: {path} with distance {distance}")

    # Test connectivity
    net.pingAll()

    # Open Mininet CLI for further interaction
    CLI(net)

    # Stop the network after exiting CLI
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    mesh_topology()
