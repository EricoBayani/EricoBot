import json
import os
from functools import lru_cache

# This was originally from my CSE123 project. It never got used
# because the RFID reader wasn't working, so authorization pairs
# couldn't get written. I changed some variable names around to
# be a little more general, but currently this is to be a supersimple
# cache-like mechanism for my discord bot. 




class JSON_Writer:
    def __init__(self, authfile = "days.json"):
        self.authfile = authfile
        try:
            test_file = open(self.authfile, "r")
            test_file.close()
    
        except FileNotFoundError:
            test_file = open(self.authfile, "w")
            test_file.close()


    def getJsonData(self):
        work = {}
        with open(self.authfile, "r") as work_file:
        
            try:
                work = json.load(work_file)
                # This catch is more reliable to deal with
                # empty files
            except json.decoder.JSONDecodeError:
                work = {"pairs":{}}
        return work

    def addPair(self, key, value):

        work = self.getJsonData()
        workList = work["pairs"]
        print(workList)
        workList[key] = value
        #json.dump(work, work_file, indent=2)

        with open(self.authfile, "w") as work_file:
            json.dump(work, work_file, indent=2)

    # getPair returns the VALUE associated with
    # the given KEY
    @lru_cache(maxsize=1)
    def getPair(self, key):
        work = self.getJsonData()
        pairsList = work["pairs"]
        print(key)
        print("===" + str(pairsList) + "===")

        return pairsList.get(str(key))

    def checkKey(self, key):
        pair = self.getPair(key)
        print(pair)
        if pair is not None:
            return True
        else:
            return False
    
    def checkValue(self, key, value):    
        pair = self.getPair(key)
        print(pair)
        if pair is value:
            return True
        else:
            return False
        


# basic tests to ensure functionality
if __name__ == '__main__':

    writer = JSON_Writer()
    writer.addPair(1111, 1111)
    writer.addPair(2222, 2222)
    writer.addPair(2222, 2332)
    writer.addPair(1111, 1444)
    writer.addPair(3333, 1444)
    writer.addPair(1111, 1111)
    writer.addPair(3333, 1444)
    writer.addPair(2222, 2332)

    writer.checkKey(2222)
    writer.checkValue(2222, 2332)
    writer.checkKey(1111)
    writer.checkValue(1111, 2332)
