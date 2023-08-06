from time import time

initialization_time = 0.0

def initialize() -> None:
    global initialization_time
    initialization_time = time()

def info(msg: str) -> str:
    time_now = time() - initialization_time
    formatted_message = f'[{time_now:.02f}] {msg}'
    print(formatted_message)
    return formatted_message