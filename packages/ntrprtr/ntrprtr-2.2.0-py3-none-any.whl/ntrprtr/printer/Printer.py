from cnvrtr.Converter import Converter
from ntrprtr.action.ActionType import ActionType

class Printer():
    def __init__(self) -> None:
        self._cnvrtr = Converter(nonAsciiPlaceholder=".")

    def print(self, results, name="ntrprtr", description="Interpret bytes through different customizable actions"):
        print("")
        print(name)
        print("-"*len(name))
        print(description)
        print("")
        print("")
        print("Analysis")
        print("--------")

        for result in results:
            hexWritten = False
            print("")
            print("--> " + result[1])
            print("    --------------")
            print("      Start Byte: " + str(result[2]) + " (" + hex(result[2]) + ")")
            print("        End Byte: " + str(result[3]) + " (" + hex(result[3]) + ")")
            print("    Nr. of Bytes: " + str(result[3] - result[2] + 1))
            print("    --------------")
            for actionResult in result[5]:
                if(actionResult[0] == ActionType.HEXDUMP):
                    print("    " + " Bytes: ")
                    print("            " + "See below")
                    print("    --------------")
                    print("    " + "Action: ")
                    print("            " + actionResult[0])
                    print("    " + "Result: ")
                    print("")
                    dump = actionResult[1].split("\n")
                    for l in dump:
                        print("            " + l)
                else:
                    if(not hexWritten):
                        print("    " + " Bytes: ")
                        print("            " + result[4].hex(" ").upper())
                        hexWritten = True
                    print("    --------------")
                    print("    " + "Action: ")
                    print("            " + actionResult[0])
                    print("    " + "Result: ")
                    print("            " + str(actionResult[1]))
            print("")