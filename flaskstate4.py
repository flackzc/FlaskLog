import sys
import os
logPath = os.getcwd() + "/log/"
logType = "detail"
keyvalue1 = "SetNextMachineState"

keyvalue2 = "deal msg"
keyvalue4 = "SetMessage"
keyvalue3 = "CheckMachineError"
keyvalue5 = "_IsCircle"
keyvalue6 = "_isTrapped"
keyvalue7 = "CCoveragePlanning"
keyvalue8 = "FaultNum"
keyvalue9 = "CleanModelCtrl::"
keyvalue10 = "SetTask - "
keyvalue11 = "mp3aplay"
#"MSG_CHARGEOK",,"MSG_LOWPOWER"
filters = ["search_time", "cleaning -> going-home", "going-home -> going-home", "charging finished -> cleaning finished", "MSG_LOWPOWER", "MSG_CHARGEOK","MachineStartSlamWaiting_S","MSG_HAVE_CHARGE_SIGNAL","MSG_NO_CHARGE_SIGNAL"]
# try:
#     logType = sys.argv[1]
#     logPath = sys.argv[2]
# except BaseException as msg:
#     print("Usage:python "+sys.argv[0]+ " simple/detail" + " logpath/parentpath")
#     exit(1)
# else:
#     if not os.path.isdir(logPath):
#         print("Usage:python "+sys.argv[0]+" simple/detail"+" logpath/parentpath")
#         exit(1)
    

def extend(func):
    def wrepper(*xargs, **kw):
        # if sys.argv[1].lower() == "simple" or sys.argv[1].lower() == "s":
        #     print("Get simple info by %s"% func.__name__)
        # elif sys.argv[1].lower() == "detail" or sys.argv[1].lower() == "d":
        #     print("Get detail info by  %s"% func.__name__)
        func(*xargs, **kw)
        print("Test finished....")
    return wrepper


def writelog(*xargs):
    fo = open("result.log", 'a+')
    # print(xargs)
    fo.write(str(xargs))
    fo.write("\n")
    fo.close()
    
# writelog("asdasdas","123","234")
def ignore(one_line_log):
    for one_word in filters:
        if one_word in one_line_log:
            return True
    return False

def time_near(time):
    timenear = [time]
    timenear2 = []
    timeH = int(time.split(":")[0])
    timeM = int(time.split(":")[1])
    timeS = int(time.split(":")[2])
    if timeS >= 60 or timeM >= 60 or timeH >= 24:
        print("time format error")
        exit(1)
   
    for j in range(5):
            timeS = timeS + 1
            if timeS == 60:
                timeS = 0
                timeM += 1
            elif timeM >= 59:
                timeM = 0
                timeH += 1
            time = ':'.join([str(timeH),str(timeM),str(timeS)])
            timenear.append(time)

    for i in timenear:
        H = i.split(":")[0]
        M = i.split(":")[1]
        S = i.split(":")[2]
        if int(H) < 10 and not H.startswith("0"):
            H = "0"+str(H)
        if int(M) < 10 and not M.startswith("0"):
            M = "0"+str(M)
        if int(S) < 10 and not S.startswith("0"):
            S = "0"+str(S)
        timenear2.append(':'.join([H,M,S]))
    return timenear2


def get_cleantime_by_time2(time):
    cleanlist = []
    fo = open('temp.log', 'r')
    for i in fo.readlines():
        log_list = i.split()
        if "UP_0x04_0x42" in i and log_list[1].split(".")[0] in time_near(time):
            cleanlist.append(log_list[11:12])
    try:
        return cleanlist[0]
    except Exception as msg:
        pass

def get_workstatus_by_time2(time):
    worklist = []
    fo = open('temp.log', 'r')

    for i in fo.readlines():
        log_list = i.split()
        if "UP_0x04_0x42" in i and log_list[1].split(".")[0] in time_near(time):
            worklist.append(log_list[6:8])
    try:
        return worklist[0]
    except Exception as msg:
        pass


def get_power_by_time2(time):
    powerlist = []
    fo = open('temp.log', 'r')
    for i in fo.readlines():
        log_list = i.split()
        if 'battery' in i and 'MCU' in i and log_list[1].split(".")[0] in time_near(time):
            powerlist.append(log_list[6].split(',')[7:10])
    try:
        return powerlist[0]
    except Exception as msg:
        pass

def merge_log(filepath, outfile):
    # k = open(filepath+outfile, 'a+')
    k = open(outfile, 'a+')
    for parent, dirnames, filenames in os.walk(filepath):
        filenames.sort()
        # print(filenames)
        for filepath in filenames:
            if filepath.startswith("LOG") and filepath.endswith("log"):
                logpath = os.path.join(parent, filepath)
                f = open(logpath)
                k.write(f.read()+"\n")
    k.close()
# def fanCheck():
#     if msg == 1:
#         return "[INFO] 当前吸力：柔和"
#     elif msg == 0:
#         return "[INFO] 当前吸力：关闭"
#     elif msg == 2:
#         return "[INFO] 当前吸力：正常（默认"        
#     elif msg == 3:
#         return "[INFO] 当前吸力：强力"   
#     elif msg == 4:
#         return "[INFO] 当前吸力：安静"   
    
# def waterCheck():
#     if msg == 1:
#         return "[INFO] 当前吸力：慢速"
#     elif msg == 0:
#         return "[INFO] 当前吸力：关闭"
#     elif msg == 2:
#         return "[INFO] 当前吸力：标准（默认"        
#     elif msg == 3:
#         return "[INFO] 当前吸力：高速"   


