# Сравнение моделей TCP Echo-сервера на Python
<p align="center">
  <h2 align="center">Threaded vs Async: производительность TCP Echo-серверов</h2>
  <p align="center">
    <b>threading • asyncio • нагрузочное тестирование</b><br>
    <b>RPS • задержки • память • визуализация</b>
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.11-blue" />
    <img src="https://img.shields.io/badge/threading-%F0%9F%A7%B5-green" />
    <img src="https://img.shields.io/badge/asyncio-%F0%9F%92%A8-orange" />
    <img src="https://img.shields.io/badge/pytest-%E2%9C%85-blue" />
    <img src="https://img.shields.io/badge/matplotlib-%F0%9F%93%8A-brightgreen" />
    <img src="https://img.shields.io/badge/json-%F0%9F%93%84-lightgrey" />
  </p>
</p>

---

## Возможности
| Функция | Описание |
| --------------------------------- | ----------------------------------------- |
| **Две реализации сервера** | Threaded (многопоточный) и Async (asyncio) |
| **Нагрузочное тестирование** | Одновременные клиенты, варьируемый размер сообщений |
| **Метрики** | RPS, средняя задержка, потребление памяти |
| **Автоматическая визуализация** | Графики в `results.png` |
| **JSON-результаты** | Читаемые данные в `results.json` |
| **Простой запуск** | Один скрипт — полный бенчмарк |

---

## Стек
```yaml
Language: Python 3.11
Threading: threading + socket
Async: asyncio + socket
Testing: multiprocessing + time.perf_counter
Visualization: matplotlib
Output: JSON + PNG
```

---

## Быстрый старт
```bash
git clone <repository_url>
cd tcp-echo-benchmark
pip install -r requirements.txt
```

---

## Запуск теста
### 1. Освободите порты 8888 и 8889
```bash
# Linux/macOS
netstat -tuln | grep -E '8888|8889'
lsof -i :8888 && lsof -i :8889
kill -9 <pid>

# Windows (PowerShell)
Get-NetTCPConnection -LocalPort 8888,8889
Stop-Process -Id <pid>
```

### 2. Запустите бенчмарк
```bash
python main.py
```

> Тест займёт ~1–2 минуты в зависимости от конфигурации.

---

## Результаты
После завершения в корне появятся:
- **`results.json`** — структурированные данные
- **`results.png`** — график сравнения

### Пример вывода в терминале:
```
[Threaded] RPS: 2841.2 | Latency: 12.4ms | Memory: 48.2 MB
[Async]    RPS: 5123.7 | Latency: 8.1ms  | Memory: 62.1 MB
```

---

## Интерпретация
| Параметр | Threaded | Async |
|--------|----------|-------|
| **RPS** | Стабильно при малых нагрузках | Выше на 50–80% при малых сообщениях |
| **Задержка** | Предсказуемая | Ниже на 30–40% при высокой конкуренции |
| **Память** | Контролируемая | Растёт при буферизации больших сообщений |
| **Масштабируемость** | Ограничена GIL и потоками | Лучше при тысячах соединений |

> **Вывод**: `asyncio` выигрывает в RPS и задержке, но требует аккуратной работы с буферами.

---

## Структура проекта
Коротко по каждому файлу.

---

### **threaded_server.py**
Многопоточный TCP Echo-сервер:
- Один поток на соединение
- `socket.SOCK_STREAM`
- Блокирующий I/O

---

### **async_server.py**
Асинхронный TCP Echo-сервер:
- `asyncio.start_server`
- Неблокирующий I/O
- Один event loop

---

### **tester.py**
Нагрузочный клиент:
- Многопроцессный пул клиентов
- Точное измерение времени
- Сбор метрик (RPS, latency, memory via `psutil`)

---

### **main.py**
Точка входа:
- Запуск обоих серверов
- Прогрев → тестирование → завершение
- Сохранение результатов

---

### **Корневые файлы**
* **requirements.txt** — `matplotlib`, `psutil`, `numpy`
* **results.json** — сырые данные бенчмарка
* **results.png** — автогенерируемый график

---

## Визуализация
![Результаты](results.png)


---

## Пример `results.json`
```json
{
  "threaded": {
    "64":  {"rps": 5123, "latency_ms": 8.1, "memory_mb": 48.2},
    "1024": {"rps": 2841, "latency_ms": 12.4, "memory_mb": 52.1}
  },
  "async": {
    "64":  {"rps": 8231, "latency_ms": 5.3, "memory_mb": 56.7},
    "1024": {"rps": 4123, "latency_ms": 9.8, "memory_mb": 78.3}
  }
}
```


## Рекомендации
- Используйте **Threaded** для простых задач с предсказуемой нагрузкой
- Используйте **Async** для высокой конкуренции и тысяч соединений
- Всегда профилируйте память при работе с большими сообщениями

---