import asyncio
import subprocess
from concurrent.futures.thread import ThreadPoolExecutor
import functools
from getpass import getpass
import logging
import signal
import hashlib
import random
import string

log = logging.getLogger(__name__)

signals = {
    k: v for v, k in signal.__dict__.items()
    if v.startswith("SIG") and not v.startswith("SIG_")
}


def already_runing(_file_):
    proc = subprocess.Popen(["pgrep", "-f", _file_], stdout=subprocess.PIPE)
    std = proc.communicate()
    if len(std[0].decode()) > 1:
        exit("Already runing")


async def ainput(prompt: str = "", *, hide: bool = False):
    """Just like the built-in input, but async"""
    with ThreadPoolExecutor(1) as executor:
        func = functools.partial(getpass if hide else input, prompt)
        return await asyncio.get_event_loop().run_in_executor(executor, func)


def md5(value: str, salt: str = '') -> str:
    return str(hashlib.md5((value+salt).encode(encoding='UTF-8')).hexdigest()).lower()


def rdValue(len: int = 20, is_digits: bool = None, is_letter: bool = None) -> str:
    '''生成随机字符

    is_digits = True 时只生成数字

    is_letter = True 时只生成字母

    否则生成字母和数字组合
    '''
    if is_digits:
        chats = string.digits
    elif is_letter:
        chats = string.ascii_letters
    else:
        chats = string.ascii_letters + string.digits
    return ''.join(random.sample(chats, len))


stop = False
# 自定义信号处理函数

def my_handler(signum, frame):
    global stop
    stop = True
    print('等待上一任务处理后即结束....')


# 设置相应信号处理的handler
signal.signal(signal.SIGINT, my_handler)
signal.signal(signal.SIGHUP, my_handler)
signal.signal(signal.SIGTERM, my_handler)


async def idle(cb=None,exit:bool=None):
    if exit:
        global stop
        stop = True
        return
    while True:
        try:
            if stop:
                # 中断时需要处理的代码
                break
            elif cb:
                await cb()
        except Exception as e:
            print(str(e))
            break
