import asyncio
import time
import json
from concurrent.futures import ThreadPoolExecutor
from threaded_server import run_threaded_server
from async_server import run_async_server
from tester import run_load_test, profile_memory, visualize_results

def run_tests():
    results = {
        'threaded': {'rps': 0, 'latency': 0, 'memory': 0},
        'async': {'rps': 0, 'latency': 0, 'memory': 0}
    }

    tests = [
        ('threaded', lambda: run_threaded_server(8888, duration=15), 8888),
        ('async', lambda: asyncio.run(run_async_server(8889, duration=15)), 8889),
    ]

    for key, server_func, port in tests:
        print(f"\nЗапуск {key} сервера...")

        with ThreadPoolExecutor() as executor:
            future = executor.submit(server_func)
            time.sleep(2)  # Даем серверу стартовать

            rps, latency = run_load_test(port, duration=10, connections=100)
            results[key]['rps'] = rps
            results[key]['latency'] = latency

            memory = profile_memory(lambda: future.result())
            results[key]['memory'] = memory

    with open('results.json', 'w') as f:
        json.dump(results, f, indent=4)

    visualize_results(results)

    print("\nФинальные результаты:")
    for key in results:
        r = results[key]
        print(f"{key.capitalize()}: RPS={r['rps']:.2f}, Latency={r['latency']:.2f}ms, Memory={r['memory']:.4f}MB")

if __name__ == "__main__":
    run_tests()
