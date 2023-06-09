import asyncio
import socket

def simple_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 3005))
        s.listen()
        conn, addr = s.accept()
        print('Address of client: ', addr)
        with conn:
            data = conn.recv(1024)
            conn.sendall(bytes(f'HTTP/1.1 200 OK\r\n\r\nHello {data} world\r\n', 'utf-8'))

# simple_server()

def multiple_connections():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 3005))
        s.listen()
        while True:
            conn, addr = s.accept()
            print('Address of client: ', addr)
            with conn:
                data = conn.recv(1024)
                conn.sendall(bytes(f'HTTP/1.1 200 OK\r\n\r\nHello {data} world\r\n', 'utf-8'))

# multiple_connections()

async def receive_and_send(conn):
    loop = asyncio.get_event_loop()
    data = await loop.sock_recv(conn, 1024)
    await asyncio.sleep(3)
    await loop.sock_sendall(conn, bytes(f'HTTP/1.1 200 OK\r\n\r\nHello {data} world\r\n', 'utf-8'))
    conn.close()

async def concurrent_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 3006))
        s.listen()
        s.setblocking(False)
        while True:
            loop = asyncio.get_event_loop()
            conn, addr = await loop.sock_accept(s)
            print('Address of client: ', addr)
            task = receive_and_send(conn)
            loop.create_task(task)
                
            
asyncio.run(concurrent_server())
