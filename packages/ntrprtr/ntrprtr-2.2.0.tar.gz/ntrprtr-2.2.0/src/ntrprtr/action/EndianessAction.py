from ntrprtr.action.ActionBase import ActionBase

class EndianessAction(ActionBase):
    def __init__(self):
        super().__init__()
        self._config["endianess"] = "little"
      
    def process(self, action, _bytes):
        self._mergeConfig(action)
        result = ""
        endianess = self._config["endianess"]
        if(endianess == "big"):
            result = _bytes.hex(" ")
        elif(endianess == "little"):
            result = self._cnvrtr.toLittleEndian(_bytes.hex(" "))
        result = " ".join(result[i:i+2] for i in range(0, len(result), 2))
        return result.upper()