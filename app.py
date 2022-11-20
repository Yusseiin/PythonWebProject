"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
import time
from datetime import date
from seleniummo import *
from flask import Flask, render_template, request, flash, redirect, url_for

# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
app = Flask(__name__)
app.config['SECRET_KEY'] = "adsdasda"
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/')
def hello():
    """Renders a sample page."""
    print("Hello World!")
    return redirect(url_for('index'))


@app.route("/hello")
def index():
    today = date.today()
    flash("Quante ore hai lavorato?", "MainText")
    flash(today, "Date")
    return render_template('index.html')


@app.route("/greet", methods=["POST", "GET"])
def greet():
    sDataSplit = str(request.args['date']).split('-')
    sData = sDataSplit[2] + "/" + sDataSplit[1] + "/" + sDataSplit[0]
    sOre = str(request.args['ora'])
    sUser = str(request.args['user'])
    sPwd = str(request.args['pwd'])
    sDescrizione = str(request.args['descrizione'])
    print("Selenium_START!!")
    driver = openFirefox(False, "http://marweb.marchianisrl.com:8086/")
    # driver = openChrome("http://marweb.marchianisrl.com:8086/")

    insertTextByID("USERNAME", 0, sUser, driver)
    insertTextByID("PASSWORD", 0, sPwd, driver)
    clickOnID("LOGIN", 0, driver)
    clickOnID("cms:12:link", 0, driver)
    clickOnCSS("#cmd\:13 > a", 0, driver)
    scounter = time.perf_counter()
    for x in range(20):
        print("for " + str(x))
        sPathFoglioLavoro = "fld:0:4:13:lv" + str(x)
        sPathData = "fld:4:4:13:lv" + str(x)
        sPathDescrizione = "fld:6:4:13:lv" + str(x)
        nDelay = 0
        if x == 0:
            nDelay = 10
        sFoglioLavoro = findsByID(sPathFoglioLavoro, nDelay, driver)
        if sFoglioLavoro != "End":
            sData = findsByID(sPathData, 0, driver)
            sDescrizione = findsByID(sPathDescrizione, 0, driver)
            print(sFoglioLavoro + "    " + sData + "    " + sDescrizione)
        else:
            print("finish")
            break

    sfinalcounter = time.perf_counter() - scounter
    print(str(sfinalcounter))
    closeChrome(driver)
    # print(findsByID("fld:0:4:13:lv0",0,driver))
    # print(findByCSS("#fld\:0\:4\:13\:lv0",0,driver).text)
    """clickOnCSS("#pan\:5\:13\:new",1,driver)
    insertDateByCSS("#fld\:2\:5\:13\:fv",1,"#pan\:5\:13\:fb > div:nth-child(1) > div:nth-child(1) > div > div > span > button",sData,driver)
    insertTextByCSS("#fld\:3\:5\:13\:fv",1,sDescrizione,driver)
    insertTextByCSS("#fld\:4\:5\:13\:fv",1,sOre,driver)
    clickOnCSS("#pan\:5\:13\:save",0,driver) 
    sleep(5)
    closeChrome(driver)
    print("Selenium_END!!") """
    # flash("Hai caricato " + sOre + " ore il giorno " + sData + ' facendo "' + sDescrizione + '" <3',"MainText")
    return redirect(url_for('index'))


def tess():
    return redirect(url_for('index'))


if __name__ == '__main__':
    import os

    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000
    app.run(HOST, PORT)
