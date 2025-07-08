import matplotlib.pyplot as plt
import tracemalloc
import time
import socket
import threading
import statistics
from concurrent.futures import ThreadPoolExecutor

def run_load_test(port, duration=10, connections=1000):
    def client_task():
        latencies = []
        requests = 0
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', port))
            sock.settimeout(2)
            start_time = time.time()

            while time.time() - start_time < duration:
                start = time.time()
                sock.sendall(b"ping\n" * 100)
                data = sock.recv(1024)
                if not data:
                    break
                latency = (time.time() - start) * 1000
                latencies.append(latency)
                requests += 1
            sock.close()
        except Exception as e:
            print(f"Client error: {e}")
        return requests, latencies

    with ThreadPoolExecutor(max_workers=connections) as executor:
        futures = [executor.submit(client_task) for _ in range(connections)]
        results = [f.result() for f in futures]

    total_requests = sum(r[0] for r in results)
    all_latencies = [lat for r in results for lat in r[1]]
    rps = total_requests / duration if duration else 0
    avg_latency = statistics.mean(all_latencies) if all_latencies else 0
    return rps, avg_latency

def profile_memory(func, *args):
    tracemalloc.start()
    func(*args)
    snapshot = tracemalloc.take_snapshot()
    tracemalloc.stop()
    return sum(stat.size for stat in snapshot.statistics('lineno')) / (1024 * 1024)

def visualize_results(results):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    labels = ['Threaded', 'Async']

    ax1.bar(labels, [results['threaded']['rps'], results['async']['rps']])
    ax1.set_title('Requests Per Second')
    ax1.set_ylabel('RPS')

    ax2.bar(labels, [results['threaded']['latency'], results['async']['latency']])
    ax2.set_title('Latency')
    ax2.set_ylabel('ms')

    ax3.bar(labels, [results['threaded']['memory'], results['async']['memory']])
    ax3.set_title('Memory Usage')
    ax3.set_ylabel('MB')

    plt.tight_layout()
    plt.savefig('results.png')
    plt.close()
