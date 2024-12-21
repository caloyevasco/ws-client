import websockets

async def websocket_stream_connection(uri: str, func : callable):
    async with websockets.connect(uri) as websocket:
        func()