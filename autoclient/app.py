# 类库 / 模块
from concurrent.futures import ThreadPoolExecutor
import requests
import paramiko
import settings
from lib.plugins import get_server_info

# 远程连接并执行命令
def ssh(host, cmd):
    """
    paramiko模块远程连接并执行命令
    :param host: 连接ip
    :param cmd: 执行的命令
    :return:
    """
    my_ssh = paramiko.SSHClient()
    my_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    my_ssh.connect(hostname=host, port=settings.SSH_PORT, username=settings.SSH_USER, password=settings.SSH_PWD)
    # 执行命令
    stdin, stdout, stderr = my_ssh.exec_command(cmd)
    result = stdout.read()
    # 关闭连接
    my_ssh.close()
    return result.decode('utf-8')

# 任务函数,递交给线程池
def task(host):
    server_info = get_server_info(ssh, host)
    # 发送采集信息到API接口
    result = requests.post(
        url=settings.API_URL,
        json={'host': host, 'info': server_info}
    )
    print(result)

# 获取今日未采集服务器列表
def get_server_list():
    response = requests.get(url=settings.API_URL)
    return response.json()['data']

# 主函数
def run():
    host_list = get_server_list()
    if host_list:
        pool = ThreadPoolExecutor(10)
        for host in host_list:
            pool.submit(task, host)
    else:
        print('目前没有需要汇报的服务器')

if __name__ == '__main__':
    run()





