from flask import Blueprint
from antipiracylite.modules.productLedger import ProductLedger
api = Blueprint('api', __name__, template_folder='templates')

pL = ProductLedger()

@api.route('/ping')
def testAPI():
    return "pong!"

@api.route('/addLicense')
def addLicense():
    pL.generateLicense()
    pL.saveLicensesToDB()
    return pL.stringifyLicenses()
    
@api.route('/saveDB')
def saveDB():
    pL.saveLicensesToDB()
    return 'DB updated!'