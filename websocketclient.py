import websocket


def on_message(ws, message):
    print('message: %s' % message)


def on_error(ws, error):
    print('error: %s' % error)


def on_close(ws):
    print('closed')


def on_open(ws):
    print('opened')


websocket.enableTrace(True)
ws = websocket.WebSocketApp("ws://localhost/ws", on_message=on_message, on_close=on_close, on_error=on_error,
                            on_open=on_open)
ws.run_forever()