def settask(msg):
    if "ENavigationFoward" in msg:
        # return "[消息] 导航直行" + " " + ' '.join(msg[7:11])
        return "[消息] 导航直行"
    elif "ECoverageFoward" in msg:
        return "[消息] 覆盖直行(弓形清扫)"
    elif "ETurnRight" in msg:
        return "[消息] 右转"
    elif "ETurnLeft" in msg:
        return "[消息] 左转"
    elif "EForward" in msg:
        return "[消息] 直行"
    elif "EStartChargePath" in msg:
        return "[消息] 开始回充"
    elif "EForwardWall" in msg:
        return "[消息] 沿墙"
    elif "EGotoCharge" in msg:
        return "[消息] 去充电座"
    elif "EArroundBarrier" in msg:
        return "[消息] 圆形延边"
    elif "EStopMove" in msg:
        return "[消息] 停止运动"
    elif "ESendChargeDock" in msg:
        # return "[消息] 发送充电座坐标" + " " +msg[7]
        return "[消息] 发送充电座坐标"
    elif "ECloseAllDevices" in msg:
        return "[消息] 关闭所有设备"
    elif "ECloseBSDevice" in msg:
        return "[消息] 关闭边刷"
    elif "EOpenBSDevice" in msg:
        return "[消息] 开启边刷"
    elif "EClearMcuStatus" in msg:
        return "[消息] 清除MCU状态"
    elif "EOpenAllDevices" in msg:
        return "[消息] 开启所有设备"
    elif "ELeaveCharge" in msg:
        return "[MCU 消息] 离开充电座"
    elif "EOpenVibMop" in msg:
        return "[消息] 开启震动拖"
    elif "ECloseVibMop" in msg:
        return "[消息] 关闭震动拖"
    elif "EOriginTurn" in msg:
        return "[消息] 原地旋转"
    elif "EStopChargePath" in msg:
        return "[消息] 关闭充电红灯"
    elif "ELeftSide" in msg:
        return "[消息] 左延边任务"
    elif "ERightSide" in msg:
        return "[消息] 右延边任务"
    elif "ELittleAreaFoward" in msg:
        return "[消息] 小区域直走"
    elif "ESyncTime" in msg:
        return "[消息] 同步时间戳"
    elif "EOpenWaterDevice" in msg:
        return "[消息] 开启水泵"

def faultnum(num):
    if num == "0x0203":
        return "[FAULT] 风机故障"
    elif num == "0x0201":
        return "[FAULT 激光传感器通信异常]"
    elif num == "0x0202":
        return "[FAULT] 主机通讯异常"
    # elif num == "0x0113":
    #     return "[ERROR] 多次回充对接失败"
    # elif num == "0x0101":
    #     return "[ERROR] 尘盒故障"
    # elif num == "0x0102":
    #     return "[ERROR] 轮组悬挂故障"
    # elif num == "0x0103":       
    #     return "[ERROR] 轮组过在故障"
    # elif num == "0x0108":
    #     return "[ERROR] 雷达罩故障"
    else:
        return "Ignore This"
  
def SetNextMachineState(state):
    if state == "MachineAreaProcessing_S":
        return "[状态] 区域延边清扫中"

    elif state == "MachineCoverProcessing_S":
        return "[状态] 区域覆盖清扫中"

    elif state == "MachineChargePathing_S":
        return "[状态] 开始回充导航"

    elif state == "MachineChargeRedFinding_S":
        return "[状态] 找到充电座红外信号"

    elif state == "MachineCharging_S":
        return "[状态] 充电中"

    elif state == "MachineLeavingChargePoint_S":
        return "[状态] 离开充电座过程中"

    elif state == "MachinePause_S":
        return "[状态] 机器暂停Pause"

    elif state == "MachineError_S":
        return "[状态] 机器异常"

    elif state == "MachineProducing_S":
        return "[状态] 进入产测模式"

    elif state == "MachineGroscopAdjusting_S":
        return "[状态] 陀螺仪校准模式"

    elif state == "MachineStartSlamWaiting_S":
        return "[状态] slam启动等待中"

    elif state == "MachineGoToPoint_S":
        return "[状态] 指哪扫哪点对点行走中"

    elif state == "MachineInit_S":
        return "[状态] 扫地机初始化过程"

