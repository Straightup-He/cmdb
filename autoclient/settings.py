
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 需要采集的服务器的各部分插件，可在此扩展
PLUGIN_CLASS_DICT = {
    'disk': 'lib.plugins.disk.DiskPlugin',
    'memory': 'lib.plugins.memory.MemoryPlugin',
    'network': 'lib.plugins.network.NetworkPlugin',
    'basic': 'lib.plugins.basic.BasicPlugin',
    'board': 'lib.plugins.board.BoardPlugin',
    'cpu': 'lib.plugins.cpu.CpuPlugin',
}

SSH_PORT = 22
SSH_USER = 'root'
SSH_PWD = '12345'

# FBV
# GET_DATA_URL = 'http://127.0.0.1:8000/api/get_data/'
# GET_SERVER_URL = 'http://127.0.0.1:8000/api/get_server/'

API_URL = 'http://127.0.0.1:8000/api/v1/server/'

LOGGING_PATH = os.path.join(BASE_DIR, 'log/cmdb.log')

# 由于项目采集的服务器用虚拟机代替，没有硬盘信息，这里用读取文件的形式来模拟效果
LOCAL_DISK_FILE_PATH = os.path.join(BASE_DIR, 'files/disk.txt')





