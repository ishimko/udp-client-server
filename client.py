#!/usr/bin/python3

import time
import socket
from threading import Thread


class UDPClient(Thread):
    UDP_IP = "192.168.56.1"
    UDP_PORT = 55555

    BUFFER_SIZE = 512

    MSG_SEND_TIME = 0
    MSG_BROADCAST_TIME = 1
    MSG_QUIT = 2

    def __init__(self):
        super().__init__()
        try:
            self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udpSocket.bind(('', UDPClient.UDP_PORT))
        except socket.error as e:
            print("Ошибка создания сокета: {}".format(e))
            exit(1)
        self.daemon = True

    def run(self):
        while True:
            data, address = self.udpSocket.recvfrom(UDPClient.BUFFER_SIZE)
            self.printServerMessage(data)

    def printServerMessage(self, message):
        print("\rсообщение от сервера: {}\n>>".format(message.decode('UTF-8')), end="")

    def requestTime(self):
        self.sendRequest(bytes([UDPClient.MSG_SEND_TIME]), (UDPClient.UDP_IP, UDPClient.UDP_PORT))

    def sendRequest(self, data, client):
        try:
            self.udpSocket.sendto(data, client)
        except socket.error as e:
            print("Ошибка при отправке запроса: ".format(e))
            exit(1)

    def requestTimeBroadcast(self):
        self.sendRequest(bytes([UDPClient.MSG_BROADCAST_TIME]), (UDPClient.UDP_IP, UDPClient.UDP_PORT))

    def processUserRequest(self, userInput):
        if not userInput.isnumeric():
            print("Ошибка: введите число!")
            return -1
        else:
            userInputCode = int(userInput)

        if userInputCode == UDPClient.MSG_SEND_TIME:
            self.requestTime()
        elif userInputCode == UDPClient.MSG_BROADCAST_TIME:
            self.requestTimeBroadcast()
        elif userInputCode != UDPClient.MSG_QUIT:
            print("Ошибка: неизвестная команда!")

        return userInputCode

    @staticmethod
    def printHelp():
        print("""
            0: запросить отправку времени
            1: запросить отправку времени всем
            2: выйти
        """)


if __name__ == "__main__":
    client = UDPClient()
    client.printHelp()
    client.start()

    userInputCode = None
    while userInputCode != UDPClient.MSG_QUIT:
        userInput = input(">>")
        userInputCode = client.processUserRequest(userInput)
