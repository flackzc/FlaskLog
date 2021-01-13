# line="I1226 09:41:22.800747 453] [MCU] Process0x03_0x37_0x01 - TaskID=10848,sendID=10848,recvcount=2613500,walkstate=2,sideState=0,version=11491, battStat=1,McuADv=161,McuADa=72,battery=80,wheelL=2, wheelR=4, Algorithm=0, Ultrasonic=0, robotType=16"
# line1=line.split()
# print(line1[7].replace("=",","))
# import requests
url="https://******/feedback/v1/web/feedback/log/download/oss?logName=20201226_131639_000_0900000002A9_complete_clean.tar.gz&sn=0000B831175000461090341Z0042Q0V2"
import requests 

r = requests.get(url,auth = ("Midea","******$$")) 
print(r)
with open("demo3.tgz", "wb") as code:
   code.write(r.content)
