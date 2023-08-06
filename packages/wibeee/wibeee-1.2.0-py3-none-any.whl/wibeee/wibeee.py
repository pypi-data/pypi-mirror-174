from .utils import *
from .errors import *
import datetime
import requests
import xmltodict
import time
import os
import xml


class WiBeee:
    def __init__(self, ip=None, port=80, timeout=10.0, verbose=False):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.verbose = verbose
        if not ip:
            print("Discovering all IPs, this will take some time...\n")
            self.ip = self.__findDeviceIP()
            print("\nIP found! Use \"WiBeee('{0}')\" next time instead of just \"WiBeee()\"\nIP: {0}".format(self.ip))
        self.baseURL = getSchemaURL(self.ip, self.port)

    def __callURL(self, url, attempts=1):
        request = requests.Request("GET", url).prepare()
        if attempts > 10:
            raise TooManyAttempts("Multiple attempts to connect to the device failed")
        try:
            with requests.Session() as sess:
                response = sess.send(request, timeout=self.timeout)
            return response.text
        except requests.exceptions.ConnectionError as e:
            if self.verbose:
                print("\nError I need to deal with")
                print(e)
                print("")
            time.sleep(1)
            return self.__callURL(url, attempts + 1)
        except requests.exceptions.ReadTimeout as e:
            if self.verbose:
                print(e)
            return self.__callURL(url, attempts + 1)
        except requests.exceptions.Timeout as e:
            if self.verbose:
                print(e)
            pass
        raise BadIP("The WiBeee device seems to be down, try autodiscovery to get the correct url")

    def __findDeviceIP(self, attempts=1):
        # This function finds / discovers the IP of a WiBeee device
        # attemps is the number of packets sent and received.
        # Usually 1 is enough, but there was one test where it wasn't
        baseIP = getBaseIP()
        for num in range(2, 255):  # for each possible IP on local network
            ip = baseIP + str(num)
            # -t timing is 1 second
            # -c is number of requests
            pingStatus = os.system("ping -t 1 -c {0} {1}".format(attempts, ip))
            if not pingStatus:  # if result is not an error
                url = getSchemaURL(ip, self.port) + "/en/login.html"
                try:
                    if "<title>WiBeee</title>" in self.__callURL(url):  # if the webpage has WiBee in it
                        return ip  # then the ip is correct and the WiBee device was found
                except TooManyAttempts:
                    # except the error because the device testing isn't WiBee, then this error will be raised
                    pass

        raise NoWiBeeeDevices("No WiBee Devices were found on the local network")

    def __getInfo(self):
        url = self.baseURL + "/en/status.xml"
        response = self.__callURL(url)
        try:
            return xmltodict.parse(response)["response"]
        except xml.parsers.expat.ExpatError as e:
            if self.verbose:
                print(e)
                print(response)
            return self.__getInfo()

    def setTimeout(self, timeout):
        self.timeout = timeout

    def setVerbose(self, verbose):
        assert verbose is type(bool)
        self.verbose = verbose

    def getPower(self, phase=1):
        # returns the active power use, not calculated
        key = "fase{}_p_activa".format(phase)
        return float(self.__getInfo()[key])

    def getCurrent(self, phase=1):
        # rms is root-mean-square
        key = "fase{}_irms".format(phase)
        return float(self.__getInfo()[key])

    def getVoltage(self, phase=1):
        # rms is root-mean-square
        key = "fase{}_vrms".format(phase)
        return float(self.__getInfo()[key])

    def getFrequency(self, phase=1):
        key = "fase{}_frecuencia".format(phase)
        return float(self.__getInfo()[key])

    def getScale(self):
        # I don't know what units are used here
        return int(self.__getInfo()["scale"])

    def getCoilStatus(self):
        return self.__getInfo()["coilStatus"]

    def getGround(self):
        # idk what the units are, I am assuming volts
        return self.__getInfo()["ground"]

    def getIP(self):
        return self.ip

    def getModel(self):
        return self.__getInfo()["model"]

    def getFirmwareVersion(self):
        return self.__getInfo()["webversion"]

    def getTime(self):
        deviceTime = int(self.__getInfo()["time"])
        return datetime.datetime.fromtimestamp(deviceTime)
