# Python-based web server interface for Magstim Rapid2 TMS device
Note: Currently under development, so this README is inaccurate.

## Installation

Requires [setuptools](https://pypi.python.org/pypi/setuptools#installation-instructions)
In the project directory run: 
```
python setup.py install
```

## Instructions

```python
#Import your stimulator class
from Magstim.MagstimInterface import Magstim, Rapid2
#Define your serial port
serPort='COM6'

#If using an additional device to do the triggering (highly recommended), try this
#This requires my caio module (see below)
from Caio.TriggerBox import TTL 
stimulator=Bistim(port=serPort, trigbox=TTL())

#Else if using the serial port to trigger (note: indeterminate lag/jitter!)
stimulator=Bistim(port=serPort)

#The following functions and attributes are now available to you.
stimulator.armed #Read-Write. Set equal to True to arm. E.g., stimulator.armed = True
stimulator.trigger()
stimulator.ready #read-only. Returns whether or not the stimulator is ready. Note that Bistim does not support this feature.
stimulator.remocon #read-write. Set to True to enable. Should be enabled by default on stimulator init.
stimulator.intensity #read-write. Set equal to an int value to change stimulator intensity. e.g. stimulator.intensity = 30

stimulator.train_duration #How long the stimulus train lasts in seconds
stimulator.train_frequency #Pulse frequency, in Hz
stimulator.train_pulses #Number of pulses in the train
```

## Differences from upstream repository

* No Bistim support
* Adds a layer for REST-ful control of the TMS device
