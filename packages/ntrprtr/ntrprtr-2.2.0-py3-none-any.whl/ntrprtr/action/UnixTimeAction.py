from datetime import datetime

from ntrprtr.action.ActionBase import ActionBase

class UnixTimeAction(ActionBase):
    def __init__(self):
        super().__init__()
        self._config["endianess"] = "little"

    def process(self, action, _bytes):
        self._mergeConfig(action)
        result = ""
        c = self._cnvrtr
        hexValues = _bytes.hex(" ")
        
        endianess = self._config["endianess"]
        if(endianess == "big"):
            result = self._cnvrtr.hexToDec(_bytes.hex())
        elif(endianess == "little"):
            result = self.__hexToLittleEndianToDec(_bytes)  

        dtObj = datetime.utcfromtimestamp(result)

        return str(dtObj.strftime("%d.%m.%y %H:%M:%S UTC"))

    def __hexToLittleEndianToDec(self, byteArr):
        le = self._cnvrtr.toLittleEndian(byteArr.hex(" "))
        return self._cnvrtr.hexToDec(le)