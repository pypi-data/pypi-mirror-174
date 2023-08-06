from ntrprtr.action.ActionBase import ActionBase

class EqualsAction(ActionBase):
    def __init__(self):
        super().__init__()
        self._config["endianess"] = "big"
        self._config["noMatch"] = "No match found!"

    def process(self, action, _bytes):
        self._mergeConfig(action)
       
        b = ""
        result = self._config["noMatch"]
        endianess = self._config["endianess"]

        if(endianess == "big"):
            b = _bytes.hex()
        elif(endianess == "little"):
            b = self._cnvrtr.toLittleEndian(_bytes.hex(" "))

        for i in range(0, len(self._config["cmp"])):
            if(b == self._config["cmp"][i]["value"].lower()):
                result = self._config["cmp"][i]["description"]
        return result