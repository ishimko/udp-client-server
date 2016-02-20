#!/usr/bin/python3

import time
import socket
from threading import Thread


class UDPServer(Thread):
    UDP_IP = "192.168.56.1"
    UDP_PORT = 8080
    BROADCAST_ADDRESS = "192.168.56.255"

    BUFFER_SIZE = 512

    MSG_SEND_TIME = 0
    MSG_BROADCAST_TIME = 1

    def __init__(self):
        Thread.__init__(self)
        self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.udpSocket.bind((UDPServer.UDP_IP, UDPServer.UDP_PORT))
            self.udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        except socket.error as e:
            print("Ошибка создания сокета: {}".format(e))
            exit(1)

    def run(self):
        print("{}: сервер запущен".format(time.ctime()))
        while True:
            data, address = self.udpSocket.recvfrom(UDPServer.BUFFER_SIZE)
            self.processRequest(address, data)

    def getCurrentTime(self):
        return bytes(time.strftime("%H:%M:%S", time.localtime()), encoding='UTF-8')

    def sendRequest(self, data, client):
        try:
            self.udpSocket.sendto(data, client)
        except socket.error:
            print("Ошибка при отправке запроса!")
            exit(1)

    def broadcastTime(self):
        self.sendRequest(self.getCurrentTime(), (UDPServer.BROADCAST_ADDRESS, UDPServer.UDP_PORT))

    def sendTime(self, client):
        self.sendRequest(self.getCurrentTime(), client)

    def processRequest(self, address, data):
        if data[0] == UDPServer.MSG_BROADCAST_TIME:
            print("{}: {} попросил отправить всем время".format(time.ctime(), address[0]))
            self.broadcastTime()
        elif data[0] == UDPServer.MSG_SEND_TIME:
            print("{}: {} попросил отправить себе время".format(time.ctime(), address[0]))
            self.sendTime(address)
        else:
            print("{}: сообщение от {} не распознано\n\tсообщение: {}".format(time.ctime(), address[0], data))


if __name__ == "__main__":
    server = UDPServer()
    server.start()
