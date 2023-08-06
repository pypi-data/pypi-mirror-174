import functools
import json
import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from contextlib import closing
from getpass import getpass
from typing import Any, Callable
import logging
import requests

from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

from .object import Object
from .utils import md5, rdValue

log = logging.getLogger(__name__)

class Result(Object):
    def __init__(self, success: bool, msg: str, data: Any, **kwargs) -> None:
        self.success = success
        self.msg = msg or ''
        self.data = data
        self.code = kwargs.get('code') or 200


async def ainput(prompt: str = "", *, hide: bool = False):
    """Just like the built-in input, but async"""
    with ThreadPoolExecutor(1) as executor:
        func = functools.partial(getpass if hide else input, prompt)
        return await asyncio.get_event_loop().run_in_executor(executor, func)


class Method:

    async def query(self, url: str, action: str, **kwargs):
        try:
            nonce = rdValue(10)
            sign = md5(action+self.appid+nonce, self.appsecret)
            url = f'{self.host}{url}?action={action}&appid={self.appid}&nonce={nonce}&sign={sign}&version={self.version}'
            headers = {'Content-Type': 'application/json'}

            response = requests.post(url, data=json.dumps(
                kwargs), headers=headers) if kwargs else requests.get(url, headers=headers)

            if(response.status_code == 200):
                value = response.json()
                res = Result(value.get('success'), value.get('msg'), value.get('data'))
                if(value.get('code')==401):
                    res.code=401
                return res
            else:
                return Result(False, str(response.status_code), None, code=response.status_code)

        except Exception as e:
            return Result(False, str(e), None)

    async def download(self, savepath: str, src: str, callback: Callable[[int, int, int], None]):
        try:
            with closing(requests.get(src, stream=True)) as response:
                chunk_size = 1024  # 单次请求最大值
                total = int(response.headers['content-length'])  # 内容体总大小
                size = 0
                with open(savepath, "wb") as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size = size + len(data)
                        progress = (size / total) * 100
                        callback(progress, size, total)
        except:
            return False
        else:
            return True

    async def upload(self, url: str, key: str, token: str, filepath: str, accept: str, callback: Callable[[int, int, int], None]):
        def cb(monitor):
            progress = (monitor.bytes_read / monitor.len) * 100
            callback(progress, monitor.bytes_read, monitor.len)

        try:
            fields = {'key': key, 'token': token, 'file': (
                key, open(filepath, 'rb'), accept)}
            e = MultipartEncoder(fields)

            m = MultipartEncoderMonitor(e, cb)

            r = requests.post(url, data=m, headers={
                              'Content-Type': m.content_type})
            v = r.json()
            if(v.get('code') == 0):
                return Result(True, '', v.get('data'))
            else:
                return Result(False, v.get(f'{v.get("code")}:{v.get("message") or "上传失败"}'))
        except Exception as ex:
            return Result(False, str(ex), None)
