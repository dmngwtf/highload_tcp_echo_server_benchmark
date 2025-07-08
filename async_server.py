import asyncio

async def handle_client(reader, writer):
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break
            writer.write(data)
            await writer.drain()
    except Exception as e:
        print(f"Ошибка в asyncio клиенте: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

async def run_async_server(port=8889, duration=30):
    server = await asyncio.start_server(handle_client, 'localhost', port)
    async with server:
        await asyncio.sleep(duration)