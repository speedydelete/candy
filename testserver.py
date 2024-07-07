
import socket
import connections

def recv(sock: socket.socket, data: dict) -> None:
    data['msg'] = sock.recv(1024)
    print(f'received data from {data['addr']}:', repr(data['msg']))

def send(sock: socket.socket, data: dict) -> None:
    sock.send(data['msg'])
    print(f'sending data to {data['addr']}:', repr(data['msg']))

connections.server(recv, send, '127.0.0.1', 42069, False)
