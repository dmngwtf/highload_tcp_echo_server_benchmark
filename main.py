import asyncio
from threaded_server import run_threaded_server
from async_server import run_async_server
from tester import run_load_test, profile_memory, visualize_results
from concurrent.futures import ThreadPoolExecutor
import json
from tqdm import tqdm
import time

def run_tests():
    results = {
        'threaded': {'rps': 0, 'latency': 0, 'memory': 0},
        'async': {'rps': 0, 'latency': 0, 'memory': 0}
    }

    tests = [
        ('Threaded', lambda: run_threaded_server(8888,30), 8888, 'threaded'),
        ('Async', lambda: asyncio.run(run_async_server(8889,30)), 8889, 'async')
    ]

    for test_name, test_func, port, key in tqdm(tests, desc="Running tests", unit="test"):
        print(f"Запуск {test_name.lower()} сервера...")
        # Запускаем сервер в отдельном потоке
        with ThreadPoolExecutor() as executor:
            future = executor.submit(test_func)
            # Ждем 2 секунды, чтобы сервер успел запуститься
            time.sleep(2)
            # Запускаем нагрузочный тест, пока сервер работает
            results[key]['rps'], results[key]['latency'] = run_load_test(port, duration=25)
            # Измеряем память после завершения сервера
            results[key]['memory'] = profile_memory(lambda: future.result())

    with open('results.json', 'w') as f:
        json.dump(results, f, indent=4)

    visualize_results(results)

    print("\nРезультаты тестирования:")
    print(f"Threaded: RPS={results['threaded']['rps']:.2f}, Latency={results['threaded']['latency']:.2f}ms, Memory={results['threaded']['memory']:.2f}MB")
    print(f"Async: RPS={results['async']['rps']:.2f}, Latency={results['async']['latency']:.2f}ms, Memory={results['async']['memory']:.2f}MB")

    return results

if __name__ == "__main__":
    run_tests()