def dealmsg(msg):
    if "MSG_NULL" == msg:
        return "[INFO] MSG_NULL"

    elif "NEED_RELOCATION" in msg:
        return  "[warning] 重定位"

    elif msg == "MSG_LOWPOWER":
        return  "[状态] 低电量"

    elif msg == "MSG_CHARGEOK":
        return  "[状态] 充电OK"

    elif msg == "MSG_WHEELUP":
        return  "[状态] 轮子抬起"

    elif msg == "MSG_WHEELDOWN":
        return  "[消息] 轮子落地"

    elif msg == "MSG_ISCHARGING":
        return  "[消息] 在充电座"

    elif msg == "MSG_UNCHARGING":
        return  "[消息] 离开充电座"

    elif msg == "MSG_APP_PAUSE":
        return  "[消息] app暂停Pause"

    elif msg == "MSG_APP_CONTINUE":
        return  "[消息] app恢复清扫"

    elif msg == "MSG_KEY_PAUSE_OR_CONTINUE":
        return  "[消息] 按键的暂停或开始"
            #
    elif msg == "MSG_KEY_GOTOCHARGE":
        return  "[消息] 按键回充"

    elif msg == "MSG_HAVE_CHARGE_SIGNAL":
        return  "[消息] 有充电座信号"

    elif msg == "MSG_NO_CHARGE_SIGNAL":
        return  "[消息] 没有充电座信号"

    elif msg == "MSG_APP_CLEAR_MAPINFO":
        return  "[消息] app清空地图信息"

    elif msg == "MSG_APP_STOP":
        return  "[消息] app暂停Stop"
            #
    elif msg == "MSG_APP_GOTOCHARGE":
        return  "[消息] app开始回充"

    elif msg == "MSG_AUTO_CLEAN":
        return  "[消息] 开始自动清扫"

    elif msg == "MSG_AREA_CLEAN":
        return  "[消息] 按区域清扫"

    elif msg == "MSG_APP_CONTROL":
        return  "[消息] app 端遥控"

    elif msg == "MSG_PRODUCING":
        return  "[消息] 产线检测消息"

    elif msg == "MSG_PRODUCING_EXIT":
        return  "[消息] 退出产测"

    elif msg == "MSG_LASER_NOT_RUN":
        return  "[消息] 雷达不转故障"

    elif msg == "MSG_MCU_ERROR":
        return  "[消息] MCU故障"

    elif msg == "MSG_MCU_RECOVERY":
        return  "[消息] MCU 故障恢复"

    elif msg == "MSG_LASER_RUN":
        return  "[消息] 雷达故障修复"

    elif msg == "MSG_ERROR_WHEELOVERLOAD":
        return  "[消息] 轮子过载"
            #
    elif msg == "MSG_ERROR_WINDOVERLOAD":
        return  "[消息] 风机过载"

    elif msg == "MSG_ERROR_BSOVERLOAD":
        return  "[消息] 边刷过载"

    elif msg == "MSG_ERROR_GSDOWN":
        return "[消息] 滚刷故障"

    elif msg == "MSG_ERROR_HITDOWN":
        return  "[消息] 撞板故障"

    elif msg == "MSG_ERROR_DOWNLOAD":
        return  "[消息] 触发防跌落故障"

    elif msg == "MSG_RECOVER_WHEELOVERLOAD":
        return  "[消息] 轮子过载恢复"

    elif msg == "MSG_RECOVER_WINDOVERLOAD":
        return  "[消息] 风机过载恢复"

    elif msg == "MSG_RECOVER_BSOVERLOAD":
        return  "[消息] 边刷过载恢复"

    elif msg == "MSG_RECOVER_GSDOWN":
        return  "[消息] 滚刷故障恢复"

    elif msg == "MSG_RECOVER_HITDOWN":
        return  "[消息] 撞板故障恢复"

    elif msg == "MSG_RECOVER_DOWNLOAD":
        return  "[消息] 防跌落故障恢复"

    elif msg == "MSG_ERROR_BOX":
        return  "[消息] 尘盒未安装"

    elif msg == "MSG_RECOVER_BOX":
        return  "[消息] 尘盒安装恢复"

    elif msg == "MSG_UPDATA_TIMEOUT":
        return  "[消息] 上报数据超时"

    elif msg == "MSG_VIRTUAL_WALL":
        return  "[消息] 设置虚拟墙"

    elif msg == "MSG_RESTRICT_AREA":
        return  "[消息] 设置禁区"

    elif msg == "MSG_LASER_COVERED":
        return  "[消息] 雷达被遮挡"

    elif msg == "MSG_LASER_UNCOVER":
        return  "[消息] 雷达恢复遮挡"

    elif msg == "MSG_ERROR_NOWATER":
        return  "[消息] 水箱缺水"

    elif msg == "MSG_ERROR_BOXFULL":
        return  "[消息] 尘盒已满"

    elif msg == "MSG_RECOVER_NOWATER":
        return  "[消息] 水箱缺水恢复"

    elif msg == "MSG_RECOVER_BOXFULL":
        return  "[消息] 尘盒已满恢复"

    elif msg == "MSG_ERROR_LOWPOWER":
        return  "[消息] 电量不足故障"

    elif msg == "MSG_RECOVER_LOWPOWER":
        return  "[消息] 电量不足故障恢复"

    elif msg == "MSG_ERROR_LASERHIT":
        return  "[消息] 雷达罩碰撞故障"

    elif msg == "MSG_RECOVER_LASERHIT":
        return  "[消息] 雷达罩故障恢复"

    elif msg == "MSG_ERROR_WHEELUP2":
        return  "[消息] 轮子悬空故障"

    elif msg == "MSG_RECOVER_WHEELUP2":
        return  "[消息] 轮子悬空故障恢复"

    elif msg == "MSG_APP_CLEAR_MAP":
        return  "[消息] app清空地图指令"

    elif msg == "MSG_SHUTDOWN_BLOCK":
        return  "[消息] 在充电座上禁止关机提示"

    elif msg == "MSG_ERROR_POSTILTSTART":
        return  "[消息] 启动时位置倾斜"

    elif msg == "MSG_RECOVER_POSTILTSTART":
        return  "[消息] 启动时位置倾斜故障恢复"

    elif msg == "MSG_INFO_MAPRELOCATION":
        return  "[消息] 地图重定位失败"

    elif msg == "MSG_RECOVER_MAPRELOCATION":
        return  "[消息] 地图重定位失败故障恢复"

    elif msg == "MSG_INFO_LOWPOWERCHARGE":
        return  "[消息] 低电量回充"

    elif msg == "MSG_RECOVER_LOWPOWERCHARGE":
        return  "[消息] 低电量回充故障恢复"

    elif msg == "MSG_ERROR_LASERCOMM":
        return  "[消息] 激光通讯异常"

    elif msg == "MSG_RECOVER_LASERCOMM":
        return  "[消息] 激光通讯异常故障恢复"

    elif msg == "MSG_ERROR_HOSTCOMM":
        return  "[消息] 主机通讯异常"

    elif msg == "MSG_RECOVER_HOSTCOMM":
        return  "[消息] 主机通讯异常故障恢复"

    elif msg == "MSG_ERROR_VIRTUALWALLSTART":
        return  "[消息] 禁区或虚拟墙位置启动"

    elif msg == "MSG_RECOVER_VIRTUALWALLSTART":
        return  "[消息] 禁区或虚拟墙位置启动故障恢复"

    elif msg == "MSG_ERROR_MAGNETICSTART":
        return  "[消息] 强磁场位置启动"

    elif msg == "MSG_ERECOVER_MAGNETICSTART":
        return  "[消息] 强磁场位置启动故障恢复"

    elif msg == "MSG_ERROR_EDGESENSOR":
        return  "[消息] 沿墙传感器被遮挡"

    elif msg == "MSG_RECOVER_EDGESENSOR":
        return  "[消息] 沿墙传感器被遮挡故障恢复"

    elif msg == "MSG_ERROR_LASERCOVER":
        return  "[消息] 激光传感器被卡住"

    elif msg == "MSG_RECOVER_LASERCOVER":
        return  "[消息] 激光传感器被卡住故障解除"

    elif msg == "MSG_ERROR_INNER":
        return  "[消息] 机器内部错误"

    elif msg == "MSG_RECOVER_INNER":
        return  "[消息] 机器内部错误故障解除"

    elif msg == "MSG_APP_GO_TO_POINT":
        return  "[消息] 指哪扫哪点对点消息"
    elif msg == "MSG_POINT_CLEAN":
        return  "[消息] 指哪扫哪清扫"

    elif msg == "MSG_NEED_REBOOT":
        return  "[消息] 需要重启系统"

    elif msg == "MSG_NEED_POWEROFF":
        return  "[消息] 手动关机"

    elif msg == "MSG_ERROR_MOPPINGDROP":
        return  "[消息] 拖地板掉落故障"

    elif msg == "MSG_RECOVER_MOPPINGDROP":
        return  "[消息] 拖地板掉落故障恢复"

    elif msg == "MSG_ERROR_SLIPJAM":
        return  "[消息] 打滑卡住故障"

    elif msg == "MSG_RECOVER_SLIPJAM":
        return  "[消息] 打滑卡住故障恢复"

    elif msg == "MSG_ERROR_CHARGE":
        return  "[消息] 回充故障"

    elif msg == "MSG_RECOVER_CHARGE":
        return  "[消息] 回充故障恢复"
    else:
        return "Unknow operation"

