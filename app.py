# author by zc
# analyse log online

from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
import os
import getstate4, test
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


@app.route('/')
def index():
    logList = []
    log = os.listdir('/media/sf_p-workspace/M7log')

    for i in log:
        print(i)
        if os.path.isdir('/media/sf_p-workspace/M7log/' + i):
            logList.append(i)
    return render_template('index.html', name=name, log=logList)

@app.route("/test2", methods=['POST', 'GET']) 
def analyse(): 
    logname = request.form.get('fname')

    # print(logname, "ddd")
    # return str(getstate4.run())
    getstate4.merge_log(getstate4.logPath, "temp.log")
    getstate4.state_log3()
    fo = open("log/result.log", 'r')
    result = fo.readlines()
    os.remove("log/result.log")
    os.remove(getstate4.logPath + "temp.log")
    return render_template('result.html', name=name, logname= logname, result=result)

if __name__ == "__main__":
    app.run(debug=True,port=5001)
    
    