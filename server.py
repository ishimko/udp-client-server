#!/usr/bin/python3

import time
import socket
from threading import Thread


class UDPServer(Thread):
    UDP_IP = "192.168.56.1"
    UDP_PORT = 8080
    BROADCAST_ADDRESS = "192.168.56.255"

    MSG_SEND_TIME = 0
    MSG_BROADCAST_TIME = 1

    def __init__(self):
        Thread.__init__(self)
        self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpSocket.bind((UDPServer.UDP_IP, UDPServer.UDP_PORT))
        self.udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #self.udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        while True:
            data, address = self.udpSocket.recvfrom(1024)
            self.processRequest(address, data)

    def getCurrentTime(self):
        return bytes(time.strftime("%H:%M:%S", time.localtime()), encoding='UTF-8')

    def broadcastTime(self):
        self.udpSocket.sendto(self.getCurrentTime(), (UDPServer.BROADCAST_ADDRESS, UDPServer.UDP_PORT))

    def sendTime(self, client):
        self.udpSocket.sendto(self.getCurrentTime(), client)

    def processRequest(self, address, data):
        if data[0] == UDPServer.MSG_BROADCAST_TIME:
            print("{}: {} попросил отправить всем время".format(time.ctime(), address))
            self.broadcastTime()
        elif data[0] == UDPServer.MSG_SEND_TIME:
            print("{}: {} попросил отправить себе время".format(time.ctime(), address))
            self.sendTime(address)
        else:
            print("{}: сообщение от {} не распознано\n\tсообщение: {}".format(time.ctime(), address, data))


if __name__ == "__main__":
    myListener = UDPServer()
    myListener.start()