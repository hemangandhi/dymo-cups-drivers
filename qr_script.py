#!/usr/bin/env python
# run with `chromium $(python qr_script.py test@example.com)`

import io
import qrcode
import PIL
import base64
import sys
import subprocess
import requests as req
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

SAMPLE_CODE_BASE_PATH = '/home/architect/dymo-cups-drivers/samples/test_label/'
PHOTO_PATH = SAMPLE_CODE_BASE_PATH + 'tel.png'
PRINTER_CMD = SAMPLE_CODE_BASE_PATH + 'TestLabel'

LCS_URL = ''

def email2qr(email):
    #construct the QR code
    img = qrcode.make(email)
    #save as a byte array
    byteArr = io.BytesIO()
    img.save(byteArr, format='PNG')
    byteImg = byteArr.getvalue()
    #then read and encode.
    encodedImg = base64.standard_b64encode(byteImg)
    return 'data:image/png;base64,' + encodedImg.decode()

def run_printer(p_exec, email, qr_path):
    #mk QR like above...
    img = qrcode.make(email)
    with open(qr_path, 'wb') as qr_out:
        img.save(qr_out, format='PNG')
    pr = subprocess.run(p_exec)
    return pr.returncode

@app.route('/print', methods=['POST'])
def web_req():
    data = request.json()
    if 'email' not in data:
        return 400, 'Need email and name to print.'

    if 'name' not in data:
        r = requests.post(LCS_URL, json={'query': {'email': data['email']}})
        rj = r.json()
        try:
            name = rj['body'][0]['first_name'] + rj['body'][0]['last_name']
        except:
            print(rj)
            return 400, 'User not found or something... check cupcake'
    else:
        name = data['name']

    role = data.get('role', 'Hacker')
    print_proc = run_printer([PRINTER_CMD, 'labels', name, email, role], email, PHOTO_PATH)
    if print_proc != 0:
        return 500, 'Check cupcake... there might be trouble'
    return 200, 'Success'

if __name__ == '__main__':
    email = sys.argv[1] if len(sys.argv) >= 2 else 'rnd@hackru.org'
    name = sys.argv[2] if len(sys.argv) >= 3 else 'Ms. Cupcake'
    print(run_printer([PRINTER_CMD, 'labels', name, email], email, PHOTO_PATH))
