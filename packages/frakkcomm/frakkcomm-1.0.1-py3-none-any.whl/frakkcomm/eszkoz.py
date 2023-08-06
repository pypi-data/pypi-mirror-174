from .frakkcomm import FrakkComm


class Eszkoz(FrakkComm):
    def __init__(self, ip_address: str, port: int, eszkoz_id: int, name: str):
        # self.entity_id = None
        # self.unique_id = None
        self.eszkoz_id = eszkoz_id
        super(Eszkoz, self).__init__(ip_address, port, name)

    def getStatus(self):
        pass
