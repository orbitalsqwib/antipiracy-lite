from flask import Blueprint, render_template, request
from antipiracylite.blueprints.api import pL
import requests
frontend = Blueprint('frontend', __name__, template_folder='templates')

@frontend.route('/')
def testFrontend():
    return render_template('test.html')

@frontend.route('/testLicenseForm', methods=["GET", "POST"])
def testLicenseForm():
    if request.method == 'GET':
        return render_template('antipiracy_frontend_ask.html')

    else:
        if 'Product_L' in request.form and 'MAC' in request.form:
            licenseStr = request.form['Product_L']
            macAddr = request.form['MAC']
            result = pL.checkLicenseValid(licenseId=licenseStr, macAddr=macAddr)

            return render_template('antipiracy_frontend_result.html', result=result)

@frontend.route('/testLicenseResult')
def testLicenseResult():
    return render_template('antipiracy_frontend_result.html')