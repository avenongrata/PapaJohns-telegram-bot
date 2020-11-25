from socket import *

ip = ''
port = 9816
psd_admin = 'NaNgrataAdminTG-t'

sock = socket(AF_INET, SOCK_STREAM)
sock.connect((ip, port))

msg = psd_admin.encode('utf-8')
sock.send(msg)

while True:
    msg = input("Message: ")
    sock.send(msg.encode('utf-8'))



