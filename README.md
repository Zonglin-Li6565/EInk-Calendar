# EInk Smart Calendar [![Build Status](https://travis-ci.com/zli117/EInk-Calendar.svg?branch=master)](https://travis-ci.com/zli117/EInk-Calendar)

<img src="https://raw.githubusercontent.com/zli117/EInk-Calendar/master/image.jpg" width="600">

## What does it do?
It's a raspberry pi based smart calendar that can tell you the current date,
weather, and your events on Google calendar. Updates once per hour. Also supports
manual update with a press of button.

## Components needed:
 * Raspberry pi (2 or 3 or zero) and SD card (with OS installed)
 * EInk display: [Waveshare 7.5 inch black and white display](https://www.waveshare.com/7.5inch-e-paper-hat.htm)
 * A 7.5 inch photo frame
 * A pushbutton
 * An LED
 * 330 Ohm resistor
 * Breadboard

## Enable SPI Mode:
To Enable, pass following command

```bash
sudo raspi-config
```

Select **Interfacing Options**

Select **P4 SPI**

Select **Yes** when asked **Would you like the SPI interface to be enabled?**

It will prompt The SPI interface is enabled, press ok

Select **Finish** to exit raspi-config

## Install the dependencies:
```bash
pip install -r requirements.txt
sudo apt install libopenjp2-7 libtiff5
```
Also make sure you have at least Python 3.7 installed, which should be the case for the most recent Raspbian releases.

## Get API credentials:
 * OWM API key:
   * Go to the Weather API page: [link](https://openweathermap.org/api)
   * Subscribe to **5 day / 3 hour forecast**
 * Google credentials:
   * Follow the instructions of this answer on [stackoverflow](https://stackoverflow.com/a/19766913/4434038).
   * Instead of choosing the drive API, choose Calendar API v3 of scope
     `https://www.googleapis.com/auth/calendar.readonly`
   * We will need the client ID, client secrete, refresh token and access token

## Hook up the wires:

<img src="https://raw.githubusercontent.com/zli117/EInk-Calendar/master/diagram.png" width="600">

Or download [diagram.fzz](https://github.com/zli117/EInk-Calendar/blob/master/diagram.fzz). Note that the labeling on
the breadboard corresponds to the wires on the hat comes with the screen. The wiring is the same as on page 12 of the
[official documentation](https://www.waveshare.com/w/upload/7/74/7.5inch-e-paper-hat-user-manual-en.pdf)


## Run it:
Once you have got all the credentials and hooked up the wires, you can run
`main.py` without any parameter to create the config file:
```bash
python3 main.py
```
and follow the interactive guide to create the config file.

You can specify the config file for later runs as:
```bash
python3 main.py -c <config file path>
```
