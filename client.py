import socket

SERVER_IP = '192.168.1.30'
SERVER_PORT = 8001

def send_message(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, SERVER_PORT))
        s.send(message.encode())
        response = s.recv(1024).decode()
        print(response)

action = input("Are you signing up or logging in? Enter 'signup' or 'login': ")
username = input("Enter your username: ")
password = input("Enter your password: ")
message = f"{action},{username},{password}"
send_message(message)
