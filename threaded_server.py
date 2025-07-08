import socket
import threading
import time

def run_threaded_server(port=8888, duration=2):
    def handle_client(client_socket, addr):
        try:
            client_socket.settimeout(1.0)  # Таймаут для recv
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                client_socket.send(data)
        except socket.timeout:
            pass
        except Exception as e:
            print(f"Ошибка в потоке {addr}: {e}")
        finally:
            client_socket.close()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.settimeout(1.0)  # Таймаут для accept
    server.bind(('localhost', port))
    server.listen(400)
    
    start_time = time.time()
    threads = []
    
    try:
        while time.time() - start_time < duration:
            try:
                client_socket, addr = server.accept()
                thread = threading.Thread(target=handle_client, args=(client_socket, addr))
                thread.start()
                threads.append(thread)
            except socket.timeout:
                continue
    finally:
        server.close()
        for thread in threads:
            thread.join(timeout=1.0)