
import socket
import connections

msg = input('enter message: ')

def func(sock: socket.socket) -> None:
    sock.sendall(msg.encode('utf-8'))
    data = sock.recv(1024)
    print('received:', data.decode('utf-8'))

connections.client(func, '127.0.0.1', 42069, False)
