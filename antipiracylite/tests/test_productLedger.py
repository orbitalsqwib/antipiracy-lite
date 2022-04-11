from antipiracylite.modules.productLedger import ProductLedger

# seed function sets up a mock product ledger with no licenses for tests
def buildMockLedger():
    return ProductLedger()

# tests

# - Given an empty ledger,
#   Where there is an incoming license validation request,
#   Then the ledger validation function should return False
def testLicenseDoesNotExist():
    # arrange
    mockLedger = buildMockLedger()
    incomingLicense = ProductLedger.License()

    # act
    res = mockLedger.checkLicenseValid(incomingLicense.licenseId, incomingLicense.macAddr)

    # assert
    assert res == False

# - Given a ledger with an existing license that is not in use,
#   Where there is an incoming license validation request with a different id,
#   Then the ledger validation function should return False
def testLicenseExistsDoesNotMatchAndNotInUse():
    # arrange
    mockLedger = buildMockLedger()
    dbLicense = ProductLedger.License()
    mockLedger.licenses.append(dbLicense)
    incomingLicense = ProductLedger.License()

    # act
    res = mockLedger.checkLicenseValid(incomingLicense.licenseId, incomingLicense.macAddr)

    # assert
    assert res == False

# - Given a ledger with an existing license that is not in use,
#   Where there is an incoming license validation request with the same id,
#   Then the ledger validation function should return True
def testLicenseExistsMatchesAndNotInUse():
    # arrange
    mockLedger = buildMockLedger()
    dbLicense = ProductLedger.License()
    mockLedger.licenses.append(dbLicense)
    incomingLicense = ProductLedger.License()
    incomingLicense.licenseId = dbLicense.licenseId

    # act
    res = mockLedger.checkLicenseValid(incomingLicense.licenseId, incomingLicense.macAddr)

    # assert
    assert res == True

# - Given a ledger with an existing license that is in use,
#   Where there is an incoming license validation request with the same id but different MAC address,
#   Then the ledger validation function should return False
def testLicenseExistsMatchesInUseAndDiffMAC():
    # arrange
    mockLedger = buildMockLedger()
    dbLicense = ProductLedger.License()
    dbLicense.macAddr = '6D-D7-6E-DD-20-38'
    dbLicense.inUse = True
    mockLedger.licenses.append(dbLicense)
    incomingLicense = ProductLedger.License()
    incomingLicense.licenseId = dbLicense.licenseId
    incomingLicense.macAddr = '5F-58-F1-DF-40-B8'

    # act
    res = mockLedger.checkLicenseValid(incomingLicense.licenseId, incomingLicense.macAddr)

    # assert
    assert res == False

# - Given a ledger with an existing license that is in use,
#   Where there is an incoming license validation request with the same id and same MAC address,
#   Then the ledger validation function should return True
def testLicenseExistsMatchesInUseAndSameMAC():
    # arrange
    mockLedger = buildMockLedger()
    dbLicense = ProductLedger.License()
    dbLicense.macAddr = '6D-D7-6E-DD-20-38'
    dbLicense.inUse = True
    mockLedger.licenses.append(dbLicense)
    incomingLicense = ProductLedger.License()
    incomingLicense.licenseId = dbLicense.licenseId
    incomingLicense.macAddr = dbLicense.macAddr

    # act
    res = mockLedger.checkLicenseValid(incomingLicense.licenseId, incomingLicense.macAddr)

    # assert
    assert res == True