def CheckMachineError(msg):
    if msg == "MCU_ERROR_WHEEL_OVERLOAD":
        return "[MCU 报警] 轮子过载 "

    elif msg == "MCU_ERROR_WIN_OVERLOAD":
        return "[MCU 报警] 风机过载"

    elif msg == "MCU_ERROR_BS_OVERLOAD":
        return "[MCU 报警] 边刷过载"

    elif msg == "MCU_ERROR_NO_BOX":
        return "[MCU 报警]] 无尘盒"

    elif msg == "MCU_ERROR_GS_OVERLOAD":
        return "[MCU 报警] 滚刷过载"

    elif msg == "MCU_ERROR_HIT_DOWN":
        return "[MCU 报警] 碰撞板故障 "

    elif msg == "MCU_ERROR_GENER":
        return "[MCU 报警]] 底板通用故障"

    elif msg == "MCU_ERROR_DOWNLOAD":
        return "[MCU 报警] empty"

    elif msg == "MCU_ERROR_TIMEOUT":
        return "[MCU 报警] 通信超时"

    elif msg == "MCU_ERROR_NOWATER":
        return "[MCU 报警]] 没水了"

    elif msg == "MCU_ERROR_BOXFULL":
        return "[MCU 报警] 尘盒满"

    elif msg == "MCU_ERROR_WHEELUP2":
        return "[MCU 报警] 轮子悬空MCU_ERROR_WHEELUP2"

    elif msg == "MCU_ERROR_LOWPOWER":
        return "[MCU 报警] 低电量"

    elif msg == "MCU_ERROR_LASERHIT":
        return "[MCU 报警]] 雷达碰撞板卡住 "

    elif msg == "MCU_ERROR_WHEELUP":
        return "[MCU 报警] 轮子悬空，MCU_ERROR_WHEELUP"

    elif msg == "MCU_ERROR_LASER_NOT_RUN":
        return "[MCU 报警] 雷达卡主"

    elif msg == "MCU_ERROR_LASER_COVERED":
        return "[MCU 报警]] 雷达被遮挡 "

    elif msg == "MCU_ERROR_VIRWALL_START":
        return "[MCU 报警] 禁区或虚拟墙位置启动"

    elif msg == "MCU_ERROR_MOPPINGDROP":
        return "[MCU 报警] 拖地板掉落故障 "

    elif msg == "MCU_ERROR_SLIPJAM":
        return "[MCU 报警]] 打滑故障"

    elif msg == "MCU_ERROR_CHARGE":
        return "[MCU 报警] 回充故障"
    else:
        return "Unknow operation"

def IsCircle(msg):
    if "Small Circle" in msg:
        return "[warning] 小区域闭环"

    elif "KeyPoint Judge circle is done!" in msg:
        return "[INFO] KeyPoint Judge circle is done!"

    elif "StartPoint Judge circle is done" in msg:
        return "[INFO] StartPoint Judge circle is done"

    elif "Boundary Circle or StartPose Circle" in msg:
        return  "[INFO] Boundary Circle or StartPose Circle"

    elif "TimeOut Judge circle is done" in msg:
        return "[INFO] 区域分割延边超时"
    
    elif "maybecircle" in msg:
        return "[INFO] maybecircle"
    else:
        return "Unknow operation"

