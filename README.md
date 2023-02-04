# MicroPython HTTPS Test
There is an ominous warning in [the MicroPython docs for the SSL module](https://docs.micropython.org/en/latest/library/ssl.html):
> Some implementations of `ssl` module do NOT validate server certificates, which makes an SSL connection established prone to man-in-the-middle attacks.

The code in this repository aims to test various implementations / microcontrollers, using the examples from [The Chromium Project's badssl.com](https://badssl.com/).

## Getting Started

You will need to edit `config.py` to include the SSID and PSK of the local wireless network.
