# hands-free-drone
This project is part of Saturdays AI Barcelona 2020 Spring Edition

Team members: Albert Montserrat, Asma Bensalah, Eva Deltor, Ali Abdul, Antonio Tripiana

## Useful info
OPEN BCI - Ganglion Getting Started Guide https://docs.openbci.com/docs/01GettingStarted/01-Boards/GanglionGS

OPEN BCI - EEG Getting Started Guide https://github.com/OpenBCI/Docs/blob/master/Tutorials/02-Ganglion_Getting%20Started_Guide.md

HOW TO CLEAN EEG ELECTRODES https://www.wikihow.com/Clean-EEG-Electrodes

![head-sensors](img/head-sensors.jpg)

![sensors-test](img/ganglion_EEG-plugged.jpg)

![sensors-test](img/IMG_4755.jpg)


## Drone API

Run `pipenv shell --python 3.6`
Run `pipenv install`

To fix the multiprocessing problem do:

```
nano .bash_profile
```

Add the following line to the end of the file:

```
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

if you're using oh-my-zsh, edit ~/.zshrc and put this export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES at the beginning of file.


## EEG API

EEG API runs using BrainFlow library.
https://brainflow.readthedocs.io/en/stable/

BrainFlow is a library intended to obtain, parse and analyze EEG, EMG, ECG and other kinds of data from biosensors.

Running the ganglion board on macOS: `python read.py --board-id 1 --serial-port /dev/cu.usbmodem11 --log`

Note this can change depending on the operating system.