def SoundMp3(msg):
    if "1.mp3" == msg:
        return "[状态] 播放：开机和弦音"
    elif "DI.mp3" == msg:
        return "[状态] 播放：嘀"
    elif "2.mp3" == msg:
        return "[状态] 播放：嘀"
    elif "4.mp3" == msg:
        return "[状态] 播放：正在等待联网，请按照手机指示操作，iot"   
    elif "5.mp3" == msg:
        return "[状态] 播放：关机和弦音"
    elif "7.mp3" == msg:
        return "[状态] 播放：预约清扫启动，开始工作"
    elif "8.mp3" == msg:
        return "[状态] 播放：预约清扫完成，回去充电"
    elif "9.mp3" == msg:
        return "[状态] 播放：电量补充完成，继续上次未完成清扫"
    elif "10.mp3" == msg:
        return "[状态] 播放：去充电"
    elif "12.mp3" == msg:
        return "[状态] 播放：电量不足，去充电"
    elif "13.mp3" == msg:
        return "[状态] 播放：清扫完成，去充电"
    elif "14.mp3" == msg:
        return "[状态] 播放：开始充电提示音和弦音"
    elif "15.mp3" == msg:
        return "[状态] 播放：请轻拍激光雷达"
    elif "17.mp3" == msg:
        return "[状态] 播放：开始固件升级，请勿操作扫地机（U盘升级）"
    elif "18.mp3" == msg:
        return "[状态] 播放：固件升级成功（U盘升级）"
    elif "19.mp3" == msg:
        return "[状态] 播放：请安装尘盒"
    elif "20.mp3" == msg:
        return "[状态] 播放：请将机器放在水平地面启动"
    elif "21.mp3" == msg:
        return "[状态] 播放：请检查并清理轮子"
    elif "23.mp3" == msg:
        return "[状态] 播放：请检查并清理边刷"
    elif "24.mp3" == msg:
        return "[状态] 播放：请检查并清理滚刷"
    elif "25.mp3" == msg:
        return "[状态] 播放：请轻拍碰撞板"
    elif "26.mp3" == msg:
        return "[状态] 播放：停止"
    elif "27.mp3" == msg:
        return "[状态] 播放：请擦拭防跌落传感器"
    elif "29.mp3" == msg:
        return "[状态] 播放：发生内部异常，请重启机器"
    elif "32.mp3" == msg:
        return "[状态] 播放：暂停"
    elif "33.mp3" == msg:
        return "[状态] 播放：停止清扫"
    elif "34.mp3" == msg:
        return "[状态] 播放：定位嫂地机位置，iot"
    elif "35.mp3" == msg:
        return "[状态] 播放：开始全屋清扫"
    elif "36.mp3" == msg:
        return "[状态] 播放：开始划区清扫"
    elif "37.mp3" == msg:
        return "[状态] 播放：开始指定区域清扫"
    elif "38.mp3" == msg:
        return "[状态] 播放：尘盒已取出"
    elif "39.mp3" == msg:
        return "[状态] 播放：地图保存中，请稍后"
    elif "40.mp3" == msg:
        return "[状态] 播放：电量过低，请充电"
    elif "41.mp3" == msg:
        return "[状态] 播放：定位失败，地图失效，开始新清扫"

    elif "42.mp3" == msg:
        return "[状态] 播放：回充失败，请擦拭触片并移除充电座周围的障碍物"
    elif "43.mp3" == msg:
        return "[状态] 播放：结束控制"
    elif "44.mp3" == msg:
        return "[状态] 播放：手动控制"
    elif "45.mp3" == msg:
        return "[状态] 播放：开始前往目标点"
    elif "46.mp3" == msg:
        return "[状态] 播放：已到达目标点"
    elif "47.mp3" == msg:
        return "[状态] 播放：请拨动激光头，确认无遮挡或卡住"
    elif "48.mp3" == msg:
        return "[状态] 播放：请擦拭机器侧边传感器"
    elif "49.mp3" == msg:
        return "[状态] 播放：请将机器搬离虚拟墙区域启动"
    elif "50.mp3" == msg:
        return "[状态] 播放：请将机器放置水平地面启动"
    elif "51.mp3" == msg:
        return "[状态] 播放：请将机器手动放回充电座"
    elif "52.mp3" == msg:
        return "[状态] 播放：如需关机，请离开充电座后再试"
    elif "53.mp3" == msg:
        return "[状态] 播放：定位失败，无法清扫"
    elif "55.mp3" == msg:
        return "[状态] 播放：无法到达目标点"

def StateChange(msg):
    if "sleep -> pause clean" in msg:
        return "[状态] 休眠->暂停清扫"

    elif "standby -> sleep" in msg:
        return "[状态] 待机->休眠"

    elif "sleep -> charging" in msg:
        return "[状态] 休眠->回充"

    elif "standby -> sleep" in msg:
        return "[状态] 待机->休眠"

    elif "pause gohome -> sleep" in msg:
        return "[状态] 暂停回充->休眠"

    elif "sleep -> cleaning" in msg:
        return "[状态] 休眠->清扫"

    elif "pause clean -> sleep" in msg:
        return "[状态] 暂停清扫->休眠"    

    elif "sleep -> going-home" in msg:
        return "[状态] 休眠->回充"

    elif "error -> sleep" in msg:
        return "[状态] 保障->休眠"
    else:
        return "待添加"   

def iSTrapped(msg):
    if "trapped" in msg:
        return "[warning] 脱困"

def getOdom():
    fo = open(logPath+'temp.log', 'r')
    OdomList = []
    for i in fo.readlines():
        log_list = i.split()
        
        if len(log_list) > 6:
            if "UpdateOdomPose" == log_list[6]:
                OdomList.append(log_list[9])
    # print(len(OdomList))
    print(OdomList)
    for i in range(len(OdomList)):
        if abs(float(OdomList[i])) - abs(float(OdomList[i - 1])) > 20:
            print(OdomList[i], OdomList[i-1])

def checkWheel(msg):
    wheelL=msg[6].replace("=",",").split(",")[21]
    wheelR=msg[6].replace("=",",").split(",")[23]
    # print(wheelL,wheelR)
    # print(msg)
    if abs(int(wheelL)) - abs(int(wheelR)) > 10:
        print(msg[1],"[error] 轮组转速异常")
    else:
        pass
