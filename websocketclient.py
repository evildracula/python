import websocket


def handle(message):
    if message == 'moto':
        print('moto called')
    elif message == 'watre':
        print('water')


def on_message(ws, message):
    print('message: %s' % message)
    handle(message)


def on_error(ws, error):
    print('error: %s' % error)


def on_close(ws):
    print('closed')


def on_open(ws):
    print('opened')
    ws.send(b'script')


websocket.enableTrace(True)
ws = websocket.WebSocketApp("ws://localhost/ws", on_message=on_message, on_close=on_close, on_error=on_error,
                            on_open=on_open)
ws.run_forever()
