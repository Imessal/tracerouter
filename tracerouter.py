import time
from subprocess import Popen, PIPE
import re
import json
import urllib.request
import urllib.error
import sys

IPS = []
start = time.time()
first = True
count = 0


def get_ips(line):
    pattern = r'[0-9]+(?:\.[0-9]+){3}'
    global first
    global count
    ip = re.findall(pattern, line)
    try:
        if first:
            IPS.append(ip[0])
            print('connecting to', ip[0], '\n')
            first = False
        else:
            IPS.append(ip[0])
            response = do_request(ip[0])
            nice_print(count, ip[0], **response)
            count += 1
    except IndexError:
        pass


def nice_print(number, ip, system, isp, country):
        number = format("{0:<4}".format(str(number))) + '|'
        ip = format("{0:<16}".format(ip)) + '|'
        country = format("{0:<7}".format(country)) + '|'
        system = format("{0:<10}".format(system)) + '|'
        isp = format("{0:<20}".format(isp))
        print(number, ip, country, system, isp)


def do_request(ip):
    url = 'http://ipinfo.io/{}/json'.format(ip)
    raw = urllib.request.urlopen(url)
    response = json.load(raw)
    if response:
        return parse_response(response)
    else:
        return '######'


def parse_response(response):
    result = {}
    if 'org' in response:
        result['system'] = response['org'].split()[0]
        result['isp'] = response['org'].split(' ', 1)[1]
    else:
        result['system'] = '######'
        result['isp'] = '######'
    if 'country' in response:
        result['country'] = response['country']
    else:
        result['country'] = '######'
    return result


def main(host):
    global start
    p = Popen(['tracert', host], stdout=PIPE)
    while time.time() - start < 10:
        start = time.time()
        line = p.stdout.readline()
        if not line:
            break
        else:
            try:
                get_ips(str(line))
            except urllib.error.URLError:
                print('URL error uccured. Check your internet connection')
                break

    if len(IPS) > 0:
        if IPS[0] == IPS[len(IPS)-1]:
            print('\nFinished!')
        else:
            print("Couldn't reach router")
    else:
        print("Error! Probably no Internet connection or invalid address")


if __name__ == '__main__':
    main(sys.argv[1])
