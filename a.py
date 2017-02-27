#coding:utf-8
from flask import Flask
from flask import render_template
from flask import request as flaskrequest
from flask import session, make_response,Response
import urllib.request
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
    #print(json.dumps(templatemap,ensure_ascii=False))
	
@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if flaskrequest.method == 'GET':
		return render_template('upload.html')
	elif flaskrequest.method == 'POST':
		f = flaskrequest.files['file']
		fname = f.filename
		print(fname)
		f.save(os.path.join(UPLOAD_FOLDER, fname))
		readfromtemplate()
		posturl = "http://10.37.1.46:5000/test"
		req = urllib.request.Request(posturl)
		req.add_header('Content-Type', 'application/json; charset=utf-8')
		uploadjson = json.dumps(templatemap,ensure_ascii=False).encode('utf-8')
		req.add_header('Content-Length',len(uploadjson))
		print(uploadjson.decode('utf-8'))
		response = urllib.request.urlopen(req,uploadjson)		
		return "upload succeed!"
	
@app.route('/login',methods=['POST','GET'])
def hello_world():
    print(flaskrequest.form)
    a = flaskrequest.form
    session['username'] = flaskrequest.form['username']
    if(a["username"] == 'admin' and a['password']=='admin'):
        res = Response('success')
        res.set_cookie(key='username',value = a['username'])
        return res
    else:
        return 'Invalid password!'

@app.route('/template/<name>')
def hello(name=None):
    username=flaskrequest.cookies.get('username')
    return render_template('templatedetail.html', templatename=name, username=username)

@app.route('/templates/<name>',methods=['POST'])
def gettemplate(name=None):
    readfromtemplate("static/Uploads/"+name)
    return json.dumps(templatemap,ensure_ascii=False)


@app.route('/createproject')
def createproject():
    posts = []
    for each in os.listdir(UPLOAD_FOLDER):
        posts.append(each)
    name=flaskrequest.cookies.get('username')
    return render_template('forms.html', username=name,posts=posts)
    
@app.route('/template',methods=['GET','POST'])
def dashboard():
    name=flaskrequest.cookies.get('username')
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
    
