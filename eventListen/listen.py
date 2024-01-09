import keyboard
import threading
import random
import time

def keyboard_listener():
    while True:
        event = keyboard.read_event()
        print(f"Key pressed: {event.name}")

def simulate_keyboard_signal():
    while True:
        key = random.choice(['up', 'down', 'left', 'right'])
        keyboard.press(key)
        keyboard.release(key)
        time.sleep(1)

if __name__ == "__main__":
    # 创建并启动监听键盘事件的线程
    listener_thread = threading.Thread(target=keyboard_listener)
    listener_thread.start()

    # 创建并启动模拟键盘信号输出的线程
    simulator_thread = threading.Thread(target=simulate_keyboard_signal)
    simulator_thread.start()

    try:
        # 主线程等待其他线程结束
        listener_thread.join()
        simulator_thread.join()
    except KeyboardInterrupt:
        print("Program terminated by user.")
