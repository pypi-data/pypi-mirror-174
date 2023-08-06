from cnvrtr.Converter import Converter

class ActionBase():
    def __init__(self) -> None:
        self._cnvrtr = Converter()
        self._config = {}

    def _mergeConfig(self, action):
        self._config |= action
