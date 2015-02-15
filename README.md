# Dream Cheeky - Big Red Button

Driver for http://dreamcheeky.com/big-red-button in python using
pyusb.

To set up on linux:

Copy the 99-dream_cheeky_button.rules into /etc/udev/rules.d

Then install the apt dependencies:

    apt-get install libusb-dev

Install python dependencies:

    pip install pyusb==1.0.0b2
