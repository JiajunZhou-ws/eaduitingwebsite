#coding:utf-8
from flask import Flask
from flask import render_template
from flask import request, session, make_response,Response
from werkzeug import secure_filename
import os
import xlrd
import json
app = Flask(__name__)
UPLOAD_FOLDER = 'static/Uploads/'
templatemap = {}
def readfromtemplate(filepath="static/Uploads/a.xlsx"):
    templatemap.clear()
    data = xlrd.open_workbook(filepath)
    table = data.sheets()[0]
    templatemap["templatename"] = table.row_values(0)[1]
    templatemap["templateshowname"] = table.row_values(1)[1]
    categoryList = []
    i = 3
    while i < table.nrows:
        tempmap = {}
        tempmap["categoryName"] = table.row_values(i)[1]
        j = i + 2
        tempmap["itemList"] = []
        while j < table.nrows and table.row_values(j)[0] != "Categoryname":
            tempmap["itemList"].append({"itemDetail":table.row_values(j)[0],
                            "violationLevel":table.row_values(j)[1],
                            "itemExplanation":table.row_values(j)[2]});
            j = j + 1
        categoryList.append(tempmap)
        if(j < table.nrows):
            i = j
        else:
            break
    templatemap["categoryList"] = categoryList
    print(json.dumps(templatemap,ensure_ascii=False))
	
@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'GET':
		return render_template('upload.html')
	elif request.method == 'POST':
		f = request.files['file']
		fname = f.filename
		print(fname)
		f.save(os.path.join(UPLOAD_FOLDER, fname))
		readfromtemplate()
		return "upload succeed!"
	
@app.route('/login',methods=['POST','GET'])
def hello_world():
    print(request.form)
    a = request.form
    session['username'] = request.form['username']
    if(a["username"] == 'admin' and a['password']=='admin'):
        res = Response('success')
        res.set_cookie(key='username',value = a['username'])
        return res
    else:
        return 'Invalid password!'

@app.route('/template/<name>')
def hello(name=None):
    return render_template('templatedetail.html', username=name)

@app.route('/createproject')
def createproject():
    name=request.cookies.get('username')
    return render_template('forms.html', username=name)
    
@app.route('/template',methods=['GET','POST'])
def dashboard():
    name=request.cookies.get('username')
    posts = []
    for each in os.listdir(UPLOAD_FOLDER):
        posts.append(each)
    return render_template('dashboard.html', username=name,posts=posts)

@app.route('/test',methods=['POST','GET'])
def test():
    # show the user profile for that user
    readfromtemplate()
    return json.dumps(templatemap,ensure_ascii=False)

if __name__ == '__main__':
    app.config.update(SECRET_KEY='123456') 
    app.run(host='0.0.0.0')
    
