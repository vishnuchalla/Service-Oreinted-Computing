import logging
import asyncio

logger = logging.getLogger("bungie")

stats = {}


def splitlines(fd, sep=None, replace=None):
    "Return split lines from any file descriptor"
    fd.seek(0)
    for line in fd.readlines():
        if replace and sep:
            yield line.replace(replace, sep).split(sep)
        elif replace:
            yield line.replace(replace, " ").split()
        else:
            yield line.split(sep)


def net_usage(dev):
    """Total network usage in bytes"""
    net = open("/proc/net/dev")
    totals = {"rx bytes": 0, "tx bytes": 0, "rx packets": 0, "tx packets": 0}
    for line in splitlines(net, replace=":"):
        # logger.info(line)
        if len(line) < 17:
            continue
        if dev in line[0]:
            totals["rx bytes"] += int(line[1])
            totals["rx packets"] += int(line[2])
            totals["tx bytes"] += int(line[9])
            totals["tx packets"] += int(line[10])
    return totals


def cpu_usage():
    """CPU usage of the current cgroup in ns"""
    cpu = open("/sys/fs/cgroup/cpuacct/cpuacct.usage")
    return int(cpu.readline())


def mem_usage():
    """Memory usage of the current cgroup in bytes"""
    mem = open("/sys/fs/cgroup/memory/memory.usage_in_bytes")
    return int(mem.readline())


def update(dev="eth0"):
    stats.update({"cpu": cpu_usage(), "mem": mem_usage(), **net_usage(dev)})


async def stats_logger(interval=1, hide=[], only=None, dev=None):
    while True:
        update(dev) if dev else update()
        if only:
            logger.info({k: v for k, v in stats.items() if k in only})
        else:
            logger.info({k: v for k, v in stats.items() if k not in hide})
        await asyncio.sleep(interval)


def increment(statistic):
    "Increment a single statistic by name"
    stats[statistic] = stats.get(statistic, 0) + 1
