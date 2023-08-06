```
██╗    ██╗██╗██████╗ ███████╗███████╗███████╗
██║    ██║██║██╔══██╗██╔════╝██╔════╝██╔════╝
██║ █╗ ██║██║██████╔╝█████╗  █████╗  █████╗  
██║███╗██║██║██╔══██╗██╔══╝  ██╔══╝  ██╔══╝  
╚███╔███╔╝██║██████╔╝███████╗███████╗███████╗
 ╚══╝╚══╝ ╚═╝╚═════╝ ╚══════╝╚══════╝╚══════╝
```
This is a python API client for WiBeee products. WiBeee client will get live info like Power (W) usage in an easy-to-use python class.
Currently, WiBeee is in the early stages and can be improved. If you have any feature requests or optimisations,
feel free to set up a pull request or drop me a message.

This project assumes you already have your WiBeee hardware setup.
This project was inspired by [pywibeee](https://pypi.org/project/pywibeee/).
To see code examples checkout `examples.py` or scroll down to [usages](https://github.com/veryheavypickle/wibeee#usages)

### Projects that use yodas
No open source projects yet! Send me your projects to be featured here.

Install
=======

From PIP
--------
The easiest method of installing is through pip
```shell
$ pip install wibeee
```
or to upgrade
```shell
$ pip install --upgrade wibeee 
```

From Git Repository
-------------------
For this I assume you already have a virtual python environment or that python3 is aliased as python.
```shell
$ python -m pip install --upgrade build
$ python -m build
$ pip install dist/*.tar.gz  # for the latest version of yodas.
```

From Releases (latest)
-------------
```shell
$ wget https://github.com/veryheavypickle/wibeee/releases/download/v1.2.0/wibeee-1.2.0.tar.gz
$ pip install wibeee-1.2.0.tar.gz
```

Usages
=========
### Connecting
If you know the local IP address of your WiBeee device, then you can connect as such.
```python
>>> from wibeee import WiBeee
>>> wb = WiBeee("192.168.1.150")
```

If you don't know the IP address, don't worry as there is a discovery function
and it will connect to the first WiBeee device it finds. This discovery will take a while.
```python
>>> from wibeee import WiBeee
>>> wb = WiBeee()
```

### WiBeee
```python
>>> from wibeee import WiBeee
>>> wb = WiBeee(ip=None, port=80, timeout=10.0, verbose=False)
```
> *ip:* `str`
> 
> *port:* `int`
> 
> *timeout:* `float`
> 
> *verbose:* `bool`
> 
> **returns:** `WiBeee`

**ip**
This is the IP address of the WiBeee device. `ip` is not a required variable but providing `ip` skips discovery which speeds up the process.
For example `WiBeee("192.168.1.150")` or `WiBeee(ip="192.168.1.150")`.

**port**
By default it is `80`, This is the open port of the WiBeee device webserver.

**timeout**
By default it is `10.0`, This is how many seconds the program waits while attempting to connect to the WiBeee device.
If you wish to change this after creating the `WiBeee` object, simply run `WiBeee.setTimeout(newValue)`.

**verbose**
By default it is `False`, in my case the WiBeee webserver is highly unreliable. If you want to watch `wibeee` solve errors in real time,
either set `verbose=True` when creating the `WiBeee` object or `WiBeee.setVerbose(True)`.

### Power
```python
>> > wb.getPower()
100.0
```
This function returns the current power usage in Watts (W). The phase is by default `1` but can be up to `4`.
> *phase:* `int`
> 
> **returns:** `float`

### Current
```python
>> > wb.getCurrent()
1.0
```
This function returns the current amp usage in Amps (A). The phase is by default `1` but can be up to `4`.
> *phase:* `int`
> 
> **returns:** `float`

### Voltage
```python
>> > wb.getVoltage()
230.0
```
This function returns the voltage in Volts (V). The phase is by default `1` but can be up to `4`.
> *phase:* `int`
> 
> **returns:** `float`

### Frequency
```python
>> > wb.getFrequency()
50.0
```
This function returns the frequency (Hz) of the AC . The phase is by default `1` but can be up to `4`.
> *phase:* `int`
> 
> **returns:** `float`

### Scale
```python
>> > wb.getScale()
60
```
This function returns the scale. Currently, I don't know what `scale` is or what its units are, but the functionality exists.
> **returns:** `int`

### Coil Status
```python
>> > wb.getCoilStatus()
'-'
```
This function returns the coil status. Currently, I don't know what the possible statuses are, I will update this README once I do know.
> **returns:** `str`

### Ground
```python
>> > wb.getGround()
'-'
```
This function returns the ground. I am assuming that ground is in Volts (V)
> **returns:** `float`

### Model
```python
>> > wb.getGround()
'-'
```
This function returns the ground. I am assuming that ground is in Volts (V)
> **returns:** `float`

### IP
```python
>>> wb.getIP()
'192.168.1.150'
```
This function returns the ip address of the WiBeee device.
> **returns:** `str`

### Model
```python
>>> wb.getModel()
'WBB'
```
This function returns the model the WiBeee device.
> **returns:** `str`

### Firmware Version
```python
>>> wb.getFirmwareVersion()
'4.4.164'
```
This function returns the firmware version of the WiBeee device.
> **returns:** `str`

### Time
```python
>>> wb.getTime()
2022-10-30 16:57:22
```
This function returns the current time in the device.
The return type is `datetime.datetime`, you can read more about it [here](https://www.geeksforgeeks.org/python-datetime-datetime-class/)
> **returns:** `datetime.datetime`

Changelog
=========
1.2.0
-----
Added more functions

1. Added `WiBeee.getScale()`
2. Added `WiBeee.getCoilStatus()`
3. Added `WiBeee.getGround()`
4. Added `WiBeee.getModel()`
5. Added `WiBeee.getFirmwareVersion()`
6. Added `WiBeee.getTime()`
7. Moved `WiBeee.getInfo()` to `WiBeee.__getInfo()`
8. Moved `WiBeee.power()` to `WiBeee.getPower()`
9. Moved `WiBeee.current()` to `WiBeee.getCurrent()`
10. Moved `WiBeee.voltage()` to `WiBeee.getVoltage()`
11. Moved `WiBeee.frequency()` to `WiBeee.getFrequency()`

1.1.0
-----
Added documentation and changed function names

1. Moved `WiBeee.getHost()` to `WiBeee.getIP()`
2. Moved `WiBeee.host` to `WiBeee.ip`
3. Removed `pretty` option in `WiBeee.power()`
4. Moved `WiBeee.callURL()` to `WiBeee.__callURL()`
5. Moved `errors.BadHostName` to `errors.BadIP`
6. Moved `WiBeee.autoDiscover()` to `WiBeee.__findDeviceIP()`
7. Added variable `attempts` to `WiBeee.__findDeviceIP()`
8. Added `WiBeee.setTimeout()`
9. Added `WiBeee.setVerbose()`
