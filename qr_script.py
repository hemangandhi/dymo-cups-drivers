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

LCS_URL = 'https://m7cwj1fy7c.execute-api.us-west-2.amazonaws.com/mlhtest/read'

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
    data = request.json
    if 'email' not in data:
        return 'Need email and name to print.', 400

    if 'name' not in data:
        q = {
            'query': {'email': data['email']},
            'email': 'c@c.com',
            'token': '791277e1-7b8b-4873-95ac-d283c3bacd84'
        }
        r = req.post(LCS_URL, json=q)
        rj = r.json()
        try:
            name = rj['body'][0]['first_name'] + ' ' + rj['body'][0]['last_name']
        except:
            print(rj)
            return 'User not found or something... check cupcake', 400
    else:
        name = data['name']

    role = data.get('role', 'Hacker')
    print_proc = run_printer([PRINTER_CMD, 'labels', name, data['email'], role], data['email'], PHOTO_PATH)
    if print_proc != 0:
        return 'Check cupcake... there might be trouble', 500
    return 'Success'

if __name__ == '__main__':
    app.run(port=5000)
