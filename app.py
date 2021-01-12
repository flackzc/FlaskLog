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
# db = SQLAlchemy(app)

# movies = [
#     {'title': 'My Neighbor Totoro', 'year': '1988'},
#     {'title': 'Dead Poets Society', 'year': '1989'},
#     {'title': 'A Perfect World', 'year': '1993'},
#     {'title': 'Leon', 'year': '1994'},
#     {'title': 'Mahjong', 'year': '1996'},
#     {'title': 'Swallowtail Butterfly', 'year': '1996'},
#     {'title': 'King of Comedy', 'year': '1999'},
#     {'title': 'Devils on the Doorstep', 'year': '1999'},
#     {'title': 'WALL-E', 'year': '2008'},
#     {'title': 'The Pork of Music', 'year': '2012'},
# ]

# print(type(log))
# print(logList)
logBasePath = '/media/sf_p-workspace/M7log/'
outPutPath = os.getcwd()
resultPath = outPutPath + "/result.log"
logList = []
log = os.listdir(logBasePath)
for line in log:
    # print(line)
    if os.path.isdir(logBasePath + line):
        logList.append(line)

def xremove(removcelogname):
    try:
        os.remove(removcelogname)
    except FileNotFoundError as e:
        pass



@app.route('/')
def index():
    xremove(resultPath)
    xremove("temp.log")

    # for line in log:
    #     # print(line)
    #     if os.path.isdir(logBasePath + line):
    #         logList.append(line)
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
    # print(type(inputLogName))

    # print(logname, "ddd")
    # return str(getstate4.run())
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
    # return "使用analyse_log analyse_map 绘图并页面显示"
    inputLogName2 = request.form.get('fname2').strip(' ')
    print("ddddddd"+logBasePath + inputLogName2)    
    if not inputLogName2:
        return "input empty"
    elif not os.path.exists(logBasePath + inputLogName2):
        return "log file not exist"
    elif inputLogName2 == "." or inputLogName2 == "..":
        return "log file not exist"
    else:
        # os.system("rm -rf analyse_log/log/Log*.log")
        # os.system("echo 111")
        print(logBasePath+inputLogName2)
        os.system("scp " + logBasePath + inputLogName2 + \
            "/userdata/logs/LOG*.log analyse_log/log")
        os.system("cd analyse_log; \
        ./analyse_log analyse_map; \
        mv *.png ../static/outputimage/")
        # for png in os.listdir("static/outputimage/"):
        #     print(png)
        #     xremove("static/outputimage/"+png)
        # for logfile in os.listdir("analyse_log/log"):
        #     print(logfile)
        #     xremove("analyse_log/log/"+logfile)  
        # xremove("static/outputimage/1.png")
        return render_template('draw.html', name=name)


@app.route("/delete", methods=['POST', 'GET'])
def delete():
    for png in os.listdir("static/outputimage/"):
        # print(png)
        xremove("static/outputimage/"+png)
    for logfile in os.listdir("analyse_log/log"):
        # print(logfile)
        xremove("analyse_log/log/"+logfile)  
    # xremove("static/outputimage/1.png")   
    return render_template('index.html', name=name, log=logList)

if __name__ == "__main__":
    app.run(debug=True,port=5001)
    
     