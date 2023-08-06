from .utils import *
from .errors import *
import requests
import xmltodict
import time
import os
import datetime
import xml


class WiBeee:
    def __init__(self, host=None, port=80, timeout=10.0, verbose=False):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.verbose = verbose
        if not host:
            print("Discovering all IPs, this will take some time...\n")
            self.host = self.autoDiscover()
            print("\nIP found! Use \"WiBeee('{0}')\" next time instead of just \"WiBeee()\"\nIP: {0}".format(self.host))
        self.baseURL = getSchemaURL(self.host, self.port)

    def callURL(self, url, attempts=1):
        """Call URL function."""
        request = requests.Request("GET", url).prepare()
        if attempts > 10:
            raise TooManyAttempts("Multiple attempts to connect to the device failed")
        try:
            with requests.Session() as sess:
                response = sess.send(
                    request, timeout=self.timeout
                )
            return response.text
        except requests.exceptions.ConnectionError as e:
            if self.verbose:
                print(e)
            time.sleep(1)
            return self.callURL(url, attempts + 1)
        except requests.exceptions.ReadTimeout as e:
            if self.verbose:
                print(e)
            return self.callURL(url, attempts + 1)
        except requests.exceptions.Timeout as e:
            if self.verbose:
                print(e)
            pass
        raise BadHostName("The WiBeee device seems to be down, try autodiscovery to get the correct url")

    def autoDiscover(self):
        baseIP = getBaseIP()
        for num in range(2, 255):  # for each possible IP on local network
            ip = baseIP + str(num)
            # -t timing is 1 second
            # -c is number of requests
            pingStatus = os.system('ping -t 1 -c 1 ' + ip)
            if not pingStatus:  # if result is not an error
                url = getSchemaURL(ip, self.port) + "/en/login.html"
                try:
                    if "<title>WiBeee</title>" in self.callURL(url):  # if the webpage has WiBee in it
                        return ip  # then the ip is correct and the WiBee device was found
                except TooManyAttempts:
                    # except the error because the device testing isn't WiBee, then this error will be raised
                    pass

        raise NoWiBeeeDevices("No WiBee Devices were found on the local network")

    def getHost(self):
        return self.host

    def getStatus(self):
        url = self.baseURL + "/en/status.xml"
        response = self.callURL(url)
        try:
            return xmltodict.parse(response)["response"]
        except xml.parsers.expat.ExpatError as e:
            if self.verbose:
                print(e)
            return self.getStatus()

    def voltage(self, phase=1):
        # rms is root-mean-square
        key = "fase{}_vrms".format(phase)
        return float(self.getStatus()[key])

    def current(self, phase=1):
        key = "fase{}_irms".format(phase)
        return float(self.getStatus()[key])

    def frequency(self, phase=1):
        key = "fase{}_frecuencia".format(phase)
        return float(self.getStatus()[key])

    def power(self, phase=1, pretty=False):
        key = "fase{}_p_activa".format(phase)
        status = float(self.getStatus()[key])
        if pretty:
            return "{0} - {1} W".format(datetime.datetime.now(), status)
        return status
