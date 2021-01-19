# author by zc
# analyse log online

from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
import os
import flaskstate4, test
from flask import redirect, url_for, request


name = 'zc'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
logBasePath = '/media/sf_p-workspace/M7log/' # 服务器日志目录
outPutPath = os.getcwd()
resultPath = outPutPath + "/result.log"

# 读取日志服务器目录
logList = []
log = os.listdir(logBasePath)
for line in log:
    print(line)
    if os.path.isdir(logBasePath + line) and line.startswith("202") and not line.endswith(")"):
        logList.append(line)
    # logList.reverse()

# init方法，点击按钮是调用该方法删除缓存文件
def xremove(removcelogname):
    try:
        os.remove(removcelogname)
    except FileNotFoundError as e:
        pass

# 主页显示，读取index.html并显示主页
@app.route('/')
def index():
    logList = []
    log = os.listdir(logBasePath)
    for line in log:
        print(line)
        if os.path.isdir(logBasePath + line) and line.startswith("202") and not line.endswith(")"):
            logList.append(line)
        logList.reverse()

    xremove(resultPath)
    xremove("temp.log")
    return render_template('index.html', name=name, log=logList)

# 日志搜索
@app.route('/search', methods=['POST', 'GET'])
def search():
    searchList = []
    searchLogName = request.form.get('fname3').strip(' ')
    log = os.listdir(logBasePath)
    for line in log:
        print(line)
        if os.path.isdir(logBasePath + line) and line.startswith("202") and not line.endswith(")") and searchLogName in line:
            searchList.append(line)
        elif not searchLogName:
            return "no data"
        searchList.reverse()

    # xremove(resultPath)
    xremove("temp.log")
    return render_template('search.html', name=name, log=searchList)

# 日志内容搜索
@app.route("/analyse/searchloginfo", methods=['POST', 'GET']) 
def searchloginfo(): 
    # xremove(resultPath)
    xremove("temp.log")
    resultList = []
    searchLogName = request.form.get('fname4').strip(' ')
    if not searchLogName:
        return "input empty"
    # elif not os.path.exists(logBasePath + inputLogName):
    #     return "log file not exist"
    # elif inputLogName == "." or inputLogName == "..":
    #     return "log file not exist"
    else:
        # print(logBasePath + inputLogName)
        # flaskstate4.merge_log(logBasePath + searchLogName, "temp.log")
        # flaskstate4.state_log3()
        fo = open(resultPath, 'r')
        for line in fo.readlines():
            if searchLogName.lower() in line.lower():
                resultList.append(line)
        print(resultList)
        # xremove(resultPath)
        xremove(flaskstate4.logPath + "temp.log")
        return render_template('searchloginfo.html', name=name, logname=searchLogName, result=resultList)

# 点击主页reduce按钮，判断输入框内容后传参给分析脚本，跳转到result.html显示分析内容
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
        # xremove(resultPath)
        xremove(flaskstate4.logPath + "temp.log")
        return render_template('result.html', name=name, logname= inputLogName, result=result)



# 点击主页draw按钮，判断输入框内容后传参给分析脚本，跳转到draw.html显示分析内容
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

# 点击主页clear按钮，调用xremote方法删除缓存文件
@app.route("/delete", methods=['POST', 'GET'])
def delete():
    for png in os.listdir("static/outputimage/"):
        xremove("static/outputimage/"+png)
    for logfile in os.listdir("analyse_log/log"):
        xremove("analyse_log/log/"+logfile)   
    xremove("temp.log")
    return render_template('index.html', name=name, log=logList)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5001)
