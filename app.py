# author by zc
# analyse log online

from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
import os
import flaskstate4, test
from flask import redirect, url_for, request


app = Flask(__name__)
name = 'zc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
logBasePath = '/media/sf_p-workspace/M7log/'
outPutPath = os.getcwd()
resultPath = outPutPath + "/result.log"
logList = []
log = os.listdir(logBasePath)
for line in log:
    print(line)
    if os.path.isdir(logBasePath + line) and line.startswith("202") and not line.endswith(")"):
        logList.append(line)
    logList.reverse()

def xremove(removcelogname):
    try:
        os.remove(removcelogname)
    except FileNotFoundError as e:
        pass

@app.route('/')
def index():
    xremove(resultPath)
    xremove("temp.log")

    return render_template('index.html', name=name, log=logList)

@app.route("/analyse", methods=['POST', 'GET']) 
def analyse(): 
    xremove(resultPath)
    xremove("temp.log")
    inputLogName = request.form.get('fname').strip(' ')
    if not inputLogName:
        return "input empty"
    elif not os.path.exists(logBasePath + inputLogName):
        return "log file not exist"
    elif inputLogName == "." or inputLogName == "..":
        return "log file not exist"
    else:
        print(logBasePath + inputLogName)
        flaskstate4.merge_log(logBasePath + inputLogName, "temp.log")
        flaskstate4.state_log3()
        fo = open(resultPath, 'r')
        result = fo.readlines()
        xremove(resultPath)
        xremove(flaskstate4.logPath + "temp.log")
        return render_template('result.html', name=name, logname= inputLogName, result=result)

@app.route("/draw", methods=['POST', 'GET'])
def draw():
    inputLogName2 = request.form.get('fname2').strip(' ')   
    if not inputLogName2:
        return "input empty"
    elif not os.path.exists(logBasePath + inputLogName2):
        return "log file not exist"
    elif inputLogName2 == "." or inputLogName2 == "..":
        return "log file not exist"
    else:
        os.system("scp " + logBasePath + inputLogName2 + \
            "/userdata/logs/LOG*.log analyse_log/log")
        os.system("cd analyse_log; \
        ./analyse_log analyse_map; \
        mv *.png ../static/outputimage/")
        return render_template('draw.html', name=name)

@app.route("/delete", methods=['POST', 'GET'])
def delete():
    for png in os.listdir("static/outputimage/"):
        xremove("static/outputimage/"+png)
    for logfile in os.listdir("analyse_log/log"):
        xremove("analyse_log/log/"+logfile)   
    return render_template('index.html', name=name, log=logList)

if __name__ == "__main__":
    app.run(debug=True,port=5001)
