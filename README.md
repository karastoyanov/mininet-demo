# Mininet UTP Project
--- 

## **Mininet Network Topology with Python API**

This project demonstrates a simple virtual network topology using the Mininet Python API, simulating real-world network scenarios for educational and testing purposes. The topology includes multiple hosts, switches, and configurable links with specific bandwidth allocations.

### 🔖  **Features**

* **Custom Network Topology**: Simulated network with two switches and three hosts, connected by links with varying bandwidths.
* **Automated Network Testing**:
	* **Connectivity**: Runs automated ping tests between hosts.
	* **Bandwidth**: Performs iperf tests to measure UDP bandwidth.
	* **Link Control**: Simulates link failures and restores connections.
	* **HTTP Service Simulation**: Hosts a basic HTTP server on one host, accessible by others.

### 🧰  **Requirements**

* [Mininet pre-defined VM template for Oracle VM VirtualBox](https://github.com/mininet/mininet/releases/)
* Mininet
* Python2

### 🛠️  **Steps to reproduce**

1.  SSH into the VM. Default credentials:
	`mininet` / `mininet`
2. Clone the repo
3. Run the `topo_demo.py` with sudo privileges (required by mininet)

The Python API will simulate mininet virtual network with two switches (s1, s2) and three hosts (h1, h2, h3) and will create links between the network components:

`h1 -- s1` with bandwidth 10Mbps

`h2 -- s1` with bandwidth 20Mbps

`h3 -- s2` with bandwidth 15Mbps

`s1 -- s2` with bandwidth 25Mbps

### 🖥️ **Basic commands**
```sh
mn> help  #Display some help commands
mn> nodes #Display all the nodes controller, switch and hosts of the topology
mn> h2 ping h1 #Ping h1 form h2
mn> h2 ifconfig #Display the ip configuration of h2 host with h2-eth0
mn> xterm h2  #Connect to the terminal of h2 host, where we can run all the commands
mn> dump #Display all the information about the nodes
mn> s1 ifconfig #This will display all the physical interface of host as well as the logical interface of the switch
mn> s1 ping 1.1.1.1 #This will ping the Cloudflare public DNS from the switch
mn> c0 ping -c 2 8.8.4.4
mn> pingall #This will ping two nodes in topology h1 and h2
mn> net #Show the links connection.
```

### 📝 **Automatic tests**

1. Ping from `h2` to `h1`
```sh
mininet> h1 ping -c 5 h2
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
10.0.0.2 - - [26/Oct/2024 14:26:22] "GET / HTTP/1.1" 200 -
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=0.183 ms
64 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=0.074 ms
64 bytes from 10.0.0.2: icmp_seq=3 ttl=64 time=0.077 ms
64 bytes from 10.0.0.2: icmp_seq=4 ttl=64 time=0.093 ms
64 bytes from 10.0.0.2: icmp_seq=5 ttl=64 time=0.085 ms

--- 10.0.0.2 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4102ms
rtt min/avg/max/mdev = 0.074/0.102/0.183/0.041 ms
```

2. Ping from `h1` to `h3`
```sh
mininet> h1 ping -c 5 h3
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=4.98 ms
64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=11.5 ms
64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=0.573 ms
64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.076 ms
64 bytes from 10.0.0.3: icmp_seq=5 ttl=64 time=0.079 ms

--- 10.0.0.3 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4160ms
rtt min/avg/max/mdev = 0.076/3.453/11.560/4.453 ms
```

3. Performance test between `h1` and `h2`
```sh
mininet> iperf h1 h2
*** Iperf: testing TCP bandwidth between h1 and h2
*** Results: ['8.74 Mbits/sec', '9.53 Mbits/sec']
```

4. Performance test between `h1` and `h3`
```sh
mininet> iperf h1 h3
*** Iperf: testing TCP bandwidth between h1 and h3
*** Results: ['9.49 Mbits/sec', '9.70 Mbits/sec']
```

5. Link status. Simulate connectivity loss between `s1` and `s2`
```sh
mininet> link s1 s2 down
mininet> h1 ping -c 5 h3
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.

--- 10.0.0.3 ping statistics ---
5 packets transmitted, 0 received, 100% packet loss, time 4074ms
```

6. Link status. Bring up back the `s1` and `s2` connectivity
```sh
mininet> link s1 s2 up
mininet> h1 ping -c 5 h3
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=3.89 ms
64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=3.68 ms
64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=1.01 ms
64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.078 ms
64 bytes from 10.0.0.3: icmp_seq=5 ttl=64 time=0.078 ms

--- 10.0.0.3 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4023ms
rtt min/avg/max/mdev = 0.078/1.750/3.895/1.701 ms
```

6. Host Config Details:
```sh
# View network details for h1
mininet> h1 ifconfig
h1-eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.0.0.1  netmask 255.0.0.0  broadcast 10.255.255.255
        ether 2e:52:ff:10:32:51  txqueuelen 1000  (Ethernet)
        RX packets 3194  bytes 1507084 (1.5 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 2500  bytes 12358979 (12.3 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

7. Deploy HTTP server and send GET request
```sh
mininet> h1 python3 -m http.server 80 &
mininet> h2 curl h1
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso8859-1">
<title>Directory listing for /</title>
</head>
<body>
<h1>Directory listing for /</h1>
<hr>
<ul>
<li><a href=".git/">.git/</a></li>
<li><a href=".topo_demo.py.swp">.topo_demo.py.swp</a></li>
<li><a href="data">data</a></li>
<li><a href="topo_demo.py">topo_demo.py</a></li>
</ul>
<hr>
</body>
</html>
```

### 🖼️ Topology Graphic
![[topo_domo.png.png]]