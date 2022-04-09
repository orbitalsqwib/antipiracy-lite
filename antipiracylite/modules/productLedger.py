# imports
import os
import base64
from typing import List
import uuid

class ProductLedger:

    # defines the shape of product licenses
    class License:

        # fields

        # - the identifier of the license
        licenseId: str

        # - the MAC address of the hardware that the license is currently in use on
        macAddr: str

        # - reflects if the license is currently in use
        inUse: bool

        # methods

        # - stringifies an individual license
        def stringify(self):
            return '+'.join([self.licenseId, self.macAddr, 'T' if self.inUse else 'F'])

        # constructor
        def __init__(self, licenseString='') -> None:
            if (licenseString == ''):
                self.licenseId = str(uuid.uuid4())
                self.macAddr = ''
                self.inUse = False
            else:
                parts = licenseString.split('+')
                self.licenseId = parts[0]
                self.macAddr = parts[1]
                self.inUse = True if parts[2] == 't' else False
    
    # fields

    # - contains the definitive list of all issued licenses and their current state
    licenses: List[License] = []

    # methods

    # - convert all licenses into a string representation
    def stringifyLicenses(self):
        return ','.join([license.stringify() for license in self.licenses])

    def destringifyLicenses(self, licensesString):
        return [self.License(lStr) for lStr in licensesString.split(',')]

    def generateLicense(self):
        newLicense = self.License()
        self.licenses.append(newLicense)
        return newLicense

    def saveLicensesToDB(self, dbPath=f'{os.getcwd()}/db.txt'):

        def encodeLicensesString(licenseStr: str):

            # get string bytes in utf-8 format
            strBytes = licenseStr.encode('utf-8')

            # convert string bytes to base 64 encoding and return it as str
            return base64.b64encode(strBytes).decode('utf-8')
            
        def writeDataToDB(data: str):
            f = open(dbPath, 'w')
            f.write(data)
            f.close()

        writeDataToDB(encodeLicensesString(self.stringifyLicenses()))

    # - check if license is valid
    def checkLicenseValid(self, licenseStr, macAddr):
        return [license.licenseId for license in self.licenses].count(licenseStr) > 0

    # - retrieves data from db if it exists, and creates a new db if it doesn't
    def loadDataFromDB(self, dbPath):

        # ensures a db file exists, creates an empty db file otherwise
        def ensureDBExists():
            try:
                f = open(dbPath, 'x')
                f.close()
            except:
                pass

        # reads and returns raw data from the local db
        def fetchRawDataFromDB():
            f = open(dbPath, 'r')
            return f.read()

        # decodes raw base64 data to its original string rep.
        def decodeRawData(rawData: str):

            # convert rawData string to b64 byte data
            b64Data = base64.b64decode(rawData)

            # convert b64 byte data to utf-8 str and return it
            return b64Data.decode('utf-8')


        ensureDBExists()
        rawData = fetchRawDataFromDB()
        data = decodeRawData(rawData)

        # loads licenses from data to field
        self.licenses = self.destringifyLicenses(data)

    # constructor
    def __init__(self, dbPath=f'{os.getcwd()}/db.txt'):
        self.loadDataFromDB(dbPath)
        