import sys
import json
import argparse

from hash_calc.HashCalc import HashCalc

from ntrprtr.Controller import Controller
from ntrprtr.ByteInterpreter import ByteInterpreter

from ntrprtr.printer.Printer import Printer
from ntrprtr.util.TestFileCreator import TestFileCreator


def main(args_=None):
    """The main routine."""
    if args_ is None:
        args_ = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", "-m", choices=["config", "interpret", "testfile"], required=True, help="The tool to use")
    # config
    parser.add_argument("--amount", "-a", type=int, default=1, help="Create a config with the given number of objects")
    parser.add_argument("--name", "-n", type=str, default="config.json", help="Name of the config file to be created ")
    # interpret
    parser.add_argument("--target", "-t", type=str, default="", help="Path to file which shall be interpreted")
    parser.add_argument("--config", "-c", type=str, default="", help="Path to config file")
    parser.add_argument("--result", "-r", type=str, default="", help="Path to result file")
    parser.add_argument("--offset", "-o", type=int, default=0, help="Offset in bytes to start reading")
    parser.add_argument("--bytes",  "-b", type=int, default=0, help="No. of bytes to read starting from offset")
    parser.add_argument("--disableHashing",  "-d", type=bool, default=False, help="True if hashing shall be disabled, False otherwise")
    # testfile
    parser.add_argument("--input",  "-i", type=str, default="", help="Path to textfile with hex values")
    parser.add_argument("--output", "-u", type=str, default="", help="Path to binary test file to be created")
    args = parser.parse_args()

    c = Controller()
    
    if(args.mode == "config"):
        config = { "name": "name", "description": "description", "ntrprtr": []}

        c.printHeader("", HashCalc(), args)

        for i in range(0, args.amount):
            o = { "name": "Name", "description": "desc", "start": 0, "end": 0, "action": [{ "type": "type" }]}
            config["ntrprtr"].append(o)

        try:
            with open(args.name, "x")as f:
                f.write(json.dumps(config, indent=4))
        except:
            c.printConfigFailureMessage(args.name)
            exit()

        c.printConfigSuccessMessage(args.name)
        c.printExecutionTime()

    elif(args.mode == "interpret"):
        # If a path to result file is specified, write stdout to file
        if(args.result != ""):
            sys.stdout = open(args.result, 'w', encoding="utf8")

        if(args.disableHashing):
            hash = HashCalc()
        else:
            hash = HashCalc(args.target)

        c.printHeader(args.target, hash, args)

        if(args.target == ""):
            print("Please provide a path to a file for reading bytes!")
            exit()
        if(args.config == ""):
            print("Please provide a path to a ntrprtr config file!")
            exit()
        
        configHandle = open(args.config, encoding="utf8")
        config = json.load(configHandle)

        if(args.offset == 0 and args.bytes == 0):
            with open(args.target, "rb") as f:
                _bytes = f.read()
                b = ByteInterpreter(_bytes, config["ntrprtr"])
                result = b.interpret()
                p = Printer()
                p.print(result, config["name"], config["description"])
        else:
            with open(args.target, "rb") as f:
                f.seek(args.offset, 0)
                _bytes = f.read(args.bytes)
                b = ByteInterpreter(_bytes, config["ntrprtr"])
                result = b.interpret()
                p = Printer()
                p.print(result, config["name"], config["description"])

        c.printExecutionTime()
    
    elif(args.mode == "testfile"):
        if(args.input == ""):
            print("Please provide a path to a hex data file!")
            exit()
        if(args.output == ""):
            print("Please provide a path to an output file!")
            exit()

        hash = HashCalc()
        c.printHeader("", hash, args)
        creator = TestFileCreator()
        creator.createFile(args.input, args.output)
        c.printTestfileSuccessMessage(args.output)


if __name__ == "__main__":
    sys.exit(main())
