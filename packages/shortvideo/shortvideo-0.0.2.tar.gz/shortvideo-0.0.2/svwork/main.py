import asyncio
import sys
from .client import Client
from .utils import already_runing

async def main():
    client = Client()
    await client.start()
    
    print('已退出程序')

if __name__ == "__main__":
    already_runing(__file__)
    if sys.version_info.minor>=10:
        asyncio.run(main())
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())