import asyncio
import sys
from svwork.client import Client
from svwork.utils import already_runing

def main():
    #already_runing(__file__)
    if sys.version_info.minor>=10:
        asyncio.run(Client().start())
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(Client().start())
    
    print('已退出程序')

