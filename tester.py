import matplotlib.pyplot as plt
import tracemalloc
import time
import socket
import threading
import statistics
from concurrent.futures import ThreadPoolExecutor

def run_load_test(port, duration=2, connections=4):
    def client_task():
        start_time = time.time()
        latencies = []
        requests = 0
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', port))
            while time.time() - start_time < duration:
                start_request = time.time()
                sock.send(b"test data\n")
                data = sock.recv(1024)
                if data:
                    latencies.append((time.time() - start_request) * 1000)
                    requests += 1
                else:
                    break
            sock.close()
        except Exception as e:
            print(f"Ошибка клиента: {e}")
        return requests, latencies

    start_time = time.time()
    results = []
    
    with ThreadPoolExecutor(max_workers=connections) as executor:
        futures = [executor.submit(client_task) for _ in range(connections)]
        for future in futures:
            results.append(future.result())
    
    total_requests = sum(r[0] for r in results)
    all_latencies = [lat for r in results for lat in r[1]]
    
    rps = total_requests / duration if total_requests > 0 else 0
    avg_latency = statistics.mean(all_latencies) if all_latencies else 0
    
    return rps, avg_latency

def profile_memory(func, *args):
    tracemalloc.start()
    start_time = time.time()
    func(*args)
    snapshot = tracemalloc.take_snapshot()
    tracemalloc.stop()
    total_memory = sum(stat.size for stat in snapshot.statistics('lineno')) / 1024 / 1024
    return total_memory

def visualize_results(results):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    
    ax1.bar(['Threaded', 'Async'], [results['threaded']['rps'], results['async']['rps']])
    ax1.set_title('Requests Per Second')
    ax1.set_ylabel('RPS')
    
    ax2.bar(['Threaded', 'Async'], [results['threaded']['latency'], results['async']['latency']])
    ax2.set_title('Latency')
    ax2.set_ylabel('ms')
    
    ax3.bar(['Threaded', 'Async'], [results['threaded']['memory'], results['async']['memory']])
    ax3.set_title('Memory Usage')
    ax3.set_ylabel('MB')
    
    plt.tight_layout()
    plt.savefig('results.png')
    plt.close()