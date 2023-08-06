from .switchbot import Switchbot


class OnOffAbirity(Switchbot):
    def __init__(self):
        pass

    def turn_on(self):
        """Turn on device"""
        self._body['command'] = "turnOn"
        result = self.command(self.deviceId, self._body)
        return result.text

    def turn_off(self):
        """Turn off device"""
        self._body['command'] = "turnOff"
        result = self.command(self.deviceId, self._body)
        return result.text
