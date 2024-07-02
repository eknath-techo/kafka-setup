import socket
import struct


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = "<localhost>"
port = 10050

client_socket.connect(host_ip,port)

data = b""
payload_size = struct.calcsize("Q")