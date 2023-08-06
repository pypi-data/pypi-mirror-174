from .eszkoz import Eszkoz


class Ejjelifeny(Eszkoz):
    def __init__(
        self,
        ip_address: str,
        port: int,
        eszkoz_id: int,
        name: str,
        min_brightness=0,
        max_brightness=255,
    ):
        self.min_brightness_pct = 0
        self.max_brightness_pct = 100
        self.min_brightness = min_brightness
        self.max_brightness = max_brightness

        super(Ejjelifeny, self).__init__(ip_address, port, eszkoz_id, name)

    def setData(self, controlledLEDs, brightness: int, speed=1):
        adat = []

        adat.append(self.eszkoz_id)

        adat.append(0)
        adat[1] += speed
        if controlledLEDs["white"]:
            adat[1] += 64
        if controlledLEDs["blue"]:
            adat[1] += 128

        adat.append(brightness)

        return adat

    def convertBrightnessFromPercentage(self, percentage):
        brightness = int(
            (self.max_brightness - self.min_brightness) * (percentage / 100)
        )
        return brightness

    def controlLight(self, controlledLEDs, brightness, speed=1):
        kezdo = 0x55
        cimzett = 0xFF
        felado = 0x00
        message_id = 0xF4
        parancs = 0x56

        # This would be for %, but Home Assistant wants to control from 0 to 255
        # if brightnessPct > self.maxBrightnessPct:
        #     brightnessPct = self.maxBrightnessPct
        # elif brightnessPct < self.minBrightnessPct:
        #     brightnessPct = self.minBrightnessPct
        # brightness = self.convertBrightnessFromPercentage(brightnessPct)

        adat = self.setData(controlledLEDs, brightness, speed)

        byteArray = self.getByteArray(kezdo, cimzett, felado, message_id, parancs, adat)

        # print(self.intListToHexByteString(byteArray))
        tcp_send_data = self.intListToHexByteString(byteArray)
        self.TCPSendData(tcp_send_data)
        return tcp_send_data

    def turnOffLight(self):
        ledConfig = {"white": False, "blue": False}
        self.controlLight(ledConfig, self.min_brightness)

    def turnOnBlueLight(self, brightness=None):
        if brightness == None:
            brightness = self.max_brightness

        ledConfig = {"white": False, "blue": True}
        self.controlLight(ledConfig, brightness)

    def turnOnWhiteLight(self, brightness=None):
        if brightness == None:
            brightness = self.max_brightness

        ledConfig = {"white": True, "blue": False}
        self.controlLight(ledConfig, brightness)


# Example hex command:
# Lampa ID: 0x41
# Light ON:  55 09 FF 00 F4 56 41 C1 8B CB
# Light Off: 55 09 FF 00 F4 56 41 01 00 16


# Example usage:
#
# import frakkcomm
# testlight = frakkcomm.Ejjelifeny("192.168.2.15", 1001, 0x40, "Lampa 1", 0, 0xFF)
# testlight.turnOnWhiteLight(100)
# testlight.turnOnBlueLight(100)
# testlight.turnOffLight()
