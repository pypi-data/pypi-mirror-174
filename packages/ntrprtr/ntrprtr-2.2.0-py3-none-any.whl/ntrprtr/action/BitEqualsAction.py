from ntrprtr.action.ActionBase import ActionBase

class BitEqualsAction(ActionBase):
    def __init__(self):
        super().__init__()
        self._config["endianess"] = "big"
        self._config["noMatch"] = "No match found!"

    def process(self, action, _bytes):
        self._mergeConfig(action)
        bits = ""
        result = self._config["noMatch"]
        
        endianess = self._config["endianess"]
        if(endianess == "big"):
            bits = self._cnvrtr.hexToBin(_bytes.hex())
        elif(endianess == "little"):
            bits = self.__hexToLittleEndianToBin(_bytes)
        
        # Always fill up zeros to represent all given bytes, even if 
        # they are zero
        bits = bits.rjust(len(_bytes)*8, "0")

        for i in range(0, len(self._config["cmp"])):
            if(bits == self._config["cmp"][i]["value"]):
                result = self._config["cmp"][i]["description"]

        return result

    def __hexToLittleEndianToBin(self, byteArr):
        le = self._cnvrtr.toLittleEndian(byteArr.hex(" "))
        return str(self._cnvrtr.hexToBin(le))