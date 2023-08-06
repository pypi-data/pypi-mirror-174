import socket
import logging


class FrakkComm:
    """FrakkComm parent class. Ezt a class-t kell minden eszkoznek orokolnie."""

    def __init__(self, ip_address: str, port: int, name: str):
        self.ip_address = ip_address
        self.port = port
        # self.comm_id = comm_id
        self.name = name
        # self.logger = logging()

    def TCPSendData(self, message: str):
        """TCP socket adat kuldes."""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip_address, self.port))
        s.send(bytes.fromhex(message))
        # data = s.recv(BUFFER_SIZE)  # only needed to recieve data back
        s.close()

    def intListToHexByteString(self, inputList):
        outStr = ""
        for currentItem in inputList:
            outStr += format(currentItem, "02x")
        return outStr

    def getByteArray(self, kezdo, cimzett, felado, message_id, parancs, adat):
        byteList = []

        byteList.append(kezdo)

        pluszHossz = False
        hossz = 7 + len(adat) - 1
        if hossz == 85:
            hossz += 1
            pluszHossz = True
        byteList.append(hossz)

        byteList.append(cimzett)
        if cimzett == 85:
            byteList.append(cimzett)

        byteList.append(felado)
        if felado == 85:
            byteList.append(felado)

        byteList.append(message_id)
        if message_id == 85:
            byteList.append(message_id)

        byteList.append(parancs)
        if parancs == 85:
            byteList.append(parancs)

        for x in adat:
            byteList.append(x)
            if x == 85:
                byteList.append(x)

        if pluszHossz:
            byteList.append(0x00.to_bytes())

        osszeg = 0
        osszeg += kezdo
        osszeg += hossz
        osszeg += cimzett
        osszeg += felado
        osszeg += message_id
        osszeg += parancs
        for x in adat:
            osszeg += x

        checkSum = 255 - osszeg
        checkSum = checkSum & 0xFF  # convert checksum to unsigned!
        byteList.append(checkSum)
        if checkSum == 85:
            byteList.append(checkSum)

        return byteList