# def CleanModelCtrl(msg):
#     if str(msg) == "LaserOnTask":
#         return "[消息] LDS雷达起动任务"
#     elif (msg) == "LaserOffTask":
#         return "[消息] LDS雷达停止任务"

# def RElocation(msg):
#     if msg == "ProcessRelocationFailed":
#         return "[warning] 重定位失败"

# def CCoveragePlan(msg):
#     if "dead lock" == msg[6:7]:
#         print(msg)
#         return "[warning] 可能小闭环导致重复撞墙"



# deal msg
@extend
def state_log1():
    fo = open(logPath+'temp.log', 'r')
    for i in fo.readlines():
        log_list = i.split()

        if keyvalue1 in i and not ignore(i):
            # print(i)
            if log_list[9] == "MachineChargePathing_S":
                print(log_list[1],SetNextMachineState(log_list[9]),get_power_by_time2(log_list[1].split('.')[0]))
            else:
                print(log_list[1],SetNextMachineState(log_list[9]))
            
        elif keyvalue2 in i and not ignore(i):
            try:
                log_list[9]
            except BaseException:
                # print(i)
                print(log_list[1], dealmsg(log_list[6].strip('.')))
            else:
                # print(i)
                if log_list[8].strip('.') == "MSG_AUTO_CLEAN":
                    print(log_list[1], dealmsg(log_list[8].strip('.')),get_workstatus_by_time2(log_list[1].split('.')[0]))
                else:
                    print(log_list[1], dealmsg(log_list[8].strip('.')))

                
    # 根据CheckMachineError获取底板报警状态
        # elif keyvalue3 in i and filter1 not in i:
        elif "MCU" in i and keyvalue3 in i and not ignore(i):
            # log_list = i.split()
            # print(log_list)
            print(log_list[1], CheckMachineError(log_list[7].lstrip("ERROR").strip(".")))
        elif keyvalue5 in i and not ignore(i):
            print(log_list[1], IsCircle(i))
        elif keyvalue6 in i and not ignore(i):
            # print(log_list[1],iSTrapped(i))
            if "trapped" in i:
                print(log_list[1], "[warning] 脱困")
        elif "ProcessRelocationFailed" in i:
            print(log_list[1], "[warning] 重定位失败")   
        elif keyvalue7 in i and not ignore(i):
            if "dead lock" in i:
                print(log_list[1], "[warning] 可能小闭环导致重复撞墙") 
        # elif keyvalue8 in i and not ignore(i):
        #     # print(log_list)
        #     print(log_list[1],faultnum(log_list[16][8:].strip("[]")))
        elif keyvalue9 in i and not ignore(i):
            # print(i)
            if log_list[4].split("::")[1] == "LaserOnTask":
                print(log_list[1],"[消息] LDS雷达起动任务")
            elif log_list[4].split("::")[1] == "LaserOffTask":
                print(log_list[1],"[消息] LDS雷达停止任务")
        elif "reboot" in i and not ignore(i):
            print(log_list[1], "[warning] 系统重启")
        elif "ProcessLookDownFault" in i and "index" in i and not ignore(i):
            if log_list[8].strip(',') == "0":
                print(log_list[1], "[warning] 右下视触发")
            elif log_list[8].strip(',') == "1":
                print(log_list[1], "[warning] 右上下视触发")
            elif log_list[8].strip(',') == "2":
                print(log_list[1], "[warning] 左上下视触发")
            elif log_list[8].strip(',') == "3":
                print(log_list[1], "[warning] 右视触发")
        elif "AstarNoOpt" in i and "no path found" in i and not ignore(i):
            print(log_list[1], "[INFO] AStar搜路无")
        elif "M7_Laser_Slam_Where_To_Go" in i and not ignore(i):
            print(log_list[1],"[INFO] 第一次重定位失败")
        elif "mcu_walkstate=4" in i and not ignore(i):
            print(log_list[1], "[warning] 可能下视导致原地转圈")
    fo.close()
    os.remove(logPath+'temp.log')

