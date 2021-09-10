import socket
import queue
import threading
import time
open = []
tmp=[]

class PortScanner():
    """
    ip:传入的是一个ip还是一个ip列表。
        如果是ip，则直接将其加入ip队列，
        如果是列表，则一个一个加入ip队列。
    ip_port:将ip+port放在该队列

    MAX:发包线程最大数

    open:将打开的端口放在该列表里
    """
    def __init__(self,listOrstr:list,MAX=50):
        self.listOrstr = listOrstr
        self.MAX = MAX
        self.ip_port = queue.Queue()
        self.open=[]

    """
    处理传入单个或多个ip的时候，将ip便利成ip加端口 eg:  [127.0.0.1:123,127.0.0.1:124...]
    """
    #将得到的数据ip或iplist将其与其端口加入队列
    def ip_port_queue(self):
            for i  in self.listOrstr:
                print(i)
                for j in range(0,65535):
                    tmp = str(i)+":"+str(j)
                    self.ip_port.put(tmp)


    """
    处理ip_port队列，将本机与每个ip:port建立socket链接(较慢)
    成功链接则返回open并将其存储在self.open列表中，未成功这不返回
    """
    def  ip_port_scaner(self):

        while True:
            tmp1 = self.ip_port.get()
            tmp = tmp1.split(":")
            ip = tmp[0]
            port = tmp[1]
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            try:
                sock.connect((ip,int(port)))
                print(f"{ip}:{port} open")
                self.open.append(tmp1)
            except Exception as err:
                pass
                # print(f"{ip}:{port} close")
            finally:
                sock.close()

    """
    MODE 
    使用该函数，使主线程在子线程结束后推出，以获取其值
    """
    def over(self,m_count):
        tmp_count = 0
        i = 0
        count = m_count
        while True:
            time.sleep(4)
            ac_count = threading.activeCount()
            if ac_count < count  and ac_count == tmp_count:
                i+=1
            else:
                i=0
            tmp_count = ac_count
            if (self.ip_port.empty() and threading.activeCount() <= 1) or i > 5:
                break

    def begin(self):
        Thread_ip_port = threading.Thread(target=self.ip_port_queue)
        Thread_ip_port.start()
        for i in range(self.MAX):
            threading.Thread(target=self.ip_port_scaner).start()
        self.over(10)
        return self.open
    #实现通过读取列表的方式实现多ip运行
if __name__ == '__main__':
    MaxThread = 500
    ip = ["192.168.231.191"]
    PS =  PortScanner(ip,MaxThread)
    print(PS.begin())


