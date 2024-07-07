
import connections

msg = input('enter message: ')

def recv(sock, data: dict) -> None:
    data['msg'] = sock.recv(1024)

def send(sock, data: dict) -> None:
    sock.send(data['msg'])

connections.server(recv, send, '127.0.0.1', 42069, False)
