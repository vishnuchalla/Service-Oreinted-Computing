from bungie.statistics import *


def test_net_usage():
    net = net_usage("")
    print(net)
    assert net


def test_cpu_usage():
    cpu = cpu_usage()
    print(cpu)
    assert cpu


def test_mem_usage():
    mem = mem_usage()
    print(mem)
    assert mem
