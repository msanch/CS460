from src.sim import Sim
from src.packet import Packet
from networks.network import Network


class DelayHandler(object):
    @staticmethod
    def receive_packet(packet):
        print('Created:{0}  ID:{1}  Received:{2}'.format(
            packet.created,
            packet.ident,
            Sim.scheduler.current_time() - packet.created
        ))


def main():
    # parameters
    Sim.scheduler.reset()

    # setup network
    net = Network('threenodes1-2.txt')

    # setup routes
    node_a = net.get_node('A')
    node_b = net.get_node('B')
    node_c = net.get_node('C')
    node_a.add_forwarding_entry(address=node_b.get_address('A'), link=node_a.links[0])
    node_b.add_forwarding_entry(address=node_c.get_address('B'), link=node_b.links[0])

    # setup app
    d = DelayHandler()
    net.nodes['A'].add_protocol(protocol='delay', handler=d)
    net.nodes['B'].add_protocol(protocol='delay', handler=d)
    net.nodes['C'].add_protocol(protocol='delay', handler=d)

    # send one packet
    for i in range(1000):
        p = Packet(destination_address=node_c.get_address('B'), ident=i, protocol='delay', length=1000)
        Sim.scheduler.add(delay=0, event=p, handler=node_a.send_packet)

    # run the simulation
    Sim.scheduler.run()


if __name__ == '__main__':
    main()

"""
1-1
Created:0  ID:995  Received:8.176000000000007
Created:0  ID:996  Received:8.184000000000006
Created:0  ID:997  Received:8.192000000000007
Created:0  ID:998  Received:8.200000000000006
Created:0  ID:999  Received:8.208000000000007

1-2
Created:0  ID:995  Received:0.2079760000000001
Created:0  ID:996  Received:0.2079840000000001
Created:0  ID:997  Received:0.20799200000000012
Created:0  ID:998  Received:0.20800000000000013
Created:0  ID:999  Received:0.20800800000000014
"""
