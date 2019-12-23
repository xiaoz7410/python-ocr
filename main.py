import keyboard  # 监听键盘
import pynput
from PIL import ImageGrab  # 截图、读取图片、保存图片
import time
from aip import AipOcr
import pyperclip as clip
import configparser
import pyautogui as gui


def get_config(name):
    return config.get('common', name)


def back_text():
    client = AipOcr(**baidu_config)
    with open('current_ocr.png', mode='rb') as f:
        image = f.read()

    result = client.basicGeneral(image)
    if result and result.__contains__('words_result'):
        text_list = [i.get('words') for i in result.get('words_result')]
    return '\n'.join(text_list)


def on_press(key):
    pass


def on_release(key):
    name = str(key).split('.')[-1].replace('\'', '')
    if name == begin:
        keyboard.send(screenshot)
        if not keyboard.wait('enter'):
            time.sleep(float(sleeptime))
            image = ImageGrab.grabclipboard()
            image.save('current_ocr.png')
            text = back_text()
            clip.copy(text)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini', 'UTF-8')

    begin = config.get('common', 'begin')
    screenshot = config.get('common', 'screenshot')
    sleeptime = config.get('common', 'sleeptime')
    appId = config.get('baidu', 'appId')
    apiKey = config.get('baidu', 'apiKey')
    secretKey = config.get('baidu', 'secretKey')

    baidu_config = {
        'appId': appId,
        'apiKey': apiKey,
        'secretKey': secretKey
    }

    print('程序启动成功')

    with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
