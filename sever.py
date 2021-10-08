import os
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.wrappers import response
from pymongo import MongoClient
from flask import jsonify
import json
import uuid
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.db_quanlydulieumoitruong

@app.route('/')
def todo():
    _items = db.tododb.find()
    items = [item for item in _items]
    resp = {"code": 200, "desc": "Success!"}
    return jsonify(resp)
    # return render_template('todo.html', items=items)

@app.route('/moitruong/api/iot/insert', methods=['POST'])
def new():
    data = json.loads(request.data)
    db.iot.insert_one(data)

    resp = {"code": 200, "desc": "Success!"}
    return jsonify(resp)

# chuc nang dang ky
@app.route('/moitruong/api/quanlytaikhoan/dangky', methods=['POST'])
def dangky():
    data = json.loads(request.data)
    #kiem tra email trong db
    timkiem = db.taikhoan.find_one({'email': data.email})
    print(timkiem)
    if timkiem is None:
        #insert vao bang taikhoan
        db.taikhoan.insert_one(data)
        resp = {"code": 200, "desc": "Dang ky thanh cong!"}
        return jsonify(resp)
    else:
        resp = {"code": 100, "desc": "Email da ton tai!"}
        return jsonify(resp)

    resp = {"code": 200, "desc": "Success!"}
    return jsonify(resp)

#-------------------------------------
#chuc nang dang nhap
@app.route('/moitruong/api/quanlytaikhoan/dangnhap', methods=['POST'])
def dangnhap():
    data = json.loads(request.data)
    print(data.get("email"))
    #kiem tra email trong he thong
    timkiem = db.taikhoan.find_one({'email': data.get("email")})
    print(timkiem)
    if timkiem is None:
    #email khong ton tai
        resp = {"code": 300, "desc": "Email khong ton tai, vui long dang ky!"}
        return jsonify(resp)
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
            return jsonify(resp)
        else:
            resp = {"code": 500, "desc": "Mat khau khong chinh xac!"}
            return jsonify(resp)
    resp = {"code": 200, "desc": "Success!"}
    return jsonify(resp)
# Chuc nag quen mat khau
if __name__ == "__main__":
    app.run(debug=True)
