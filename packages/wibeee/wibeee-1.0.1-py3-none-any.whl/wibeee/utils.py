import socket


def getMachineIP():
    # this returns the internet connected IP of the device running this code
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def getBaseIP(ip=None):
    # where ip is a full local ip address
    # this function gets the base IP of the local network,
    # most networks have a base IP of 192.168.1.
    if not ip:
        ip = getMachineIP()
    ip = ip.split(".")
    baseIP = ""
    for i in range(len(ip) - 1):
        baseIP += ip[i] + "."
    return baseIP


def getSchemaURL(ip, port):
    return "http://{0}:{1}".format(ip, port)
