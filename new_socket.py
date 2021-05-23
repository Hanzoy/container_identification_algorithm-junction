# encoding: utf-8

import socket
import threading
import json
from time import time
import re
from remake import east_pred
from model.OCR.init import init_detector, init_recognizer

def main():

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # host = socket.gethostname()
    host = '127.0.0.1'
    port = 55533
    serversocket.bind((host, port))
    serversocket.listen(5)
    myaddr = serversocket.getsockname()
    print("服务器地址:%s" % str(myaddr))
    while True:
        clientsocket, addr = serversocket.accept()
        print("连接地址:%s" % str(addr))
        try:
            t = ServerThreading(clientsocket)
            t.start()

        except Exception as identifier:
            print(identifier)


class ServerThreading(threading.Thread):

    def __init__(self, clientsocket, recvsize=1024 * 1024, encoding="utf-8"):
        threading.Thread.__init__(self)
        self._socket = clientsocket
        self._recvsize = recvsize
        self._encoding = encoding

    def run(self):
        print("开启线程.....")

        time_dec = time()

        detector = init_detector(r'model/OCR/model//model\craft_mlt_25k.pth', 'cuda')

        print("detector耗时：" + str(time() - time_dec))
        time_reg = time()

        character = '0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk' \
                    'lmnopqrstuvwxyzÀÁÂÃÄÅÆÇÈÉÊËÍÎÑÒÓÔÕÖØÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿąęĮįıŁłŒœŠšųŽž'
        separator_list = {}
        dict_list = {'en': 'D:\\集装箱\\集装箱\\model\\OCR\\dict\\en_char.txt'}
        model_path = r'model/OCR/model//model\latin.pth'
        recognizer, converter = init_recognizer(1, 512, 512, character, separator_list, dict_list, model_path,
                                                'cuda')

        print("recognizer耗时：" + str(time() - time_reg))

        while True:
            try:
                msg = ''
                while True:
                    rec = self._socket.recv(self._recvsize)
                    msg += rec.decode(self._encoding)
                    # msg = bytes(msg, encoding=self._encoding)

                    if msg.strip().endswith('over'):
                        msg = re.match(r'\{[^\}]+\}', msg).group()
                        # 文件名用{}框起来
                        break
                    if msg.strip().endswith('end'):
                        self._socket.close()
                        break
                if msg.strip().endswith('end'):
                    break

                print(msg)
                print("1")
                msg_dict = json.loads(msg)

                file_name = msg_dict['file_name']
                print(file_name)

                # file_name = 0

                east_pred(file_name, detector, recognizer, converter)

                with open("result.txt", "r") as f:
                    res = f.readline()
                    print(res)

                pred = {'sendmsg': res}
                sendmsg = json.dumps(pred)
                print(sendmsg)
                # print(self._socket)
                # self._socket.send(sendmsg.encode(self._encoding))
                # pass



                # sendmsg = json.dumps(pred[sendmsg])
                self._socket.send(sendmsg.encode(self._encoding) + bytes('\n', encoding=self._encoding))


            except Exception as identifier:
                self._socket.send("500".encode(self._encoding))
                print(identifier)

        print("任务结束.....")


if __name__ == "__main__":
    main()
