import sys
import os
# logPath = './log/'
keyvalue1 = "SetNextMachineState"
# keyvalue1 = "machinestate"

keyvalue2 = "deal msg"
keyvalue4 = "SetMessage"
keyvalue3 = "CheckMachineError"
keyvalue5 = "_IsCircle"
keyvalue6 = "_isTrapped"
keyvalue7 = "CCoveragePlanning"
keyvalue8 = "FaultNum"
keyvalue9 = "CleanModelCtrl::"
keyvalue10 = "SetTask - "
filters = ["MSG_CHARGEOK","MachineStartSlamWaiting_S","MSG_LOWPOWER","MSG_HAVE_CHARGE_SIGNAL","MSG_NO_CHARGE_SIGNAL"]
try:
    logPath = sys.argv[1]
except BaseException as msg:
    print("Usage:python "+sys.argv[0]+" logpath/parentpath")
    exit(1)
else:
    if not os.path.isdir(logPath):
        print("Usage:python "+sys.argv[0]+" logpath/parentpath")
        exit(1)
    


def extend(func):
    def wrepper(*xargs, **kw):
        if func.__name__ == "state_log1":
            print("Get info by deal return with fuction %s"% func.__name__)
        elif func.__name__ == "state_log2":
            print("Get info by SetMessage,with function %s"% func.__name__)
        func(*xargs, **kw)
        print("Test finished....")
    return wrepper

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

    fo = open(logPath+'temp.log', 'r')

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

    fo = open(logPath+'temp.log', 'r')

    for i in fo.readlines():
        log_list = i.split()
 
        if "UP_0x04_0x42" in i and log_list[1].split(".")[0] in time_near(time):

            worklist.append(log_list[7:9])
    try:
        return worklist[0]
    except Exception as msg:
        pass


def get_power_by_time2(time):
    powerlist = []

    fo = open(logPath+'temp.log', 'r')

    
    for i in fo.readlines():
        log_list = i.split()
        if 'battery' in i and 'MCU' in i and log_list[1].split(".")[0] in time_near(time):
            powerlist.append(log_list[6].split(',')[7:10])
    try:
        return powerlist[0]
    except Exception as msg:
        pass


def merge_log(filepath, outfile):
    k = open(filepath+outfile, 'a+')
    for parent, dirnames, filenames in os.walk(filepath):
        filenames.sort()
        # print(filenames)
        for filepath in filenames:
            if filepath.startswith("LOG") and filepath.endswith("log"):
                logpath = os.path.join(parent, filepath)
                f = open(logpath)
                k.write(f.read()+"\n")
    k.close()

def setmask(msg):
    if "ENavigationFoward" in msg:
        return "[状态] 导航直行"
    elif "ECoverageFoward" in msg:
        return "[状态] 覆盖直行"
    elif "ETurnRight" in msg:
        return "[状态] youzhuan"

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
        
    else:
        return "Unknow operation"


def iSTrapped(msg):
    if "trapped" in msg:
        return "[warning] 脱困"

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
        elif keyvalue7 in i and not ignore(i):
            if "dead lock" in i:
                print(log_list[1], "[warning] 可能小闭环导致重复撞墙") 
            elif "no uncover area" in i:
                print(log_list[1], "[INFO] 检测到没有覆盖区域")
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
        elif "ProcessLookDownFault" in i and "index" in i and not ignore(i):
            if log_list[8].strip(',') == "0":
                print(log_list[1], "[warning] 右下视触发")
            elif log_list[8].strip(',') == "1":
                print(log_list[1], "[warning] 右上下视触发")
            elif log_list[8].strip(',') == "2":
                print(log_list[1], "[warning] 左上下视触发")
            elif log_list[8].strip(',') == "3":
                print(log_list[1], "[warning] 左下视触发")
        # elif "AstarNoOpt" in i and "no path found" in i and not ignore(i):
        elif "no path found" in i and not ignore(i):
            print(log_list[1], "[INFO] AStar搜路无")
        elif "M7_Laser_Slam_Where_To_Go" in i and not ignore(i):
            print(log_list[1],"[INFO] 第一次重定位失败")
        elif "mcu_walkstate=4" in i and not ignore(i):
            print(log_list[1], "[warning] 可能下视导致原地转圈")
        elif "[SLAM]" in i and "no laser data send" in i and not ignore(i):
            print(log_list[1], "[ERROR] lds数据不更新")
        elif "FaultNum" in i and not ignore(i):
            print(log_list[1], faultnum(log_list[12]))        

        elif "SetTask - ETurnRight" in i and not ignore(i):
            print("youzhuan")
    fo.close()
    os.remove(logPath+'temp.log')


merge_log(logPath, "temp.log")
state_log2()



