import usb
import time

STATE_LID_DOWN = 21
STATE_LID_UP = 23
STATE_BUTTON_DOWN = 22


class Button(object):
    """Button object for the Dream Cheeky BIG RED BUTTON.

    Provides the following event methods to override in your subclass:
    - lid_down
    - lid_up
    - button_down
    - button_up


    Usage:
    btn = Button()
    btn.connect()

    while 1:
        btn.heartbeat()

    btn.disconnect()
    """
    def __init__(self, vendor_id=0x1d34, product_id=0x000d, interval=0.02):
        self.interface = 0
        self.interval = interval
        self.current_state = STATE_LID_DOWN
        self.previous_state = STATE_LID_DOWN

        self.dev = usb.core.find(idVendor=vendor_id,
                                 idProduct=product_id)

        if self.dev is None:
            print "Device couldn't be found"
            sys.exit(1)

        # Events for direct device results, doesn't include the
        # button up event
        self.map = {STATE_LID_DOWN: self.lid_down,
                    STATE_LID_UP: self.lid_up,
                    STATE_BUTTON_DOWN: self.button_down}


    def connect(self):
        # Deactivate kernel driver if it's active
        if self.dev.is_kernel_driver_active(self.interface) is True:
            self.dev.detach_kernel_driver(self.interface)

        self.dev.set_configuration()

        usb.util.claim_interface(self.dev, self.interface)

        self.endpoint = self.dev[0][(0,0)][0]


    def heartbeat(self):
        # Send a USB control packet
        result = self.dev.ctrl_transfer(bmRequestType=0x21,
                                        bRequest=0x09,
                                        wValue=0x0200,
                                        data_or_wLength="\x00\x00\x00\x00\x00\x00\x00\x02")

        # Read the result
        try:
            result = self.dev.read(self.endpoint.bEndpointAddress,
                                    self.endpoint.wMaxPacketSize)
        except usb.core.USBError, e:
            # Sometimes see a timeout but it's not fatal
            return

        self.current_state = result[0]

        # Cheesy event dispatcher - have to hard-code the
        # button up event as there isn't an explicit state
        # for it.
        if self.current_state != self.previous_state:
            if self.previous_state == STATE_BUTTON_DOWN and self.current_state == STATE_LID_UP:
                self.button_up()
            else:
                self.map[self.current_state]()

        # Store the previous state and rest for an interval
        self.previous_state = self.current_state
        time.sleep(self.interval)

    def disconnect(self):
        usb.util.release_interface(self.dev, self.interface)
        self.dev.attach_kernel_driver(self.interface)

    def lid_down(self):
        pass

    def lid_up(self):
        pass

    def button_down(self):
        pass

    def button_up(self):
        pass
