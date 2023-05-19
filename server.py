import socket
import hashlib
import secrets

SERVER_IP = '192.168.1.30'
SERVER_PORT = 8001


def salt():
    salt = secrets.token_hex(16)
    return salt

def hashPassword(password, salt):
    saltedPassword = password + salt
    hashed_password = hashlib.sha512(saltedPassword.encode()).hexdigest()
    return hashed_password

def saveUser(username, hashed_password, salt):
    with open('user_data.txt', 'a') as file:
        file.write(f"{username},{hashed_password},{salt}\n")

def getUserInfo():
    userData = {}
    with open('user_data.txt', 'r') as file:
        for line in file:
            username, hashed_password, salt = line.strip().split(',')
            userData[username] = {'hashed_password': hashed_password, 'salt': salt}
    return userData

def authenticateUser(username, password):
    userData = getUserInfo()
    if username not in userData:
        return False
    
    hashed_password = hashPassword(password, userData[username]['salt'])
    savedHashedPassword = userData[username]['hashed_password']

    return hashed_password == savedHashedPassword

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER_IP, SERVER_PORT))
    print('Server is listening...')
    s.listen(1)
    conn, addr = s.accept()
    print(f'Connection accepted from: {addr}')
    with conn:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
        
            messageType, username, password = data.split(',')

            if messageType == "signup":
                salt = salt()
                hashed_password = hashPassword(password, salt)
                saveUser(username, hashed_password, salt)
                response = "Signup Successful!"
            elif messageType == "login":
                authenticated = authenticateUser(username, password)
                if authenticated:
                    response = "Login Successful!"
                else:
                    response = "Invalid Username Or Password"
            else:
                response = "Invalid Message Type"
            
            conn.send(response.encode())
