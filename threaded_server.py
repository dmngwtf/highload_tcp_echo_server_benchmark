import socket
import threading
import time

def run_threaded_server(port=8888, duration=30):
    def handle_client(client_socket):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                client_socket.sendall(data)
        except Exception as e:
            print(f"Ошибка в потоке: {e}")
        finally:
            client_socket.close()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', port))
    server.listen(1000)
    server.settimeout(1.0)

    threads = []
    start_time = time.time()
    
    try:
        while time.time() - start_time < duration:
            try:
                client_socket, _ = server.accept()
                thread = threading.Thread(target=handle_client, args=(client_socket,))
                thread.daemon = True
                thread.start()
                threads.append(thread)
            except socket.timeout:
                continue
    finally:
        server.close()
        for thread in threads:
            thread.join(timeout=1.0)
