from src.sim import Sim
from src.packet import Packet
from networks.network import Network


class DelayHandler(object):
    @staticmethod
    def receive_packet(packet):
        print('Created:{0}  ID:{1}  Received:{2}'.format(
            packet.created, packet.ident, Sim.scheduler.current_time() - packet.created)
        )


def main():
    # parameters
    Sim.scheduler.reset()

    # setup network
    net = Network('twonodes1.txt')

    # setup routes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n1.add_forwarding_entry(address=n2.get_address('n1'), link=n1.links[0])
    n2.add_forwarding_entry(address=n1.get_address('n2'), link=n2.links[0])

    # setup app
    d = DelayHandler()
    net.nodes['n2'].add_protocol(protocol="delay", handler=d)

    # send one packet
    p = Packet(destination_address=n2.get_address('n1'), ident=1, protocol='delay', length=1000)
    Sim.scheduler.add(delay=0, event=p, handler=n1.send_packet)

    # run the simulation
    Sim.scheduler.run()


if __name__ == '__main__':
    main()

"""
Created:0  ID:1  Received:1.008
"""
