import os
import time

from datetime import datetime

class Controller():
    def __init__(self) -> None:
        self.startTime = time.time()

    def printHeader(self, path, hash, args):
        print("###########################################################################################")
        print("")
        print("ntrprtr by 5f0")
        print("Interpret bytes through different customizable actions")
        print("")
        print("                Arguments: ")
        print(''.join(f'                           {k}={v}\n' for k, v in vars(args).items()))
        print("Current working directory: " + os.getcwd())
        print("        Investigated File: " + path)
        print("")
        print("                      MD5: " + hash.md5)
        print("                   SHA256: " + hash.sha256)
        print("")        
        print("                 Datetime: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print("")
        print("###########################################################################################")

    def printConfigSuccessMessage(self, name):
        print("")
        print("Template successfully created: " + name)
        print("")

    def printConfigFailureMessage(self, name):
        print("")
        print("Configuration File exists already: " + name)
        print("")
        self.printExecutionTime()

    def printTestfileSuccessMessage(self, name):
        print("")
        print("Testfile created successfully: " + name)
        print("")
        self.printExecutionTime()    

    def printExecutionTime(self):
        end = time.time()
        print("###########################################################################################")
        print("")
        print("Execution Time: " + str(end-self.startTime)[0:8] + " sec")
        print("")