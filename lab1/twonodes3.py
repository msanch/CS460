from src.sim import Sim
from src.packet import Packet
from networks.network import Network


class DelayHandler(object):
    @staticmethod
    def receive_packet(packet):
        print('Created:{0}  ID:{1}  Received:{2}'.format(
            packet.created,
            packet.ident,
            Sim.scheduler.current_time()
        ))


def main():
    # parameters
    Sim.scheduler.reset()

    # setup network
    net = Network('twonodes3.txt')

    # setup routes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n1.add_forwarding_entry(address=n2.get_address('n1'), link=n1.links[0])
    n2.add_forwarding_entry(address=n1.get_address('n2'), link=n2.links[0])

    # setup app
    d = DelayHandler()
    net.nodes['n2'].add_protocol(protocol="delay", handler=d)

    # send one packet
    p1 = Packet(destination_address=n2.get_address('n1'), ident=1, protocol='delay', length=1000)
    Sim.scheduler.add(delay=0, event=p1, handler=n1.send_packet)
    p2 = Packet(destination_address=n2.get_address('n1'), ident=2, protocol='delay', length=1000)
    Sim.scheduler.add(delay=0, event=p2, handler=n1.send_packet)
    p3 = Packet(destination_address=n2.get_address('n1'), ident=3, protocol='delay', length=1000)
    Sim.scheduler.add(delay=0, event=p3, handler=n1.send_packet)
    p4 = Packet(destination_address=n2.get_address('n1'), ident=4, protocol='delay', length=1000)
    Sim.scheduler.add(delay=2, event=p4, handler=n1.send_packet)

    # run the simulation
    Sim.scheduler.run()


if __name__ == '__main__':
    main()

"""
Created:0  ID:1  Received:0.018000000000000002
Created:0  ID:2  Received:0.026000000000000002
Created:0  ID:3  Received:0.034
Created:2.0  ID:4  Received:0.017999999999999794
"""
