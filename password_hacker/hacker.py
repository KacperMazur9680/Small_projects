import sys
import socket
import itertools
import os

def checker(data, client_socket):
    for p in data:
        bp = p.encode()
        client_socket.send(bp)
        response = client_socket.recv(1024)
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


def connect(client_socket):
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    address = (hostname, port)
    client_socket.connect(address)


def main():
    with socket.socket() as client_socket:
        connect(client_socket)
        print(brute_force(client_socket))

if __name__ == "__main__":
    main()

