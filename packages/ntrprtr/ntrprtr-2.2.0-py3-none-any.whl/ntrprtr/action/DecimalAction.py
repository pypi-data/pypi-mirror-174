from ntrprtr.action.ActionBase import ActionBase

class DecimalAction(ActionBase):
    def __init__(self):
        super().__init__()
        self._config["endianess"] = "little"
        

    def process(self, action, _bytes):
        self._mergeConfig(action)
        result = ""
        endianess = self._config["endianess"]
        if(endianess == "big"):
            result = self._cnvrtr.hexToDec(_bytes.hex())
        elif(endianess == "little"):
            result = self.__hexToLittleEndianToDec(_bytes)
        return result

    def __hexToLittleEndianToDec(self, byteArr):
        le = self._cnvrtr.toLittleEndian(byteArr.hex(" "))
        return str(self._cnvrtr.hexToDec(le))