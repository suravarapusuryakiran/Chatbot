# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 15:02:04 2021

@author: USU1LO
"""

from flask import Flask, send_file, request
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/download')
 
def download_file():
    
    con_id=request.args.get('con_id')
    filename=request.args.get('filename')
    
    print(con_id)
    print(filename)
    
    userpath=os.path.join("C:/work/usu1lo/spyderPro/customer_files"+"/"+con_id)
    filepath_name=os.path.join("C:/work/usu1lo/spyderPro/customer_files"+"/"+con_id+"/"+filename)
    print(userpath)
    os.chdir(userpath)
    
    print(os.getcwd())
    
    return send_file(filepath_name,as_attachment=True)

if __name__ == '__main__':
    
    app.run(host="localhost", port=5012, debug=True)
    print("executed app.run on port {port}")
