import schedule
import time
import os

#修改为你的路径名
shell_command = r"python /home/ubuntu/work/tj/check.py &" # &是为了在后台执行 

def job():
    #执行脚本命令
    os.system(shell_command)

def job_info():
    print("I am working!")

if __name__ == '__main__':
    
    job()                             #初始化第一次
    schedule.every(0.5).hours.do(job) #之后每半个小时调用一次
    schedule.every(0.3).hours.do(job_info) #之后每半个小时调用一次
    while True:
        schedule.run_pending()    # 运行所有可以运行的任务
        time.sleep(1)
        