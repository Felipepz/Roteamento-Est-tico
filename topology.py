#!/usr/bin/python
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi

def topology(remote_controller):
   "Create a network."
   net = Mininet_wifi()
   info("*** Adding stations/hosts\n")
   h1s1 = net.addHost("h1s1", ip="200.15.35.1/24")
   h2s1 = net.addHost("h2s1", ip="200.15.35.2/24")
   h1s2 = net.addHost("h1s2", ip="198.98.99.65/27")
   h1s3 = net.addHost("h1s3", ip="200.57.59.1/24")
   h2s3 = net.addHost("h2s3", ip="200.57.59.2/24")
   h1s4 = net.addHost("h1s4", ip="198.98.99.33/27")
   h2s4 = net.addHost("h2s4", ip="198.98.99.34/27")

   roteador1 = net.addHost("roteador1")
   roteador2 = net.addHost("roteador2")
   roteador3 = net.addHost("roteador3")
   roteador4 = net.addHost("roteador4")

   info("*** Adding P4Switches (core)\n")
   switch1 = net.addSwitch("switch1")
   switch2 = net.addSwitch("switch2")
   switch3 = net.addSwitch("switch3")
   switch4 = net.addSwitch("switch4")

   info("*** Creating links\n")
   net.addLink(h1s1, switch1, bw=1000)
   net.addLink(h2s1, switch1, bw=1000)
   net.addLink(roteador1, switch1, bw=1000)
   net.addLink(h1s2, switch2, bw=1000)
   net.addLink(roteador2, switch2, bw=1000)
   net.addLink(h2s3, switch3, bw=1000)
   net.addLink(h1s3, switch3, bw=1000)
   net.addLink(roteador3, switch3, bw=1000)
   net.addLink(h1s4, switch4, bw=1000)
   net.addLink(h2s4, switch4, bw=1000)
   net.addLink(roteador4, switch4, bw=1000)
   net.addLink(roteador1, roteador2, bw=1000)
   net.addLink(roteador1, roteador3, bw=1000)
   net.addLink(roteador2, roteador4, bw=1000)
   net.addLink(roteador3, roteador4, bw=1000)

   info("*** Starting network\n")
   net.start()
   net.staticArp()
   info("*** Applying switches configurations\n")
   switch1.cmd('ovs-ofctl add-flow {} "actions=output:NORMAL"'.format(switch1.name))
   switch2.cmd('ovs-ofctl add-flow {} "actions=output:NORMAL"'.format(switch2.name))
   switch3.cmd('ovs-ofctl add-flow {} "actions=output:NORMAL"'.format(switch3.name))
   switch4.cmd('ovs-ofctl add-flow {} "actions=output:NORMAL"'.format(switch4.name))
   info("*** Applying hosts and routers configurations\n")
   roteador1.cmd("ifconfig roteador1-eth0 200.15.35.254/24")
   roteador1.cmd("ifconfig roteador1-eth1 200.1.2.1/26")
   roteador1.cmd("ifconfig roteador1-eth2 200.1.2.65/26")
   roteador2.cmd("ifconfig roteador2-eth0 198.98.99.94/27")
   roteador2.cmd("ifconfig roteador2-eth1 200.1.2.2/26")
   roteador2.cmd("ifconfig roteador2-eth2 200.1.2.129/26")
   roteador3.cmd("ifconfig roteador3-eth0 200.57.59.254/24")
   roteador3.cmd("ifconfig roteador3-eth1 200.1.2.66/26")
   roteador3.cmd("ifconfig roteador3-eth2 200.1.2.193/26")
   roteador4.cmd("ifconfig roteador4-eth0 198.98.99.62/27")
   roteador4.cmd("ifconfig roteador4-eth1 200.1.2.130/26")
   roteador4.cmd("ifconfig roteador4-eth2 200.1.2.194/26")
   h1s1.cmd("ip route add default via 200.15.35.254")
   h2s1.cmd("ip route add default via 200.15.35.254")
   h1s2.cmd("ip route add default via 198.98.99.94")
   h1s3.cmd("ip route add default via 200.57.59.254")
   h2s3.cmd("ip route add default via 200.57.59.254")
   h1s4.cmd("ip route add default via 198.98.99.62")
   h2s4.cmd("ip route add default via 198.98.99.62")
   roteador1.cmd("ip route add 198.98.99.64/27 via 200.1.2.2 ")
   roteador1.cmd("ip route add 200.57.59.0/24 via 200.1.2.66")
   roteador1.cmd("ip route add 198.98.99.32/27 via 200.1.2.2")
   roteador2.cmd("ip route add 198.98.99.32/27 via 200.1.2.130")
   roteador2.cmd("ip route add 200.57.59.0/24 via 200.1.2.130")
   roteador2.cmd("ip route add 200.15.35.0/24 via 200.1.2.1")
   roteador3.cmd("ip route add 200.15.35.0/24 via 200.1.2.65")
   roteador3.cmd("ip route add 198.98.99.32/27 via 200.1.2.194")
   roteador3.cmd("ip route add 198.98.99.64/27 via 200.1.2.194")
   roteador4.cmd("ip route add 198.98.99.64/27 via 200.1.2.129")
   roteador4.cmd("ip route add 200.57.59.0/24 via 200.1.2.193")
   roteador4.cmd("ip route add 200.15.35.0/24 via 200.1.2.193")
    
   info("*** Running CLI\n")
   CLI(net)
    
   info("*** Stopping network\n")
   net.stop()
    
if __name__ == "__main__":
 setLogLevel("info")
 remote_controller = False
 topology(remote_controller