from __future__ import print_function

from src.sim import Sim
from src.packet import Packet

from networks.network import Network

import random

import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np


class Generator(object):
    def __init__(self, node, destination, load, duration):
        self.node = node
        self.load = load
        self.destination = destination
        self.duration = duration
        self.start = 0
        self.ident = 1

    def handle(self, event):
        # quit if done
        now = Sim.scheduler.current_time()
        if (now - self.start) > self.duration:
            return

        # generate a packet
        self.ident += 1
        p = Packet(destination_address=self.destination, ident=self.ident, protocol='delay', length=1000)
        Sim.scheduler.add(delay=0, event=p, handler=self.node.send_packet)
        # schedule the next time we should generate a packet
        Sim.scheduler.add(delay=random.expovariate(self.load), event='generate', handler=self.handle)


total_packets = 0
total_queue_delay = 0


class DelayHandler(object):
    @staticmethod
    def receive_packet(packet):
        global total_packets, total_queue_delay
        total_packets += 1
        total_queue_delay += packet.queueing_delay


def main():

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

    plot_data = []

    for rate in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, .8, 0.9, 0.95, 0.97]:
        # parameters
        Sim.scheduler.reset()

        # setup packet generator
        destination = n2.get_address('n1')
        max_rate = 1000000 // (1000 * 8)
        load = rate * max_rate
        g = Generator(node=n1, destination=destination, load=load, duration=100)
        Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

        # run the simulation
        global total_packets, total_queue_delay
        total_packets = 0
        total_queue_delay = 0
        Sim.scheduler.run()
        avg_queue_delay = total_queue_delay / total_packets
        plot_data.append([rate, avg_queue_delay])

    data_rows = ['Utilization', 'Queueing Delay']
    with open('lab1.csv', 'w', newline='') as csv_file:
        data_writer = csv.writer(csv_file)
        data_writer.writerow(data_rows)
        for row in plot_data:
            data_writer.writerow(row)

    plt.style.use('ggplot')
    pd.set_option('display.width', 1000)
    data = pd.read_csv("lab1.csv")
    plt.figure()
    ax = data.plot(x=data_rows[0], y=data_rows[1])
    ax.set_xlabel(data_rows[0])
    ax.set_ylabel(data_rows[1])
    # fig = ax.get_figure()
    # fig.savefig('line.png')

    service = (1000.0 * 8) / 1000000
    mu = 1.0 / service
    rho = np.arange(0, 1, 1.0 / 100)
    print((1 / (2 * mu)) * (rho / (1 - rho)))
    data_theoretical = pd.Series((1 / (2 * mu)) * (rho / (1 - rho)), index=rho)
    bx = data_theoretical.plot(x=data_rows[0], y=data_rows[1])
    bx.set_xlabel(data_rows[0])
    bx.set_ylabel(data_rows[1])
    fig2 = bx.get_figure()
    fig2.savefig('r.png')


if __name__ == '__main__':
    main()
