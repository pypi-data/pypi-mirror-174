from BirdBrain import Hummingbird

class HummingbirdLedButton:
    BRIGHTNESS_UP = 0
    BRIGHTNESS_DOWN = 100

    def __init__(self, device = None, brightness_up = None, brightness_down = None):
        self.device = device
        self.brightness_up = brightness_up
        self.brightness_down = brightness_down

        self.button = None

        if self.brightness_up is None: self.brightness_up = HummingbirdLedButton.BRIGHTNESS_UP
        if self.brightness_down is None: self.brightness_down = HummingbirdLedButton.BRIGHTNESS_DOWN

        if self.device is not None:
            try:
                self.button = Hummingbird(self.device)
            except ConnectionRefusedError:
                print("LED button device not available")
                raise

    def down(self, port):
        if self.button.getVoltage(port) > 0.0:
            self.indicate_down(port)
            return True
        else:
            self.indicate_up(port)
            return False

    def up(self, port):
        return(not self.down(port))

    def indicate_down(self, port):
        self.button.setLED(port, self.brightness_down)

    def indicate_up(self, port):
        self.button.setLED(port, self.brightness_up)