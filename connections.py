
import socket
import selectors

from typing import Callable, IO

def client(func: Callable[[socket.socket], None], host: str, port: int, ipv6: bool = False) -> None:
    sock = socket.socket(socket.AF_INET6 if ipv6 else socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        func(sock)
    except KeyboardInterrupt:
        print('keyboard interrupt, exiting')
    finally:
        sock.close()

# def mc_client(recv: Callable[[IO, dict], None | bool], send: Callable[[IO, dict], None], \
#            host: str, port: int, ipv6: bool = False) -> None:
#     pass

def server(recv: Callable[[IO, dict], None | bool], send: Callable[[IO, dict], None], \
           host: str, port: int, ipv6: bool = False) -> None:
    sel = selectors.DefaultSelector()
    msock = socket.socket(socket.AF_INET6 if ipv6 else socket.AF_INET, socket.SOCK_STREAM)
    msock.bind((host, port))
    msock.listen()
    print('server started')
    msock.setblocking(False)
    sel.register(msock, selectors.EVENT_READ)
    try:
        while True:
            events = sel.select(None)
            for event, evtmask in events:
                print(event.events, evtmask)
                sock: IO = event.fileobj #type:ignore
                print(sock, type(sock))
                data = event.data
                if data is None:
                    conn, addr = sock.accept() #type:ignore
                    print(f'accepted connection from {addr}')
                    conn.setblocking(False)
                    data = {'addr': addr}
                    sel.register(conn, selectors.EVENT_READ | selectors.EVENT_WRITE, data=data)
                else:
                    if evtmask & selectors.EVENT_READ:
                        end = recv(sock, data)
                        if end:
                            sel.unregister(sock)
                            sock.close()
                    if evtmask & selectors.EVENT_WRITE:
                        send(sock, data)
    except KeyboardInterrupt:
        print('keyboard interrupt, exiting')
    finally:
        sel.close()
