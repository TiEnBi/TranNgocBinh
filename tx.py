import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo.message import query
from werkzeug.wrappers import response
from pymongo import MongoClient
# from flask import dumps
import json
import uuid
import datetime
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
client = MongoClient('localhost', 27017)
db = client.db_quanlydulieumoitruong

@app.route('/')
@cross_origin()
def todo():
    _items = db.tododb.find()
    items = [item for item in _items]
    resp = {"code": 200, "desc": "Success!"}
    return dumps(resp)
    # return render_template('todo.html', items=items)

@app.route('/moitruong/api/iot/insert', methods=['POST'])
@cross_origin()
def new():
    data = json.loads(request.data)
    db.iot.insert_one(data)

    resp = {"code": 200, "desc": "Success!"}
    return dumps(resp)

# chuc nang dang ky
@app.route('/moitruong/api/quanlytaikhoan/dangky', methods=['POST'])
@cross_origin()
def dangky():
    data = json.loads(request.data)
    #kiem tra email trong db
    timkiem = db.taikhoan.find_one({'email': data.get("email")})
    print(timkiem)
    if timkiem is None:
        #insert vao bang taikhoan
        db.taikhoan.insert_one(data)
        resp = {"code": 200, "desc": "Dang ky thanh cong!"}
        return dumps(resp)
    else:
        resp = {"code": 100, "desc": "Email da ton tai!"}
        return dumps(resp)

    resp = {"code": 200, "desc": "Success!"}
    return dumps(resp)

#-------------------------------------
#chuc nang dang nhap
@app.route('/moitruong/api/quanlytaikhoan/dangnhap', methods=['POST'])
@cross_origin()
def dangnhap():
    data = json.loads(request.data)
    print(data.get("email"))
    #kiem tra email trong he thong
    timkiem = db.taikhoan.find_one({'email': data.get("email")})
    print(timkiem)
    if timkiem is None:
    #email khong ton tai
        resp = {"code": 300, "desc": "Email khong ton tai, vui long dang ky!"}
        return dumps(resp)
    else:
        #kiem tra mat khau
        print(data.get("email"))
        print(timkiem.get("email"))
        if data.get("password") == timkiem.get("password"):
            #tạo session
            uuidOne = uuid.uuid1()
            myquery = {'email': data.get("email")}
            newvalues = { "$set": { "session": uuidOne } }
            db.taikhoan.update_one(myquery, newvalues)
            resp = {"code": 400, "desc": "Dang nhap thanh cong!", "session": uuidOne}
            return dumps(resp)
        else:
            resp = {"code": 500, "desc": "Mat khau khong chinh xac!"}
            return dumps(resp)
    resp = {"code": 200, "desc": "Success!"}
    return dumps(resp)
# Chuc nag them dư lieu tu cam bien
@app.route('/moitruong/api/quanlytram/themdulieutucambien', methods=['POST'])
@cross_origin()
def themdulieutucambien():
    data = json.loads(request.data)
    print(data)

    #luu du lieu vao he thong
    query = {
        "data": data.get("data"), 
        "iot_id": ObjectId(data.get("iot_id")), 
        "vitri_id": ObjectId(data.get("vitri_id")),
        "thoigian": datetime.datetime.now()
    }
    db.dulieucambien.insert_one(query)

    

    resp = {"code": 200, "desc": "Success!"}
    return dumps(resp)

# Chuc nag lay toan bo du lieu
@app.route('/moitruong/api/quanlydulieu/laytoanbodulieu', methods=['POST']) 
@cross_origin()
def laytoanbodulieu():
    data = json.loads(request.data)
    a = list(db.dulieucambien.find({}))
    print(a)
    
    resp = {"code": 200, "desc": "Success!", "data": a}
    return dumps(resp)
# Chuc nag lay toan bo du lieu tu 1 tram
@app.route('/moitruong/api/quanlydulieu/laytoanbodulieutumottram', methods=['POST'])
@cross_origin()
def laytoanbodulieutumottram():
    data = json.loads(request.data)
    query = {
        "vitri_id" : ObjectId(data.get("vitri_id"))
    }
    a = list(db.dulieucambien.find(query))
    print(a)
    
    resp = {"code": 200, "desc": "Success!", "data": a}
    return dumps(resp)
# Chuc nag them cam bien moi
@app.route('/moitruong/api/quanlytram/themcambienmoi', methods=['POST'])
@cross_origin()
def themcambienmoi():
    data = json.loads(request.data)
    #tao ra id cam bien
    # uuidOne = uuid.uuid1()
    query = {
        "name": data.get("name"), 
        "value": data.get("value"),
        "vitri_id": ObjectId(data.get("vitri_id")
        )}
    db.iot.insert_one(query)
    
    resp = {"code": 200, "desc": "Success!"}
    return dumps(resp)
# Chuc nag tao vi tri moi
@app.route('/moitruong/api/quanlytram/themvitrimoi', methods=['POST'])
@cross_origin()
def themvitrimoi():
    data = json.loads(request.data)
    uuidOne = uuid.uuid1()
    query = {"name": data.get("name")}
    db.vitri.insert_one(query)

    resp = {"code": 200, "desc": "Success!"}
    return dumps(resp)
# Chuc nag lay toan bo vi tri
@app.route('/moitruong/api/quanlytram/laytoanbovitri', methods=['POST'])
@cross_origin()
def laytoanbovitri():
    data = json.loads(request.data)
    a = list(db.vitri.find({}))
    print(a)
    
    resp = {"code": 200, "desc": "Success!", "data": a}
    return dumps(resp)
# Chuc nag lay toan bo IOT
@app.route('/moitruong/api/quanlytram/laytoanboiot', methods=['POST'])
@cross_origin()
def laytoanboiot():
    print("aaaaaaaaaaaaaaaaaaaaaaaa",  request.data)
    data = json.loads(request.data)
    a = list(db.iot.find({}))
    print(a)
    
    resp = {"code": 200, "desc": "Success!", "data": a}
    return dumps(resp)
# Chuc nag moi
@app.route('/moitruong/api/quanlytram/zzzz', methods=['POST'])
@cross_origin()
def zzzz():
    data = json.loads(request.data)

    
    resp = {"code": 200, "desc": "Success!"}
    return dumps(resp)
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
