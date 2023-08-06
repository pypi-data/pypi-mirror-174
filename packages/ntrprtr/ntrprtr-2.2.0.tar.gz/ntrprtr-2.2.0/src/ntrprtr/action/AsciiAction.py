from ntrprtr.action.ActionBase import ActionBase

class AsciiAction(ActionBase):
    def __init__(self):
        super().__init__()
        self._config["nonAsciiPlaceholder"] = "."

    def process(self, action, _bytes):
        self._mergeConfig(action)
        self._cnvrtr._nonAsciiPlaceholder = self._config["nonAsciiPlaceholder"]
        return self._cnvrtr.hexToAsciiString(_bytes.hex())