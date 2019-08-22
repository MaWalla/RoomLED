"""
Interprets the various things, the user will throw at this server
"""

LED_STRIPS = ('leds1', 'leds2', 'leds3')
LED_STRIP_LENGTH = {'leds1': 10, 'leds2': 10, 'leds3': 10}  # Replace with actual numbers
MODES = ('random',)


class ValidateJson:
    def __init__(self, json):
        self.json = json
        self.validated = self.input_valid

    @property
    def input_valid(self):
        for key, value in self.json.items():
            if key in LED_STRIPS:
                if self.check_mode(key, value):
                    pass
                else:
                    return False
            else:
                return False
        return True

    @staticmethod
    def check_mode(key, value):
        if type(value) is str:
            if value[0] == '#':
                if len(value) == 7 or len(value) == 3:
                    return True
            elif value in MODES:
                return True
        elif type(value) is list:
            if len(value) == 3:
                return True

        elif type(value) is dict:
            for led, rgb in value.items():
                if type(led) is str and int(led) < LED_STRIP_LENGTH.get(key):  # TODO try catch for nonetype or keyerror
                    if type(rgb) is list and len(rgb) == 3:
                        return True  # TODO Check List for int (or convert while cleaning maybe)
                    else:
                        return False
        return False
