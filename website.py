from logging import error
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
app = Flask(__name__, template_folder='template')

client = MongoClient('localhost', 27017)
db = client.db_quanlydulieumoitruong

@app.route('/moitruong/thongtin')
def todo():
    
    return render_template('thongtin.html') 

#chức năng đăng ký
@app.route('/moitruong/website/signupform', methods=['GET', 'POST'])
def signupform():
    error = None
    if request.method == 'GET':
        return render_template('signup.html', error=error)
    elif request.method == 'POST':
        print(request.form['email'])
    #kiem tra email trong he thong
        timkiem = db.taikhoan.find_one({'email': request.form['email']})
        print(timkiem)
        if timkiem is None:
            #insert vao bang taikhoann
            data = {
                'email' : request.form['email'],
                'password' : request.form['psw'],
                'name' : request.form['fullname']
            }
            db.taikhoan.insert_one(data)
            resp = {"code": 200, "desc": "Dang ky thanh cong!"}
            return redirect(url_for('loginform'))
            #return dumps(resp)
        else:
            resp = {"code": 100, "desc": "Email da ton tai!"}
            return dumps(resp)


#Chức năng đăng nhập
@app.route('/moitruong/website/loginform', methods=['GET', 'POST'])
def loginform():
    error = None
    if request.method == 'GET':
        return render_template('login.html', error=error)
    elif request.method == 'POST':
        print(request.form['email'])
        # data = json.loads(request.form)
        # print(data.get("email"))
        #kiem tra email trong he thong
        timkiem = db.taikhoan.find_one({'email': request.form['email']})
        print(timkiem)
        if timkiem is None:
        #email khong ton tai
            resp = {"code": 300, "desc": "Email khong ton tai, vui long dang ky!"}
            return dumps(resp)
        else:
            #kiem tra mat khau
            print(request.form['email'])
            print(timkiem.get("email"))
            if request.form['password'] == timkiem.get("password"):
                #tạo session
                uuidOne = uuid.uuid1()
                myquery = {'email': request.form['email']}
                newvalues = { "$set": { "session": uuidOne } }
                db.taikhoan.update_one(myquery, newvalues)
                resp = {"code": 400, "desc": "Dang nhap thanh cong!", "session": uuidOne}
                #return dumps(resp)
                return redirect(url_for('trangchu'))
            else:
                resp = {"code": 500, "desc": "Mat khau khong chinh xac!"}
                return dumps(resp)
    resp = {"code": 200, "desc": "Success!"}
    return dumps(resp)
        # return redirect(url_for('trangchu'))
    # return render_template('login.html', error=error)

#Trang chủ
@app.route('/moitruong/website/trangchu', methods=['GET', 'POST'])
def trangchu():
    error = None
    if request.method == 'GET':
        a = list(db.vitri.find({}))
        print(a)
    
        return render_template('trangchu.html', data = a)
    elif request.method == 'POST':
        print(request.form)
        query = {"name": request.form['tenvitri']}
        db.vitri.insert_one(query)
        #resp = {"code": 200, "desc": "Success!"}
        a = list(db.vitri.find({}))
        print(a)
        return redirect(url_for('trangchu'))
        #return None
        #return render_template('trangchu.html', data = a)
def move_forward():
    #Moving forward code
    print("Moving Forward...")
        # return redirect(url_for('home'))

@app.route('/moitruong/website/vitri/<vitri_id>', methods=['GET', 'POST'])
def vitri(vitri_id):
    print(vitri_id)
    error = None
    if request.method == 'GET':
        timkiemvitri = db.vitri.find_one({'name' : vitri_id})
        print(timkiemvitri)
        a = list(db.iot.find({'vitri_id' : timkiemvitri.get('_id')}))
        print(a)
        return render_template('vitri.html', data = a, vitri=timkiemvitri)
    elif request.method == 'POST':
        print(request.form)
        timkiemvitri = db.vitri.find_one({'name' : vitri_id})
        query = {
            "name": request.form['tencambien'], 
            #"value": data.get("value"),
            "vitri_id": timkiemvitri.get('_id')
            }
        db.iot.insert_one(query)
        a = list(db.iot.find({'vitri_id' : timkiemvitri.get('_id')}))
        print(a)
        #return render_template('vitri.html', data = a, vitri=timkiemvitri)
        return redirect(url_for('vitri', vitri_id=vitri_id))

@app.route('/moitruong/website/dulieuiot/<vitri_id>/<iot_id>', methods=['GET', 'POST'])
def dulieuiot(vitri_id, iot_id):
    print(iot_id)
    error = None
    if request.method == 'GET':
        timkiemvitri = db.vitri.find_one({'name' : vitri_id})
        timkiemiot = db.iot.find_one({'name' : iot_id, 'vitri_id' : timkiemvitri.get('_id')})
        print(timkiemiot)
        a = list(db.dulieucambien.find({'iot_id' : timkiemiot.get('_id'), 'vitri_id' : timkiemvitri.get('_id')}))
        print(a)
        return render_template('bangthongso.html', data = a, vitri=timkiemvitri, iot=timkiemiot)
    elif request.method == 'POST':
        print(request.form)
        
        # return redirect(url_for('home'))
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5002)


