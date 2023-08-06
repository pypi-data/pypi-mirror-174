#import logging
import os
#import logging.handlers
import datetime
import importlib
logging=importlib.import_module("logging")
logging.handlers=importlib.import_module("logging.handlers")

try:
    host_ip=os.popen("curl ifconfig.me").read()
except Exception as err:
    host_ip=""
try:
    mid=str(os.popen("head -1 /proc/self/cgroup|cut -d/ -f3|cut -c8-19").read()).replace("\n","")
except Exception as ex:
    print(ex.args)
    mid = ""

class WeLog():
    first_signal=[]
    init_config={"path":"","filename_pre":"","filename_suffix":""}
    date_info={"ori":""}
    def __init__(self):
        self.log=logging
    def init_log(self,path,filename):
        self.log=importlib.reload(self.log)
        if os.path.exists(path):
            mode = 'a'
        else:
            mode = 'w'
        self.log.basicConfig(
            level=self.log.INFO, 
            format="host_ip:"+str(host_ip)+'  mid:'+str(mid)+'  '+'%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', 
            filename=path,
            filemode=mode, 
        )
        return self.log

    def init(self,path,filename):
        self.init_config["path"]=path
        self.init_config["filename_pre"]=filename.split(".log")[0]
        self.init_config["filename_suffix"]=filename.split(".")[-1]
        #fullpath = os.path.join(path, filename)
        #log = init_log(fullpath,filename)
        #return log

    def whether_init_log(self,ori_date):
        cur_date=str(datetime.datetime.now()).split(" ")[0]
        ###cur_date=str(datetime.datetime.now()).replace(" ","").replace(":","")
        ###print(cur_date)
        if(ori_date==cur_date):
            #同一天，不切
            return False
        else:
            #不同一天，切
            return True
    def whether_first_running(self):
        if('first_signal' in self.first_signal):
            return False
        else:
            self.first_signal.append("first_signal")
            return True

    def info(self,content):
        try:
            try:
                print(content)
            except Exception as err:
                print(err)
            if(self.init_config["path"]==""):
                print("请先配置log文件信息")
                return 
            if("log" != self.init_config["filename_suffix"]):
                print("日志文件必须以log结尾，请重新配置正确")
                return 
            if(self.whether_first_running()):
                #首次运行
                ###print("首次运行")
                cur_date=str(datetime.datetime.now()).split(" ")[0]
                ###cur_date=str(datetime.datetime.now()).replace(" ","").replace(":","")
                self.date_info={"ori":cur_date}
                filename=self.init_config["filename_pre"]+"_"+cur_date+".log"
                fullpath = os.path.join(self.init_config["path"], filename)
                self.log = self.init_log(fullpath,filename)
            else:
                #非首次运行
                ###print("非首次运行")
                if(self.whether_init_log(self.date_info["ori"])):
                    #跨天，重新初始化
                    cur_date=str(datetime.datetime.now()).split(" ")[0]
                    ###cur_date=str(datetime.datetime.now()).replace(" ","").replace(":","")
                    self.date_info={"ori":cur_date}
                    filename=self.init_config["filename_pre"]+"_"+cur_date+".log"
                    ###print(filename)
                    fullpath = os.path.join(self.init_config["path"], filename)
                    self.log = self.init_log(fullpath,filename)
            self.log.info(content)
        except Exception as err:
            print(err)

def instance():
    return WeLog()
