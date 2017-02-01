from src.sim import Sim
import sys
sys.path.append('..')


def say_packet(packet):
    print(packet)


def main():
    Sim.scheduler.reset()
    Sim.scheduler.add(delay=0, event="Hello", handler=say_packet)
    Sim.scheduler.add(delay=4, event="Goodbye", handler=say_packet)
    Sim.scheduler.run()


if __name__ == '__main__':
    main()
