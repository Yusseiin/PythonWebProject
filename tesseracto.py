
from ast import Try
from asyncio.windows_events import NULL
from re import T, search
from PIL import Image
from itertools import cycle
import re
import pytesseract

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
# Simple image to string
#print(pytesseract.image_to_string(Image.open('C:\\Users\\mdesimone\\Desktop\\test.jpg'), lang='chi_sim'))
def getTotal(Path):
    text = (pytesseract.image_to_string(Image.open(Path), lang='eng'))
    text = text.lower()
    print(text)
    tokens = text.split()
    result = 'Not found'
    sReturn = 'Not found'
    for n,i in enumerate(tokens):
        if 'total' in i:
            result = ' '.join(tokens[n:n+2])
            print('found ' + result)
            s = [float(s) for s in
            re.findall (r'-?\d+\.?\d*', result)]
            try:
                sReturn = "You have spent " + s[0]
                print(s[0])
            except IndexError:
                print('Number not found')
    if result == 'Not found':
        sReturn = "Total not found"
        print('Total not found')
    return sReturn


#print(pytesseract.image_to_string(Image.open('C:\\Users\\mdesimone\\Desktop\\IMG_20221105_173649.jpg')))

# In order to bypass the image conversions of pytesseract, just use relative or absolute image path
# NOTE: In this case you should provide tesseract supported images or tesseract will return error
#print(pytesseract.image_to_string('test.png'))

## List of available languages
#print(pytesseract.get_languages(config=''))

## French text image to string
#print(pytesseract.image_to_string(Image.open('test-european.jpg'), lang='fra'))

