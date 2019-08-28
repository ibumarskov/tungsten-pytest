import random
import re


def rand_name(name='', prefix='tft'):
    """Generate a random name that includes a random number

    :param str name: The name that you want to include
    :param str prefix: The prefix that you want to include
    :return: a random name. The format is
             '<prefix>-<name>-<random number>'.
             (e.g. 'prefixfoo-namebar-154876201')
    :rtype: string
    """
    rand_name = str(random.randint(1, 0x7fffffff))
    if name:
        rand_name = name + '-' + rand_name
    if prefix:
        rand_name = prefix + '-' + rand_name
    return rand_name


def parser_iperf_output(text, udp=False):
    """Parse summary line written by an `iperf` run into a Python dict."""
    pattern = (r'\[(.{3})\]\s+(?P<interval>.*?sec)\s+'
               r'(?P<transfer>.*?Bytes|bits)'
               r'\s+(?P<bandwidth>.*?/sec)')
    if udp:
        pattern += r'\s+(?P<jitter>.*?s)\s+(?P<datagrams>\d+/\s*\d+)\s+' \
                   r'\((?P<datagrams_rate>\d+)%\)'
    iperf_re = re.compile(pattern)
    for line in text.splitlines():
        match = iperf_re.match(line)
        if match:
            iperf = match.groupdict()
            bval, bunit = iperf['bandwidth'].split()
            iperf['bandwidth'] = float(bval)
            iperf['bandwidth_unit'] = bunit
            tval, tunit = iperf['transfer'].split()
            iperf['transfer'] = float(tval)
            iperf['transfer_unit'] = tunit
            lost, total = iperf['datagrams'].replace(" ", "").split('/')
            iperf['datagrams_lost'] = int(lost)
            iperf['datagrams'] = int(total)
            iperf['datagrams_rate'] = int(iperf['datagrams_rate'])
            return iperf
    return {}
