**Installation and usage: gsr   -  Gnuradio Spectro Radiometer**

Author : Pierre Terrier

The code is based of baa_seminar gnuradio created by Marcus Leech (CCERA)
![gsr1](https://github.com/user-attachments/assets/950105db-625b-4c65-adda-832d558dfd15)


You can see an fork of baa_seminar that have created here : https://github.com/Radio-Source/baa_seminar_fork 

**Introduction**

This document describes the installation, system requirements, and usage of the *Gnu Radio* application known as **gsr** Gnuradio Spectro Radiometer.

**System Requirements**

**Ubuntu 24.04 LTS** or **Windows 10/11**

The system hardware should be a fairly-modern, multi-core system, preferably X86-based, but some of the higher-end ARM SBCs, like the *Raspberry PI 4/5* will also work, albeit at lower sample rates.

There should be at least 2G of system memory, with a basic clock speed of at least 1.4GHz for X86 systems, and 1.8GHz for ARM systems.

*SDR requirements*

The software supports many different SDR hardware platforms:

-   USRP products: B2xx series, and N2xx, X3xx and N3xx series

-   RTLSDR dongles

-   HackRF

-   LimeSDR and LimeSDR-mini

-   AirSpy R2 and AirSpy mini

This document will **NOT** cover installation requirements for this hardware, as that information is generally provided by the manufacturers.

Prerequisite Installation  

There are certain prerequisites for the **gsr** software that must be satisfied before installing the software.

**- LINUX Install -**

1.  ### Development Tools

``` {.western style="margin-left: 0.38in; font-weight: normal"}
sudo apt install build-essential
```

``` {.western style="margin-left: 0.38in; font-weight: normal"}
sudo apt install git
```

``` {.western style="margin-left: 0.38in; font-weight: normal"}
sudo apt install python3-pip
```

``` {.western style="margin-left: 0.38in; font-weight: normal"}
pip install --user ephem --break-system-packages
```

1.  ### Gnu Radio

``` {.western style="margin-left: 0.38in; font-weight: normal"}
sudo apt-get install gnuradio gnuradio*
```

**Application: gsr**

In your home directory:

``` {.western style="margin-left: 0.38in"}
git clone https://github.com/Radio-Source/GSR
```

``` {.western style="margin-left: 0.38in; font-weight: normal"}
cd GSR
```
``` {.western style="margin-left: 0.38in; font-weight: normal"}
cd gsr
```
To copy ra_funcs.py to Python bin
``` {.western style="margin-left: 0.38in; font-weight: normal"}
sudo make install
```

1.  ### Invoking gsr

gsr is a Python3 script run by

``` {.western style="margin-left: 0.38in; font-weight: normal"}
python3 gsr.py 
```

But also you run gsr from GnuRadio-Compagnion

------------------------

Windows (10-11) Install
------------------------
Prerequisite Installation  

There are certain prerequisites for the **gsr** software that must be satisfied before installing the software.

1.  ### Development Tools

Download and install Python 3.12 or 3.13
``` {.western style="margin-left: 0.38in; font-weight: normal"}
https://www.python.org/downloads/windows/
```

Download and install radioconda (Gnu Radio for Windows)
``` {.western style="margin-left: 0.38in; font-weight: normal"}
 https://github.com/ryanvolz/radioconda
```

Download and install Ephem from binaries for windows
``` {.western style="margin-left: 0.38in; font-weight: normal"}
https://pypi.org/project/ephem/#files
```

Download and install git for windows
``` {.western style="margin-left: 0.38in; font-weight: normal"}
https://git-scm.com/downloads/win
```
Download git for easy copying my repository https://git-scm.com/downloads/win After install open CMD shell and goto your Documents directory Then type command :

git clone https://github.com/Radio-Source/GSR/
![gsr2](https://github.com/user-attachments/assets/0a1f7495-0c65-4722-9dec-c1f20a90395a)

Goto in your Documents in GSR subdir and gsr subdir

Copy ra_funcs.py file to Scrpits radioconda subdir.
Radioconda is in your users space subdir
example for me user name is "smrt" in this screeshot
![gsr3](https://github.com/user-attachments/assets/2be19355-84a0-4c53-b76e-0716f2475386)


**Then reboot Windows to load ra_funcs.py at start of radioconda next time**

And open Gnuradio

![new_gr-radio_astro-gnuradio-windows](https://github.com/user-attachments/assets/faffae3b-cf05-425c-b59d-6246b7e8b241)




In file menu goto /Documents/GSR/gsr/ directory and open "gsr.grc" then run flowgraph
![gsr4](https://github.com/user-attachments/assets/b484ef1a-316f-4a34-b809-1db6c2184a0c)


You can run directly from CMD shell
For example on my computer my Users account is smrt
You can see this command line at run in radioconda
*C:\Users\smrt\radioconda\python.exe -u C:\Users\smrt\Documents\gsr\gsr.py*


Usage :
after running

You can change some parameters Location, longitude, latitude, amsl (Altitude above Mean Sea Level)

Antenna orientation parameters, for the moment we have chosen that the antenna only points upwards. It is oriented to the meridian in azimuth

You can choice Frequency file type .csv or ezRA type (txt)

ezRA file have header ezRA compatible, directly usable with ezCon see https://github.com/tedcline/ezRA/


![gsr1](https://github.com/user-attachments/assets/53c6b99c-0e2a-451c-ba3c-04b9259ef5fb)