@extend
def state_log2():
    fo = open(logPath+'temp.log', 'r')
    for i in fo.readlines():
        log_list = i.split()

        if keyvalue1 in i and not ignore(i):
            if log_list[9] == "MachineChargePathing_S":
                print(log_list[1],SetNextMachineState(log_list[9]),get_power_by_time2(log_list[1].split('.')[0]))
            else:
                print(log_list[1],SetNextMachineState(log_list[9]))
        elif keyvalue4 in i and not ignore(i):
            try:
                log_list[9]
            except BaseException:
                # print(i)
                print(log_list[1], dealmsg(log_list[6].strip('.')))
            else:
                # print(i)
                if log_list[9].strip('.') == "MSG_AUTO_CLEAN":
                    print(log_list[1], dealmsg(log_list[9].strip('.')),get_workstatus_by_time2(log_list[1].split('.')[0]))
                else:
                    print(log_list[1], dealmsg(log_list[9].strip('.')))
              
    # 根据CheckMachineError获取底板报警状态
        elif "MCU" in i and keyvalue3 in i and not ignore(i):
            # log_list = i.split()
            # print(log_list)
            print(log_list[1], CheckMachineError(log_list[7].lstrip("ERROR").strip(".")))
        elif keyvalue5 in i and not ignore(i):
            print(log_list[1], IsCircle(i))
        elif keyvalue6 in i and not ignore(i):
            # print(log_list[1],iSTrapped(i))
            if "trapped" in i:
                print(log_list[1], "[warning] 脱困")
        elif "ProcessRelocationFailed" in i:
            print(log_list[1], "[warning] 重定位失败")   
        # elif keyvalue7 in i and not ignore(i):
        #     if "dead lock" in i:
        #         print(log_list[1], "[warning] 可能小闭环导致重复撞墙") 
        #     elif "no uncover area" in i:
        #         print(log_list[1], "[INFO] 检测到没有覆盖区域")
        # elif keyvalue8 in i and not ignore(i):
        #     # print(log_list)
        #     print(log_list[1],faultnum(log_list[16][8:].strip("[]")))
        elif keyvalue9 in i and not ignore(i):
            # print(i)
            # print(i)
            if log_list[4].split("::")[1] == "LaserOnTask":
                print(log_list[1],"[消息] LDS雷达起动任务")
            elif log_list[4].split("::")[1] == "LaserOffTask":
                print(log_list[1],"[消息] LDS雷达停止任务")
            elif "m_nRelocationResult=160" in i and not ignore(i):
                print(log_list[1],"[INFO] 重定位成功")            
        elif "system  reboot" in i and "Process0x03_0x37_0x01" in i and not ignore(i):
            print(log_list[1], "[warning] 系统重启")
        # elif "ProcessLookDownFault" in i and "index" in i and not ignore(i):
        #     if log_list[8].strip(',') == "0":
        #         print(log_list[1], "[warning] 右下视触发")
        #     elif log_list[8].strip(',') == "1":
        #         print(log_list[1], "[warning] 右上下视触发")
        #     elif log_list[8].strip(',') == "2":
        #         print(log_list[1], "[warning] 左上下视触发")
        #     elif log_list[8].strip(',') == "3":
        #         print(log_list[1], "[warning] 左下视触发")
        # elif "AstarNoOpt" in i and "no path found" in i and not ignore(i):
        # elif "no path found" in i and not ignore(i):
        #     print(log_list[1], "[INFO] AStar搜路无")
        # elif "M7_Laser_Slam_Where_To_Go" in i and not ignore(i):
        #     print(log_list[1],"[INFO] 第一次重定位失败")
        # elif "mcu_walkstate=4" in i and not ignore(i):
        #     print(log_list[1], "[warning] 可能下视导致原地转圈")
        # elif "[SLAM]" in i and "no laser data send" in i and not ignore(i):
        #     print(log_list[1], "[ERROR] lds数据不更新")
        elif "FaultNum" in i and not ignore(i):
            print(log_list[1], faultnum(log_list[12]))        
    fo.close()
    os.remove(logPath+'temp.log')


