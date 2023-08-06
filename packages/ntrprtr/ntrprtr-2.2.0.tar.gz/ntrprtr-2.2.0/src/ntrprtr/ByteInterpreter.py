from ntrprtr.action.ActionType import ActionType
from ntrprtr.action.DOSDateAction import DOSDateAction
from ntrprtr.action.DOSTimeAction import DOSTimeAction
from ntrprtr.action.DecimalAction import DecimalAction
from ntrprtr.action.AsciiAction import AsciiAction
from ntrprtr.action.BinaryAction import BinaryAction
from ntrprtr.action.EqualsAction import EqualsAction
from ntrprtr.action.BitEqualsAction import BitEqualsAction
from ntrprtr.action.HexdumpAction import HexdumpAction
from ntrprtr.action.UnicodeAction import UnicodeAction
from ntrprtr.action.EndianessAction import EndianessAction
from ntrprtr.action.UnixTimeAction import UnixTimeAction
from ntrprtr.action.Win32TimeAction import Win32TimeAction

class ByteInterpreter():
    def __init__(self, bytes, config) -> None:
        self._bytes = bytes
        self._config = config        

    def interpret(self):
        result = []
        for c in self._config:
            b = bytearray()
            amount = c["end"] - c["start"] + 1
            subBytes = [self._bytes[i:i + amount] for i in range(c["start"], c["end"]+1, amount)][0]
            b.extend(subBytes)
        
            if(c.get("action") != None and len(c["action"]) > 0):
                actionResults = []
                for a in c["action"]:
                    actionResult = self.__processAction(a, b)
                    actionResults.append((a["type"], actionResult))     
                result.append((c["name"], c["description"], c["start"], c["end"], b, actionResults))
            else:
                result.append((c["name"], c["description"],c["start"], c["end"], b, [("none", "-")])) 
        
        return result

    def __processAction(self, action, b):
        result = ""
        type_ = action["type"]
        if(type_ == ActionType.ENDIANESS):
            result = EndianessAction().process(action, b)
        if(type_ == ActionType.DECIMAL):
            result = DecimalAction().process(action, b)
        elif(type_ == ActionType.ASCII):
            result = AsciiAction().process(action, b)
        elif(type_ == ActionType.EQUALS):
            result = EqualsAction().process(action, b)
        elif(type_ == ActionType.BITEQUALS):
            result = BitEqualsAction().process(action, b)
        elif(type_ == ActionType.BINARY):
            result = BinaryAction().process(action, b)
        elif(type_ == ActionType.HEXDUMP):
            result = HexdumpAction().process(action, b)
        elif(type_ == ActionType.DOSDATE):
            result = DOSDateAction().process(action, b)
        elif(type_ == ActionType.DOSTIME):
            result = DOSTimeAction().process(action, b)
        elif(type_ == ActionType.UNIXTIME):
            result = UnixTimeAction().process(action, b)
        elif(type_ == ActionType.WIN32TIME):
            result = Win32TimeAction().process(action, b)
        elif(type_ == ActionType.UNICODE):
            result = UnicodeAction().process(action, b)

        return result

    