import time
from socket import *
from threading import Thread
from threading import Lock


class udpListener(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.l = []

    def run(self):
        while True:
            self.l.append(1)
            time.sleep(1)


    def getList(self):
        lock = Lock()
        lock.acquire()
        returningList = self.l[:]
        lock.release()
        return returningList



myListener = udpListener()
myListener.start()

while True:
    a = input()

    if a == '1':
        print(myListener.getList())



            # host = "<broadcast>"
            # port = 8888
            # buf = 1024
            # s = socket(family=AF_INET, type=SOCK_DGRAM)
            # s.bind(("", 0))
            # s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
            # msg = bytes("test", encoding="UTF-8")
            # s.sendto(msg, (host, port))

            # cs = socket(AF_INET, SOCK_DGRAM)
            # cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            # cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
            # cs.sendto(b'This is a test', ('192.168.1.255', 8888))
