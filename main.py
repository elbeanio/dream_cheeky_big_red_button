from cheeky import Button


class MyButton(Button):
    def button_down(self):
        print "The button is down"

    def button_up(self):
        print "The button is up"

    def lid_down(self):
        print "The lid is down"

    def lid_up(self):
        print "The lid is up"


if __name__ == "__main__":
    btn = MyButton()
    btn.connect()

    while 1:
        btn.heartbeat()

    btn.disconnect()