@extend
def state_log3():
    fo = open('temp.log', 'r')
    for i in fo.readlines():
        log_list = i.split()

        if keyvalue1 in i and not ignore(i):
            if log_list[9] == "MachineChargePathing_S":
                writelog(log_list[1],SetNextMachineState(log_list[9]),get_power_by_time2(log_list[1].split('.')[0]))
            else:
                writelog(log_list[1],SetNextMachineState(log_list[9]))

        elif keyvalue4 in i and not ignore(i):
            if len(log_list) >= 9:
                # print(i)
                if log_list[9].strip('.') == "MSG_AUTO_CLEAN":
                    # print(log_list)
                    # print(log_list[1], dealmsg(log_list[9].strip('.')),','.join(get_workstatus_by_time2(log_list[1].split('.')[0])))
                    if get_workstatus_by_time2(log_list[1].split('.')[0]):
                        writelog(log_list[1], dealmsg(log_list[9].strip('.')),' '.join(get_workstatus_by_time2(log_list[1].split('.')[0])).replace(",",""))
                    else:
                        writelog(log_list[1], dealmsg(log_list[9].strip('.')),get_workstatus_by_time2(log_list[1].split('.')[0]))

                elif log_list[9].strip(".") == "MSG_KEY_PAUSE_OR_CONTINUE":

                    if get_workstatus_by_time2(log_list[1].split('.')[0]):
                        
                        writelog(log_list[1], dealmsg(log_list[9].strip('.')),' '.join(get_workstatus_by_time2(log_list[1].split('.')[0])).replace(",",""))
                    else:
                        writelog(log_list[1], dealmsg(log_list[9].strip('.')),get_workstatus_by_time2(log_list[1].split('.')[0]))
                else:
                    writelog(log_list[1], dealmsg(log_list[9].strip('.')))
              
    # 根据CheckMachineError获取底板报警状态
        elif "MCU" in i and keyvalue3 in i and not ignore(i):
            writelog(log_list[1], CheckMachineError(log_list[7].lstrip("ERROR").strip(".")))

        elif keyvalue5 in i and not ignore(i):
            writelog(log_list[1], IsCircle(i))
            
        elif keyvalue6 in i and not ignore(i):
            if "trapped" in i:
                writelog(log_list[1], "[warning] 脱困")

        elif keyvalue7 in i and not ignore(i):
            if "dead lock" in i:
                writelog(log_list[1], "[warning] 可能小闭环导致重复撞墙") 
            elif "no uncover area" in i:
                writelog(log_list[1], "[INFO] 检测到没有覆盖区域")
            
            elif "find uncovered area" in i and not ignore(i):
                # writelog(log_list[1], "[INFO] 找到未覆盖区域%s" % ''.join(log_list[9:13]).rstrip(","))
                writelog(log_list[1], "[INFO] 找到未覆盖区域")
        # elif keyvalue8 in i and not ignore(i):
        #     # print(log_list)
        #     print(log_list[1],faultnum(log_list[16][8:].strip("[]")))
        elif keyvalue9 in i and not ignore(i):
            if log_list[4].split("::")[1] == "LaserOnTask":
                writelog(log_list[1],"[消息] LDS雷达起动任务")

            elif log_list[4].split("::")[1] == "LaserOffTask":
                writelog(log_list[1],"[消息] LDS雷达停止任务")

            elif "m_nRelocationResult=160" in i and not ignore(i):
                writelog(log_list[1],"[INFO] 重定位成功")   

            elif "m_bLowerPowerContinue: start clean" in i and not ignore(i):
                writelog(log_list[1], "[INFO] 开始断点续嫂")

            elif "MSG_CHARGEOK" in i and not ignore(i):
                writelog(log_list[1], "[INFO] 充电完成",get_power_by_time2(log_list[1].split('.')[0]))
            
            elif "lookDownFaultHappen, sensor index: 0" in i and not ignore(i):
                writelog(log_list[1], "[ERROR] 机器人防跌落传感器被遮挡")

        elif keyvalue10 in i and not ignore(i):
            writelog(log_list[1], settask(log_list))

        elif keyvalue11 in i and "exec" in i and not ignore(i):
            ll = log_list[7].split('/')[3]
            writelog(log_list[1], SoundMp3(ll))

        elif "system  reboot" in i and "Process0x03_0x37_0x01" in i and not ignore(i):
            writelog(log_list[1], "[warning] 系统重启")

        elif "ProcessRelocationFailed" in i:
            writelog(log_list[1], "[warning] 重定位失败")   

        elif "ProcessLookDownFault" in i and "index" in i and not ignore(i):
            if log_list[8].strip(',') == "0":
                writelog(log_list[1], "[warning] 右下视触发")
            elif log_list[8].strip(',') == "1":
                writelog(log_list[1], "[warning] 右上下视触发")
            elif log_list[8].strip(',') == "2":
                writelog(log_list[1], "[warning] 左上下视触发")
            elif log_list[8].strip(',') == "3":
                writelog(log_list[1], "[warning] 左下视触发")

        # elif "CPathPlan" in i and not ignore(i):
            if "MAStar" in i:
                writelog(log_list[1], "[INFO] 开始Astar搜路", ''.join(log_list[6:]))

            elif "no path found" in i:
                writelog(log_list[1], "[INFO] AStar搜路no path found")

        elif "M7_Laser_Slam_Where_To_Go" in i and not ignore(i):
            writelog(log_list[1],"[INFO] 第一次重定位失败")

        elif "mcu_walkstate=4" in i and not ignore(i):
            writelog(log_list[1], "[warning] 可能下视导致原地转圈")

        elif "[SLAM]" in i and "no laser data send" in i and not ignore(i):
            writelog(log_list[1], "[ERROR] lds数据不更新")

        elif "FaultNum" in i and not ignore(i):
            writelog(log_list[1], faultnum(log_list[12]))        

        elif "_GotoNextCleanArea" in i and not ignore(i):
            # writelog(log_list[1], "[消息] 去下一个分区",log_list[5].strip())
            writelog(log_list[1], "[消息] 去下一个分区")
        elif "CMotionPlanTask::UpdateForbiddenSetting" in i and "ForbiddenZone" in i and not ignore(i):
            # writelog(log_list[1], "[消息] 更新虚拟禁区设置", ''.join(log_list[7:]))
            writelog(log_list[1], "[消息] 更新虚拟禁区设置")
        elif "CMotionPlanTask::GetWalkStatus" in i and not ignore(i):
            if "stopped1111111111111111" in i:
                writelog(log_list[1], "[状态] 停止状态")

            elif "stop by collision" in i:
                writelog(log_list[1], "[状态] 区域分割延边时碰撞停止")
        
        elif "Area Can not find Entry" in i and not ignore(i):
            # writelog(log_list[1], "[状态] 区域无法找到入口",i.split('-')[1].strip())
            writelog(log_list[1], "[状态] 区域无法找到入口")
        elif "We Think Area Is Cleand" in i and not ignore(i):
            # writelog(log_list[1], "[状态] 区域清扫完成", ''.join(log_list[11:]))
            writelog(log_list[1], "[状态] 区域清扫完成")
        elif "Area Entry Pos" in i and not ignore(i):
            # writelog(log_list[1], "[状态] 找到区域入口",i.split('-')[1].strip())
            writelog(log_list[1], "[状态] 找到区域入口")
        elif "start path failed" in i and not ignore(i):
            writelog(log_list[1], "[error] 搜路去起始点失败")

        elif "StartCoverage - failed" in i and not ignore(i):
            print(log_list[1], "[error] 覆盖失败")
        
        elif "STATUS" in i and "sleep" in i and not ignore(i):
            writelog(log_list[1], StateChange(i))
        
        elif "wheelL" in i and "wheelR" in i and not ignore(i):
            try:
                wheelL=log_list[6].replace("=",",").split(",")[21]
                wheelR=log_list[6].replace("=",",").split(",")[23]
                if abs(abs(int(wheelL)) - abs(int(wheelR))) > 25:
                    # writelog(log_list[1],"[error] 轮组差速异常", "左轮：%s,右轮：%s" %(wheelL, wheelR)) 
                    writelog(log_list[1],"[error] 轮组差速异常")
                # elif wheelL == 0 and wheelR == 0:
                #     print(log_list[1],"[error] 轮组转速异常", "左轮：%s,右轮：%s" %(wheelL, wheelR)) 
                elif wheelL > 46 or wheelR > 46:
                    # writelog(log_list[1],"[error] 轮组转速异常", "左轮：%s,右轮：%s" %(wheelL, wheelR)) 
                    writelog(log_list[1],"[error] 轮组转速异常")
            except BaseException as e:
                pass
        
        # elif "search_time" in i and not ignore(i):
        #     # print(len(log_list))
        #     writelog(log_list[1], "[INFO] 单次搜索时间 %sms" % log_list[11].split("=")[1], ''.join(log_list[6:11]).rstrip(","))

        elif "get_closet_cell_run_time" in i and not ignore(i):
            writelog(log_list[1], "[INFO] 区域搜索时间 %sms" % log_list[7].split("=")[1])
        
        elif "CSlip::Run" in i and not ignore(i):
            writelog(log_list[1], "[warning] 机器打滑了")


    fo.close()
    # os.remove(logPath+'temp.log')

merge_log(logPath, "temp.log")
# state_log3()


