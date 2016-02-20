#!/usr/bin/python3

import time
import socket
from threading import Thread


class UDPClient(Thread):
    UDP_IP = "192.168.56.1"
    UDP_PORT = 8080

    MSG_SEND_TIME = 0
    MSG_BROADCAST_TIME = 1

    def __init__(self):
        super().__init__()
        self.serverMessages = []
        self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpSocket.bind(('', UDPClient.UDP_PORT))

    def run(self):
        while True:
            data, address = self.udpSocket.recvfrom(1024)
            self.printServerMessage(data)

    def printServerMessage(self, message):
        print("{}: {}".format(time.ctime(), message))

    def requestTime(self):
        print("requestTime")
        self.udpSocket.sendto(bytes([UDPClient.MSG_SEND_TIME]), (UDPClient.UDP_IP, UDPClient.UDP_PORT))

    def requestTimeBroadcast(self):
        print("requestTimeBroadcast")
        self.udpSocket.sendto(bytes([UDPClient.MSG_BROADCAST_TIME]), (UDPClient.UDP_IP, UDPClient.UDP_PORT))

    def processUserRequest(self, userInput):
        if not userInput.isnumeric():
            print("Ошибка: введите число!")
            return
        else:
            userInputCode = int(userInput)

        if userInputCode == UDPClient.MSG_SEND_TIME:
            self.requestTime()
        elif userInputCode == UDPClient.MSG_BROADCAST_TIME:
            self.requestTimeBroadcast()
        else:
            print("Ошибка: неизвестная команда!")

    @staticmethod
    def printHelp():
        print("""
            0: запросить отправку времени
            1: запросить отправку времени всем
        """)


if __name__ == "__main__":
    client = UDPClient()
    client.printHelp()
    client.start()

    while True:
        userInput = input(">>")
        client.processUserRequest(userInput)
