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
outPutPath = os.getcwd() + "/log"
resultPath = outPutPath + "/result.log"

def xremove(removcelogname):
    try:
        os.remove(removcelogname)
    except FileNotFoundError as e:
        pass

@app.route('/')
def index():
    xremove(resultPath)
    xremove(flaskstate4.logPath + "temp.log")
    logList = []
    log = os.listdir(logBasePath)
    for line in log:
        print(line)
        if os.path.isdir(logBasePath + line):
            logList.append(line)
    return render_template('index.html', name=name, log=logList)

@app.route("/analyse", methods=['POST', 'GET']) 
def analyse(): 
    inputLogName = request.form.get('fname')

    # print(logname, "ddd")
    # return str(getstate4.run())
    flaskstate4.merge_log(flaskstate4.logPath, "temp.log")
    flaskstate4.state_log3()
    fo = open(resultPath, 'r')
    result = fo.readlines()
    xremove(resultPath)
    xremove(flaskstate4.logPath + "temp.log")
    return render_template('result.html', name=name, logname= inputLogName, result=result)

@app.route("/draw", methods=['POST', 'GET'])
def draw():
    # return "使用analyse_log analyse_map 绘图并页面显示"
    return render_template('draw.html', name=name)


if __name__ == "__main__":
    app.run(debug=True,port=5001)
    
    