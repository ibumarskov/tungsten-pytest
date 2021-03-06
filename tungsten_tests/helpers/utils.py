import logging
import random
import re

logger = logging.getLogger()


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


def check_iperf_res(res, loss_rate=1):
    """Check `iperf` test results."""
    logger.info("Iperf data:\n{}".format(res))
    if not res:
        raise Exception("Traffic wasn't detected")
    elif res['datagrams_rate'] > loss_rate:
        raise Exception("The loss of traffic is too much.\n"
                        "Expected: {}% Loss: {}%"
                        "".format(loss_rate, res['datagrams_rate']))


def parser_lb_responses(text, req_num, member_num):
    res_list = text.splitlines()
    if len(res_list) != req_num:
        raise Exception("Amount of requests ({}) isn't equal to output:\n"
                        "{}".format(req_num, res_list))
    unique_res = set(res_list)
    if len(unique_res) != member_num:
        raise Exception("Amount of unique responses isn't equal to amount of "
                        "pool members ({}):\n"
                        "{}".format(member_num, unique_res))
    stat = {}
    for i in unique_res:
        stat.update({i: res_list.count(i)})
    logger.info("LB response statistics:\n{}".format(stat))
    return stat
