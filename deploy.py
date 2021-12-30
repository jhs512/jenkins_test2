import os,sys
import locale
import subprocess
import time
import socket
from datetime import datetime
def get_sys():
    """
    get_os_name
    """
    os_encoding = locale.getpreferredencoding()
    if os_encoding.upper() == 'cp949'.upper():
        return "Win"
    elif os_encoding.upper() == 'UTF-8'.upper():
        return "Lin"
def get_logs(cmd):
    """
    get_logs_from_command
    """
    os_encoding = locale.getpreferredencoding()
    if os_encoding.upper() == 'cp949'.upper():  # Windows
        return subprocess.Popen(
            cmd, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()
    elif os_encoding.upper() == 'UTF-8'.upper():  # Mac&Linux
        return os.popen(cmd).read()
    else:
        print("None matched")
        exit()
def get_ports_from_strings(_result, words):
    """
    parse_ports_from_logs
    """
    try:
        tcp = words[-2].split("->")
        _tcp = ""
        for strings in tcp:
            if "tcp" in strings:
                _tcp = strings
                break
        return _tcp.split("/")[0]
    except:
        return ""        
def get_docker_containers():
    """
    parse_containers_informations
    """
    cmd = "docker ps -a"
    logs = get_logs(cmd).split("\n")
    column = logs.pop(0)
    result = []
    if logs:
        for line in logs:
            words = line.split("  ")

            while '' in words:
                words.remove('')

            for i in range(len(words)):
                words[i] = words[i].strip().strip()
            try:
                status = words[4].strip().split(" ")[0]
                # print(f"C Name :: {words[-1]}, C ID :: {words[0]}, Img Name :: {words[1]} , Status :: {status}")
                _result = [words[-1], words[0], words[1], status]
                # get ports
                _result.append(get_ports_from_strings(_result, words))
                # get ip
                _result.append(get_logs(
                    "docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "+words[0]).strip("'").strip("\n"))
            except:
                pass
            result.append(_result)
    else:
        print("No Containers")
    return result
def get_specific_container(cmd):
    """
    get_specific_container
    """
    a = get_docker_containers()
    for i in a:
        if i[0] == cmd:
            return i
    return []
def get_now():
    """
    make a string by current time
    """
    now=datetime.now()
    nows = [now.year,now.month,now.day,now.hour,now.minute,now.second]
    nowtime = ""
    for i in nows:
        nowtime = nowtime + str(i).zfill(2)
    return nowtime
def connection_checker(test_con):
    """
    check container's network
    """
    osType = get_sys()
    print(osType)
    if osType == "Lin":
        myip = test_con.ip
    else:
        myip = socket.gethostbyname(socket.gethostname())
    print(myip)
    print(test_con.port)
    server_address = (myip,int(test_con.port))
    fail_counter = 0
    for i in range(10):
        time.sleep(1)
        try:
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect(server_address)            
            sock.close()
            print(f"{i+1} Connection Succeed")
        except:
            print(f"{i+1} Connection Failed")
            fail_counter += 1
    sock.close()
    if fail_counter:
        return False
    else:
        return True
def get_setting_path():
    """
    find the setting.py's directory
    """
    setting_path = ""
    for path, dirs, files in os.walk(os.getcwd()):
        for i in files:
            if i == 'settings.py':
                setting_path = path
                break
    osType = get_sys()
    if osType == "Win":
        return setting_path.split("\\")[-1]
    else:
        return setting_path.split("/")[-1]

class Container:
    def __init__(self,con):
        self.container_name = con[0]
        self.image_name = con[2]
        self.ip = con[-1]
        self.port = con[-2]

def main():
    cur_time = get_now()
    path = get_setting_path()
    init = False
    try:
        now_con = Container(get_specific_container("now_con"))
    except:
        init = True
    try:
        shut_con = Container(get_specific_container("test_con"))
        os.system(f"docker rm -f test_con")
        os.system(f"docker rmi -f {shut_con.image_name}")
    except:
        pass
    os.system("docker pull python:3")
    os.system(f"docker build -t python:{cur_time} .")
    os.system(f"docker run -d -p 8001:8001 --name test_con python:{cur_time} gunicorn --bind 0:8001 {path}.wsgi")
    con_info = get_specific_container("test_con")
    print(con_info)
    test_con = Container(con_info)
    if connection_checker(test_con) == False:
        os.system(f"docker rm -f test_con")
        os.system(f"docker rmi -f python:{cur_time}")
        raise Exception("Connection Error")
    else:
        os.system(f"docker rm -f test_con")
        if init == False:
            os.system(f"docker rm -f now_con")
        os.system(f"docker run -d -p 8000:8000 --name now_con python:{cur_time} gunicorn --bind 0:8000 {path}.wsgi")
        if init == False:
            os.system(f"docker rmi -f {now_con.image_name}")
        #messagr success##
        os.system("python3 manage.py test")
        print(" ")
        print("Build Succeed")

if __name__ == "__main__":
    main()#